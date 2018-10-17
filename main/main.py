import sys

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox
from PyQt5.QtWidgets import QPushButton

from kerasPhysical_test import kerasSoftPhysical

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.p)
        self.setWindowTitle("AI Persona")

        education = QLabel("Education", self)
        educationFont = QtGui.QFont("Aerial", 12, QtGui.QFont.Bold)
        education.setFont(educationFont)
        education.resize(200, 34)
        education.move(50, 20)

        instituteLbl = QLabel("Institution", self)
        institute = QComboBox(self)
        institute.resize(200, 50)
        instituteLbl.resize(200, 50)
        instituteLbl.move(50, 70)
        institute.move(200, 70)
        institute.addItem("School")
        institute.addItem("College")

        gradeLbl = QLabel("Grade", self)
        grade = QComboBox(self)
        grade.addItem("1")
        grade.addItem("2")
        grade.resize(200, 50)
        gradeLbl.move(50, 140)
        grade.move(150, 140)

        courseLbl = QLabel("Course", self)
        course = QComboBox(self)
        course.addItem("MNIST Image classification")
        course.addItem("MNIST2 Image classification")
        course.resize(400, 50)
        courseLbl.move(50, 200)
        course.move(150, 200)

        startClass = QPushButton('Enroll into school', self)
        startClass.clicked.connect(self.clickMethod)
        startClass.resize(300, 64)
        startClass.move(50, 300)

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