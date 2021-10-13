import json
from importlib import import_module
import requests

from bson import ObjectId
from pymongo import MongoClient


class Persona:

    def __init__(self, persona_name):
        self.mongodb_port = 27017
        client = MongoClient(port=self.mongodb_port)
        self.db = client.aiPersonas
        self.persona_collection = 'personas'
        self.spec_id = 1
        self.persona_name = persona_name
        self.base_url = 'http://localhost:8090/personas/' + str(self.spec_id)
        self.persona_details = self.get_persona(persona_name)

    def get_persona_details(self):
        return self.persona_details

    '''
     create persona with given hash number. The hash number is the arbitrary hash used to differentiate persona_specs. 
     It allows any specs to be coded and this number can be used by the ai-personas python project (etc.,) to recognize the structure and work accordingly.
    '''
    def create_persona(self, persona_details, arch):
        db_col = self.db[self.persona_collection]
        record = {
            'persona': persona_details,
            'hash': arch
        }
        result = db_col.insert_one(record)
        print('Created persona record: {0}'.format(result.inserted_id))

    def get_persona(self, persona_name):
        url = self.base_url + '/get/' + persona_name
        data = requests.get(url).json()
        return data['persona']

    '''
        update persona for the given training loss
    '''
    def update_training_loss(self, training_loss, val_loss):
        url = self.base_url + '/update/' + self.persona_name + '/trainingLoss'
        data = {"trainingLoss": training_loss, "valLoss": val_loss}
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)

    '''
        upload model to the api  
    '''
    def save_model(self, file_name):
        url = self.base_url + '/' + self.persona_name + '/model/' + file_name
        r = requests.post(url, files={'file': open(file_name, 'rb')})

    def run_persona(self, persona_name):
        return
