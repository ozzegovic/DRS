import random
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QGraphicsBlurEffect, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, pyqtSlot, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5 import QtCore

from ProjectPrep.CustomWidgets.HUD import HUD
from ProjectPrep.CustomWidgets.player import Player
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.layouts.boardNotifier import Worker
from ProjectPrep.layouts.pauseView import pauseView
from ProjectPrep.CustomWidgets.Obstacle import Obstacle

class Boardgame(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        super(Boardgame, self).__init__()
        self.hud = HUD()
        self.obstacles = [Obstacle(100), Obstacle(100),Obstacle(100), Obstacle(100)]
        self.previous = 0  #obstacle
        self.viewlist = centralWidget
        self.winnerCar = ""
        self.winnerName = ""
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.keybed1 = [Qt.Key_Right, Qt.Key_Down, Qt.Key_Up, Qt.Key_Left]
        self.keybed2 = [Qt.Key_D, Qt.Key_S, Qt.Key_W, Qt.Key_A]
        self.keybed3 = [Qt.Key_L, Qt.Key_K, Qt.Key_I, Qt.Key_J]
        self.keybed4 = [Qt.Key_6, Qt.Key_5, Qt.Key_8, Qt.Key_4]
        self.keybeds = [self.keybed1, self.keybed2, self.keybed3, self.keybed4]
        self.initUI()
        self.gametype = 0
        self.networkcode = None

        #timer
        self.level = 1
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.speedUp)

        self.players = []  # moving cars
        self.deaths = [0, 0, 0, 0] #number of deaths per player

        self.worker = Worker(10)
        self.worker.update.connect(self.movepicture)

        #self.obstaclethread = Worker(0.01)
        self.worker.update.connect(self.moveObstacle)

        self.collisionNotifier = Worker(100)
        self.collisionNotifier.update.connect(self.checkCollision)

        # 1. step - set one transition image - self.graphicsPixmapItem set to transition image
        # 2. step - set transition image on one and new image on the other (the one that previously had the transition image)
        # self.graphicsPixmapItem - new level image
        # self.mapcontiniue - transition image
        # 3. step - set the new image on the one that previously had the transition image
        # self.mapcontinue - new level image

        self.phaseIndex = -1
        self.nextBackground = 1

    def activateThreads(self):
        self.worker.start() # resume option, not reseting obstacle position
        self.collisionNotifier.start()
        self.activatePlayerThreads()  # for each player start key notifier thread
        self.timer.start(5000)

    def stopThreads(self):
        self.worker.stop()
        self.collisionNotifier.stop()
        self.stopPlayerThreads()    # for each player stop key notifier thread
        self.timer.stop()

    def setStartPositions(self):
        for obsticale in self.obstacles:
            self.createObstacle(obsticale)

    def restart(self):
        self.setStartPositions() # reset option, resets all the positions and starts the thread again
        self.playerStartPositions(self.players)
        self.playerStartLives(self.players)
        self.hud.restart()
        self.hud.initHudFrames(self.players)
        self.playerStartLivesHud()
        self.resetBackground()
        self.activateThreads()
        self.level = 1
        self.deaths = [0, 0]

    def playerStartPositions(self, players):
        self.widthPosition = 550 / (1 + len(players))
        self.padding = 0
        for i in range(len(players)):
            self.players[i].setPos(150 + self.widthPosition + self.widthPosition * i + self.padding * i, 500)
            self.padding = 50

    def playerStartLives(self, players):
        for player in players:
            player.resetLives()

    # reset hearts shown in the hud frame for each player
    def playerStartLivesHud(self):
        for player in self.players:
            self.hud.updatePlayerLives(player)

    def stopPlayerThreads(self):
        for player in self.players:
            player.stopThread()

    # key notifier threads # question
    def activatePlayerThreads(self):
        for player in self.players:
            player.activateThreads()

    # add players to the boardgame
    def initPlayers(self, players, gametype, networkCode=None):
        self.players.clear()
        self.networkcode = networkCode

        self.i = 0
        for player in players:
            # players dictionary: key(player) - playerName, value(players[player]) - playerCar
            if gametype != 3:
                self.player = Player(player, str(players[player]), self.keybeds[self.i], self.grafickascena.width() / 15)
            else:
                self.player = Player(player, str(players[player]), self.keybeds[0], self.grafickascena.width() / 15)
            self.player.setNetworkCode(self.networkcode)
            self.players.append(self.player)
            self.grafickascena.addItem(self.player)
            self.i = self.i + 1
        self.restart()

        # init hud frame with array of Player objects
        self.hud.initHudFrames(self.players)
        if gametype == 1:# 1v1 turnir
            self.hud.setMode(1)

        self.gametype = gametype

    # remove each car from the graphics scene, stop all threads, delete players list
    def deletePlayers(self):
        for player in self.players:
            self.grafickascena.removeItem(player)

        self.stopThreads()
        self.players = []
        self.deaths = [0, 0]

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.tempImg = QPixmap('PNG/background/road0.png')
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
        self.level += 1
        if self.level % 4 == 0:
            self.setNextBackgroundPath()
            self.phaseIndex = 0
        self.hud.updateHUD()

    def resetBackground(self):
        self.phaseIndex = -1
        self.nextBackground = 1
        self.startBackground = QPixmap("PNG/Background/road0")
        self.startBackground = self.startBackground.scaled(self.grafickascena.width(),self.grafickascena.height())
        self.graphicsPixmapItem.setPixmap(self.startBackground)
        self.mapContinue.setPixmap(self.startBackground)

    def setNextBackgroundPath(self):
        self.pathNext = "PNG/Background/road" + str(self.nextBackground%5)
        self.pathTransition = "PNG/Background/road" + str((self.nextBackground - 1) % 5) + str(self.nextBackground % 5)
        self.nextBackground = self.nextBackground + 1

    def startBackgroundTransition(self):
        self.graphicsPixmapItem.setPixmap(
            QPixmap(self.pathTransition).scaled(self.grafickascena.width(), self.grafickascena.height()))
        self.phaseIndex = 1

    def middleBackgroundTransition(self):
        self.mapContinue.setPixmap(
            QPixmap(self.pathTransition).scaled(self.grafickascena.width(), self.grafickascena.height()))
        self.graphicsPixmapItem.setPixmap(
            QPixmap(self.pathNext).scaled(self.grafickascena.width(), self.grafickascena.height()))
        self.phaseIndex = 2

    def completeBackgroundTransition(self):
        self.mapContinue.setPixmap(
            QPixmap(self.pathNext).scaled(self.grafickascena.width(), self.grafickascena.height()))
        self.phaseIndex = -1

    @pyqtSlot()
    def movepicture(self):
        self.graphicsPixmapItem.moveBy(0, 2 + self.level * 0.2)
        res1 = self.graphicsPixmapItem.y() % self.tempImg.height()
        self.mapContinue.setY(res1)

        if self.graphicsPixmapItem.y() >= 0:
            if self.phaseIndex != -1:
                if self.phaseIndex == 0:
                    self.startBackgroundTransition()
                elif self.phaseIndex == 1:
                    self.middleBackgroundTransition()
                elif self.phaseIndex == 2:
                    self.completeBackgroundTransition()

            self.graphicsPixmapItem.setY(-self.tempImg.height())

    @pyqtSlot()
    def moveObstacle(self):

        for Ob in self.obstacles:
            Ob.moveBy(0, 2 + self.level * 0.2)
            if Ob.y() > (self.grafickascena.height()-200):
                self.createObstacle(Ob)

    def createObstacle(self, Ob : Obstacle):

        x = random.randint(170, 720)
        y = random.randint(-self.grafickascena.height(), - 100)

        #while (x>(self.previous-100)) & (x<(self.previous+100)):
        ##    x = random.randint(300, 700)
        #self.previous = x
        Ob.setY(y)
        Ob.setX(x)
        Ob.setObstaclePix()
        sansa = random.randint(0,100)  # simulacija coin toss-a. Ako je sansa 0 sakriti prepreku. Ako je jedan prikazati.
        # prvih nekoliko prepreka se pojavljuje na pocetku nezavisno od sanse?

        if self.level < 7:
            if sansa > self.level * 10:
                Ob.hide()
            else:
                Ob.show()
        else:
            if sansa > 70:
                Ob.hide()
            else:
                Ob.show()

    @pyqtSlot(int, int, int, int, bool)
    def networkSetObstacles(self, index, x, y, type, visible):
        pass # TODO

    @pyqtSlot(str, float, float, int)
    def networkPlayerPosition(self, name, x, y, keyindex):
        pass # TODO

    def keyPressEvent(self, event) -> None:
        if event.key() in self.keybed1:
            self.players[0].keyPressEvent(event)

        if len(self.players) >= 2:
            if event.key() in self.keybed2:
                self.players[1].keyPressEvent(event)
        if len(self.players) >= 3:
            if event.key() in self.keybed3:
                self.players[2].keyPressEvent(event)
        if len(self.players) >= 4:
            if event.key() in self.keybed4:
                self.players[3].keyPressEvent(event)

    def keyReleaseEvent(self, event) -> None:
        if event.key() in self.keybed1:
            self.players[0].keyReleaseEvent(event)

        if len(self.players) >= 2:
            if event.key() in self.keybed2:
                self.players[1].keyReleaseEvent(event)
        if len(self.players) >= 3:
            if event.key() in self.keybed3:
                self.players[2].keyReleaseEvent(event)
        if len(self.players) >= 4:
            if event.key() in self.keybed4:
                self.players[3].keyReleaseEvent(event)

    @pyqtSlot()
    def checkCollision(self):

        for player in self.players:
            for item in player.collidingItems():
                if isinstance(item, Obstacle):
                    if player.killable:
                        if item.id == 0:
                            player.die()
                            self.hud.updatePlayerLives(player)
                            self.checkAlivePlayers(player.playerName,player.Car)
                            self.setPlayerPosition(player)

                            if self.gametype == 1:  # 1v1
                                index = self.players.index(player)
                                self.deaths[index] = self.deaths[index] + 1
                                self.hud.setHUDResult(self.deaths[0], self.deaths[1])
                                opindex = 1 - index  # Opposite index 1 - 0 = 1, 1 - 1 = 0.

                                if (self.deaths[index] == 2 and self.deaths[opindex] == 0) or self.deaths[index] == 3:
                                    self.setTournamentWinner(self.players[opindex])
                                    # self.drawTournamentTree(self.players[0])
                                    self.deletePlayers()
                            # 4 man tournament
                            elif self.gametype == 2:
                                index = self.players.index(player)
                                opindex = 1 - index

                                if self.players[index].getLives() == 0:
                                    # self.setTournamentWinner(self.players[0])
                                    self.drawTournamentTree(self.players[opindex])
                                    self.deletePlayers()

                        elif item.id == 1:
                            player.disableMoving()
                        elif item.id == 2:
                            item.hide()  # if not hidden it would add lives as long as the car is still colliding with it, other players could get it as well
                            player.addLife()
                            self.hud.updatePlayerLives(player)

    def drawTournamentTree(self, player):
        self.stopThreads()
        self.tree = self.viewlist.widget(5)
        self.winnerName, self.winnerCar = player.getNameCar()
        self.tree.setPhaseWinner(self.winnerName, self.winnerCar)
        self.viewlist.setCurrentWidget(self.tree)

    def setTournamentWinner(self, player):
        self.stopThreads()
        self.winner = self.viewlist.widget(6)
        self.winnerName, self.winnerCar = player.getNameCar()
        self.winner.lastPlayer(self.winnerName, self.winnerCar)
        self.viewlist.setCurrentWidget(self.winner)

    # position the player on the original starting position
    def setPlayerPosition(self, player):
        self.widthPosition = 550 / (1 + len(self.players))
        self.padding = 50
        for i in range(len(self.players)):
            if player == self.players[i]:
                self.players[i].setPos(150 + self.widthPosition + self.widthPosition * i + self.padding * i, 500)

    def checkAlivePlayers(self,playerName,playerCar):
        anyAlive = False
        for player in self.players:
            if player.lives != 0:
                anyAlive = True

        if anyAlive == False:
                self.View = self.viewlist.widget(6)
                self.View.lastPlayer(playerName,playerCar)
                self.stopThreads()
                self.viewlist.setCurrentWidget(self.View)

