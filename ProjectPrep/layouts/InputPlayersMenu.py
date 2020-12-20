from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.CustomWidgets.InputOkvir import InputOkvir
from ProjectPrep.CustomWidgets.CustomButton import StyleButton

addedPlayers = 0
players = {}  # dictionary {"username" : carNumber}

class InputPlayersView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):
        super(InputPlayersView, self).__init__()

        self.viewlist = centralWidget
        self.infoLabel = QLabel()
        self.initUI()

    def initUI(self):
        self.player1 = InputOkvir()
        self.player2 = InputOkvir()
        self.player3 = InputOkvir()
        self.player4 = InputOkvir()

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

        self.setbackground()
        self.playbutton = StyleButton('PNG/Buttons/Play_BTN.png', 'Play', 40, 40)
        self.playbutton.clicked.connect(self.drawBoard)
        self.backbutton = StyleButton('PNG/Buttons/Close_BTN.png', 'Back', 40, 40)
        self.backbutton.clicked.connect(self.backbuttonClick)

        # move(left, top)
        self.player1.move(75, 200)
        self.player2.move(375, 200)
        self.player3.move(675, 200)
        self.player4.move(975, 200)

        self.grafickascena.addWidget(self.playbutton)
        self.grafickascena.addWidget(self.backbutton)
        self.grafickascena.addWidget(self.player1)
        self.grafickascena.addWidget(self.player2)
        self.grafickascena.addWidget(self.player3)
        self.grafickascena.addWidget(self.player4)

        self.infoLabel = QLabel()
        self.infoLabel.move(500, 400)
        self.infoLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.grafickascena.addWidget(self.infoLabel)

        self.playbutton.move(400, 500)
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
        global addedPlayers
        global players
        # check added players
        if self.player1.playerName != '':
            players[self.player1.playerName] = self.player1.Car
            addedPlayers += 1
        if self.player2.playerName != '':
            players[self.player2.playerName] = self.player2.Car
            addedPlayers += 1
        if self.player3.playerName != '':
            players[self.player3.playerName] = self.player3.Car
            addedPlayers += 1
        if self.player4.playerName != '':
            players[self.player4.playerName] = self.player4.Car
            addedPlayers += 1

        if addedPlayers == 0:
            self.infoLabel.setText('Please add at least one player.')
            self.infoLabel.adjustSize()
        else:
            self.viewlist.setCurrentWidget(self.viewlist.widget(3))

    def backbuttonClick(self):
        # back to main menu
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

