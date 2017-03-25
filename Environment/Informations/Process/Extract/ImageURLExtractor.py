
# coding: utf-8

# In[1]:

import requests
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np

class ImageURLExtractor(object):
    
    #default image size and dimension
    img_rows, img_cols, dim = 100, 100, 1
    
    def __init__(self, information):
        self.information = information
    
    def getTrainingData(self, inputTransform):
        no_of_images = len(self.information.trainingDataList)
        data = np.random.random((no_of_images, self.dim, inputTransform.transformSize[0].dimensionSize, inputTransform.transformSize[1].dimensionSize))
        image_index = 0
        
        if self.information.extractor == type(self).__name__:
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
                
        else:
            print ("Extractor in the information file and running extractor is not matching.")
        return data
    
    def getTestData(self, inputTransform):
        no_of_images = len(self.information.trainingDataList)
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
    
