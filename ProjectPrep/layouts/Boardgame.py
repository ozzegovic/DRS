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


class Boardgame(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        super(Boardgame, self).__init__()
        self.hud = HUD()
        self.viewlist = centralWidget
        self.backgroundItem = QGraphicsPixmapItem()
        self.initUI()

        self.worker = Worker()
        self.worker.update.connect(self.movepicture)
        self.worker.start() # Pokreni ovo na tajmer.

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

        self.tempImg = QPixmap('PNG/background-1.png')
        self.tempImg = self.tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        self.graphicsPixmapItem = QGraphicsPixmapItem(self.tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)

        self.mapContinue = QGraphicsPixmapItem(self.tempImg)
        self.grafickascena.addItem(self.mapContinue)
        self.grafickascena.addWidget(self.hud).moveBy(0, 380)

        self.pauseButton = StyleButton('PNG/Main_UI/Pause_BTN.png', 'Play', 40, 40)
        self.pauseButton.clicked.connect(self.pauseButtonClick)
        self.pauseButton.move(self.grafickascena.width()-45, 8)
        self.grafickascena.addWidget(self.pauseButton)

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
        self.backgroundItem = QGraphicsPixmapItem(new_pix)
        self.grafickascena.addItem(self.backgroundItem)

    def pauseButtonClick(self):
        self.pauseview = pauseView(self.viewlist, self.grafickascena.width()/4, self.grafickascena.height()/4)
        self.pauseview.move(self.grafickascena.width() / 3, self.grafickascena.height() / 3)
        self.worker.killThread = True
        self.pauseButton.setEnabled(False)
        #self.setbackground()
        self.grafickascena.addWidget(self.pauseview)
        self.pauseview.show()

    @pyqtSlot()
    def movepicture(self):
        self.graphicsPixmapItem.moveBy(0, -2)
        res1 = self.graphicsPixmapItem.y() % self.tempImg.height()

        self.mapContinue.setY(res1)

        if self.graphicsPixmapItem.y() == -self.tempImg.height():

            self.graphicsPixmapItem.setY(0)
