import ipfsapi
from  storage.decentralizedStorage import DecentralizedStorage
from storage.centralizedStorage import PrivateStorage

class Storage:

    def store(self, file):
        location = {}
        # centralized storage
        cstorage = PrivateStorage()
        location['personas.ai'] = cstorage.store(file)
        # decentralized storage
        dstorage = DecentralizedStorage()
        location['ipfs'] = dstorage.store(file)
        return location

    def retrieve(self, location, dir_name, file_name):
        print('hash', location['ipfs'])
        # retrieve it from decentralized storage
        dstorage = DecentralizedStorage()
        return dstorage.retrieve(location['ipfs'], dir_name, file_name)
