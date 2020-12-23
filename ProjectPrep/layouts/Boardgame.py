import random
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QGraphicsBlurEffect, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, pyqtSlot, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.CustomWidgets.ButtonNotifier import Worker
from ProjectPrep.CustomWidgets.HUD import HUD
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.layouts.boardNotifier import Worker
from ProjectPrep.layouts.pauseView import pauseView
from ProjectPrep.CustomWidgets.Obstacle import Obstacle

class Boardgame(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        super(Boardgame, self).__init__()
        self.hud = HUD()
        self.obstacles = [Obstacle(100), Obstacle(100)]
        self.viewlist = centralWidget
        self.backgroundItem = QGraphicsPixmapItem()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.initUI()

        self.worker = Worker()
        self.worker.update.connect(self.movepicture)
        self.worker.update.connect(self.moveObstacle)

    def activateThreads(self):

        self.setStartPositions()
        self.worker.start()

    def setStartPositions(self):
        pass # to be implemented

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.tempImg = QPixmap('PNG/background-1.png')
        self.tempImg = self.tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        self.graphicsPixmapItem = QGraphicsPixmapItem(self.tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)

        self.mapContinue = QGraphicsPixmapItem(self.tempImg)
        self.grafickascena.addItem(self.mapContinue)
        self.graphicsPixmapItem.setY(-self.tempImg.height())

        self.grafickascena.addItem(self.obstacles[0])
        self.grafickascena.addItem(self.obstacles[1])

        self.grafickascena.addWidget(self.hud).setY(self.grafickascena.height() - self.hud.height())

        self.pauseButton = StyleButton('PNG/Main_UI/Pause_BTN.png', 'Play', 40, 40)
        self.pauseButton.clicked.connect(self.pauseButtonClick)
        self.pauseButton.move(self.grafickascena.width() - 45, 8)
        self.grafickascena.addWidget(self.pauseButton)

        self.setScene(self.grafickascena)

    def pauseButtonClick(self):
        self.pauseview = pauseView(self.viewlist, self.grafickascena.width() / 4, self.grafickascena.height() / 4)
        self.pauseview.move(self.grafickascena.width() / 3, self.grafickascena.height() / 3)
        self.worker.killThread = True
        self.pauseButton.worker.killThread = True
        self.pauseButton.setEnabled(False)
        self.grafickascena.addWidget(self.pauseview)
        self.pauseview.show()
        self.effect = QGraphicsBlurEffect()
        self.setGraphicsEffect(self.effect)

    @pyqtSlot()
    def movepicture(self):
        self.graphicsPixmapItem.moveBy(0, 2)
        res1 = self.graphicsPixmapItem.y() % self.tempImg.height()
        self.mapContinue.setY(res1)

        if self.graphicsPixmapItem.y() == 0:
            self.graphicsPixmapItem.setY(-self.tempImg.height())

    @pyqtSlot()
    def moveObstacle(self):
        for Ob in self.obstacles:
            Ob.moveBy(0, 1)
            if Ob.y() > self.grafickascena.height():

                sansa = random.randint(0, 1) # simulacija coin toss-a. Ako je sansa 0 sakriti prepreku. Ako je jedan prikazati.
                if sansa == 0:
                    Ob.hide()
                else:
                    self.createObstacle(Ob)

    def createObstacle(self, Ob : Obstacle):

        Ob.show()
        x = random.randint(0, self.grafickascena.width())

        Ob.setY(-200)
        Ob.setX(x)
        Ob.setObstaclePix()