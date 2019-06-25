import json
from importlib import import_module

class Persona:

    def __init__(self, personaName):
        # todo: load it from ip address
        personas_local_path = 'personas/'+personaName+'.json'
        with open(personas_local_path) as f:
            persona_def = json.load(f)['persona']
        age = persona_def['age'][0]
        brain_loc = age['brain']['location']
        print(brain_loc)

    def energize_persona(self, personaName):
        age = persona_def['age'][0]
        dna = age['dna']['code']
        print(age)
        if age['brain']['location'] == '':
            mod = import_module('dna.' + dna)
            get_dna = getattr(mod, 'get_dna')




