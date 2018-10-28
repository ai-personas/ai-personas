
from __future__ import print_function

import json
from collections import namedtuple

from keras.engine.saving import load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, K
from keras.models import Sequential
from keras.optimizers import RMSprop, Adadelta


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
                                    input_shape=self.get_input_shape()))
                else:
                    model.add(Dense(int(self.dna.layers[li].size),
                                    activation=self.dna.layers[li].activation))
            elif self.dna.layers[li].type == 'Dropout':
                model.add(Dropout(float(self.dna.layers[li].dropoutRate)))
            elif self.dna.layers[li].type == 'Conv2D':
                if str(li+1) in self.dna.input.connected_layer:
                    model.add(Conv2D(int(self.dna.layers[li].filters),
                                    kernel_size=(int(self.dna.layers[li].kernal_size[0]),
                                                 int(self.dna.layers[li].kernal_size[1])
                                                 ),
                                    activation=self.dna.layers[li].activation,
                                    input_shape=self.get_input_shape()
                                     )
                              )
                else:
                    model.add(Conv2D(int(self.dna.layers[li].filters),
                                    kernel_size=(int(self.dna.layers[li].kernal_size[0]),
                                                 int(self.dna.layers[li].kernal_size[1])
                                                 ),
                                    activation=self.dna.layers[li].activation
                                     )
                              )
            elif self.dna.layers[li].type == 'MaxPooling2D':
                model.add(MaxPooling2D(pool_size=(
                    int(self.dna.layers[li].pool_size[0]),
                    int(self.dna.layers[li].pool_size[1])
                )))
            elif self.dna.layers[li].type == 'Flatten':
                model.add(Flatten())

        model.summary()
        model.compile(loss=self.get_loss(),
                      optimizer=self.get_optimizer(),
                      metrics=['accuracy'])
        return model

    # def personaTeaching(self):



        # score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        # print('Test loss:', score[0])
        # print('Test accuracy:', score[1])

    def mnist_test(self):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def learn(self, x_train, y_train, x_test, y_test):
        if self.dna.input.channels_present:
            print("---------", x_train.shape)
        model = self.load_brain()
        batch_size = 128
        epochs = 2
        history = model.fit(x_train, y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_data=(x_test, y_test))


    def get_loss(self):
        if self.dna.loss == 'categorical crossentropy':
            return 'categorical_crossentropy'

    def get_optimizer(self):
        if self.dna.optimizer == 'RMS Probability':
            return RMSprop()
        elif self.dna.optimizer == 'Adadelta':
            return Adadelta()


    def load_brain(self):
        print("****************", self.personaDef.name)
        return load_model("model/" + self.personaDef.name + ".h5")

    def get_input_shape(self):
        if len(self.dna.input.size) == 1:
            return (int(self.dna.input.size[0]), )
        elif self.dna.input.channels_present:
            if K.image_data_format() == 'channels_first':
                return (int(self.dna.input.size[0]),
                        int(self.dna.input.size[1]),
                        int(self.dna.input.size[2]))
            else:
                return (int(self.dna.input.size[1]),
                        int(self.dna.input.size[2]),
                        int(self.dna.input.size[0]))
        elif len(self.dna.input.size) == 2:
            return (int(self.dna.input.size[0]),
                    int(self.dna.input.size[1]))
