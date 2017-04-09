
# coding: utf-8

# In[2]:

import os, sys, inspect
import copy
import imp

INSTALLATION_PATH = "C:\Users\rames\Documents\GitHub\ai-personas"

PROTO_DEF_EXTENSION = ".bin"
PROTO_PYTHON_EXTENSION = "_pb2.py"
PERSONA_BLUEPRINT = "version_1/personBlueprint" + PROTO_PYTHON_EXTENSION
PERSONA_NAME = "Khandhasamy"
PERSONA_NAME_QUALIFIER = "PersonaDefinition"
PERSONA_AGE = 1
PERSONA_DEF_PATH="../Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_" + str(PERSONA_AGE) + "/" + PERSONA_NAME + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
DNA_BLUEPRINT = "../../DNA/dnaBlueprint/version_1/dnaBlueprint" +  PROTO_PYTHON_EXTENSION
DNA_NAME_QUALIFIER = "DnaDefinition"
DNA_NAME = "Khandhasamy" + DNA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
DNA_DEF_PATH = "../../DNA/dnaFamily/Khandhasamy/Evolution_1/" + DNA_NAME
SOURCE_PATH = "Environment\Informations\Category\Portraits\scientists.bin"

class PersonaDefinitionGeneration(object):
    
    def getDnaBlueprint(self, dnaBlueprintPath):
        #DNA blueprint path
        dna_blueprint_path = os.path.abspath(os.path.join(dnaBlueprintPath))
        print (dna_blueprint_path)
        #dna blueprint
        dnaBlueprint = imp.load_source('DNA', dna_blueprint_path).DNA() 
        return dnaBlueprint
    
    def getDnaDefinition(self, dna, dnaDefPath):
        # read dna definition
        f = open(dnaDefPath, "rb")
        dna.ParseFromString(f.read())
        f.close()
        return dna 

    def getPersonaBlueprint(self, dnaBlueprintPath, dnaDefPath, personaBlueprintPath): 
        #persona blueprint path
        persona_blueprint_path = os.path.abspath(os.path.join(personaBlueprintPath))        
        #persona blueprint
        personaBlueprint = imp.load_source('Persona', persona_blueprint_path).Persona() 
        return personaBlueprint

    def savePersonaDefinition(self, personaDefPath, persona):
        print (personaDefPath)
        # write persona definition
        f = open(personaDefPath, "wb")
        f.write(persona.SerializeToString())
        f.close()
        
    def generatePersonaDefinition(self, dnaBlueprintPath, dnaDefPath, personaBlueprintPath, personaDefPath):
        persona = self.getPersonaBlueprint(dnaBlueprintPath, dnaDefPath, personaBlueprintPath)
        dna = persona.DNAs.add()
        # load dna definition
        dna = self.getDnaDefinition(dna, dnaDefPath)
        # generate physical 
        self.generatePhysical(persona)
        #generate age
        self.generateAge(persona)
        # save persona
        self.savePersonaDefinition(personaDefPath, persona)
        return
    
    def generatePhysical(self, persona):
        persona.physical = "keras"
        return persona
    
    def generateAge(self, persona):
        persona.age.old = 1
        persona.age.learningCycle = 50
        persona.age.learningBatchSize = 3
        self.generateEnvironment(persona)
        return persona
    
    def generateEnvironment(self, persona):
        environment = persona.age.environments.add()
        environment.society = ""
        self.generateLibrary(environment)
        return environment
    
    def generateLibrary(self, environment):
        source = environment.library.sources.add()
        source.sourceName = SOURCE_PATH
        self.generateSourceConnectionLayer(source)
        return environment.library
    
    def generateSourceConnectionLayer(self, source):
        sourceConnectionLayer = source.sourceConnectionLayers.add()
        sourceConnectionLayer.connectedLayerName = "Layer1"
        sourceConnectionLayer.imageSource.imageWidth = 50
        sourceConnectionLayer.imageSource.imageHeight = 50
        sourceConnectionLayer.imageSource.imageProcess.append("grey")
        sourceConnectionLayer.imageSource.imageProcess.append("edge")
        return sourceConnectionLayer
        
    
personaDefinitionGeneration = PersonaDefinitionGeneration()
personaDefinitionGeneration.generatePersonaDefinition(DNA_BLUEPRINT, DNA_DEF_PATH,  PERSONA_BLUEPRINT, PERSONA_DEF_PATH)


# In[ ]:



