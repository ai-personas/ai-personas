import requests


class PrivateStorage:

    def __init__(self):
        self.url = "http://localhost:8080"

    def save_new_persona(self, persona_name, persona_meta):
        path = "/save-new-persona"
        return requests.post(self.url + path, data = persona_meta)

    def save_persona_def(self, persona_name, age, fPath):
        path = "/save-brain/" + persona_name + "/" + age
        files = {'upload_file': open(fPath, 'rb')}
        return requests.post(self.url + path, files=files)

    def save_brain(self, persona_name, age, fPath):
        path = "/save-brain/" + persona_name + "/" + age
        files = {'upload_file': open(fPath, 'rb')}
        return requests.post(self.url + path, files=files)
