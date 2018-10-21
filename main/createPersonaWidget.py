
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit)

import json
import persona_pb2
from kerasPhysical import KerasSoftPhysical

class CreatePersonaWidget(QWidget):

    def __init__(self, dnaJson, environmentJson):
        super().__init__()
        self.dnaJson = dnaJson
        self.environmentJson = environmentJson
        self.initUI()

    def initUI(self):
        self.initializePersona()

        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.p)

        widgetLayout = QVBoxLayout(self)
        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

        nameBox = QHBoxLayout()
        nameLbl = QLabel("Persona name", self)
        nameBox.addWidget(nameLbl)
        name = QLineEdit(self)
        name.textChanged.connect(self.on_name_change)
        nameBox.addWidget(name)

        createPersonaBox = QHBoxLayout()
        createPersona = QPushButton('Create Persona', self)
        createPersona.clicked.connect(self.createPersona)
        createPersonaBox.addWidget(createPersona)

        widgetLayout.addLayout(nameBox)
        widgetLayout.addLayout(createPersonaBox)

    def createPersona(self):
        self.persona.dna = json.dumps(self.dnaJson)
        self.persona.softPhysical = "keras"
        self.persona.age.old = 0
        self.persona.age.knowledgeCycle = 0
        self.persona.age.environments = json.dumps(self.environmentJson)
        if self.persona.softPhysical == 'keras':
            keras = KerasSoftPhysical(self.persona)
            brain = keras.create_persona()
            brain.save_weights(self.persona.name + ".h5")
            self.persona.brain.modelJson = brain.to_json()
            self.persona.brain.modelUrl = self.persona.name + ".h5"
            self.store_persona()

    def initializePersona(self):
        self.persona = persona_pb2.Persona()

    def on_name_change(self, value):
        self.persona.name = value

    def store_persona(self):
        f = open(self.persona.name + ".proto", "wb")
        f.write(self.persona.SerializeToString())
        f.close()
