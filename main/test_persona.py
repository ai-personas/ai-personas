import ipfsapi
import json
from collections import namedtuple

import persona_pb2
from kerasPhysical import KerasSoftPhysical
# from school import School

LOCAL_PERSONA_FOLDER = "model/"
PERSONAS_PATH = "personas/personas.json"

def test_persona():
    # persona =  createPersona('test', 'kandhasamy', 'Ramesh_school')
    # persona_def = get_persona('test')
    # persona =  createPersona('test3', 'mnist_cnn_dna', 'Ramesh_school')
    # persona_def = get_persona('test3')

    persona_name = 'test4'
    persona_age = '0'
    persona =  createPersona(persona_name, 'mnist_siamese', 'Ramesh_school')
    add_new_age(persona_name)

    # persona_def = get_persona(persona_name)
    # env = json.loads(persona_def.age.environments, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    # if env.school:
    #     School().schedule(persona_def)

def get_persona_proto(name):
    f = open(LOCAL_PERSONA_FOLDER + name + ".proto", "rb")
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
        brain.save_weights(get_brain_storage_location(persona))
        persona.brain.modelUrl = get_brain_storage_location(persona)
        store_persona_proto(persona)


def store_persona_proto(persona):
    f = open(LOCAL_PERSONA_FOLDER + persona.name + ".proto", "wb")
    f.write(persona.SerializeToString())
    f.close()


def get_brain_storage_location(persona):
    return LOCAL_PERSONA_FOLDER + persona.name + ".h5"


def get_persona_meta(personas, persona_name):
    for p in range(len(personas)):
        persona_meta = personas[p]
        if persona_meta['name'] == persona_name:
            return persona_meta


def add_persona(persona_meta, ipfs_hash, age):
    if not is_persona_age_exist(persona_meta, age):
        newAge = {}
        newAge['hash'] = ipfs_hash
        newAge['age'] = age
        persona_meta['ipfs'].append(newAge)
    return persona_meta


def is_persona_age_exist(persona_meta, age):
    for a in range(len(persona_meta['ipfs'])):
        age_hash = persona_meta['ipfs'][a]
        if age_hash['age'] == age:
            return True
    return False


def get_age_increment(persona_meta):
    max_age = 0
    for a in range(len(persona_meta['ipfs'])):
        age_hash = persona_meta['ipfs'][a]
        if int(age_hash['age']) > max_age:
            max_age = max_age + 1
    return max_age + 1


def add_new_age(persona_name):
    personas_str = json.dumps(json.load(open(PERSONAS_PATH)))
    personas_obj = json.loads(personas_str)
    personas = personas_obj['personas']
    ipfs_client = ipfsapi.Client('127.0.0.1', 5001)
    ipfs_res = ipfs_client.add(LOCAL_PERSONA_FOLDER + persona_name + ".proto")
    persona_meta = get_persona_meta(personas, persona_name)
    new_age = get_age_increment(persona_meta)
    add_persona(persona_meta, ipfs_res['Hash'], str(new_age))
    with open(PERSONAS_PATH, 'w') as outfile:
        json.dump(personas_obj, outfile)
    print(ipfs_res)
    print(ipfs_client.swarm_peers())
    # ipfs_publish_res = ipfs_client.name_publish(ipfs_res['Hash'])
    # print(ipfs_publish_res)
    # ipfs_client.get()
    # print(ipfs_client.dht_put(ipfs_res['Hash'], 'aiPersonas'))

