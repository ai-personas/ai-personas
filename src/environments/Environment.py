from bson import ObjectId
from pymongo import MongoClient


class Environment:

    def __init__(self):
        self.mongodb_port = 27017

    '''
        Retrieve environment details for given environment meta information
    '''
    def retrieveEnvDetails(self, environment):
        client = MongoClient(port=self.mongodb_port)
        db = client.aiPersonas
        db_col = db[environment['environment']]
        return [
            rec for rec in db_col.find(
                {
                    "_id": ObjectId(environment['id'])
                }
            )
        ]

