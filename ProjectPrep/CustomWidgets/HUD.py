from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint

from ProjectPrep.CustomWidgets.HUDOkvir import *


class HUD(QGraphicsView):

    def __init__(self):
        super(HUD, self).__init__()
        self.scene = QGraphicsScene()
        self.level = 1
        self.label = QLabel('Level\n\n{}'.format(self.level))
        self.label.setFixedWidth(300)
        self.label.setFont(QFont('Ariel', 25))
        self.label.setAlignment(Qt.AlignCenter)

        self.players = [] #igraci
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background: transparent")
        self.scene.setSceneRect(0, 0, 1000, 223)

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

        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.label)
        self.scene.addWidget(self.label)

        self.setFrameShape(QFrame.NoFrame)
        self.setLayout(self.hbox)
        self.setScene(self.scene)

    def restart(self):
        self.label.setStyleSheet('color: white; font-weight: bold; background: transparent;')
        self.level = 1
        self.label.setText("Level\n\n{}".format(self.level))

    def updateHUD(self):
        if self.level < 10:
            self.level += 1

        if self.level == 10:
            self.label.setStyleSheet('color: red; font-weight: bold; background: transparent;')

        self.label.setText("Level\n\n{}".format(self.level))

    def initHudFrames(self, players):
        for okvir in self.players:
            okvir.deleteLater()

        self.players.clear()

        for player in players:
            okvir = HUDOkvir(player, players[player])
            self.players.append(okvir)
            self.hbox.addWidget(okvir)
