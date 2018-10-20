
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit)

import json

class CreatePersonaWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.personaJson = {}

        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.p)

        widgetLayout = QVBoxLayout(self)
        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

        createPersonaBox = QHBoxLayout()
        createPersona = QPushButton('Create Persona', self)
        createPersona.clicked.connect(self.compilePersona)
        createPersonaBox.addWidget(createPersona)

        widgetLayout.addLayout(createPersonaBox)

    def compilePersona(self):
        print("test")

