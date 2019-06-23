import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import ipfsapi

UPLOAD_FOLDER = 'localFolder/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            local_storage_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_storage_path)
            api = ipfsapi.connect('127.0.0.1', 5001)
            res = api.add(local_storage_path)
            print(res)
            return 'success'
    return 'failed'


# def power_persona():
#     if persona_def.softPhysical == 'keras':
#         keras = KerasSoftPhysical(persona_def)
#         keras.learn(x_train, y_train, x_test, y_test)
#
# def get_persona(name):
#     f = open("model/" + name + ".proto", "rb")
#     persona = persona_pb2.Persona()
#     persona.ParseFromString(f.read())
#     f.close()
#     return persona

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8000)