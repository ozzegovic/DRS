from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView

class SettingsView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        super(SettingsView, self).__init__()

        self.viewlist = centralWidget
        self.initUI()

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

        self.setbackground()
        self.backbtn = QPushButton('Back')
        self.backbtn.clicked.connect(self.backtomenu)

        self.grafickascena.addWidget(self.backbtn)

        self.backbtn.move(500, 500)

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

        self.graphicsPixmapItem = QGraphicsPixmapItem(new_pix)
        self.grafickascena.addItem(self.graphicsPixmapItem)

    def backtomenu(self):
        pass
