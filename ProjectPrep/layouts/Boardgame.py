import random
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QGraphicsBlurEffect, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, pyqtSlot, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5 import QtCore

from ProjectPrep.CustomWidgets.ButtonNotifier import Worker
from ProjectPrep.CustomWidgets.HUD import HUD
from ProjectPrep.CustomWidgets.player import Player
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.layouts.boardNotifier import Worker
from ProjectPrep.layouts.pauseView import pauseView
from ProjectPrep.CustomWidgets.Obstacle import Obstacle
from ProjectPrep.CustomWidgets.collisionNotifier import CollisionNotifier

class Boardgame(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        super(Boardgame, self).__init__()
        self.hud = HUD()
        self.obstacles = [Obstacle(100), Obstacle(100),Obstacle(100), Obstacle(100)]
        self.previous = 0  #obstacle
        self.viewlist = centralWidget
        #self.backgroundItem = QGraphicsPixmapItem()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.keybed1 = [Qt.Key_Right, Qt.Key_Down, Qt.Key_Up, Qt.Key_Left]
        self.keybed2 = [Qt.Key_D, Qt.Key_S, Qt.Key_W, Qt.Key_A]
        self.keybeds = [self.keybed1, self.keybed2]
        self.initUI()

        #timer
        self.level = 1
        self.cntSecs = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.speedUp)
        self.pauseTimer = False

        self.players = []  # moving cars

        self.worker = Worker(0.01)
        self.worker.update.connect(self.movepicture)
        self.worker.update.connect(self.moveObstacle)

        self.collisionNotifier = Worker(0.01)
        self.collisionNotifier.update.connect(self.checkCollision)


    def activateThreads(self):
        self.worker.start() # resume option, not reseting obstacle position
        self.collisionNotifier.start()
        self.activatePlayerThreads()  # for each player start key notifier thread
        self.timer.start(20000) # svakih 20 sekundi ce se pozivati self.speedUp, nije potrebna counter promenljiva.

    def stopThreads(self):
        self.worker.stop()
        self.collisionNotifier.stop()
        self.stopPlayerThreads()    # for each player stop key notifier thread
        self.timer.stop()

    def setStartPositions(self):
        self.obstacles[0].setY(-200)
        self.obstacles[0].setX(170)
        self.obstacles[1].setY(-200)
        self.obstacles[1].setX(500)
        self.obstacles[2].setY(-600)
        self.obstacles[2].setX(400)
        self.obstacles[3].setY(-600)
        self.obstacles[3].setX(720)

    def restart(self):
        self.setStartPositions() # reset option, resets all the positions and starts the thread again
        self.playerStartPositions(self.players)
        self.playerStartLives(self.players)
        self.activateThreads()

    def playerStartPositions(self, players):
        self.widthPosition = 550 / (1 + len(players))
        self.padding = 0
        for i in range(len(players)):
            self.players[i].setPos(150 + self.widthPosition + self.widthPosition * i + self.padding * i, 500)
            self.padding = 50

    def playerStartLives(self, players):
        for player in players:
            player.resetLives()

    def stopPlayerThreads(self):
        for player in self.players:
            player.stopThread()

    # key notifier threads # question
    def activatePlayerThreads(self):
        for player in self.players:
            player.activateThreads()

    # add players to the boardgame
    def initPlayers(self, players):
        self.players.clear()
        self.i = 0
        for player in players:
            # players dicttionary: key(player) - playerName, value(players[player]) - playerCar
            self.player = Player(player, ('PNG/Car_' + str(players[player]) + '_Main_Positions/Car_' + str(players[player]) + '_01'), self.keybeds[self.i], self.grafickascena.width() / 15)
            self.players.append(self.player)
            self.grafickascena.addItem(self.player)
            self.i = + 1
        self.playerStartPositions(self.players)

    def deletePlayers(self):
        for player in self.players:
            player.key_notifier.isDone = True
            self.collisionNotifier.killThread = True
            self.grafickascena.removeItem(player)

        self.players = []

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
        self.grafickascena.addItem(self.obstacles[2])
        self.grafickascena.addItem(self.obstacles[3])

        #self.setStartPositions() #restart se zove na play button click pa ne treba ovde

        self.grafickascena.addWidget(self.hud).setY(self.grafickascena.height() - self.hud.height())

        self.pauseButton = StyleButton('PNG/Main_UI/Pause_BTN.png', 'Play', 40, 40)
        self.pauseButton.clicked.connect(self.pauseButtonClick)
        self.pauseButton.move(self.grafickascena.width() - 45, 8)
        self.grafickascena.addWidget(self.pauseButton)

        self.setScene(self.grafickascena)

    def pauseButtonClick(self):
        self.pauseview = pauseView(self.viewlist, self.grafickascena.width() / 4, self.grafickascena.height() / 4)
        self.pauseview.move(self.grafickascena.width() / 3, self.grafickascena.height() / 3)
        self.pauseButton.worker.killThread = True
        self.pauseButton.setEnabled(False)
        self.grafickascena.addWidget(self.pauseview)
        self.pauseview.show()
        self.stopThreads()

    def speedUp(self):
        self.hud.updateHUD()
        self.worker.decreaseperiod(0.001)

    @pyqtSlot()
    def movepicture(self):
        self.graphicsPixmapItem.moveBy(0, self.level*0.7*2+1)
        res1 = self.graphicsPixmapItem.y() % self.tempImg.height()
        self.mapContinue.setY(res1)

        if self.graphicsPixmapItem.y() >= 0:
            self.graphicsPixmapItem.setY(-self.tempImg.height())

    @pyqtSlot()
    def moveObstacle(self):

        for Ob in self.obstacles:
            Ob.moveBy(0, self.level*0.7*2+1)
            if Ob.y() > (self.grafickascena.height()-200):
                    self.createObstacle(Ob)

    def createObstacle(self, Ob : Obstacle):

        x = random.randint(170, 720)
        while (x>(self.previous-100)) & (x<(self.previous+100)):
            x = random.randint(300, 700)
        self.previous = x
        Ob.setY(-150)
        Ob.setX(x)
        Ob.setObstaclePix()
        sansa = random.randint(0, 100)  # simulacija coin toss-a. Ako je sansa 0 sakriti prepreku. Ako je jedan prikazati.
        #prvih nekoliko prepreka se pojavljuje na pocetku nezavisno od sanse?

        if self.level < 7:
            if sansa > self.level*10:
                Ob.hide()
            else:
                Ob.show()
        else:
            if sansa > 70:
                Ob.hide()
            else:
                Ob.show()

    def keyPressEvent(self, event) -> None:
        if event.key() in self.keybed1:
            self.players[0].keyPressEvent(event)

        if len(self.players) >= 2:
            if event.key() in self.keybed2:
                self.players[1].keyPressEvent(event)

    def keyReleaseEvent(self, event) -> None:
        if event.key() in self.keybed1:
            self.players[0].keyReleaseEvent(event)

        if len(self.players) >= 2:
            if event.key() in self.keybed2:
                self.players[1].keyReleaseEvent(event)

    @pyqtSlot()
    def checkCollision(self):
        for player in self.players:
            if len(player.collidingItems()) != 0:
                for item in player.collidingItems():
                    if isinstance(item, Obstacle):
                        if player.killable == True:
                            player.die()
                            self.setPlayerPosition(player)

    # position the player on the original starting position
    def setPlayerPosition(self, player):
        self.widthPosition = 550 / (1 + len(self.players))
        self.padding = 50
        for i in range(len(self.players)):
            if player == self.players[i]:
                self.players[i].setPos(150 + self.widthPosition + self.widthPosition * i + self.padding * i, 500)
