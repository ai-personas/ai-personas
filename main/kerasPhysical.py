
from __future__ import print_function

import json
from collections import namedtuple

from keras import Input, Model
from keras.engine.saving import load_model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, K, Lambda
from keras.optimizers import RMSprop, Adadelta
import numpy as np
import random

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
            input_id = self.dna.input.layers[ip].id
            print("inputId:", input_id)
            layers[input_id] = Input(shape=self.get_input_shape(ip))
            print("input:", layers[input_id])
            print("inputShape:", self.get_input_shape(ip))

        # build rest of the layers
        # todo: models and layers needs to sorted based on lower dependency before building it
        for mi in range(len(self.dna.models)):
            model = self.dna.models[mi]
            for li in range(len(model.layers)):
                layer = model.layers[li]
                if layer.sharedLayer:
                    # todo: sort lower dependent layers and create them first
                    layers[model.id + layer.id] = layers[layer.sharedLayer.model + layer.sharedLayer.layer]
                else:
                    if layer.type == 'Dense':
                        layers[model.id + layer.id] = Dense(int(layer.size),
                                                                activation=layer.activation)
                    elif layer.type == 'Dropout':
                        layers[model.id + layer.id] = Dropout(float(layer.dropoutRate))
                    elif layer.type == 'Conv2D':
                        layers[model.id + layer.id] = Conv2D(int(layer.filters),
                                        kernel_size=(int(layer.kernal_size[0]),
                                                     int(layer.kernal_size[1])
                                                     ),
                                        activation=layer.activation
                                         )
                    elif layer.type == 'MaxPooling2D':
                        layers[model.id + layer.id] = MaxPooling2D(pool_size=(
                            int(layer.pool_size[0]),
                            int(layer.pool_size[1])
                        ))
                    elif layer.type == 'Flatten':
                        layers[model.id + layer.id] = Flatten()
                    elif layer.type == 'Lambda':
                        layers[model.id + layer.id] = Lambda(self.euclidean_distance,
                                                             output_shape=self.eucl_dist_output_shape)

        print("***********", layers)
        print("***********", range(len(layers)))

        # build connections
        for id, layer in layers.items():
            # todo: is there optimization here for graph?
            incomingLayersIds = self.findIncomingLayers(id)
            print(id, incomingLayersIds)
            incoming_layers = []
            for ild in range(len(incomingLayersIds)):
                print("incomingLayerId:", incomingLayersIds[ild])
                incoming_layers.append(layers[incomingLayersIds[ild]])
            if incoming_layers:
                print("incoming:", incoming_layers)
                if len(incoming_layers) == 1:
                    layers[id] = layer(incoming_layers[0])
                else:
                    print("incoming more than one")
                    layers[id] = layer(incoming_layers)

        # build inputs
        print("last layer:", list(layers.keys())[-1])
        final_layer = layers[list(layers.keys())[-1]]
        inputs = []
        for ip in range(len(self.dna.input.layers)):
            inputs.append(layers[self.dna.input.layers[ip].id])
        return Model(inputs, final_layer)

    def findIncomingLayers(self, layerId):
        incomingLayers = []
        for ip in range(len(self.dna.input.layers)):
            ip_layer = self.dna.input.layers[ip]
            for cl in range(len(ip_layer.connected)):
                connected = ip_layer.connected[cl]
                for li in range(len(connected.layers)):
                    layer = connected.layers[li]
                    if (connected.model + layer) == layerId:
                        incomingLayers.append(ip_layer.id)
                        break
        for mi in range(len(self.dna.models)):
            model = self.dna.models[mi]
            for li in range(len(model.layers)):
                layer = model.layers[li]
                for ci in range(len(layer.connected)):
                    connected = layer.connected[ci]
                    for cli in range(len(connected.layers)):
                        c_layer = connected.layers[cli]
                        if (connected.model + c_layer) == layerId:
                            incomingLayers.append(model.id + layer.id)
        return incomingLayers

    def mnist_test(self):
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def learn(self, x_train, y_train, x_test, y_test):
        # todo: mutliple input, multi output generalization
        (x_train, y_train), (x_test, y_test) = self.multi_platform_input_handling(x_train, y_train, x_test, y_test)


        if self.dna.input.preTransform:
            (tr_pairs, tr_y) = self.transform_by_dna(self.dna.input.preTransform.type,
                                                    x_train, y_train)
            (te_pairs, te_y) = self.transform_by_dna(self.dna.input.preTransform.type,
                                                    x_test, y_test)
        model = self.load_brain()
        batch_size = 128
        epochs = 2
        history = model.fit([tr_pairs[:, 0], tr_pairs[:, 1]], tr_y,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_data=([te_pairs[:, 0], te_pairs[:, 1]], te_y))
        # history = model.fit(x_train, y_train,
        #                     batch_size=batch_size,
        #                     epochs=epochs,
        #                     verbose=1,
        #                     validation_data=(x_test, y_test))

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
        if self.dna.loss == 'Contrastive Loss':
            return self.contrastive_loss

    def get_optimizer(self):
        if self.dna.optimizer == 'RMS Probability':
            return RMSprop()
        elif self.dna.optimizer == 'Adadelta':
            return Adadelta()

    def load_brain(self):
        print("****************", self.personaDef.name)
        return load_model("model/" + self.personaDef.name + ".h5")


    def get_input_shape(self, id):
        ip_layer = self.dna.input.layers[id]
        if len(ip_layer.size) == 1:
            return (int(ip_layer.size[0]),)
        # todo: assumed here 3d, make it generic
        elif ip_layer.channels_present:
            if K.image_data_format() == 'channels_first':
                return (int(ip_layer.size[0]),
                        int(ip_layer.size[1]),
                        int(ip_layer.size[2]))
            else:
                return (int(ip_layer.size[1]),
                        int(ip_layer.size[2]),
                        int(ip_layer.size[0]))
        elif len(ip_layer.size) == 2:
            return (int(ip_layer.size[0]),
                    int(ip_layer.size[1]))


    def euclidean_distance(self, vects):
        x, y = vects
        sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
        return K.sqrt(K.maximum(sum_square, K.epsilon()))

    def eucl_dist_output_shape(self, shapes):
        shape1, shape2 = shapes
        return (shape1[0], 1)

    def contrastive_loss(self, y_true, y_pred):
        '''Contrastive loss from Hadsell-et-al.'06
        http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf
        '''
        margin = 1
        sqaure_pred = K.square(y_pred)
        margin_square = K.square(K.maximum(margin - y_pred, 0))
        return K.mean(y_true * sqaure_pred + (1 - y_true) * margin_square)

    def transform_by_dna(self, type, x, y):
        if type == 'positiveNegativePair':
            return self.createPositiveNegativePair(x, y, 10)

    def createPositiveNegativePair(self, x_train, y_train, num_classes):
        # create training+test positive and negative pairs
        digit_indices = [np.where(y_train == i)[0] for i in range(num_classes)]
        tr_pairs, tr_y = self.create_pairs(x_train, digit_indices)
        print("tr_y:", tr_y)
        return (tr_pairs, tr_y)

        # digit_indices = [np.where(y_test == i)[0] for i in range(num_classes)]
        # te_pairs, te_y = self.create_pairs(x_test, digit_indices)


    def create_pairs(self, x, digit_indices, num_classes):
        '''Positive and negative pair creation.
        Alternates between positive and negative pairs.
        '''
        pairs = []
        labels = []
        n = min([len(digit_indices[d]) for d in range(num_classes)]) - 1
        print("create pair min:", n)
        for d in range(num_classes):
            for i in range(n):
                z1, z2 = digit_indices[d][i], digit_indices[d][i + 1]
                pairs += [[x[z1], x[z2]]]
                inc = random.randrange(1, num_classes)
                dn = (d + inc) % num_classes
                z1, z2 = digit_indices[d][i], digit_indices[dn][i]
                pairs += [[x[z1], x[z2]]]
                labels += [1, 0]
        return np.array(pairs), np.array(labels)

