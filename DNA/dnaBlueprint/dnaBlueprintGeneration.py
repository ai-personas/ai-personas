
# coding: utf-8

# In[1]:

import os, sys, inspect
import copy
import imp

PROTO_DEF_EXTENSION = ".bin"
PROTO_PYTHON_EXTENSION = "_pb2.py"
DNA_BLUEPRINT_PATH = "../../DNA/dnaBlueprint/version_1/dnaBlueprint" +  PROTO_PYTHON_EXTENSION
DNA_NAME_QUALIFIER = "DnaDefinition"
DNA_NAME = "Khandhasamy" + DNA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
DNA_DEF_PATH = "../dnaFamily/Khandhasamy/Evolution_1/" + DNA_NAME

class DnaDefinitionGeneration(object):
    
    layer_index = 1
    layer_size = 50
    layer_convolution_filter = 100
    layer_border_mode = "same"
    
    def getDnaBlueprint(self, dnaBlueprintPath):
        #DNA blueprint path
        dna_blueprint_path = os.path.abspath(os.path.join(dnaBlueprintPath))
        print (dna_blueprint_path)
        #dna blueprint
        dnaBlueprint = imp.load_source('DNA', dna_blueprint_path).DNA() 
        return dnaBlueprint
    
    def saveDnaDefinition(self, dnaDefPath, dna):
        dna_def_path = os.path.abspath(os.path.join(dnaDefPath))
        # read dna definition
        f = open(dna_def_path, "wb")
        f.write(dna.SerializeToString())
        f.close()

    def getLayerName(self, layerIndex):
        if layerIndex is None:
            return ''
        else:
            return 'layer' + str(layerIndex)
            
    def generateDnaDefinition(self, dnaBlueprintPath, dnaDefPath):
        dna = self.getDnaBlueprint(dnaBlueprintPath)
        self.generateConvoution2DLayer(dna, None , 2)
        self.generateActivationLayer(dna, 1, 3)
        self.generateDropoutLayer(dna, 2, 4)
        self.generateConvoution2DLayer(dna, 3, 5)
        self.generateActivationLayer(dna, 4, 6)
        self.generateDropoutLayer(dna, 5, 7)     
        self.generateConvoution2DLayer(dna, 6, 8)
        self.generateConvoution2DLayer(dna, 7, None)
        self.saveDnaDefinition(dnaDefPath, dna)
        return
    
    def generateConvoution2DLayer(self, dna, sourceLayer, destLayer):
        layer = dna.layers.add()
        layer.layerName = "layer" + str(self.layer_index)
        layerSize1 = layer.layerSize.add()
        layerSize1.dimension = 1
        layerSize1.dimensionSize = 50
        layerSize2 = layer.layerSize.add()
        layerSize2.dimension = 2
        layerSize2.dimensionSize = 50
        layerConnection1 = layer.connections.add()
        layerConnection1.sourceLayerName = self.getLayerName(sourceLayer)
        layerConnection1.destinationLayerName = self.getLayerName(destLayer)
        layer.layerConvolution.convolutionDimension = 2
        layer.layerConvolution.filters = 100
        layer.layerConvolution.borderMode = "same"
        layer.layerConvolution.kernelSize.append(3)
        layer.layerConvolution.kernelSize.append(3)
        layer.layerConvolution.inputShape.append(1)
        layer.layerConvolution.inputShape.append(50)
        layer.layerConvolution.inputShape.append(50)
        
    def generateActivationLayer(self, dna, sourceLayer, destLayer):
        layer = dna.layers.add()
        layer.layerName = "layer" + str(self.layer_index)
        layerConnection1 = layer.connections.add()
        layerConnection1.sourceLayerName = self.getLayerName(sourceLayer)
        layerConnection1.destinationLayerName = self.getLayerName(destLayer)
        layer.layerActivation.activationType = "relu"
    
    def generateDropoutLayer(self, dna, sourceLayer, destLayer):
        layer = dna.layers.add()
        layer.layerName = "layer" + str(self.layer_index)
        layerConnection1 = layer.connections.add()
        layerConnection1.sourceLayerName = self.getLayerName(sourceLayer)
        layerConnection1.destinationLayerName = self.getLayerName(destLayer)
        layer.layerDropout.dropPercentage = 0.3
        
dnaDef = DnaDefinitionGeneration()
dnaDef.generateDnaDefinition(DNA_BLUEPRINT_PATH, DNA_DEF_PATH)


# In[ ]:



