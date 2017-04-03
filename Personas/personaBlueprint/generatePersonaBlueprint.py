
# coding: utf-8

# In[7]:

import os, sys, inspect
import copy
import imp

PROTO_DEF_EXTENSION = ".bin"
PROTO_PYTHON_EXTENSION = "_pb2.py"
PERSONA_BLUEPRINT = "version_1/personBlueprint" + PROTO_PYTHON_EXTENSION
PERSONA_NAME_QUALIFIER = "PersonaDefinition"
PERSONA_AGE = 1
PERSONA_DEF_PATH="../Artist/Portraits/sketchToGreyImage/Khandhasamy/Evolution_1/age_" + str(PERSONA_AGE) + "/" + PERSONA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
DNA_BLUEPRINT = "../../DNA/dnaBlueprint/version_1/dnaBlueprint" +  PROTO_PYTHON_EXTENSION
DNA_NAME_QUALIFIER = "DnaDefinition"
DNA_NAME = "Khandhasamy" + DNA_NAME_QUALIFIER + PROTO_DEF_EXTENSION
DNA_DEF_PATH = "../DNA/dnaFamily/Khandhasamy/Evolution_1/" + DNA_NAME

def loadDNA(dnaName, evolution, dnaInstance):
    dna_path = os.path.abspath(os.path.join('..', 'DNA', 'Family', dnaName, 'Evolution ' + str(evolution)))

    # use this if you want to include modules from a subfolder
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],dna_path)))
    if cmd_subfolder not in sys.path:
        print (cmd_subfolder)
    sys.path.insert(0, cmd_subfolder)

    f = open(dna_path + "\\" + dnaName + ".bin", "rb")
    #dnaInstance = DynamicImporter(dnaName+"_pb2", "DNA")
    dnaInstance.ParseFromString(f.read())
    f.close()

    return dnaInstance

class PersonaDefinitionGeneration(object):
    
    def getDnaBlueprint(self):
        #DNA blueprint path
        dna_blueprint_path = os.path.abspath(os.path.join(DNA_BLUEPRINT))
        print (dna_blueprint_path)
        #dna blueprint
        dnaBlueprint = imp.load_source('DNA', dna_blueprint_path).DNA() 
        return dnaBlueprint
    
    def getDnaDefinition(self, dnaDefPath):
        # read dna definition
        dna = getDnaBlueprint()
        f = open(dnaDefPath, "rb")
        dna.ParseFromString(f.read())
        f.close()

    def getPersonaBlueprint(self, personaBlueprintPath): 
        #persona blueprint path
        persona_blueprint_path = os.path.abspath(os.path.join(personaBlueprintPath))
        print (persona_blueprint_path)
        #persona blueprint
        personaBlueprint = imp.load_source('Persona', persona_blueprint_path).Persona() 
        return personaBlueprint

    def savePersonaDefinition(self, personaDefPath):
        # write persona definition
        f = open(personaDefPath, "wb")
        f.write(generatePersonaDefinition().SerializeToString())
        f.close()
        
personaDefinitionGeneration = PersonaDefinitionGeneration()
personaDefinitionGeneration.getPersonaBlueprint(PERSONA_BLUEPRINT)

#generate persona definitions 
def generatePersonaDefinition():
    persona = personaDefinition_pb2.Persona()
    persona.physical = "keras"
    
    persona.age.old = 1
    persona.age.learningCycle = 50
    persona.age.learningBatchSize = 3
    
    ################ environments #############################
    environment = persona.age.environments.add()

    ################ environments #############################
    information = environment.informations.add()
    information.informationSource = "Informations\Category\Portraits\scientists"
    information.connectedLayerName.append("imageInput")
    information.connectedLayerName.append("imageOutput")
    
    ################# get DNA from file######################
    dna = persona.DNAs.add()
    dna = loadDNA("Khandhasamy", 1, dna)
    
    return persona
    
# Write persona to file
# f = open(PERSONA_DEF_PATH, "wb")
# f.write(generatePersonaDefinition().SerializeToString())
# f.close()



# In[ ]:



