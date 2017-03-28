
# coding: utf-8

# In[16]:

import sys
import imp
import os

class Loader(object):

    def __init__(self, processor):
        self.processor = processor
        
    # get data 
    def getData(self):
        loaderName = self.processor.WhichOneof("Loader")
        loader_path = os.path.abspath(os.path.join(loaderName + '.py'))
        loader = imp.load_source('Loader', loader_path).Loader(self.processor)
        return loader.getData()          
    
#Testing
INFORMATION_BLUEPRINT = "informationBlueprint"
INFORMATION_NAME = "scientists"
INFORMATION_CATEGORY = ["Category", "Portraits"]

def getInformationBlueprint():
    #information blueprint path
    information_blueprint_path = os.path.join("..", "..")
    information_blueprint_path = os.path.abspath(os.path.join(information_blueprint_path, INFORMATION_BLUEPRINT + '_pb2.py'))
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

    for processor in information.processors:
        print ("Loader name: " + processor.WhichOneof("Loader"))
        loader = Loader(processor);
        loader.getData();

# test()


# In[ ]:



