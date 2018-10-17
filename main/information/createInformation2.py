from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication,
                             QFormLayout, QSpacerItem,
                             QSizePolicy, QGridLayout)
from PyQt5.QtCore import Qt

import sys

class Main(QWidget):

    def __init__(self):
        super().__init__()

        # Set window background color
        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.p)

        self.initUI()

    def initUI(self):
        # self.layout = QFormLayout()
        # hzSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        #
        # self.versionLabel = QLabel("Version", self)
        #
        # versionDropDown = QComboBox(self)
        # versionDropDown.addItem("v1")
        # versionDropDown.addItem("v2")
        # versionDropDown.activated[str].connect(self.onActivated)
        # versionDropDown.setMaximumWidth(100)
        #
        # self.layout.addRow(self.versionLabel, versionDropDown)
        # self.setLayout(self.layout)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        versionLabel = QLabel("Version", self)
        versionDropDown = QComboBox(self)
        versionDropDown.addItem("v1")
        versionDropDown.addItem("v2")
        versionDropDown.activated[str].connect(self.onActivated)
        versionDropDown.setMaximumWidth(100)
        self.grid.addWidget(versionLabel, 1, 1)
        self.grid.addWidget(versionDropDown, 2, 1)

        self.setLayout(self.grid)
        self.setWindowTitle('aiPersona')
        self.showMaximized()

    def onActivated(self, text):
        hzSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.versionLabel = QLabel("Test", self)

        versionDropDown = QComboBox(self)
        versionDropDown.addItem("v1")
        versionDropDown.addItem("v2")
        versionDropDown.activated[str].connect(self.onActivated)
        versionDropDown.setMaximumWidth(100)

        self.layout.addRow(self.versionLabel, versionDropDown)


app = QApplication(sys.argv)
ex = Main()
sys.exit(app.exec_())


