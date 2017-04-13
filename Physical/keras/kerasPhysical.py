
# coding: utf-8

# In[6]:

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


# In[9]:

INSTALLATION_PATH = "C:\\Users\\rames\\Documents\\GitHub\\ai-personas\\"
PYTHON_EXTENSION = ".py"
PROTO_PYTHON_EXTENSION = "_pb2.py"
PROTO_DEF_EXTENSION = ".bin"
INFORMATION_BLUEPRINT = "../../informationBlueprint" + PROTO_PYTHON_EXTENSION

PERSONA_NAME_QUALIFIER = "PersonaDefinition"
PERSONA_BLUEPRINT = "../../Personas/personaBlueprint/version_1/personBlueprint" + PROTO_PYTHON_EXTENSION
PERSONA_NAME = "Khandhasamy" + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
PERSONA_DEF = "../../Personas/Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_1/" + PERSONA_NAME

class KerasPhysical(object):
    
    def __init__(self):
        return 
        
    def getPersonaBlueprint(self, personaBlueprintPath): 
        #persona blueprint path
        persona_blueprint_path = os.path.abspath(os.path.join(personaBlueprintPath))
        logger.debug("Persona blueprint path: " + persona_blueprint_path)
        #persona blueprint
        personaBlueprint = imp.load_source('Persona', persona_blueprint_path).Persona() 
        return personaBlueprint
    
    def loadPersona(self, personaBlueprintPath, personaDefPath):
        # persona blueprint
        persona = self.getPersonaBlueprint(personaBlueprintPath)
        #load persona
        persona_path = os.path.abspath(os.path.join(personaDefPath))
        logger.debug("Persona definition path:" + persona_path)
        f = open(personaDefPath, "rb")
        persona.ParseFromString(f.read())
        f.close()        
        return persona   
    
    def getExtractor(self, source):
        return

class Test(object):
    
    def __init__(self):
        return 
    
    def testExtractor(self, personaBlueprintPath, personaDefPath):
        kerasPhysical = KerasPhysical()
        persona = kerasPhysical.loadPersona(personaBlueprintPath, personaDefPath)   
        for environment in persona.age.environments:
            for source in environment.library.sources:
                kerasPhysical.getExtractor(source)
        return
    
tst = Test()
tst.testExtractor(PERSONA_BLUEPRINT, PERSONA_DEF)


# In[ ]:



