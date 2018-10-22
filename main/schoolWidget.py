import json

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication, QComboBox, QLayout, QLabel, QPushButton, QHBoxLayout,
                             QLineEdit)


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

        nameBox = QHBoxLayout()
        nameLbl = QLabel("Name", self)
        nameBox.addWidget(nameLbl)
        name = QLineEdit(self)
        name.textChanged.connect(self.on_name_change)
        nameBox.addWidget(name)

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
        grade.currentTextChanged.connect(self.on_grade_change)
        gradeBox.addWidget(grade)

        courseBox = QHBoxLayout()
        courseLbl = QLabel("Course", self)
        courseBox.addWidget(courseLbl)
        course = QComboBox(self)
        course.addItem("MNIST Image classification")
        course.addItem("MNIST2 Image classification")
        course.currentTextChanged.connect(self.on_course_change)
        courseBox.addWidget(course)

        scheduleBox = QHBoxLayout()
        scheduleLbl = QLabel("Class schedule", self)
        scheduleBox.addWidget(scheduleLbl)
        schedule = QLineEdit(self)
        schedule.textChanged.connect(self.on_schedule_change)
        scheduleBox.addWidget(schedule)

        createSchoolBox = QHBoxLayout()
        createSchool = QPushButton('Create School', self)
        createSchool.clicked.connect(self.on_create_school)
        createSchoolBox.addWidget(createSchool)

        widgetLayout.addLayout(titleBox)
        widgetLayout.addLayout(nameBox)
        widgetLayout.addLayout(instituteBox)
        widgetLayout.addLayout(gradeBox)
        widgetLayout.addLayout(courseBox)
        widgetLayout.addLayout(scheduleBox)
        widgetLayout.addLayout(createSchoolBox)

    def get_school(self):
        return self.schoolJson

    def on_name_change(self, value):
        self.schoolJson['name'] = value

    def on_institute_change(self, value):
        self.schoolJson['institute'] = value

    def on_grade_change(self, value):
        self.schoolJson['grade'] = value

    def on_course_change(self, value):
        self.schoolJson['course'] = value

    def on_schedule_change(self, value):
        self.schoolJson['classSchedule'] = value

    def on_create_school(self):
        f = open(self.schoolJson['name'] + ".json", "w")
        f.write(json.dumps(self.schoolJson))
        f.close()
