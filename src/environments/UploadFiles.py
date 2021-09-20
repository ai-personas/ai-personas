import gridfs
from pymongo import MongoClient


class UploadFiles:

    def __init__(self):
        self.mongodb_port = 27017

    '''
        Upload local file to storage
    '''
    def uploadLocalFile(self, environment, fileName, filePath, description):
        client = MongoClient(port=self.mongodb_port)
        db = client.aiPersonas
        fs = gridfs.GridFS(db)
        return