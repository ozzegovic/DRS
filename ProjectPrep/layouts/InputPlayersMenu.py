from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.CustomWidgets.InputOkvir import InputOkvir
from ProjectPrep.CustomWidgets.CustomButton import StyleButton



class InputPlayersView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):
        super(InputPlayersView, self).__init__()

        self.viewlist = centralWidget
        self.playerFrames = []  # array of inputOkvir, get inputs from previous view

        # dictionary {"username" : carNumber}
        # dictionary needs to reset so that previously added players wouldn't be kept
        self.players = {}
        self.gametype = 0

        self.infoLabel = QLabel()
        self.initUI()

    def initUI(self):

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.setbackground()
        self.playbutton = StyleButton('PNG/Buttons/Play_BTN.png', 'Play', 40, 40)
        self.playbutton.clicked.connect(self.drawBoard)
        self.backbutton = StyleButton('PNG/Buttons/Close_BTN.png', 'Back', 40, 40)
        self.backbutton.clicked.connect(self.backbuttonClick)

        self.holder = QVBoxLayout()
        self.playersLayout = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        self.titleLabel = QLabel()
        self.titleLabel.setText("ENTER A NAME AND CHOOSE A CAR:")
        self.titleLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.buttonsLayout.addWidget(self.playbutton)
        self.buttonsLayout.addWidget(self.backbutton)
        self.buttonsLayout.setAlignment(Qt.AlignCenter)

        self.infoLabel = QLabel()
        self.infoLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.infoLabel.setAlignment(Qt.AlignCenter)

        self.holder.addWidget(self.titleLabel)
        self.holder.addLayout(self.playersLayout)
        self.holder.addWidget(self.infoLabel)
        self.holder.addLayout(self.buttonsLayout)

        self.setLayout(self.holder)
        self.setScene(self.grafickascena)

    # make a specific amount of input player frames
    def initFrames(self, number, gametype):
        for okvir in self.playerFrames:
            okvir.deleteLater()
        self.playerFrames.clear()

        for i in range(number):
            self.playerFrames.append(InputOkvir(i))

        for okvir in self.playerFrames:
            self.playersLayout.addWidget(okvir)
        self.playersLayout.setAlignment(Qt.AlignCenter)

        self.gametype = gametype

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
        self.validated = True
        # check added players
        # username must be unique and not empty
        for i in range(len(self.playerFrames)):
            if self.playerFrames[i].playerName != '':
                if self.players.get(self.playerFrames[i].playerName) == None:
                    self.players[self.playerFrames[i].playerName] = self.playerFrames[i].Car
                else:
                    # key already exists
                    self.setInfoLabelText(1)
            else:
                self.setInfoLabelText(2)

        if self.validated:
            self.setInfoLabelText(0) # if there was a validation error that is not fixed, delete text from info label
            if self.gametype == 0 or self.gametype == 1: #1v1

                self.boardgame = self.viewlist.widget(2)
                self.boardgame.initPlayers(self.players, self.gametype)
                self.viewlist.setCurrentWidget(self.boardgame)
                # self.tournamentview = self.viewlist.widget(5)
                # self.tournamentview.setPlayers(self.players)

                self.resetPlayers()
            elif self.gametype == 2: #4 players

                self.tournamentview = self.viewlist.widget(5)
                self.tournamentview.setPlayers(self.players)
                self.viewlist.setCurrentWidget(self.viewlist.widget(5))
                self.resetPlayers()

    def setInfoLabelText(self, error):
        if error == 0:
            self.validated = True
            self.infoLabel.setText("")
            self.infoLabel.adjustSize()
        elif error == 1:
            self.resetPlayers()  # reset recnika mora jer se na play proveravaju SVI okviri, cak i oni koji su bili okej - ako je nesto ostalo sto je valjalo sledeci put ne bi proslo
            self.validated = False
            self.infoLabel.setText('All players must have a unique name.')
            self.infoLabel.adjustSize()
        elif error == 2:
            self.resetPlayers()
            self.validated = False
            self.infoLabel.setText('All players must enter a name.')
            self.infoLabel.adjustSize()

    def backbuttonClick(self):
        # if there was an error
        # need to reset players dictionary
        # npr prvi put ime 'player' ce proci i bice ubacen u recnik, sledeci sa istim imenom nece i pojavice se greska u infolabeli
        # ako se ode iz ovog pogleda nazad - bez reseta recnik bi ostao popunjen sa igracima koji su prosli validaciju
        self.setInfoLabelText(0)
        self.resetPlayers()
        # back to input number of players
        if self.gametype == 0:
            self.viewlist.setCurrentWidget(self.viewlist.widget(3))
        else:
            self.viewlist.setCurrentWidget(self.viewlist.widget(0))

    def resetPlayers(self):
        self.players = {}
