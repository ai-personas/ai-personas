import requests
from kerasPhysical import KerasSoftPhysical


class Energy:

    def __init__(self, address):
        self.address = address

    def power(self, persona_name, persona_def, x_train, y_train, x_test, y_test):
        persona_def = open("model/" + persona_name + ".proto", "rb")
        persona_model = open("model/" + persona_name + ".h5", "rb")
        persona_def_file = [('file', persona_def)]
        persona_model_file = [('file', persona_model)]
        persona_def_req = requests.post(self.address, files=persona_def_file)
        # if persona_def_req.status_code == 200:
        #     persona_model_req = requests.post(self.address, files=persona_model_file)
        #     print(persona_model_req.status_code)

        # if persona_def.softPhysical == 'keras':
        #     keras = KerasSoftPhysical(persona_def)
        #     keras.learn(x_train, y_train, x_test, y_test)



e = Energy("http://localhost:8000")
e.power("test4", "","","","","")
