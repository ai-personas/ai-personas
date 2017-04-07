
# coding: utf-8

# In[14]:

import sys
import imp
import os
import requests
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
import logging

INFORMATION_BLUEPRINT = "../../informationBlueprint"
INFORMATION_BASE = "../../"
PROTO_PYTHON_EXTENSION = "_pb2.py"
PROTO_DEF_EXTENSION = ".bin"

logger = logging.getLogger('Extractor')

class Extractor(object):
        
    def __init__(self, source):
        self.source = source
        #load information
        self.informationDefinition = loadInformationDefinition(getInformationBlueprint())
        
    def getInformationBlueprint(self, informationBluePrintPath):
        #information blueprint path
        information_blueprint_path = os.path.abspath(os.path.join(informationBluePrintPath))
        logger.info("information blue print path: " + information_blueprint_path)
        #import information blueprint
        informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()
        return informationBlueprint
        
    def loadInformationDefinition(self, informationBluePrintPath):
        #load information
        information_path = os.path.abspath(os.path.join(self.source.sourceName + PROTO_DEF_EXTENSION))
        logger.info("information path: " + information_path)
        f = open(information_path, "rb")
        information = self.getInformationBlueprint()
        information.ParseFromString(f.read())
        f.close()
        return informationBluePrint

    def getImages(dataPercentage):
        return
        
    def getExtractedData(self, inputTransform, images):
        return

    
# ext = Extractor()
# ext.loadInformationDefinition(INFORMATION_BLUEPRINT)

class test(object):
    
    def __init__(self):
        return 
        
    def getPersonaBlueprint(self, personaBlueprintPath): 
        #persona blueprint path
        persona_blueprint_path = os.path.abspath(os.path.join(personaBlueprintPath))
        print (persona_blueprint_path)
        #persona blueprint
        personaBlueprint = imp.load_source('Persona', persona_blueprint_path).Persona() 
        return personaBlueprint
    
    def loadPersona(self, personaBlueprintPath, personaDefPath):
        # persona blueprint
        persona = self.getPersonaBlueprint(personaBlueprintPath)
        #load persona
        persona_path = os.path.abspath(os.path.join(personaDefPath))
        print (persona_path)
        f = open(personaDefPath, "rb")
        persona.ParseFromString(f.read())
        f.close()        
        return persona
    
    def testExtractedData(self, personaBlueprintPath, personaDefPath):
        persona = self.loadPersona(personaBlueprintPath, personaDefPath)
        
        return 
    
PERSONA_NAME_QUALIFIER = "PersonaDefinition"
TEST_PERSONA_BLUEPRINT = "../../../../Personas/personaBlueprint/version_1/personBlueprint" + PROTO_PYTHON_EXTENSION
TEST_PERSONA_NAME = "Khandhasamy" + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
TEST_PERSONA_DEF = "../../../../Personas/Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_1/" + TEST_PERSONA_NAME
    
tst = test()
tst.loadPersona(TEST_PERSONA_BLUEPRINT, TEST_PERSONA_DEF)

def testExtractor():
    #persona blueprint path
    information_blueprint_path = os.path.join("..", "..")
    information_blueprint_path = os.path.abspath(os.path.join(information_blueprint_path, INFORMATION_BLUEPRINT + PROTO_PYTHON_EXTENSION))
    #import information blueprint
    informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()

    #Testing
    persona = personaDefinition_pb2.Persona()
    dna = persona.DNAs.add()
    inputLayer = dna.inputs.add()
    inputLayer.inputTransform.transformerName = "imageTransform"
    inputLayer.inputTransform.informationType = "image"
    transformInputSize1 =  inputLayer.inputTransform.transformSize.add()
    transformInputSize1.dimension = 1
    transformInputSize1.dimensionSize = 50
    transformInputSize2 =  inputLayer.inputTransform.transformSize.add()
    transformInputSize2.dimension = 1
    transformInputSize2.dimensionSize = 50
    transformParam1 = inputLayer.inputTransform.transformParam.add()
    transformParam1.parameterName = "color"
    transformParam1.parameterValue  = "grey"
    # transformParam2 = inputLayer.inputTransform.transformParam.add()
    # transformParam2.parameterName = "process"
    # transformParam2.parameterValue  = "edge"


    # Read the existing address book.
    f = open("test.bin", "rb")
    information.ParseFromString(f.read())
    f.close()

    imageURLExtractor = ImageURLExtractor(information)
    x = imageURLExtractor.getTestData(inputLayer.inputTransform)

    for imgIndex in range(x.shape[0]):
        plt.imshow(x[imgIndex][0]*255, cmap = cm.Greys_r)
        plt.show()

    return

def testPopulatePersonaInformation():
    return

# testExtractor()

def getTrainingData(self, inputTransform):
    for trainingData in self.information.trainingDataList:
        response = requests.get(trainingData.URL)
        img = Image.open(BytesIO(response.content))

        #FIXME: move transformer to transform package
        img_rows = inputTransform.transformSize[0].dimensionSize
        img_cols = inputTransform.transformSize[1].dimensionSize
        img = img.resize((img_rows,img_cols), Image.ANTIALIAS)

        for parameter in inputTransform.transformParam:
            if parameter.parameterName == 'color':
                if parameter.parameterValue == 'grey':
                    print ("transform grey")
                    img = img.convert("L")         
            if parameter.parameterName == 'process':
                if parameter.parameterValue == 'edge':
                    print ("transform edge")
                    img = img.filter(ImageFilter.FIND_EDGES)

        img = np.asarray(img, dtype=np.float32)     
        data[image_index, 0, :, :] = img
        print (img.shape)
        print (trainingData.URL)

    return data

def getTestData(self, inputTransform):
    no_of_images = len(self.information.testDataList)
    data = np.random.random((no_of_images, self.dim, inputTransform.transformSize[0].dimensionSize, inputTransform.transformSize[1].dimensionSize))
    image_index = 0

    if self.information.extractor == type(self).__name__:
        for testData in self.information.testDataList:
            response = requests.get(testData.URL)
            img = Image.open(BytesIO(response.content))

            #FIXME: move transformer to transform package
            img_rows = inputTransform.transformSize[0].dimensionSize
            img_cols = inputTransform.transformSize[1].dimensionSize
            img = img.resize((img_rows,img_cols), Image.ANTIALIAS)

            for parameter in inputTransform.transformParam:
                if parameter.parameterName == 'color':
                    if parameter.parameterValue == 'grey':
                        img = img.convert("L")         
                if parameter.parameterName == 'process':
                    if parameter.parameterValue == 'edge':
                        img = img.filter(ImageFilter.FIND_EDGES)

            img = np.asarray(img, dtype=np.float32)     
            data[image_index, 0, :, :] = img
            print (img.shape)
            print (testData.URL)

    else:
        print ("Extractor in the information file and running extractor is not matching.")
    return data   


# In[ ]:



