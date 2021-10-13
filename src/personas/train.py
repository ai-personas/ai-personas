from x_transformers import TransformerWrapper, Decoder
from x_transformers.autoregressive_wrapper import AutoregressiveWrapper

import random
import tqdm
import gzip
import numpy as np
import torch
import torch.optim as optim
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from environments.Environment import Environment
import sys
from personas.persona import Persona

class Train:

    def __init__(self, persona_name):
        self.persona = Persona(persona_name)
        self.persona_details = self.persona.get_persona_details()

        specification = self.persona_details['specification']
        self.NUM_BATCHES = int(1e5)
        self.BATCH_SIZE = specification['batch_size']
        self.GRADIENT_ACCUMULATE_EVERY = specification['gradient_accumulate_every']
        self.LEARNING_RATE = specification['learning_rate']
        self.VALIDATE_EVERY  = specification['validate_every']
        self.GENERATE_EVERY  = 500
        self.GENERATE_LENGTH = 1024
        self.SEQ_LEN = specification['sequence_length']
        self.NUM_TOKENS = specification['num_tokens']
        attn_layers_spec = specification['attnLayers']
        self.ATTN_DIM = attn_layers_spec['dim']
        self.ATTN_DEPTH = attn_layers_spec['depth']
        self.ATTN_HEADS = attn_layers_spec['heads']

        env = Environment(self.persona_details['environments'])
        envDetails = env.retrieveEnvDetails()
        self.DATASET = env.getEnvironmentUrlToLocal(envDetails)

        self.validation_loss = []
        self.training_loss = []
        self.STORE_PERSONA_WHILE_TRAINING_EVERY = 2

    def cycle(self, loader):
        while True:
            for data in loader:
                yield data

    def decode_token(self, token):
        return str(chr(max(32, token)))

    def decode_tokens(self, tokens):
        return ''.join(list(map(self.decode_token, tokens)))

    def run(self):

        # instantiate GPT-like decoder model
        model = TransformerWrapper(
            num_tokens = self.NUM_TOKENS,
            max_seq_len = self.SEQ_LEN,
            attn_layers = Decoder(dim = self.ATTN_DIM, depth = self.ATTN_DEPTH, heads = self.ATTN_HEADS)
        )

        model = AutoregressiveWrapper(model)
        model.cuda()

        # prepare enwik8 data
        if self.DATASET is None:
            return
        with gzip.open(self.DATASET) as file:
            X = np.fromstring(file.read(int(95e6)), dtype=np.uint8)
            trX, vaX = np.split(X, [int(90e6)])
            data_train, data_val =\
                torch.from_numpy(trX), torch.from_numpy(vaX)

        train_dataset = TextSamplerDataset(data_train, self.SEQ_LEN)
        val_dataset   = TextSamplerDataset(data_val, self.SEQ_LEN)
        train_loader  = self.cycle(DataLoader(train_dataset, batch_size = self.BATCH_SIZE))
        val_loader    = self.cycle(DataLoader(val_dataset, batch_size = self.BATCH_SIZE))

        # optimizer
        optim = torch.optim.Adam(model.parameters(), lr=self.LEARNING_RATE)

        # training
        for i in tqdm.tqdm(range(self.NUM_BATCHES), mininterval=10., desc='training'):
            model.train()

            for __ in range(self.GRADIENT_ACCUMULATE_EVERY):
                loss = model(next(train_loader))
                loss.backward()

            self.training_loss.append(loss.item())
            print(f'training loss: {loss.item()}')
            torch.nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            optim.step()
            optim.zero_grad()

            if i % self.VALIDATE_EVERY == 0:
                model.eval()
                with torch.no_grad():
                        loss = model(next(val_loader))
                        self.validation_loss.append(loss.item())
                        print(f'validation loss: {loss.item()}')

            if i % self.STORE_PERSONA_WHILE_TRAINING_EVERY == 0:
                self.persona.update_training_loss(self.training_loss, self.validation_loss)
                torch.save({
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optim.state_dict()
                }, self.persona.persona_name + '.torch')
                self.persona.save_model(self.persona.persona_name + '.torch')

            if i % self.GENERATE_EVERY == 0:
                model.eval()
                inp = random.choice(val_dataset)[:-1]
                prime = self.decode_tokens(inp)
                print(f"{prime} \n\n {'*' * 100}")

                sample = model.generate(inp, self.GENERATE_LENGTH)
                output_str = self.decode_tokens(sample)
                print(output_str)

class TextSamplerDataset(Dataset):
    def __init__(self, data, seq_len):
        super().__init__()
        self.data = data
        self.seq_len = seq_len

    def __getitem__(self, index):
        rand_start = torch.randint(0, self.data.size(0) - self.seq_len - 1, (1,))
        full_seq = self.data[rand_start: rand_start + self.seq_len + 1].long()
        return full_seq.cuda()

    def __len__(self):
        return self.data.size(0) // self.seq_len

