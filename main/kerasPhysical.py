
from __future__ import print_function

from collections import namedtuple

import keras
from keras.datasets import mnist
from keras.engine.saving import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import json

class KerasSoftPhysical():

    def __init__(self, personaDef):
        self.personaDef = personaDef
        self.dna = json.loads(personaDef.dna, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def create_persona(self):
        model = Sequential()
        output = self.dna.output.size

        for li in range(len(self.dna.layers)):
            if self.dna.layers[li].type == 'Dense':
                if str(li+1) in self.dna.input.connected_layer:
                    model.add(Dense(int(self.dna.layers[li].size),
                                    activation=self.dna.layers[li].activation,
                                    input_shape=(int(self.dna.input.size),)))
                else:
                    model.add(Dense(int(self.dna.layers[li].size),
                                    activation=self.dna.layers[li].activation))
            elif self.dna.layers[li].type == 'Dropout':
                model.add(Dropout(float(self.dna.layers[li].dropoutRate)))

        model.summary()
        model.compile(loss=self.get_loss(),
                      optimizer=self.get_optimizer(),
                      metrics=['accuracy'])
        return model

    # def personaTeaching(self):



    def persona(self, environment):
        self.model = self.create_persona()

        train_img_count = int(environment.school.grades[0].courses[0].image_count)
        test_img_count = int(environment.school.grades[0].test[0].image_count)

        batch_size = 128
        epochs = 2

        # the data, split between train and test sets
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()

        self.x_train = self.x_train.reshape(train_img_count, 784)
        self.x_test = self.x_test.reshape(test_img_count, 784)
        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255
        print(self.x_train.shape[0], 'train samples')
        print(self.x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(self.y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(self.y_test, self.num_classes)

        history = self.model.fit(self.x_train, self.y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_data=(self.x_test, self.y_test))
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def mnist_test(self):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def main(self, environment):
        self.persona(environment)


    def get_loss(self):
        if self.dna.loss == 'categorical crossentropy':
            return 'categorical_crossentropy'

    def get_optimizer(self):
        if self.dna.optimizer == 'RMS Probability':
            return RMSprop()

    def load_brain(self, personaDef):
        return load_model("model/" + personaDef.name + ".h5")