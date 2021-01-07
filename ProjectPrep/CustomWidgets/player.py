from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsColorizeEffect
from ProjectPrep.CustomWidgets.keyNotifier import KeyNotifier
from PyQt5.QtCore import Qt, QTimer

from ProjectPrep.layouts.boardNotifier import Worker
from ProjectPrep.CustomWidgets.Obstacle import Obstacle

class Player(QGraphicsPixmapItem):
    def __init__(self, playerName, playerCar , keybed, width, car):
        self.playerName = playerName
        self.playerCar = playerCar
        self.Car=car
        self.qpix = QPixmap(playerCar)
        self.qpix = self.qpix.scaled(width, width * 1.5)
        self.keybed = keybed
        super(Player, self).__init__(self.qpix)
        self.lives = 3

        self.effect = QGraphicsColorizeEffect()
        self.effect.setColor(QColor(189, 189, 189))
        self.effect.setStrength(0.5)
        self.effect.setEnabled(False)
        self.setGraphicsEffect(self.effect)

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.movePlayer)

        self.safeTimer = QTimer()
        self.safeTimer.timeout.connect(self.makeKillable)
        self.killable = True
        self.safeTimerRemaining = 0
        self.touchesplayer = False

        self.notMoving = QTimer()
        self.notMoving.timeout.connect(self.enableMoving)
        self.canMove = True
        self.notMovingRemaining = 0

    def die(self):
        if self.killable == True:
            self.lives = self.lives - 1
            print("Player: {}, Lives: {}".format(self.playerName, self.lives))
            if self.lives == 0:
                self.key_notifier.die()
                self.killable = False  # died three times already, no need to count lives anymore
            else:
                self.makeUnkillable() # calls timer

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())

    def movePlayer(self, key):
        # if it's not killable, means player died and cannot move
        if self.killable == True:
            if key == self.keybed[0]:
                if self.pos().x() + 15 <= 790:
                    self.moveBy(15, 0)
                    self.checkifCollision(key)
            elif key == self.keybed[1]:
                if self.pos().y() + 15 <= 530:
                    self.moveBy(0, 15)
                    self.checkifCollision(key)
            elif key == self.keybed[2]:
                if self.pos().y() - 15 >= 0:
                    self.moveBy(0, -15)
                    self.checkifCollision(key)
            elif key == self.keybed[3]:
                if self.pos().x() - 15 >= 150:
                    self.moveBy(-15, 0)
                    self.checkifCollision(key)

    def checkifCollision(self, key):

        touchedplayer = self.doesitTouch()
        if self.touchesplayer:
            if key == self.keybed[0]:
                self.moveBy(-15, 0)
                if touchedplayer.pos().x() + 30 <= 790:
                    touchedplayer.moveBy(30, 0)
            elif key == self.keybed[1]:
                self.moveBy(0, -15)
                if touchedplayer.pos().y() + 30 <= 530:
                    touchedplayer.moveBy(0, 30)
            elif key == self.keybed[2]:
                self.moveBy(0, 15)
                if touchedplayer.pos().y() - 30 >= 0:
                    touchedplayer.moveBy(0, -30)
            elif key == self.keybed[3]:
                self.moveBy(15, 0)
                if touchedplayer.pos().x() - 30 >= 150:
                    touchedplayer.moveBy(-30, 0)

    def doesitTouch(self):

        collidingPlayers = list(filter(lambda x: isinstance(x, Player), self.collidingItems()))
        if len(collidingPlayers) != 0:
            self.touchesplayer = True
            return collidingPlayers[0]
        else:
            self.touchesplayer = False

    def resetLives(self):
        self.lives = 3
        self.effect.setEnabled(False)
        self.killable = True
        self.canMove = True
        self.safeTimerRemaining = 0
        self.notMovingRemaining = 0

    def activateThreads(self):
        if self.safeTimerRemaining != 0:
            self.safeTimer.start(self.safeTimerRemaining)   # resuming timers
            self.safeTimerRemaining = 0
        if self.notMovingRemaining != 0:
            self.notMoving.start(self.notMovingRemaining)
            self.notMoving = 0
        if self.killable and self.canMove:
            self.key_notifier.start()

    def stopThread(self):
        if self.safeTimer.isActive():
            self.safeTimerRemaining = self.safeTimer.remainingTime()    #pausing timers
            self.safeTimer.stop()

        if self.notMoving.isActive():
            self.notMovingRemaining = self.notMoving.remainingTime()
            self.notMoving.stop()

        self.key_notifier.die()

    def makeUnkillable(self):
        self.killable = False
        self.safeTimer.start(5000)  # After 5 seconds, calls makeKillable.
        self.effect.setEnabled(True)

    def makeKillable(self):
        self.effect.setEnabled(False)
        self.safeTimer.stop()
        self.killable = True
        self.key_notifier.start()

    def addLife(self):
        self.lives += 1
        print("Player: {}, Lives: {}".format(self.playerName, self.lives))

    def disableMoving(self):
        self.key_notifier.die()
        self.canMove = False
        self.notMoving.start(2000)

    def enableMoving(self):
        self.notMoving.stop()
        self.canMove = True
        if self.killable:
            self.key_notifier.start()   # if didn't lose a life while unable to move, enable moving
                                        # if died while unable to move, makeKillable will enable moving after the safe timer expires

