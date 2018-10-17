from PyQt5.QtWidgets import (QWidget, QLabel,
                             QComboBox, QApplication,
                             QFormLayout, QSpacerItem,
                             QSizePolicy)
import sys


class CreateNewInformation(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QFormLayout()
        hzSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.versionLabel = QLabel("Version", self)

        versionDropDown = QComboBox(self)
        versionDropDown.addItem("v1")
        versionDropDown.addItem("v2")
        versionDropDown.activated[str].connect(self.onActivated)
        versionDropDown.setMaximumWidth(100)

        layout.addRow(self.versionLabel, versionDropDown)
        self.setLayout(layout)

        self.setWindowTitle('aiPersona')
        self.showMaximized()

    def onActivated(self, text):
        layout = QFormLayout()
        hzSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.versionLabel = QLabel("Test", self)

        versionDropDown = QComboBox(self)
        versionDropDown.addItem("v1")
        versionDropDown.addItem("v2")
        versionDropDown.activated[str].connect(self.onActivated)
        versionDropDown.setMaximumWidth(100)

        layout.addRow(self.versionLabel, versionDropDown)
        self.setLayout(self.layout)


app = QApplication(sys.argv)
ex = CreateNewInformation()
sys.exit(app.exec_())


