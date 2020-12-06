from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter


class InputPlayersView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):
        super(InputPlayersView, self).__init__()

        self.viewlist = centralWidget
        self.initUI()

    def initUI(self):
        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

        self.setbackground()
        self.playbutton = QPushButton('Play')
        self.playbutton.clicked.connect(self.drawBoard)
        self.backbutton = QPushButton('Back')

        self.grafickascena.addWidget(self.playbutton)
        self.grafickascena.addWidget(self.backbutton)

        self.playbutton.move(500, 500)
        self.backbutton.move(600, 500)

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

    def drawBoard(self):

        self.viewlist.setCurrentWidget(self.viewlist.widget(3))