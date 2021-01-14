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
        self.mode = 0
        # dictionary {playerName : hudFrame} easier to access each player's frame
        self.players = {} #igraci
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

    def setMode(self, mode):
        self.mode = mode
        self.label.setText("Result\n\n0 - 0")

    def setHUDResult(self, deaths1, deaths2):
        self.label.setText("Result\n\n{} - {}".format(deaths2, deaths1))

    def updateHUD(self):
        if self.mode == 1:
            return

        if self.level < 10:
            self.level += 1

        if self.level == 10:
            self.label.setStyleSheet('color: red; font-weight: bold; background: transparent;')

        self.label.setText("Level\n\n{}".format(self.level))

    def initHudFrames(self, players):
        for key in self.players.keys():
           self.players[key].deleteLater() #delete hudFrames

        self.players = {}

        for player in players:
            okvir = HUDOkvir(player.playerName, player.Car)
            okvir.setLives(player.lives)
            self.players[player.playerName] = okvir #init dictionary
            self.updatePlayerLives(player)
            self.hbox.addWidget(okvir)

    def updatePlayerLives(self, player):
        # self.players - dictionary {playerName : hudFrame}
        # easier to access and update lives for a specific player
        hudOkvir = self.players[player.playerName]
        hudOkvir.setLives(player.lives)

