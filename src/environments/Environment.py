import cgi
import shutil

import requests
from bson import ObjectId
from pymongo import MongoClient
from tqdm import tqdm

from commons.FileUtils import FileUtils
from constants.PersonaConstants import BASE_URL


class Environment:

    def __init__(self, env_meta):
        self.mongodb_port = 27017
        self.env_collection = 'environments'
        self.base_url = BASE_URL + '/personas/env/'
        self.env_meta = env_meta
        self.fileUtils = FileUtils('downloaded/')

    def getEnvironmentUrlToLocal(self, env):
        url = env['url']
        return self.fileUtils.downloadDataToLocal(url)

    '''
        Retrieve environment details for given environment meta information
    '''
    def retrieveEnvDetails(self):
        url = self.base_url + '/' + str(self.env_meta['specId']) + '/get/' + self.env_meta['name']
        data = requests.get(url).json()
        return data['environment']


    '''
        Create new environment with given hash number. The hash is the arbitrary number.
    '''
    def createEnvironment(self, env_details, hash):
        client = MongoClient(port=self.mongodb_port)
        db = client.aiPersonas
        db_col = db[self.env_collection]
        record = {
            'environment': env_details,
            'hash': hash
        }
        result = db_col.insert_one(record)
        print('Created environment record: {0}'.format(result.inserted_id))
