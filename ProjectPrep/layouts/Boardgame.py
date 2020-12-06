from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton

class Boardgame(QGraphicsView):

    def __init__(self):

        super(Boardgame, self).__init__()

        self.initUI()

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

        self.setScene(self.grafickascena)