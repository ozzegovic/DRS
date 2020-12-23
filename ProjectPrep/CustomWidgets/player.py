from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from ProjectPrep.CustomWidgets.keyNotifier import KeyNotifier
from PyQt5.QtCore import Qt

from ProjectPrep.layouts.boardNotifier import Worker
from ProjectPrep.CustomWidgets.Obstacle import Obstacle

class Player(QGraphicsPixmapItem):
    def __init__(self, image):
        self.qpix = QPixmap(image)
        self.qpix = self.qpix.scaled(130, 100)
        super(Player, self).__init__(self.qpix)
        self.lives = 3

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.movePlayer)
        self.key_notifier.start()

        self.worker = Worker()
        self.worker.update.connect(self.checkCollision)
        self.worker.start()


    def die(self):
        self.lives = self.lives - 1
        print("ostalo jos {} zivota".format(self.lives))
        if self.lives == 0:
            self.key_notifier.die()
            self.worker.killThread = True
            return True
        else:
            return False

    def keyPressEvent(self, event):
        self.key_notifier.add_key(event.key())

    def keyReleaseEvent(self, event):
        self.key_notifier.rem_key(event.key())

    def movePlayer(self, key):
        print(key)
        if key == Qt.Key_Down:
            self.moveBy(0, 15)
        elif key == Qt.Key_Right:
            self.moveBy(15, 0)
        elif key == Qt.Key_Up:
            self.moveBy(0, -15)
        elif key == Qt.Key_Left:
            self.moveBy(-15, 0)

    def checkCollision(self):
        if len(self.collidingItems()) != 0:
            for item in self.collidingItems():
                if isinstance(item, Obstacle):
                    self.die()
