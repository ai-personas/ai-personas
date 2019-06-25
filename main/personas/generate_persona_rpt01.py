from persona import Persona
import tensorflow as tf
import json
from storage.storage import Storage
from importlib import import_module
import os
import zipfile
import requests

def generate_persona_rpt01():
    personas_local_path = 'personas/persona_template_v0_1.json'
    with open(personas_local_path) as f:
        persona = json.load(f)
    persona_def = persona['persona']
    persona_def['name'] = 'rpt01'
    persona_def['status'] = 'exploration'
    age = persona_def['age'][0]

    # store dna in ipfs
    storage = Storage()
    age['dna']['location'] = storage.store('dna/basic/dna_rpt01.py')

    #  store brain in ipfs
    dna_mod = import_module('dna.basic.dna_rpt01')
    brain = getattr(dna_mod, 'generate_brain')()
    brain_path = 'tmp/gen/rpt01/'
    checkpoint = tf.train.Checkpoint(x=brain)
    checkpoint.save(brain_path)
    brain_path = makeZip('rpt01')
    age['brain']['location'] = storage.store(brain_path)

    # set environments
    del age['environments'][-1]
    age['environments'].append({'type': 'books', 'name': 'random_integers', "intention" : "learn" })
    age['environments'].append({'type': 'books', 'name': 'random_integers', "intention" : "self_evaluate" })

    # set status
    persona['persona']['status'] = 'exploration'

    return persona

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            arcname = root[len(root) + 1:]
            print(arcname)
            ziph.write(os.path.join(root, file), file)

def makeZip(dirName):
    zipFileName = dirName + '.zip'
    zipf = zipfile.ZipFile('tmp/gen/' + zipFileName, 'w', zipfile.ZIP_DEFLATED)
    zipdir('tmp/gen/' + dirName, zipf)
    zipf.close()
    return 'tmp/gen/' + zipFileName

