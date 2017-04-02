
# coding: utf-8

# In[5]:

import os, sys, inspect
import copy
import imp

PROTO_DEF_EXTENSION = ".bin"
PROTO_PYTHON_EXTENSION = "_pb2.py"
DNA_BLUEPRINT = "../../DNA/dnaBlueprint/version_1/dnaBlueprint" +  PROTO_PYTHON_EXTENSION
DNA_NAME_QUALIFIER = "DnaDefinition"
DNA_NAME = "Khandhasamy" + DNA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
DNA_DEF_PATH = "../dnaFamily/Khandhasamy/Evolution_1/" + DNA_NAME

class DnaDefinitionGeneration(object):
    
    input_layer_index = 1
    
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

    def generateDnaDefinition(self, dnaBlueprint, dnaDefPath):
        dnaBlueprint = self.getDnaBlueprint(dnaBlueprint)
        self.saveDnaDefinition(dnaDefPath, dnaBlueprint)
        return
    
    def generateInputLayer(dna):
        inputLayer = dna.inputs.add()
        inputLayer.layerName = "input" + input_layer_index
        
    
dnaDef = DnaDefinitionGeneration()
dnaDef.generateDnaDefinition(DNA_BLUEPRINT, DNA_DEF_PATH)

# This function fills in a Person message based on user input.
def generateDNA():
    dna = dnaDefinition_pb2.DNA()
    dna.DNA = "Khandasamy"
    
    ################ input layer #############################
    inputLayer = dna.inputs.add()
    inputLayer.layerName = "imageInput"

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
    transformParam2 = inputLayer.inputTransform.transformParam.add()
    transformParam2.parameterName = "process"
    transformParam2.parameterValue  = "edge"
    
    connection1 = inputLayer.connections.add()
    connection1.destinationLayerName = "layer1"
    
    ################ convolution layer #############################
    layer1 = dna.layers.add()
    layer1.layerName = "layer1"
    layer1Size1 = layer1.layerSize.add()
    layer1Size1.dimension = 1
    layer1Size1.dimensionSize = 50
    layer1Size2 = layer1.layerSize.add()
    layer1Size2.dimension = 2
    layer1Size2.dimensionSize = 50
    layer1Connection1 = layer1.connections.add()
    layer1Connection1.sourceLayerName = "imageInput"
    layer1Connection1.destinationLayerName = "layer2"
    layer1.layerConvolution.convolutionDimension = 2
    layer1.layerConvolution.filters = 100
    layer1.layerConvolution.borderMode = "same"
    layer1.layerConvolution.kernelSize.append(3)
    layer1.layerConvolution.kernelSize.append(3)
    layer1.layerConvolution.inputShape.append(1)
    layer1.layerConvolution.inputShape.append(50)
    layer1.layerConvolution.inputShape.append(50)
    
    ################ activation layer #############################
    layer2 = dna.layers.add()
    layer2.layerName = "layer2"
    layer2Connection1 = layer2.connections.add()
    layer2Connection1.sourceLayerName = "layer1"
    layer2Connection1.destinationLayerName = "layer3"
    layer2.layerActivation.activationType = "relu"

    ################ dropout layer #############################
    layer3 = dna.layers.add()
    layer3.layerName = "layer3"
    layer3Connection1 = layer3.connections.add()
    layer3Connection1.sourceLayerName = "layer2"
    layer3Connection1.destinationLayerName = "layer4"
    layer3.layerDropout.dropPercentage = 0.3
    
    ################ convolution layer #############################
    layer4 = dna.layers.add()
    layer4.layerName = "layer4"
    layer4Size1 = layer4.layerSize.add()
    layer4Size1.dimension = 1
    layer4Size1.dimensionSize = 50
    layer4Size2 = layer4.layerSize.add()
    layer4Size2.dimension = 2
    layer4Size2.dimensionSize = 50
    layer4Connection1 = layer4.connections.add()
    layer4Connection1.sourceLayerName = "layer3"
    layer4Connection1.destinationLayerName = "layer5"
    layer4.layerConvolution.convolutionDimension = 2
    layer4.layerConvolution.filters = 100
    layer4.layerConvolution.borderMode = "same"
    layer4.layerConvolution.kernelSize.append(3)
    layer4.layerConvolution.kernelSize.append(3)
    layer4.layerConvolution.inputShape.append(1)
    layer4.layerConvolution.inputShape.append(50)
    layer4.layerConvolution.inputShape.append(50)    
    
    ################ activation layer #############################
    layer5 = dna.layers.add()
    layer5.layerName = "layer5"
    layer5Connection1 = layer5.connections.add()
    layer5Connection1.sourceLayerName = "layer4"
    layer5Connection1.destinationLayerName = "layer6"
    layer5.layerActivation.activationType = "relu"

    ################ dropout layer #############################
    layer6 = dna.layers.add()
    layer6.layerName = "layer6"
    layer6Connection1 = layer3.connections.add()
    layer6Connection1.sourceLayerName = "layer5"
    layer6Connection1.destinationLayerName = "layer7"
    layer6.layerDropout.dropPercentage = 0.3
    
    ################ convolution layer #############################
    layer7 = dna.layers.add()
    layer7.layerName = "layer7"
    layer7Size1 = layer7.layerSize.add()
    layer7Size1.dimension = 1
    layer7Size1.dimensionSize = 50
    layer7Size2 = layer7.layerSize.add()
    layer7Size2.dimension = 2
    layer7Size2.dimensionSize = 50
    layer7Connection1 = layer7.connections.add()
    layer7Connection1.sourceLayerName = "layer6"
    layer7Connection1.destinationLayerName = "layer8"
    layer7.layerConvolution.convolutionDimension = 2
    layer7.layerConvolution.filters = 1
    layer7.layerConvolution.borderMode = "same"
    layer7.layerConvolution.kernelSize.append(3)
    layer7.layerConvolution.kernelSize.append(3)
    layer7.layerConvolution.inputShape.append(1)
    layer7.layerConvolution.inputShape.append(50)
    layer7.layerConvolution.inputShape.append(50)    
    
    ################ activation layer #############################
    layer8 = dna.layers.add()
    layer8.layerName = "layer8"
    layer8Connection1 = layer8.connections.add()
    layer8Connection1.sourceLayerName = "layer7"
    layer8Connection1.destinationLayerName = "output"
    layer8.layerActivation.activationType = "relu"
    
    ################ output layer #############################
    outputLayer = dna.outputs.add()
    outputLayer.layerName = "imageOutput"

    outputLayer.inputTransform.transformerName = "imageTransform"
    outputLayer.inputTransform.informationType = "image"
    transformInputSize1 =  outputLayer.inputTransform.transformSize.add()
    transformInputSize1.dimension = 1
    transformInputSize1.dimensionSize = 50
    transformInputSize2 =  outputLayer.inputTransform.transformSize.add()
    transformInputSize2.dimension = 1
    transformInputSize2.dimensionSize = 50
    transformParam1 = outputLayer.inputTransform.transformParam.add()
    transformParam1.parameterName = "color"
    transformParam1.parameterValue  = "grey"
        
    return dna
    
# # Write the new address book back to disk.
# f = open("Family\Khandhasamy\Evolution 1\Khandhasamy.bin", "wb")
# f.write(generateDNA().SerializeToString())
# f.close()


# In[ ]:



