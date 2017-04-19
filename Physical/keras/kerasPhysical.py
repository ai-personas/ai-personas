
# coding: utf-8

# In[1]:

import os
os.environ["KERAS_BACKEND"] = "theano"

import imp
import logging
from __future__ import print_function
import numpy as np

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import PIL
from PIL import Image, ImageFilter
import requests
from io import BytesIO

#------------- Logging configuration ------------------#
logging.basicConfig()
logger = logging.getLogger('Extractor')
logger.setLevel(logging.DEBUG)
#------------------------------------------------------#


# In[18]:

INSTALLATION_PATH = "C:\\Users\\rames\\Documents\\GitHub\\ai-personas\\"
PYTHON_EXTENSION = ".py"
PROTO_PYTHON_EXTENSION = "_pb2.py"
PROTO_DEF_EXTENSION = ".bin"
PERSONA_VERSION = "1"
EXTRACTOR_MODULE = "../../Environment/Informations/Process/Extract/Extractor.py"
INFORMATION_BLUEPRINT = "../../Environment/Informations/informationBlueprint" + PROTO_PYTHON_EXTENSION

PERSONA_NAME_QUALIFIER = "PersonaDefinition"
PERSONA_BLUEPRINT_BASE = "Personas/personaBlueprint/version_" 
PERSONA_BLUEPRINT_NAME = "personBlueprint" + PROTO_PYTHON_EXTENSION
PERSONA_NAME = "Khandhasamy" + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
PERSONA_DEF = "../../Personas/Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_1/" + PERSONA_NAME

class KerasPhysical(object):
    
    LAYER_CONVOLUTION = "layerConvolution"
    LAYER_ACTIVATION = "layerActivation"
    LAYER_DROPOUT = "layerDropout"

    model = Sequential()
    
    def __init__(self):
        return 
    
    ''' Load persona blue print (aka persona prototype). 
        Blue print path is constant. It won't change normally. From given version number, load respective persona blue print.
    '''
    def getPersonaBlueprint(self, version): 
        #persona blueprint path
        persona_blueprint_path = os.path.abspath(os.path.join(INSTALLATION_PATH,PERSONA_BLUEPRINT_BASE+str(version), PERSONA_BLUEPRINT_NAME ))
        logger.debug("Persona blueprint path: " + persona_blueprint_path)
        #persona blueprint
        personaBlueprint = imp.load_source('Persona', persona_blueprint_path).Persona() 
        return personaBlueprint
    
    ''' Load persona definition for given version persona blue print.
    '''
    def loadPersona(self, version, personaDefPath):
        # persona blueprint
        persona = self.getPersonaBlueprint(version)
        #load persona
        persona_path = os.path.abspath(os.path.join(personaDefPath))
        logger.debug("Persona definition path:" + persona_path)
        f = open(personaDefPath, "rb")
        persona.ParseFromString(f.read())
        f.close()        
        return persona   
    
    def getExtractor(self, version, source):
        logger.debug("get extractor path")
        extractor_path = os.path.abspath(os.path.join(EXTRACTOR_MODULE))
        logger.debug("extractor path: " + extractor_path)
        logger.debug("import extractor")
        extractor = imp.load_source('Extractor', extractor_path).Extractor(version, source.sourceName)
        return extractor
    
    def generateConvolutionLayer(self, layer):
        nb_filters = layer.layerConvolution.filters
        convDimension = layer.layerConvolution.convolutionDimension
        borderMode = layer.layerConvolution.borderMode
        kernelSize = layer.layerConvolution.kernelSize
        inputShape = layer.layerConvolution.inputShape
        if K.image_dim_ordering() == 'th':
            conv_input_shape = (inputShape[0], inputShape[1], inputShape[2])
        else:
            conv_input_shape = (inputShape[1], inputShape[2], inputShape[0])
        if convDimension == 2:
            self.model.add(Convolution2D(nb_filters, kernelSize[0], kernelSize[1],
                border_mode=borderMode,
                input_shape=conv_input_shape))
            logger.debug("Convolution layer generated")
            
    def generateActivationLayer(self, layer):
        activationType = layer.layerActivation.activationType
        self.model.add(Activation(activationType))
        logger.debug("Activation layer generated")
        
    def generateDropoutLayer(self, layer):
        dropoutPercentage = layer.layerDropout.dropPercentage
        self.model.add(Dropout(dropoutPercentage))
        logger.debug("Dropout layer generated")
        
    def generateDNA(self, dna):
        for layer in dna.layers:
            if (LAYER_CONVOLUTION == layer.WhichOneof("SubLayer")): 
                self.generateConvolutionLayer(layer)
            elif (LAYER_ACTIVATION == layer.WhichOneof("SubLayer")):
                self.generateActivationLayer(layer)
            elif (LAYER_DROPOUT == layer.WhichOneof("SubLayer")):
                self.generateDropoutLayer(layer)
        return
    
    def compileModel(self):
        self.model.compile(loss='binary_crossentropy', optimizer='adadelta')
        return
    
    def runModel(self):
        self.model.fit(x_train_data, y_train_data, batch_size=batch_size, nb_epoch=nb_epoch,
                    verbose=1, validation_data=(x_train_data, y_train_data))
        return

    def savePersona(self):
        return
    
class Test(object):
    
    def __init__(self):
        return 
    
    def testExtractor(self, personaDefPath, version):
        kerasPhysical = KerasPhysical()
        persona = kerasPhysical.loadPersona(version, personaDefPath)   
        for environment in persona.age.environments:
            for source in environment.library.sources:
                logger.debug("TEST source name: " + source.sourceName)
                extractor = kerasPhysical.getExtractor(version, source)
                sourceConnectionLayer = source.sourceConnectionLayers[0]
                extractor.getTeachingData(sourceConnectionLayer)
        return
    
tst = Test()
tst.testExtractor(PERSONA_DEF, PERSONA_VERSION)


# In[ ]:




# In[ ]:



