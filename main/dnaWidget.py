
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit)

import json

class DnaWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.dnaJson = {}
        self.initUI()

    def initUI(self):

        self.setAutoFillBackground(True)
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.p)

        widgetLayout = QVBoxLayout(self)
        widgetLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(widgetLayout)

        inputSizeBox = QHBoxLayout()
        inputSizeLbl = QLabel("Input size", self)
        inputSizeBox.addWidget(inputSizeLbl)
        inputSize = QLineEdit(self)
        inputSize.textChanged.connect(self.on_input_size_change)
        inputSizeBox.addWidget(inputSize)

        layerBox = QHBoxLayout()
        layerLbl = QLabel("Layer", self)
        layerBox.addWidget(layerLbl)
        layer = QComboBox(self)
        layer.addItem("")
        layer.addItem("Dense")
        layer.addItem("Dropout")
        layer.currentTextChanged.connect(self.on_layer_selection)
        layerBox.addWidget(layer)

        addLayerBox = QHBoxLayout()
        addLayer = QPushButton('Add Layer', self)
        addLayer.clicked.connect(self.addNewLayer)
        addLayerBox.addWidget(addLayer)

        lossBox = QHBoxLayout()
        lossLbl = QLabel("Loss", self)
        lossBox.addWidget(lossLbl)
        loss = QComboBox(self)
        loss.addItem("")
        loss.addItem("categorical crossentropy")
        loss.currentTextChanged.connect(self.on_loss_change)
        lossBox.addWidget(loss)

        optimizerBox = QHBoxLayout()
        optimizerLbl = QLabel("Optimizer", self)
        optimizerBox.addWidget(optimizerLbl)
        optimizer = QComboBox(self)
        optimizer.addItem("")
        optimizer.addItem("RMS Probability")
        optimizer.currentTextChanged.connect(self.on_optimizer_change)
        optimizerBox.addWidget(optimizer)

        widgetLayout.addLayout(inputSizeBox)
        widgetLayout.addLayout(layerBox)
        widgetLayout.addLayout(addLayerBox)
        widgetLayout.addLayout(lossBox)
        widgetLayout.addLayout(optimizerBox)

    def addNewLayer(self):
        print("test")

    def on_layer_selection(self, value):
        if 'layers' in self.dnaJson:
            self.dnaJson['layers'].append(value)
        else:
            self.dnaJson['layers'] = [value]

    def on_input_size_change(self, value):
        self.dnaJson['inputSize'] = value

    def on_loss_change(self, value):
        self.dnaJson['loss'] = value

    def on_optimizer_change(self, value):
        self.dnaJson['optimizer'] = value

    def get_dna(self):
        return self.dnaJson