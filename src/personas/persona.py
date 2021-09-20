import json
from importlib import import_module

from bson import ObjectId
from pymongo import MongoClient


class Persona:

    def __init__(self):
        self.mongodb_port = 27017
        client = MongoClient(port=self.mongodb_port)
        self.db = client.aiPersonas
        self.persona_collection = 'personas'

    '''
     create persona with given architecture number. The architecture number is the git commit hash where the given persona_spec will work.
    '''
    def create_persona(self, persona_details, arch):
        db_col = self.db[self.persona_collection]
        record = {
            'persona': persona_details,
            'architecture': arch
        }
        result = db_col.insert_one(record)
        print('Created persona record: {0}'.format(result.inserted_id))

    def get_persona(self, persona_name):
        db_col = self.db[self.persona_collection]
        return [
            rec for rec in db_col.find(
                {
                    "name": persona_name
                }
            )
        ][0]

    '''
        update persona for the given fields on the persona id
    '''
    def update_persona(self, id, update_details):
        db_col = self.db[self.persona_collection]
        filter = {
            "_id": id
        }
        db_col.update_one(filter, update_details)

    def run_persona(self, persona_name):
        return
