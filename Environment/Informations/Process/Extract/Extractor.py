
# coding: utf-8

# In[1]:

import sys
import imp
import os
import requests
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
import logging

INSTALLATION_PATH = "C:\\Users\\rames\\Documents\\GitHub\\ai-personas\\"
PYTHON_EXTENSION = ".py"
PROTO_PYTHON_EXTENSION = "_pb2.py"
PROTO_DEF_EXTENSION = ".bin"
EXTRACTOR_BASE = "Environment/Informations/Process/Extract"
INFORMATION_BLUEPRINT_BASE = "Environment/Informations/"
INFORMATION_BLUEPRINT_NAME = "informationBlueprint" + PROTO_PYTHON_EXTENSION

#------------- Logging configuration ------------------#
logging.basicConfig()
logger = logging.getLogger('Extractor')
logger.setLevel(logging.DEBUG)
#------------------------------------------------------#
              
class Extractor(object):
            
    def __init__(self, version, sourceName):
        self.informationDefinition = self.loadInformationDefinition(version, sourceName)
        
    ''' Get information blue print (aka information prototype) for given version.
    '''        
    def getInformationBlueprint(self, version):
        logger.debug("get information blueprint path")
        information_blueprint_path = os.path.abspath(os.path.join(INSTALLATION_PATH, INFORMATION_BLUEPRINT_BASE, INFORMATION_BLUEPRINT_NAME))
        logger.debug("information blue print path: " + information_blueprint_path)
        logger.debug("import information blueprint")
        informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()
        return informationBlueprint
        
    ''' Load information definition for given version.
    '''        
    def loadInformationDefinition(self, version, informationSourcename):
        logger.debug("get information path")
        information_path = os.path.abspath(os.path.join(INSTALLATION_PATH, informationSourcename))
        logger.debug("information path: " + information_path)
        f = open(information_path, "rb")
        information = self.getInformationBlueprint(version)
        information.ParseFromString(f.read())
        f.close()
        return information
        
    def loadSpecificExtractor(self, extractorName):
        logger.debug("load extractor: " + extractorName)
        specific_extractor_path = os.path.abspath(os.path.join(INSTALLATION_PATH, EXTRACTOR_BASE, extractorName + PYTHON_EXTENSION))
        logger.debug("import extractor " + specific_extractor_path)
        specificExtractor = imp.load_source('Extractor', specific_extractor_path).Extractor(self.informationDefinition)
        return specificExtractor
        
    def getExtractedData(self, sourceConnectionLayer):
        #FIXME: array shape has to be dynamic
        dataArray = np.zeros(shape=(0,1,50,50))
        for processor in self.informationDefinition.processors:
            specificExtractor = self.loadSpecificExtractor(processor.WhichOneof("Extractor"))
            logger.debug("data array shape: " + str(dataArray.shape))
            dataArray = np.vstack([specificExtractor.getExtractedData(processor, sourceConnectionLayer), dataArray])
        #split data for teaching, validation and test
        return dataArray
    
    def getTeachingData(self, sourceConnectionLayer):
        dataArray = self.getExtractedData(sourceConnectionLayer)
        logger.debug("data array shape: " + str(dataArray.shape))
        '''Get data for teaching percentage'''
        teaching_data_percentage = sourceConnectionLayer.teachingDataPercentage
        logger.debug("Teaching data percentage: " + str(teaching_data_percentage))
        teaching_data_length = dataArray.shape[0] * (teaching_data_percentage/100)
        teaching_data_array = dataArray[:teaching_data_length,:]
        logger.debug(teaching_data_array.shape)
        return teaching_data_array 


# In[2]:

PERSONA_NAME_QUALIFIER = "PersonaDefinition"
TEST_PERSONA_BLUEPRINT = "../../../../Personas/personaBlueprint/version_1/personBlueprint" + PROTO_PYTHON_EXTENSION
TEST_PERSONA_NAME = "Khandhasamy" + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
TEST_PERSONA_DEF = "../../../../Personas/Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_1/" + TEST_PERSONA_NAME
TEST_VERSION = "1"

class test(object):
    
    def __init__(self):
        return 
        
    def getPersonaBlueprint(self, personaBlueprintPath): 
        #persona blueprint path
        persona_blueprint_path = os.path.abspath(os.path.join(personaBlueprintPath))
        logger.debug("TEST - Persona blueprint path: " + persona_blueprint_path)
        #persona blueprint
        personaBlueprint = imp.load_source('Persona', persona_blueprint_path).Persona() 
        return personaBlueprint
    
    def loadPersona(self, personaBlueprintPath, personaDefPath):
        # persona blueprint
        persona = self.getPersonaBlueprint(personaBlueprintPath)
        #load persona
        persona_path = os.path.abspath(os.path.join(personaDefPath))
        logger.debug("TEST - Persona definition path:" + persona_path)
        f = open(personaDefPath, "rb")
        persona.ParseFromString(f.read())
        f.close()        
        return persona
    
    def testExtractedData(self, personaBlueprintPath, personaDefPath):
        persona = self.loadPersona(personaBlueprintPath, personaDefPath)
        #get source name
        environment = persona.age.environments[0]
        source = environment.library.sources[0]
        logger.debug("TEST - information source: " + source.sourceName)
        extractor = Extractor(TEST_VERSION, INSTALLATION_PATH + source.sourceName)
        sourceConnectionLayer = source.sourceConnectionLayers[0]
        informationDef = extractor.loadInformationDefinition(TEST_VERSION, INSTALLATION_PATH + source.sourceName)
        processor = informationDef.processors[0]
        logger.debug("get extracted data")
        extractor.getTeachingData(sourceConnectionLayer)
        return 

# tst = test()
# tst.testExtractedData(TEST_PERSONA_BLUEPRINT, TEST_PERSONA_DEF)


# In[ ]:



