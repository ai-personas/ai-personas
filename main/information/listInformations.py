from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt
import sys


class listInformations(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.changeEvent)

        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.showMaximized()

    def changeEvent(self, state):

        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')


app = QApplication(sys.argv)
ex = listInformations()
sys.exit(app.exec_())

