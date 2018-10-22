
from __future__ import print_function

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import json

class KerasSoftPhysical():

    def __init__(self, personaDef):
        self.personaDef = personaDef

    def create_persona(self):
        self.num_classes = 10

        model = Sequential()
        dna = json.loads(self.personaDef.dna)
        layer = dna['layers']

        for li in range(len(layer)):
            if layer[li] == 'Dense':
                model.add(Dense(512, activation='relu', input_shape=(784,)))
            elif layer[li] == 'Dropout':
                model.add(Dropout(0.2))

        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.summary()
        model.compile(loss='categorical_crossentropy',
                      optimizer=RMSprop(),
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
