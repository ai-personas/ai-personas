
from __future__ import print_function

from collections import namedtuple

import keras
from keras.datasets import mnist
from keras.engine.saving import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, K
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
            elif self.dna.layers[li].type == 'Conv2D':
                if str(li+1) in self.dna.input.connected_layer:
                    model.add(Conv2D(int(self.dna.layers[li].filters),
                                    kernel_size=(int(self.dna.layers[li].kernal_size[0]),
                                                 int(self.dna.layers[li].kernal_size[1])
                                                 ),
                                    activation=self.dna.layers[li].activation,
                                    input_shape=(int(self.dna.input.size[0]),
                                                 int(self.dna.input.size[1])
                                                 )
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

    def load_brain(self):
        print("****************", self.personaDef.name)
        return load_model("model/" + self.personaDef.name + ".h5")

    def get_input_shape(self):
        if K.image_data_format() == 'channels_first':
            
