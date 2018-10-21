from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLayout)

from createPersonaWidget import CreatePersonaWidget
from dnaWidget import DnaWidget
from schoolWidget import SchoolWidget


class LayoutWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        school = SchoolWidget()
        school.resize(school.sizeHint())

        dna = DnaWidget()
        dna.resize(dna.sizeHint())

        createPersona = CreatePersonaWidget(dna.get_dna(), school.get_school())
        createPersona.resize(dna.sizeHint())

        vbox = QVBoxLayout(self)
        vbox.addWidget(school)
        vbox.addWidget(dna)
        vbox.addWidget(createPersona)
        vbox.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(vbox)

