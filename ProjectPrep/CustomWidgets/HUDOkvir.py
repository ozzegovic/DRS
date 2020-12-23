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

        for i in range(3):
            heart = QPixmap('PNG/heartlife32.png')
            heart = QGraphicsPixmapItem(heart)
            heart.moveBy(8+i*36,160)
            self.grafickascena.addItem(heart)


        #-----------------------------------------

        self.label = QLabel(self.name)
        self.label.move(33, 11)
        self.label.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')

        self.grafickascena.addWidget(self.label)
        self.setScene(self.grafickascena)
