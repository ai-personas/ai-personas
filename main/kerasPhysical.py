from __future__ import print_function

import json
from collections import namedtuple

from keras import Input, Model
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, Lambda
from keras.optimizers import RMSprop, Adadelta

from inputTransformation import InputTransformation as ipT
from outputTransformation import OutputTransformation as opT


class KerasSoftPhysical:

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
        from predefinedLambda import PredefinedLambda
        from outputShape import OutputShape
        layers = {}
        # build input layer
        # todo: layers should be sorted on lower to higher dependencies
        for ip in range(len(self.dna.input.channels)):
            input_id = self.dna.input.channels[ip].id
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
                        layers[model.id + layer.id] = Lambda(PredefinedLambda.euclidean_distance,
                                                             output_shape=OutputShape.single_output)

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
        for ip in range(len(self.dna.input.channels)):
            inputs.append(layers[self.dna.input.channels[ip].id])
        return Model(inputs, final_layer)

    def findIncomingLayers(self, layerId):
        incomingLayers = []
        for ip in range(len(self.dna.input.channels)):
            ip_layer = self.dna.input.channels[ip]
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
        # (x_train, y_train), (x_test, y_test) = self.multi_platform_input_handling(x_train, y_train, x_test, y_test)

        x_train_data = []
        y_train_data = []
        x_test_data = []
        y_test_data = []
        if self.dna.input.preTransform:
            if self.dna.input.preTransform.type == 'positiveNegativePair':
                # todo: generalize this for multi input, output
                (tr_pairs, tr_y) = ipT.input_transform_by_dna(self.dna.input.preTransform.type,
                                                              x_train, y_train)
                x_train_data.append(tr_pairs[:, 0])
                x_train_data.append(tr_pairs[:, 1])
                # todo: apart from pair creation, if input transformed, the output transformation not expected
                # todo: output transformation taken out separately
                y_train_data.append(tr_y)
                (te_pairs, te_y) = ipT.input_transform_by_dna(self.dna.input.preTransform.type,
                                                              x_test, y_test)
                x_test_data.append(te_pairs[:, 0])
                x_test_data.append(te_pairs[:, 1])
                y_test_data.append(te_y)
            elif self.dna.input.preTransform.type == 'match input size':
                x_train_data.append(ipT.match_input_size(x_train,
                                                         self.dna.input.channels,
                                                         self.dna.input.preTransform))
                x_test_data.append(ipT.match_input_size(x_test,
                                                        self.dna.input.channels,
                                                        self.dna.input.preTransform))
        else:
            x_train_data.append(x_train)
            x_test_data.append(x_test)

        if self.dna.output.postTransform:
            tr_y = opT.output_transform_by_dna(self.dna.output.postTransform.type,
                                               y_train,
                                               self.dna.output.channels[0])
            y_train_data.append(tr_y)
            te_y = opT.output_transform_by_dna(self.dna.output.postTransform.type,
                                               y_test,
                                               self.dna.output.channels[0])
            y_test_data.append(te_y)

        model = self.load_brain()
        batch_size = 128
        epochs = 2

        if len(x_train_data) == 1:
            x_train_data = x_train_data[0]
            y_train_data = y_train_data[0]
            x_test_data = x_test_data[0]
            y_test_data = y_test_data[0]

        history = model.fit(x_train_data, y_train_data,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            validation_data=(x_test_data, y_test_data))

    def get_loss(self):
        from customLoss import CustomLoss
        if self.dna.loss == 'categorical crossentropy':
            return 'categorical_crossentropy'
        if self.dna.loss == 'Contrastive Loss':
            return CustomLoss.contrastive_loss

    def get_optimizer(self):
        if self.dna.optimizer == 'RMS Probability':
            return RMSprop()
        elif self.dna.optimizer == 'Adadelta':
            return Adadelta()

    def load_brain(self):
        print("****************", self.personaDef.name)
        brain = self.create_persona()
        brain.load_weights("model/" + self.personaDef.name + ".h5")
        return brain

    def get_input_shape(self, id):
        from keras import backend as K
        channel = self.dna.input.channels[id]
        if len(channel.size) == 1:
            return (int(channel.size[0]),)
        # todo: assumed here 3d, make it generic
        elif self.dna.input.preTransform.channels_present:
            if K.image_data_format() == 'channels_first':
                return (int(channel.size[0]),
                        int(channel.size[1]),
                        int(channel.size[2]))
            else:
                return (int(channel.size[1]),
                        int(channel.size[2]),
                        int(channel.size[0]))
        elif len(channel.size) == 2:
            return (int(channel.size[0]),
                    int(channel.size[1]))
