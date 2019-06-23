from persona import Persona
import tensorflow as tf
import json
from storage.storage import Storage
from importlib import import_module
import os
import zipfile
import requests

def generate_environment_random_integers():
    storage = Storage()
    env_local_path = 'environments/environment_template_v0_1.json'
    with open(env_local_path) as f:
        environment = json.load(f)['environment']
    environment['name'] = 'random_integers'
    environment['type'] = 'book'
    environment['interface'] = storage.store('./tmp/BasicResearch/random_integers.py')
    environment['data'][0] = {'input': 'input_integers', 'output': 'output_integers'}
    save_environment(environment)

def save_environment(environment):
    personas_ai_url = "http://localhost:8080/save-environment/" + environment['name']
    data = { 'environmentDef': environment }
    # print("env:",json.dumps(environment))
    r = requests.post(url=personas_ai_url, json=environment)


