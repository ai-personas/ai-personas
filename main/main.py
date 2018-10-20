import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from kerasPhysical_test import kerasSoftPhysical
from layoutWidget import LayoutWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.p)
        self.setWindowTitle("AI Persona")

        w = LayoutWidget()
        self.setCentralWidget(w)
        self.showMaximized()

    def clickMethod(self):
        environment = self.getEnvironment()
        keras = kerasSoftPhysical()
        keras.main(environment)

    def getEnvironment(self):
        import json
        from collections import namedtuple

        with open('Environment.json') as f:
            # Parse JSON into an object with attributes corresponding to dict keys.
            x = json.loads(f.read(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            return x

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )