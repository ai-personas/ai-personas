import sys
import imp
import os
import requests
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
import logging

PROTO_PYTHON_EXTENSION = "_pb2.py"
INFORMATION_BLUEPRINT = "informationBlueprint_v1" + PROTO_PYTHON_EXTENSION

logging.basicConfig()
logger = logging.getLogger('Extractor')
logger.setLevel(logging.DEBUG)

information_blueprint_path = os.path.abspath(os.path.join(INFORMATION_BLUEPRINT))
logger.debug("information blue print path: " + information_blueprint_path)
logger.debug("import information blueprint")
informationBlueprint = imp.load_source('Information', information_blueprint_path).Information()



print(list(informationBlueprint.DESCRIPTOR.fields_by_name.keys()))

for f in informationBlueprint.DESCRIPTOR.fields:

    print(f.type)

