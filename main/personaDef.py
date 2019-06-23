import json
import time

# import persona_pb2
from collections import namedtuple

from physical.kerasPhysical import KerasSoftPhysical
from storage.decentralizedStorage import Storage
from storage.privateStorage import PrivateStorage


class PersonaMeta:

    def __init__(self):
        self.personas_local_path = 'personas/personas.json'
        self.persona_local_folder = 'tmp/'
        self.storage = Storage()
        self.isPublic = False
        self.personas_network_file = ''
        with open('personas/persona.json') as f:
            persona_json = json.load(f)
            self.persona_def = json.loads(persona_json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def get_dna_def(self, dna_name):
        # todo: get it from private/public storage
        with open('dna/'+dna_name+'.json') as f:
            dna_json = json.load(f)
            return json.loads(dna_json, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def get_new_age_model(self, hash, age):
        newAge = {}
        newAge['hash'] = hash
        newAge['age'] = age
        newAge['timestamp'] = time.time()
        return newAge

    def get_new_persona_meta(self, persona_name):
        new_persona_meta = {}
        new_persona_meta['persona_name'] = persona_name
        new_persona_meta['tags'] = []
        new_persona_meta['ages'] = []
        return new_persona_meta

    def get_persona_meta(self, personas_obj, persona_name):
        personas = personas_obj['personas']
        for p in range(len(personas)):
            persona_meta = personas[p]
            if persona_meta['persona_name'] == persona_name:
                return persona_meta
        return self.get_new_persona_meta(persona_name)

    def get_current_age(self, persona_meta):
        max_age = 0
        for a in range(len(persona_meta['ages'])):
            age_hash = persona_meta['ages'][a]
            if int(age_hash['age']) > max_age:
                max_age = max_age + 1
        return max_age

    def is_persona_age_exist(self, persona_meta, age):
        for a in range(len(persona_meta['ages'])):
            age_hash = persona_meta['ages'][a]
            if age_hash['age'] == age:
                return True
        return False

    def get_persona_age(self, persona_meta, age):
        for a in range(len(persona_meta['ages'])):
            age_hash = persona_meta['ages'][a]
            if age_hash['age'] == age:
                return age_hash['age']

    def get_personas_obj(self):
        personas_str = json.dumps(json.load(open(self.personas_local_path)))
        return json.loads(personas_str)

    def add_age(self, persona_name, hash, age):
        personas_obj = self.get_personas_obj()
        persona_meta = self.get_persona_meta(personas_obj, persona_name)
        current_age = self.get_current_age(persona_meta)
        if age == (current_age + 1):
            new_age_entry = self.get_new_age_model(hash, str(age))
            persona_meta['ages'].append(new_age_entry)
            with open(self.personas_local_path, 'w') as outfile:
                json.dump(personas_obj, outfile)
        else:
            print(json.dump(personas_obj))
        # res = self.storage.add_ipfs_file(self.personas_local_path)
        # self.storage.update_file(res['Hash'])

    def add_new_age(self, persona_name):
        personas_obj = self.get_personas_obj()
        persona_meta = self.get_persona_meta(personas_obj, persona_name)
        current_age = self.get_current_age(persona_meta)
        new_age = current_age + 1

        # personas_str = json.dumps(json.load(open(self.personas_local_path)))
        # personas_obj = json.loads(personas_str)
        # persona_meta = self.get_persona_meta(personas_obj, persona_name)
        # current_age = self.get_current_age(persona_meta)
        # new_age = current_age + 1
        # if not self.is_persona_age_exist(persona_meta, new_age):
        #     new_age_entry = self.get_new_age_model('123', str(new_age))
        #     persona_meta['ages'].append(new_age_entry)
        # with open(self.personas_local_path, 'w') as outfile:
        #     json.dump(personas_obj, outfile)
        # res = self.storage.add_ipfs_file(self.personas_local_path)
        # self.storage.update_file(res['hash'])

    def update_age(self, persona_name, age, hash):
        personas_obj = self.get_personas_obj()
        persona_meta = self.get_persona_meta(personas_obj, persona_name)
        current_age = self.get_current_age(persona_meta)
        if current_age == age:
            age_hash = self.get_persona_age(persona_meta, age)
            age_hash['hash'] = hash
            with open(self.personas_local_path, 'w') as outfile:
                json.dump(personas_obj, outfile)
            res = self.storage.add_ipfs_file(self.personas_local_path)
            self.storage.update_file(res['hash'])

    def create_age_0(self, name, dna, env):
        hash = self.create_persona(name, dna, env)
        self.add_age(name, hash, 0)

    def get_local_persona_def_location(self, persona):
        return self.persona_local_folder + persona.name + ".json"

    def get_brain_storage_location(self, persona):
        return self.persona_local_folder + persona.name + ".h5"

    def create_persona(self, name, dna_name, env):
        persona = self.persona_def
        persona.name = name
        persona.age[0].dna = self.get_dna_def(dna_name)
        persona.type = "keras"
        persona.age[0].old = 0
        persona.age[0].knowledge_cycle = 0
        persona.age[0].environments[0] = json.dumps(json.load(open("environments/school/" + env + ".json")))
        if persona.type == 'keras':
            keras = KerasSoftPhysical(persona)
            brain = keras.create_persona()
            return self.store_brain_and_persona(brain, persona)

    def store_persona_def(self, persona):
        f = open(self.get_local_persona_def_location(persona), "wb")
        f.write(json.dumps(persona.__dict__))
        f.close()

    def get_persona_proto(self, name):
        # todo: load it from persona multiverse
        f = open(name, "rb")
        # persona = persona_pb2.Persona()
        # persona.ParseFromString(f.read())
        # f.close()
        # return persona

    def retrieve_persona(self, persona_name, age):
        personas_obj = self.get_personas_obj()
        persona_meta = self.get_persona_meta(personas_obj, persona_name)
        persona_age = self.get_persona_age(persona_meta, age)
        if persona_age:
            self.storage.load_ipfs_file(persona_age['hash'])
            return self.get_persona_proto(persona_age['hash'])

    def store_brain_and_persona(self, brain, persona):
        if self.isPublic:
            brain.save_weights(self.get_brain_storage_location(persona))
            res = self.storage.add_ipfs_file(self.get_brain_storage_location(persona))
            persona.brain.modelUrl = res['Hash']
            self.store_persona_def(persona)
            res = self.storage.add_ipfs_file(self.get_local_persona_def_location(persona))
            return res['Hash']
        else:
            # todo: store it in url and update it in modelUrl
            brain_file = self.get_brain_storage_location(persona)
            private_storage = PrivateStorage()
            brain.save_weights(brain_file)
            private_storage.save_brain(persona.name, persona.age.old, brain_file)
