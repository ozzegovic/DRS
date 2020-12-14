from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint

from ProjectPrep.CustomWidgets.HUDOkvir import *


class HUD(QGraphicsView):

    def __init__(self):
        super(HUD, self).__init__()
        self.scene = QGraphicsScene()
        self.label = QLabel('Level\n\n3')
        self.label.setFixedSize(300, 250)
        self.label.setFont(QFont('Ariel', 25))
        self.label.setAlignment(Qt.AlignCenter)

        self.players = [] #igraci
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background: red")
        self.scene.setSceneRect(0, 0, 1200, 250)

        tempImg = QPixmap('PNG/9c49087c09fd07a10ae3887a7825f389.jpg')
        tempImg = tempImg.scaled(self.scene.width(), self.scene.height())

        new_pix = QPixmap(tempImg.size())
        new_pix.fill(Qt.darkGray)
        painter = QPainter(new_pix)
        painter.setOpacity(0.35)
        painter.drawPixmap(QPoint(), tempImg)
        painter.end()

        self.graphicsPixmapItem = QGraphicsPixmapItem(new_pix)
        self.scene.addItem(self.graphicsPixmapItem)


        self.label.setStyleSheet('color: white; font-weight: bold; background: transparent;')

        self.scene.addWidget(self.label).moveBy(20,0)

        for i in range(4):
            okvir = HUDOkvir('Player {}'.format(i))
            self.players.append(okvir)
            self.scene.addWidget(okvir).moveBy(210*i+350, 35)

        self.setScene(self.scene)