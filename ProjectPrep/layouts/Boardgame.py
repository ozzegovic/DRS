import sys

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from ProjectPrep.CustomWidgets.HUD import HUD
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton


class Boardgame(QGraphicsView):

    def __init__(self):

        super(Boardgame, self).__init__()

        self.hud = HUD()
        self.initUI()

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)
        self.setScene(self.grafickascena)

        self.grafickascena.addWidget(self.hud).moveBy(0,380)

        self.pausebutton = StyleButton('PNG/Main_UI/Pause_BTN.png', 'Pause', 40, 40)
        self.pausebutton.clicked.connect(self.pauseButtonClick)
        self.grafickascena.addWidget(self.pausebutton).moveBy(self.grafickascena.width()-45, 0)

    def pauseButtonClick(self):
        a = 5

