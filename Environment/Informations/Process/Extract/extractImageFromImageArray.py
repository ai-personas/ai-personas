
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

PROTO_PYTHON_EXTENSION = "_pb2.py"
PROTO_DEF_EXTENSION = ".bin"
INFORMATION_BLUEPRINT = "../../informationBlueprint" + PROTO_PYTHON_EXTENSION
LOADER_NAME = "Loader.py"
LOADER_PATH = "Environment/Informations/Process/Load/" + LOADER_NAME


#------------- Logging configuration ------------------#
logging.basicConfig()
logger = logging.getLogger('Extractor')
logger.setLevel(logging.DEBUG)
#------------------------------------------------------#
              
class Extractor(object):
        
    SOURCE_TRANSFORMATION = "imageSource"
    
    def __init__(self, informationDef, sourceName):
        self.informationDefinition = informationDef
    
    def getLoader(self, processor):
        logger.debug("get loader path")
        loader_path = os.path.abspath(os.path.join(INSTALLATION_PATH, LOADER_PATH))
        logger.debug("loader path: " + loader_path)
        logger.debug("import loader")
        loader = imp.load_source('Loader', loader_path).Loader(processor)
        return loader
    
    def transformImage(self, imageSourceParameter, img):
        img_width = int(imageSourceParameter.imageWidth)
        img_height = int(imageSourceParameter.imageHeight)
        img = img.resize((img_width, img_height), Image.ANTIALIAS)
        imageProcess = imageSourceParameter.imageProcess
        for pIndex in range(len(imageProcess)):
            if imageProcess[pIndex] == 'grey':
                img = img.convert("L")         
            if imageProcess[pIndex] == 'edge':
                img = img.filter(ImageFilter.FIND_EDGES)        
        return img
    
    def getExtractedData(self, processor, sourceConnectionLayer):
        logger.debug("call loader: " + processor.WhichOneof("Loader"))
        #call loader
        loader = self.getLoader(processor)
        logger.debug("source parameter: " + sourceConnectionLayer.WhichOneof("SourceParameter"))
        processedImgDataList = []
        if sourceConnectionLayer.WhichOneof("SourceParameter") == self.SOURCE_TRANSFORMATION:      
            imgList = loader.getData()
            for imgIndex in range(len(imgList)):
                img = self.transformImage(sourceConnectionLayer.imageSource, imgList[imgIndex])
                imgToArray = np.asarray(img, dtype=np.float32)
                #if 2d array, then its grey color and append as list to make it as 3d array in conversion 
                if len(imgToArray.shape) == 2:
                    processedImgDataList.append([imgToArray])
                else:
                    #else, its multi array, append as its.
                    processedImgDataList.append(imgToArray)
            processedImgDataList = np.asarray(processedImgDataList)
            logger.debug("data shape: " + str(processedImgDataList.shape))
            return processedImgDataList
        return


# In[2]:

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
        
    def getInformationBlueprint(self, informationBlueprintPath):
        logger.debug("get information blueprint path")
        information_blueprint_path = os.path.abspath(os.path.join(informationBlueprintPath))
        logger.debug("information blue print path: " + information_blueprint_path)
        logger.debug("import information blueprint")
        informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()
        return informationBlueprint
        
    def loadInformationDefinition(self, informationBlueprintPath, informationSourcename):
        logger.debug("get information path")
        information_path = os.path.abspath(os.path.join(informationSourcename))
        logger.debug("information path: " + information_path)
        f = open(information_path, "rb")
        information = self.getInformationBlueprint(informationBlueprintPath)
        information.ParseFromString(f.read())
        f.close()
        return information
    
    def testExtractedData(self, personaBlueprintPath, personaDefPath):
        persona = self.loadPersona(personaBlueprintPath, personaDefPath)
        #get source name
        environment = persona.age.environments[0]
        source = environment.library.sources[0]
        logger.debug("TEST - information source: " + source.sourceName)
        informationDef = self.loadInformationDefinition(INFORMATION_BLUEPRINT, INSTALLATION_PATH + source.sourceName)
        extractor = Extractor(informationDef, INSTALLATION_PATH + source.sourceName)
        sourceConnectionLayer = source.sourceConnectionLayers[0]
        processor = informationDef.processors[0]
        logger.debug("get extracted data")
        extractor.getExtractedData(processor,sourceConnectionLayer)
        return 
    
PERSONA_NAME_QUALIFIER = "PersonaDefinition"
TEST_PERSONA_BLUEPRINT = "../../../../Personas/personaBlueprint/version_1/personBlueprint" + PROTO_PYTHON_EXTENSION
TEST_PERSONA_NAME = "Khandhasamy" + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
TEST_PERSONA_DEF = "../../../../Personas/Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_1/" + TEST_PERSONA_NAME
    
tst = test()
tst.testExtractedData(TEST_PERSONA_BLUEPRINT, TEST_PERSONA_DEF)


# In[ ]:



