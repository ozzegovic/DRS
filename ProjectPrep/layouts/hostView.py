from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap

from ProjectPrep.CustomWidgets.HUDOkvir import HUDOkvir
from ProjectPrep.CustomWidgets.InputOkvir import InputOkvir
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.networking.HostClass import NetworkHost


class HostView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):
        super(HostView, self).__init__()

        self.grafickascena = QGraphicsScene()
        self.viewlist = centralWidget
        self.guestFrames = [HUDOkvir("", ""), HUDOkvir("", ""), HUDOkvir("", "")]  # array of HUDOkvir, get inputs from previous view
        self.gamemode = 0
        self.players = {}
        self.initUI()

    def initUI(self):
        self.titleLabel = QLabel()
        self.titleLabel.setText("ENTER YOUR NAME CHOOSE A CAR AND WAIT FOR PLAYERS TO JOIN")
        self.titleLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.setbackground()
        self.holder = QVBoxLayout()
        self.hostLayout = QHBoxLayout()
        self.guestsLayout = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        self.playbutton = StyleButton('PNG/Buttons/Play_BTN.png', 'Play', 40, 40)
        self.playbutton.clicked.connect(self.startgame)
        self.backbutton = StyleButton('PNG/Buttons/Close_BTN.png', 'Back', 40, 40)
        self.backbutton.clicked.connect(self.backbuttonClick)

        self.buttonsLayout.addWidget(self.playbutton)
        self.buttonsLayout.addWidget(self.backbutton)
        self.buttonsLayout.setAlignment(Qt.AlignCenter)

        self.hostFrame = InputOkvir(0)
        self.hostLayout.addWidget(self.hostFrame)

        for i in range(0, len(self.guestFrames)):
            self.guestsLayout.addWidget(self.guestFrames[i])


        self.holder.addWidget(self.titleLabel)
        self.holder.addLayout(self.hostLayout)
        self.holder.addLayout(self.guestsLayout)
        self.holder.addLayout(self.buttonsLayout)

        self.setLayout(self.holder)

        self.setScene(self.grafickascena)


        #self.addHudOkvir("fgfer", "2")
        #self.chooseType()

    @pyqtSlot(str, str)
    def addHudOkvir(self, name, car):  # kada se igrac konektuje poziva ovo
        # index = len(self.players)
        # self.newPlayerFrame = HUDOkvir(name, car)
        # self.guestFrames.append(self.newPlayerFrame)
        #
        # index = self.guestFrames.index(self.newPlayerFrame)
        # self.guestsLayout.addWidget(self.guestFrames[index])

        if len(self.players) == 0:
            self.guestFrames[0].setNameAndCar(name, car)
        if len(self.players) == 1:
            self.guestFrames[1].setNameAndCar(name, car)
        if len(self.players) == 2:
            self.guestFrames[2].setNameAndCar(name, car)

        self.players[name] = car #ubacuje se u grupu igraca

    def startServerHosting(self):

        self.host = NetworkHost()
        self.host.addPlayerFrameSignal.connect(self.addHudOkvir)
        self.host.starthost()

    # Connect this.
    def setGameDictionary(self, dict):
        self.host.broadcastdictionary(dict)
        self.boardgame = self.viewlist.widget(2)
        self.boardgame.initPlayers(self.players, 3)
        self.viewlist.setCurrentWidget(self.boardgame)

    def setbackground(self):
        tempImg = QPixmap('PNG/9c49087c09fd07a10ae3887a7825f389.jpg')
        tempImg = tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        self.graphicsPixmapItem = QGraphicsPixmapItem(tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)

    def startgame(self):
        if self.hostFrame.playerName != '':
            self.players[self.hostFrame.playerName] = self.hostFrame.Car
            self.setGameDictionary(self.players)

    def backbuttonClick(self):
        # self.closeConnection()
        # for i in range(0, len(self.guestFrames)):
        #     self.guestFrames[i].deleteLater()

        self.resetPlayers()
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

    def resetPlayers(self):
        self.players = {}
        for i in range(0, 3):
            self.guestFrames[i].setNameAndCar("", "")