from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.uic.properties import QtWidgets, QtGui

from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.CustomWidgets.HUDOkvir import HUDOkvir
import ctypes


class WinnerView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):
        self.isFullScreen = False
        super(WinnerView, self).__init__()
        self.viewlist = centralWidget
        self.player = ""
        self.playerCar = 0
        self.initUI()

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.setbackground()
        self.backbtn1 = StyleButton('PNG/Buttons/Close_BTN.png', 'Back to Menu', 40, 40)
        self.backbtn1.clicked.connect(self.backtomenu)

        self.backbtn2 = StyleButton('PNG/Buttons/Replay_BTN.png', 'Replay', 40, 40)
        self.backbtn2.clicked.connect(self.replay)


        self.grafickascena.addWidget(self.backbtn1)
        self.backbtn1.move(500, 500)

        self.grafickascena.addWidget(self.backbtn2)
        self.backbtn2.move(250, 500)





        tempImg = QPixmap('PNG/You_Win/Header.png')
        tempImg = tempImg.scaled(500,100)
        self.graphicsPixmapItem = QGraphicsPixmapItem(tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)
        self.graphicsPixmapItem.setPos(220,100)

        self.setScene(self.grafickascena)

    def setbackground(self):
        tempImg = QPixmap('PNG/9c49087c09fd07a10ae3887a7825f389.jpg')
        tempImg = tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        new_pix = QPixmap(tempImg.size())
        new_pix.fill(Qt.darkGray)
        painter = QPainter(new_pix)
        painter.setOpacity(0.35)
        painter.drawPixmap(QPoint(), tempImg)
        painter.end()

        self.graphicsPixmapItem = QGraphicsPixmapItem(new_pix)
        self.grafickascena.addItem(self.graphicsPixmapItem)

    def backtomenu(self):
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

    def replay(self):
        self.viewlist.setCurrentWidget(self.viewlist.widget(3))

    def lastPlayer(self, player, playerCar):
        okvir = HUDOkvir(player,playerCar)  # OVDE UBACITI KOJI IGRAC JE POBEDIO I NJEGOV AUTO
        self.grafickascena.addWidget(okvir)
        okvir.move(370, 230)
