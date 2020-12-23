from PyQt5.QtWidgets import QPushButton, QGraphicsScene, QGraphicsView, QGraphicsItem, QLineEdit, QGraphicsPixmapItem, \
    QFrame, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QEvent, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage
import time
import random
from ProjectPrep.CustomWidgets.CustomButton import StyleButton


class Obstacle(QGraphicsPixmapItem):

    def __init__(self, width):
        super().__init__()
        self.width = width

        num = random.randint(1, 3)
        if num == 1:
            self.picture = QPixmap('PNG/Decor/Bush.png')
        if num == 2:
            self.picture = QPixmap('PNG/Decor/Rock.png')
        if num == 3:
            self.picture = QPixmap('PNG/Decor/Tree.png')

        self.setPixmap(self.picture.scaledToWidth(width))

    def setObstaclePix(self):

        num = random.randint(1, 3)
        if num == 1:
            self.picture = QPixmap('PNG/Decor/Bush.png')
        if num == 2:
            self.picture = QPixmap('PNG/Decor/Rock.png')
        if num == 3:
            self.picture = QPixmap('PNG/Decor/Tree.png')

        self.setPixmap(self.picture.scaledToWidth(self.width))
