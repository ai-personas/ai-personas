import cgi
import shutil

import requests
from bson import ObjectId
from pymongo import MongoClient
from tqdm import tqdm


class Environment:

    def __init__(self, env_meta):
        self.mongodb_port = 27017
        self.env_collection = 'environments'
        self.base_url = 'http://localhost:8090/personas/env/'
        self.env_meta = env_meta

    def getEnvironmentUrlToLocal(self, env):
        url = env['url']

        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

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
