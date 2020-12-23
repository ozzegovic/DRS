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

        num = random.randint(1, 7)
        if num == 1:
            self.picture = QPixmap('PNG/Decor/Bush.png')
        if num == 2:
            self.picture = QPixmap('PNG/Decor/Rock.png')
        if num == 3:
            self.picture = QPixmap('PNG/Decor/Tree.png')
        if num == 4:
            self.picture = QPixmap('PNG/Game_Props_Items/Barrel_01.png')
        if num == 5:
            self.picture = QPixmap('PNG/Game_Props_Items/Jumping_Pad_02.png')
        if num == 6:
            self.picture = QPixmap('PNG/Game_Props_Items/Oil.png')
        if num == 7:
            self.picture = QPixmap('PNG/Game_Bonus_Items/HP_Bonus.png')

        self.setPixmap(self.picture.scaledToWidth(self.width))

