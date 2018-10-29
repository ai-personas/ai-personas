import json
from collections import namedtuple

import persona_pb2
from kerasPhysical import KerasSoftPhysical
from school import School


def test_persona():
    persona =  createPersona('test', 'kandhasamy', 'Ramesh_school')
    persona_def = get_persona('test')
    # persona =  createPersona('test3', 'mnist_cnn_dna', 'Ramesh_school')
    # persona_def = get_persona('test3')
    # persona =  createPersona('test4', 'mnist_siamese', 'Ramesh_school')
    # persona_def = get_persona('test4')
    env = json.loads(persona_def.age.environments, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    if env.school:
        School().schedule(persona_def)

def get_persona(name):
    f = open("model/" + name + ".proto", "rb")
    persona = persona_pb2.Persona()
    persona.ParseFromString(f.read())
    f.close()
    return persona


def createPersona(name, dna, env):
    persona = persona_pb2.Persona()
    persona.name = name
    persona.dna = json.dumps(json.load(open("dna/" + dna + ".json")))
    persona.softPhysical = "keras"
    persona.age.old = 0
    persona.age.knowledgeCycle = 0
    persona.age.environments = json.dumps(json.load(open("society/school/" + env + ".json")))
    if persona.softPhysical == 'keras':
        keras = KerasSoftPhysical(persona)
        brain = keras.create_persona()
        brain.save(get_brain_storage_location(persona))
        persona.brain.modelUrl = get_brain_storage_location(persona)
        store_persona_proto(persona)

def store_persona_proto(persona):
    f = open("model/" + persona.name + ".proto", "wb")
    f.write(persona.SerializeToString())
    f.close()

def get_brain_storage_location(persona):
    return "model/" + persona.name + ".h5"

