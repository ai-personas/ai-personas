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

        x_train = self.transform(x_train, dna, env)
        x_test = self.transform(x_test, dna, env)

        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, int(dna.output.size))
        y_test = keras.utils.to_categorical(y_test, int(dna.output.size))

        energy = Energy()
        energy.power(persona_def, x_train, y_train, x_test, y_test)

        return

    def transform(self, data, dna, env):
        # train_img_count = int(env.school.grades[0].courses[0].image_count)
        if len(dna.input.size) == 1:
            data = data.reshape(data.shape[0], int(dna.input.size[0]))
        elif len(dna.input.size) == 2:
            data = data.reshape(data.shape[0],
                                int(dna.input.size[0]),
                                int(dna.input.size[1])
                                )
        elif len(dna.input.size) == 3:
            data = data.reshape(data.shape[0],
                                int(dna.input.size[0]),
                                int(dna.input.size[1]),
                                int(dna.input.size[2])
                                )
        data = data.astype('float32')
        data /= 255
        return data

