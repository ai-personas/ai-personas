
from __future__ import print_function

import json
from collections import namedtuple

from keras import Input, Model
from keras.engine.saving import load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, K
from keras.optimizers import RMSprop, Adadelta


class KerasSoftPhysical():

    def __init__(self, personaDef):
        self.personaDef = personaDef
        self.dna = json.loads(personaDef.dna, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def create_persona(self):
        model = self.create_network()
        model.summary()
        model.compile(loss=self.get_loss(),
                      optimizer=self.get_optimizer(),
                      metrics=['accuracy'])
        return model

    def create_network(self):
        layers = {}
        # build input layer
        # todo: layers should be sorted on lower to higher dependencies
        for ip in range(len(self.dna.input)):
            layers[self.dna.input[ip].id] = Input(shape=self.get_input_shape(ip))

        # build rest of the layers
        for li in range(len(self.dna.layers)):
            if self.dna.layers[li].type == 'Dense':
                layers[self.dna.layers[li].id] = Dense(int(self.dna.layers[li].size),
                                                        activation=self.dna.layers[li].activation)
            elif self.dna.layers[li].type == 'Dropout':
                layers[self.dna.layers[li].id] = Dropout(float(self.dna.layers[li].dropoutRate))
            elif self.dna.layers[li].type == 'Conv2D':
                layers[self.dna.layers[li].id] = Conv2D(int(self.dna.layers[li].filters),
                                kernel_size=(int(self.dna.layers[li].kernal_size[0]),
                                             int(self.dna.layers[li].kernal_size[1])
                                             ),
                                activation=self.dna.layers[li].activation
                                 )
            elif self.dna.layers[li].type == 'MaxPooling2D':
                layers[self.dna.layers[li].id] = MaxPooling2D(pool_size=(
                    int(self.dna.layers[li].pool_size[0]),
                    int(self.dna.layers[li].pool_size[1])
                ))
            elif self.dna.layers[li].type == 'Flatten':
                layers[self.dna.layers[li].id] = Flatten()

        print("***********", layers)
        print("***********", range(len(layers)))

        # build connections
        for id, layer in layers.items():
            # todo: is there optimization here for graph?
            incomingLayers = self.findIncomingLayers(id)
            print(id, incomingLayers)
            # todo: merge layers if incoming more than 1
            if len(incomingLayers) == 1:
                layers[id] = layer(layers[incomingLayers[0]])
        # todo: multiple input possible here?
        print("last layer:", list(layers.keys())[-1])
        return Model(layers["i1"], layers[list(layers.keys())[-1]])

    def findIncomingLayers(self, layerId):
        incomingLayers = []
        for ip in range(len(self.dna.input)):
            for cl in range(len(self.dna.input[ip].connected_layer)):
                if self.dna.input[ip].connected_layer[cl] == layerId:
                    incomingLayers.append(self.dna.input[ip].id)
                    break
        for li in range(len(self.dna.layers)):
            for cl in range(len(self.dna.layers[li].connected_layer)):
                if self.dna.layers[li].connected_layer[cl] == layerId:
                    incomingLayers.append(self.dna.layers[li].id)
        return incomingLayers

    def mnist_test(self):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def teach(self, x_train, y_train, x_test, y_test):
        (x_train, y_train), (x_test, y_test) = self.multi_platform_input_handling(x_train, y_train, x_test, y_test)
        model = self.load_brain()
        batch_size = 128
        epochs = 2
        history = model.fit(x_train, y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_data=(x_test, y_test))

    def multi_platform_input_handling(self, x_train, y_train, x_test, y_test):
        # todo: multiple input handling
        if self.dna.input[0].channels_present:
            print("---------", x_train.shape)
            # todo: handle it in generic way.
            if K.image_data_format() == 'channels_first':
                x_train = x_train.reshape(x_train.shape[0],
                                          x_train.shape[1],
                                          x_train.shape[2],
                                          x_train.shape[3])
                x_test = x_test.reshape(x_test.shape[0],
                                        x_test.shape[1],
                                        x_test.shape[2],
                                        x_test.shape[3])
            else:
                x_train = x_train.reshape(x_train.shape[0],
                                          x_train.shape[2],
                                          x_train.shape[3],
                                          x_train.shape[1])
                x_test = x_test.reshape(x_test.shape[0],
                                        x_test.shape[2],
                                        x_test.shape[3],
                                        x_test.shape[1])
        return (x_train, y_train), (x_test, y_test)

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


    def get_input_shape(self, ip):
        if len(self.dna.input[ip].size) == 1:
            return (int(self.dna.input[ip].size[0]), )
        # todo: assumed here 3d, make it generic
        elif self.dna.input[ip].channels_present:
            if K.image_data_format() == 'channels_first':
                return (int(self.dna.input[ip].size[0]),
                        int(self.dna.input[ip].size[1]),
                        int(self.dna.input[ip].size[2]))
            else:
                return (int(self.dna.input[ip].size[1]),
                        int(self.dna.input[ip].size[2]),
                        int(self.dna.input[ip].size[0]))
        elif len(self.dna.input[ip].size) == 2:
            return (int(self.dna.input[ip].size[0]),
                    int(self.dna.input[ip].size[1]))
