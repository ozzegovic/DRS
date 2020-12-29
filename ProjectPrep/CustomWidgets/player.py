from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsColorizeEffect
from ProjectPrep.CustomWidgets.keyNotifier import KeyNotifier
from PyQt5.QtCore import Qt, QTimer

from ProjectPrep.layouts.boardNotifier import Worker
from ProjectPrep.CustomWidgets.Obstacle import Obstacle

class Player(QGraphicsPixmapItem):
    def __init__(self, playerName, playerCar , keybed, width):
        self.playerName = playerName
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
        self.touchesplayer = False


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
                if self.pos().x() + 15 <= 750:
                    self.moveBy(15, 0)
                    self.checkifCollision(key)
            elif key == self.keybed[1]:
                if self.pos().y() + 15 <= 500:
                    self.moveBy(0, 15)
                    self.checkifCollision(key)
            elif key == self.keybed[2]:
                if self.pos().y() + 15 >= 20:
                    self.moveBy(0, -15)
                    self.checkifCollision(key)
            elif key == self.keybed[3]:
                if self.pos().x() + 15 >= 180:
                    self.moveBy(-15, 0)
                    self.checkifCollision(key)

    def checkifCollision(self, key):

        touchedplayer = self.doesitTouch()
        if self.touchesplayer:
            if key == self.keybed[0]:
                self.moveBy(-15, 0)
                touchedplayer.moveBy(30, 0)
            elif key == self.keybed[1]:
                self.moveBy(0, -15)
                touchedplayer.moveBy(0, 30)
            elif key == self.keybed[2]:
                self.moveBy(0, 15)
                touchedplayer.moveBy(0, -30)
            elif key == self.keybed[3]:
                self.moveBy(15, 0)
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
        self.key_notifier.is_done = False
        self.effect.setEnabled(False)
        self.killable = True

    def activateThreads(self):
        self.key_notifier.start()

    def makeUnkillable(self):
        self.killable = False
        self.safeTimer.start(5000)  # After 5 seconds, calls makeKillable.
        self.effect.setEnabled(True)

    def makeKillable(self):
        self.effect.setEnabled(False)
        self.safeTimer.stop()
        self.killable = True
        self.key_notifier.start()


