from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap

from ProjectPrep.CustomWidgets.ButtonNotifier import Worker
from ProjectPrep.CustomWidgets.HUD import HUD
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton

class Boardgame(QGraphicsView):

    def __init__(self):

        super(Boardgame, self).__init__()
        self.hud = HUD()
        self.initUI()

        self.worker = Worker()
        self.worker.update.connect(self.movepicture)
        #self.worker.start() # Pokreni ovo na tajmer.

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

        self.tempImg = QPixmap('PNG/background-1.png')
        self.tempImg = self.tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        self.graphicsPixmapItem = QGraphicsPixmapItem(self.tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)

        self.mapContinue = QGraphicsPixmapItem(self.tempImg)
        self.grafickascena.addItem(self.mapContinue)

        self.grafickascena.addWidget(self.hud).moveBy(0,380)

        self.pauseButton = StyleButton('PNG/Main_UI/Pause_BTN.png', 'Play', 40, 40)
        self.pauseButton.clicked.connect(self.pauseButtonClick)
        self.pauseButton.move(self.grafickascena.width()-45, 8)
        self.grafickascena.addWidget(self.pauseButton)

        self.setScene(self.grafickascena)

    def pauseButtonClick(self):
            a = 5

    @pyqtSlot()
    def movepicture(self):
        self.graphicsPixmapItem.moveBy(0, -2)
        res1 = self.graphicsPixmapItem.y() % self.tempImg.height()

        self.mapContinue.setY(res1)

        if self.graphicsPixmapItem.y() == -self.tempImg.height():
            self.graphicsPixmapItem.setY(0)
