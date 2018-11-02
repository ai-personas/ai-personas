import json
from collections import namedtuple

import keras
from keras.datasets import mnist

from energy import Energy


class School():

    def schedule(self, persona_def):
        #TODO: check previous passed grades????
        #TODO: courses are just materials???? who is teaching it????
        env = json.loads(persona_def.age.environments, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        dna = json.loads(persona_def.dna, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        school = env.school
        train_img_count = int(school.grades[0].courses[0].image_count)
        test_img_count = int(school.grades[0].test[0].image_count)

        x_train = []
        y_train = []
        x_test = []
        y_test = []

        if school.grades[0].courses[0].data_provider == 'keras.mnist':
            (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # todo: if multiple input present, how school know which input preferred by persona
        # todo: if course has audio, video, action etc., and persona has multiple input, where is the coordination?
        x_train = self.transform(x_train, dna.input[0])
        x_test = self.transform(x_test, dna.input[0])

        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        # todo: if multiple represented by persona, which one or many considered by school?
        y_train = keras.utils.to_categorical(y_train, int(dna.output[0].size))
        y_test = keras.utils.to_categorical(y_test, int(dna.output[0].size))

        energy = Energy()
        energy.power(persona_def, x_train, y_train, x_test, y_test)
        return

    def transform(self, data, input):
        # todo: make it generic
        if len(input.size) == 1:
            data = data.reshape(data.shape[0], int(input.size[0]))
        elif len(input.size) == 2:
            data = data.reshape(data.shape[0],
                                int(input.size[0]),
                                int(input.size[1])
                                )
        elif len(input.size) == 3:
            data = data.reshape(data.shape[0],
                                int(input.size[0]),
                                int(input.size[1]),
                                int(input.size[2])
                                )
        data = data.astype('float32')
        data /= 255
        return data

