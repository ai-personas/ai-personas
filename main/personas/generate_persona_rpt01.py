from persona import Persona
import tensorflow as tf
import json
from storage.storage import Storage
from importlib import import_module
import os
import zipfile
import requests

def generate_persona_gsc01():
    personas_local_path = 'personas/persona_template_v0_1.json'
    with open(personas_local_path) as f:
        persona = json.load(f)
    persona_def = persona['persona']
    persona_def['name'] = 'gsc01'
    persona_def['status'] = 'exploration'
    age = persona_def['age'][0]

    # store dna in ipfs
    storage = Storage()
    age['dna']['location'] = storage.store('tmp/dna_gsc01.py')

    #  store brain in ipfs
    dna_mod = import_module('tmp.dna_gsc01')
    brain = getattr(dna_mod, 'generate_brain')()
    brain_path = './tmp/gsc01/'
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver.save(sess, brain_path)
    brain_path = makeZip('gsc01')
    age['brain']['location'] = storage.store(brain_path)

    # set environments
    age['environments'][0] = {'type': 'books', 'name': 'google_speech_commands' }
    return persona


def generate_environment_google_speech_commands():
    storage = Storage()
    env_local_path = 'environments/environment_template_v0_1.json'
    with open(env_local_path) as f:
        environment = json.load(f)['environment']
    environment['name'] = 'google_speech_commands'
    environment['type'] = 'book'
    environment['interface'] = storage.store('./tmp/google_speech_commands.py')
    environment['data'][0] = {'input': 'audio', 'output': 'labels'}
    save_environment(environment)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def makeZip(dirName):
    zipFileName = dirName + '.zip'
    zipf = zipfile.ZipFile('./tmp/' + zipFileName, 'w', zipfile.ZIP_DEFLATED)
    zipdir('./tmp/' + dirName, zipf)
    zipf.close()
    return './tmp/' + zipFileName

def save_environment(environment):
    personas_ai_url = "http://localhost:8080/save-environment/" + environment['name']
    data = { 'environmentDef': environment }
    # print("env:",json.dumps(environment))
    r = requests.post(url=personas_ai_url, json=environment)


