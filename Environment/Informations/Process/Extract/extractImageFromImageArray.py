
# coding: utf-8

# In[5]:

import sys
import imp
import os
import requests
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np

PERSONA_BLUEPRINT = "../../../../Personas/personaBlueprint/version_1/personBlueprint"
INFORMATION_BLUEPRINT = "../../informationBlueprint"
INFORMATION_BASE = "../../"
PROTO_PYTHON_EXTENSION = "_pb2.py"

class Extractor(object):
        
    def __init__(self, personaInformation):
        self.personaInformation = personaInformation
        #load information
        loadInformationDefinition(getInformationBlueprint())
        
    def getInformationBlueprint(self):
        #information blueprint path
        information_blueprint_path = os.path.abspath(os.path.join(PERSONA_BLUEPRINT + PROTO_PYTHON_EXTENSION))
        #import information blueprint
        informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()
        return informationBlueprint
        
    def loadInformationDefinition(self, informationBluePrint):
        #load information
        information_path = os.path.abspath(os.path.join(INFORMATION_BASE, self.personaInformation.informationSource + ".bin"))
        f = open(information_path, "rb")
        informationBluePrint.ParseFromString(f.read())
        f.close()
        return informationBluePrint

    def getImages(dataPercentage):
        return
        
    def getExtractedData(self, inputTransform, images):
        return
    
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
    
    def getValidationData():
        return
    
    def getActionData():
        return

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

testExtractor()


# In[ ]:



