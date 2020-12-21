from PyQt5.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView, QGraphicsItem, QLineEdit, QGraphicsPixmapItem, QFrame, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QEvent, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage
import time
from ProjectPrep.CustomWidgets.CustomButton import StyleButton


class InputOkvir(QGraphicsView):

    def __init__(self, number):
        super().__init__()
        self.playercounter = number + 1  # to avoid 'Player 0' name
        self.playerName = ''
        self.Car = 1  # default car choice is 1
        self.graphicsPixmapItemCar = QGraphicsPixmapItem()
        self.initUI()

    def initUI(self):

        self.setStyleSheet("background: transparent")
        self.setFrameShape(QFrame.NoFrame)

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 150, 200)

        tempImg = QPixmap('PNG/Level_Menu/Window.png')
        tempImg = tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        self.graphicsPixmapItem = QGraphicsPixmapItem(tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)

        # set default label text
        self.label = QLabel('Car ' + str(self.Car))

        self.label.move(33, 11)
        self.label.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')

        # set default car
        carImg = QPixmap('PNG/Car_1_Main_Positions/Car_1_01')
        carImg = carImg.scaled(100, 120)
        self.graphicsPixmapItemCar = QGraphicsPixmapItem(carImg)
        self.graphicsPixmapItemCar.setPos(25, 30)
        self.grafickascena.addItem(self.graphicsPixmapItemCar)

        self.nextButton = StyleButton('PNG/Main_UI/Right', '', 20, 15)
        self.nextButton.resize(20, 20)
        self.nextButton.move(130, 5)
        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.grafickascena.addWidget(self.nextButton)

        self.previousButton = StyleButton('PNG/Main_UI/Left', '', 20, 15)
        self.previousButton.move(10, 5)
        self.previousButton.resize(20, 20)
        self.previousButton.clicked.connect(self.previousButtonClicked)
        self.grafickascena.addWidget(self.previousButton)

        self.playerNameEdit = QLineEdit()
        self.playerNameEdit.resize(130, 30)
        self.playerNameEdit.setText('Player ' + str(self.playercounter))
        self.playerNameEdit.editingFinished.connect(self.onChanged)
        self.playerNameEdit.move(10, 160)
        self.playerNameEdit.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')

        self.grafickascena.addWidget(self.playerNameEdit)
        self.grafickascena.addWidget(self.label)
        self.setScene(self.grafickascena)

    def onChanged(self):
        self.playerName = self.playerNameEdit.text()

    def nextButtonClicked(self):
        # generate path to the next car based on the current car
        self.tempCar = ((self.Car + 1) % 4)
        if self.tempCar == 0:
            self.Car = 1
        else:
            self.Car = self.tempCar

        path = 'PNG/Car_' + str(self.Car) + '_Main_Positions/Car_' + str(self.Car) + '_01'

        # replace car image
        carImg = QPixmap(path)
        carImg = carImg.scaled(100, 120)
        self.grafickascena.removeItem(self.graphicsPixmapItemCar)
        self.graphicsPixmapItemCar = QGraphicsPixmapItem(carImg)
        self.graphicsPixmapItemCar.setPos(25, 30)
        self.grafickascena.addItem(self.graphicsPixmapItemCar)

        # change label text above the image
        self.label.setText('Car ' + str(self.Car))

    def previousButtonClicked(self):
        # generate path to the previous car based on the current car
        self.tempCar = ((self.Car  - 1) % 4)
        if self.tempCar == 0:
            self.Car = 3
        else:
            self.Car = self.tempCar
        path = 'PNG/Car_' + str(self.Car) + '_Main_Positions/Car_' + str(self.Car) + '_01'

        # replace car image
        carImg = QPixmap(path)
        carImg = carImg.scaled(100, 120)
        self.grafickascena.removeItem(self.graphicsPixmapItemCar)
        self.graphicsPixmapItemCar = QGraphicsPixmapItem(carImg)
        self.graphicsPixmapItemCar.setPos(25, 30)
        self.grafickascena.addItem(self.graphicsPixmapItemCar)

        # change label text above the image
        self.label.setText('Car ' + str(self.Car))


