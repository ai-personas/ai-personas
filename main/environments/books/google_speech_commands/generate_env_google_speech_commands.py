from persona import Persona
import tensorflow as tf
import json
from storage.storage import Storage
from importlib import import_module
import os
import zipfile
import requests

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

