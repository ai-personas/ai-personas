import json

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication, QComboBox, QLayout, QLabel, QPushButton, QHBoxLayout)
from keras.engine.saving import load_model

import persona_pb2
from energy import Energy
from school import School


class EnrollPersonaWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.enrollJson = {}
        self.initUI()

    def initUI(self):

        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.p)

        widgetLayout = QVBoxLayout(self)
        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

        titleBox = QHBoxLayout()
        education = QLabel("Enroll Persona", self)
        educationFont = QtGui.QFont("Aerial", 12, QtGui.QFont.Bold)
        education.setFont(educationFont)
        titleBox.addWidget(education)

        personaBox = QHBoxLayout()
        personaLbl = QLabel("Persona", self)
        personaBox.addWidget(personaLbl)
        persona = QComboBox(self)
        persona.addItem("Fantastic MNIST")
        persona.currentTextChanged.connect(self.on_institute_change)
        personaBox.addWidget(persona)

        instituteBox = QHBoxLayout()
        instituteLbl = QLabel("Institution", self)
        instituteBox.addWidget(instituteLbl)
        institute = QComboBox(self)
        institute.addItem("Kandhasamy School")
        institute.currentTextChanged.connect(self.on_institute_change)
        instituteBox.addWidget(institute)

        enrollBox = QHBoxLayout()
        enroll = QPushButton('Enroll', self)
        enroll.clicked.connect(self.on_enroll)
        enrollBox.addWidget(enroll)

        widgetLayout.addLayout(titleBox)
        widgetLayout.addLayout(personaBox)
        widgetLayout.addLayout(instituteBox)
        widgetLayout.addLayout(enrollBox)

    def on_institute_change(self, value):
        self.enrollJson['institute'] = value

    def on_persona_change(self, value):
        self.enrollJson['persona'] = value

    def get_persona(self):
        # f = open(self.enrollJson['persona'], "rb")
        f = open("model/fantastic_mnist.proto", "rb")
        persona = persona_pb2.Persona()
        persona.ParseFromString(f.read())
        f.close()
        return persona

    def get_brain(self, personaDef):
        return load_model(personaDef.brain.modelUrl)

    def on_enroll(self):
        #TODO: store enrollment somewhere and schedule has to happen in the background????

        persona_def = self.get_persona()
        env = json.loads(persona_def.age.environments)
        f = open('dna.json', 'r', encoding='utf-8')
        json.loads("{  }", encoding='utf-8')
        persona_def.dna = json.loads("{  }", encoding='utf-8')
        persona_def.age.environments = json.load(open('Environment.json'))
        if env['school']:
            School().schedule(persona_def)
        # energy = Energy()
        # energy.power(self.get_brain(personaDef), personaDef)
        return


