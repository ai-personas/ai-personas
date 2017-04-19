
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


# In[2]:

INSTALLATION_PATH = "C:\\Users\\rames\\Documents\\GitHub\\ai-personas\\"
PYTHON_EXTENSION = ".py"
PROTO_PYTHON_EXTENSION = "_pb2.py"
PROTO_DEF_EXTENSION = ".bin"
PERSONA_VERSION = "1"
EXTRACTOR_MODULE = "../../Environment/Informations/Process/Extract/Extractor.py"
INFORMATION_BLUEPRINT = "../../Environment/Informations/informationBlueprint" + PROTO_PYTHON_EXTENSION

PERSONA_NAME_QUALIFIER = "PersonaDefinition"
PERSONA_BLUEPRINT_BASE = "../../Personas/personaBlueprint/version_" 
PERSONA_BLUEPRINT_NAME = "/personBlueprint" + PROTO_PYTHON_EXTENSION
PERSONA_NAME = "Khandhasamy" + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
PERSONA_DEF = "../../Personas/Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_1/" + PERSONA_NAME

class KerasPhysical(object):
    
    def __init__(self):
        return 
    
    ''' Load persona blue print (aka persona prototype). 
        Blue print path is constant. It won't change normally. From given version number, load respective persona blue print.
    '''
    def getPersonaBlueprint(self, version): 
        #persona blueprint path
        persona_blueprint_path = os.path.abspath(os.path.join(PERSONA_BLUEPRINT_BASE + str(version) + PERSONA_BLUEPRINT_NAME ))
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

class Test(object):
    
    def __init__(self):
        return 
    
    def testExtractor(self, personaBlueprintPath, personaDefPath, version):
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
tst.testExtractor(PERSONA_BLUEPRINT, PERSONA_DEF, PERSONA_VERSION)


# In[ ]:




# In[ ]:



