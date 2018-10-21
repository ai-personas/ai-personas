from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication, QComboBox, QLayout, QLabel, QPushButton, QHBoxLayout)


class SchoolWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.schoolJson = {}
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
        education = QLabel("Education", self)
        educationFont = QtGui.QFont("Aerial", 12, QtGui.QFont.Bold)
        education.setFont(educationFont)
        titleBox.addWidget(education)

        instituteBox = QHBoxLayout()
        instituteLbl = QLabel("Institution", self)
        instituteBox.addWidget(instituteLbl)
        institute = QComboBox(self)
        institute.addItem("School")
        institute.addItem("College")
        institute.currentTextChanged.connect(self.on_institute_change)
        instituteBox.addWidget(institute)

        gradeBox = QHBoxLayout()
        gradeLbl = QLabel("Grade", self)
        gradeBox.addWidget(gradeLbl)
        grade = QComboBox(self)
        grade.addItem("1")
        grade.addItem("2")
        grade.currentTextChanged.connect(self.on_institute_change)
        gradeBox.addWidget(grade)

        courseBox = QHBoxLayout()
        courseLbl = QLabel("Course", self)
        courseBox.addWidget(courseLbl)
        course = QComboBox(self)
        course.addItem("MNIST Image classification")
        course.addItem("MNIST2 Image classification")
        course.currentTextChanged.connect(self.on_institute_change)
        courseBox.addWidget(course)

        enrollBox = QHBoxLayout()
        startClass = QPushButton('Enroll into school', self)
        # startClass.clicked.connect(self.clickMethod)
        enrollBox.addWidget(startClass)

        widgetLayout.addLayout(titleBox)
        widgetLayout.addLayout(instituteBox)
        widgetLayout.addLayout(gradeBox)
        widgetLayout.addLayout(courseBox)
        widgetLayout.addLayout(enrollBox)

    def get_school(self):
        return self.schoolJson

    def on_institute_change(self, value):
        self.dnaJson['institute'] = value

    def on_grade_change(self, value):
        self.dnaJson['grade'] = value

    def on_course_change(self, value):
        self.dnaJson['course'] = value
