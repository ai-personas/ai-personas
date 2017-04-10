
# coding: utf-8

# In[1]:

import sys
import imp
import os
import numpy as np
import zipfile
import requests
import StringIO
from PIL import Image


class Loader(object):

    def __init__(self, processor):
        self.processor = processor
    
    # get data 
    def getData(self):
        imgDataList = []
        downloadURL = self.processor.downloadZipImageFile.downloadURL
        directoryName = self.processor.downloadZipImageFile.directoryName
        
#         u = requests.get(downloadURL)
#         f = StringIO.StringIO() 
#         f.write(u.content)
            
        input_zip = zipfile.ZipFile(downloadURL)
        for fileName in input_zip.namelist():
            if (directoryName+"/") in fileName:
                try:
                    imgFile = input_zip.open(fileName)
                    img = Image.open(imgFile)
#                     img = np.asarray(img, dtype=np.float32)
                    imgDataList.append(img)
                except Exception as e: 
                    pass
        print ("Loaded images: " + str(len(imgDataList)))
        return imgDataList

#Test code
INFORMATION_BLUEPRINT = "informationBlueprint"
INFORMATION_NAME = "scientists"
INFORMATION_CATEGORY = ["Category", "Portraits"]

def getInformationBlueprint():
    #information blueprint path
    information_blueprint_path = os.path.join("..", "..")
    information_blueprint_path = os.path.abspath(os.path.join(information_blueprint_path, INFORMATION_BLUEPRINT + '_pb2.py'))
    print (information_blueprint_path)
    #import information blueprint
    informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()
    return informationBlueprint

def loadInformationDefinition(informationBluePrint):
    #load information
    information_path = os.path.join("..", "..")
    for category in INFORMATION_CATEGORY:
        information_path = os.path.join(information_path, category)
    information_path = os.path.abspath(os.path.join(information_path, INFORMATION_NAME + ".bin"))
    f = open(information_path, "rb")
    informationBluePrint.ParseFromString(f.read())
    f.close()
    return informationBluePrint

def test():
    
    information = loadInformationDefinition(getInformationBlueprint())
    LOADER_DOWNLOAD_ZIP_IMAGE_FILE = "downloadZipImageFile"

    for processor in information.processors:
        if LOADER_DOWNLOAD_ZIP_IMAGE_FILE == processor.WhichOneof("Loader"):
            loader = Loader(processor);
            loader.getData();
            
# test()


# In[ ]:




# In[ ]:



