import requests
import json
from storage.storage import Storage
from importlib import import_module
import tensorflow as tf
import zipfile
import os

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

    def to(self, persona):
        self.persona = persona
        # get current age
        age = persona['persona']['age'][0]

        # personas moves around all the environments
        for persona_env in age['environments']:
            storage = Storage()

            # import dna
            dna = storage.retrieve(age['dna']['location'], 'tmp/run/dna/',
                                   persona['persona']['name'] + ".py")
            print(dna)
            dna_mod = import_module('tmp.run.dna.' + persona['persona']['name'])

            # restore brain
            zip_file_dir = 'tmp/run/persona/rpt01/'
            brain_old = storage.retrieve(age['brain']['location'], zip_file_dir,
                                   persona['persona']['name'] + ".zip")
            self.extract_zip(zip_file_dir + 'ext/',
                            zip_file_dir + persona['persona']['name'] + ".zip")
            brain = getattr(dna_mod, 'generate_brain')()
            checkpoint = tf.train.Checkpoint(x=brain)
            checkpoint.restore(tf.train.latest_checkpoint(zip_file_dir + 'ext/'))

            # get current environment
            environment = self.get_environment(persona_env['name'])
            print(environment)

            # import env interface
            envInterface = storage.retrieve(environment['interface'], 'tmp/run/env/',
                                            environment['name'] + ".py")
            print(envInterface)
            env_mod = import_module('tmp.run.env.' + environment['name'])

            # place persona to receive feed from environment
            feed = getattr(env_mod, 'get_data')()
            print(feed)
            if persona_env['intention'] == 'learn':
                getattr(dna_mod, 'learn')(brain, feed['input_integers'], feed['output_integers'], 100)
            if persona_env['intention'] == 'self_evaluate':
                score = getattr(dna_mod, 'self_evaluate')(brain, feed['input_integers'], feed['output_integers'])
                age['history'][0] = {'environment' : environment['name'], 'score' : score}

            # save brain
            self.save_brain(age, zip_file_dir + 'ext/', brain)
            # save persona definition
            self.save_persona_def(persona['persona']['name'], persona)
        return

    def get_environment(self, name):
        personas_ai_url = "http://localhost:8080/get-environment/" + name
        r = requests.get(url=personas_ai_url)
        return json.loads(r.json()['environmentDef'])

    def save_brain(self, age, brain_path, brain):
        checkpoint = tf.train.Checkpoint(x=brain)
        checkpoint.save(brain_path)
        brain_path = self.makeZip(self.persona['persona']['name'])
        age['brain']['location'] = storage.store(brain_path)

    def save_persona_def(self, name, persona_def):
        personas_ai_url = "http://localhost:8080/save-persona/" + name
        r = requests.post(url=personas_ai_url, json=persona_def)

    def extract_zip(self, dir_to_extract, zip_file_name):
        zip_ref = zipfile.ZipFile(zip_file_name, 'r')
        zip_ref.extractall(dir_to_extract)
        zip_ref.close()

    def zipdir(self, path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                arcname = root[len(root) + 1:]
                print(arcname)
                ziph.write(os.path.join(root, file), file)

    def makeZip(self, dirName):
        zipFileName = dirName + '.zip'
        zipf = zipfile.ZipFile('tmp/gen/' + zipFileName, 'w', zipfile.ZIP_DEFLATED)
        self.zipdir('tmp/gen/' + dirName, zipf)
        zipf.close()
        return 'tmp/gen/' + zipFileName

