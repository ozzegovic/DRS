from PyQt5.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView, QGraphicsItem, QLineEdit, QGraphicsPixmapItem, QFrame, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QEvent, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage
import time

class HUDOkvir(QGraphicsView):

    def __init__(self, name):
        super().__init__()
        self.name = name
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

        #slika na okviru za hud
        img = QPixmap('PNG/Car_1_Main_Positions/Car_1_01.png')
        img = img.scaled(130, 100)
        self.image = QGraphicsPixmapItem(img)
        self.image.moveBy(10,40)
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