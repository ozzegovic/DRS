from PyQt5.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView, QGraphicsItem, QLineEdit, QGraphicsPixmapItem, QFrame, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QEvent, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage
import time

class HUDOkvir(QGraphicsView):

    def __init__(self, name, car):
        super().__init__()
        self.name = name
        self.car = car
        self.lives = [] #array of QGraphicsPixmapItem for hearts
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

        self.path = 'PNG/Car_' + str(self.car) + '_Main_Positions/Car_' + str(self.car) + '_01'
        #slika na okviru za hud
        img = QPixmap(self.path)
        img = img.scaled(100, 120)
        self.image = QGraphicsPixmapItem(img)
        self.image.moveBy(25, 30)
        self.grafickascena.addItem(self.image)

        self.initLives(4) # makes 4 heart images and positions them correctly
        self.setLives(3)  # show only 3 on init
        #-----------------------------------------

        self.label = QLabel(self.name)
        self.label.setFixedWidth(120)
        self.label.move(33, 11)
        self.label.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')

        self.grafickascena.addWidget(self.label)
        self.setScene(self.grafickascena)

    def setNameAndCar(self, name, car):

        self.label.setText(name)
        if car == '0':
            self.grafickascena.removeItem(self.image)
        else:
            self.image.setPixmap(QPixmap('PNG/Car_' + car + '_Main_Positions/Car_' + car + '_01').scaled(100, 120))
            self.grafickascena.addItem(self.image)

    def initLives(self, lifeCount):
        for i in range(lifeCount):
            heart = QPixmap('PNG/Main_UI/HP_Dot.png')
            heart = QGraphicsPixmapItem(heart.scaledToWidth(32))
            heart.moveBy(8+i*33, 160)
            self.lives.append(heart)
            self.grafickascena.addItem(heart)

    # show the exact amount of hearts a specific player has
    def setLives(self, lifeCount):
        for i in range(lifeCount):
            self.lives[i].show()
        for i in range(4 - lifeCount):  # maximum number of lives is 4, calculate how many to hide
            self.lives[3-i].hide()      # start from the last
