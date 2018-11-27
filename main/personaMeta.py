import json
import time

import persona_pb2
from kerasPhysical import KerasSoftPhysical
from storage import Storage


class PersonaMeta:

    def __init__(self):
        self.personas_local_path = 'personas/personas.json'
        self.persona_loca_folder = 'model/'
        self.storage = Storage()
        self.personas_network_file = ''

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
        res = self.storage.add_ipfs_file(self.personas_local_path)
        self.storage.update_file(res['Hash'])

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

    def get_local_persona_proto_location(self, persona):
        return self.persona_loca_folder + persona.name + ".proto"

    def get_brain_storage_location(self, persona):
        return self.persona_loca_folder + persona.name + ".h5"

    def create_persona(self, name, dna, env):
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
            return self.store_brain_and_persona(brain, persona)

    def store_local_persona_proto(self, persona):
        f = open(self.get_local_persona_proto_location(persona), "wb")
        f.write(persona.SerializeToString())
        f.close()

    def get_persona_proto(self, name):
        f = open(name, "rb")
        persona = persona_pb2.Persona()
        persona.ParseFromString(f.read())
        f.close()
        return persona

    def retrieve_persona(self, persona_name, age):
        personas_obj = self.get_personas_obj()
        persona_meta = self.get_persona_meta(personas_obj, persona_name)
        persona_age = self.get_persona_age(persona_meta, age)
        if persona_age:
            self.storage.load_ipfs_file(persona_age['hash'])
            return self.get_persona_proto(persona_age['hash'])

    def store_brain_and_persona(self, brain, persona):
        brain.save_weights(self.get_brain_storage_location(persona))
        res = self.storage.add_ipfs_file(self.get_brain_storage_location(persona))
        persona.brain.modelUrl = res['Hash']
        self.store_local_persona_proto(persona)
        res = self.storage.add_ipfs_file(self.get_local_persona_proto_location(persona))
        return res['Hash']

