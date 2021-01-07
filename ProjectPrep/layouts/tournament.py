from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.CustomWidgets.InputOkvir import InputOkvir
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.CustomWidgets.HUDOkvir import HUDOkvir


class TournamentTree(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):
        super(TournamentTree, self).__init__()

        self.viewlist = centralWidget
        self.playerFrames = []  # array of inputOkvir, get inputs from previous view

        # dictionary {"username" : carNumber}
        # dictionary needs to reset so that previously added players wouldn't be kept
        self.players = {}
        self.winner1phase = HUDOkvir('?', 0) # pobednik prve faze
        self.winner2phase = HUDOkvir('?', 0) # pobednik druge faze
        self.winner = HUDOkvir('?', 0) # pobednik trece faze(definitivni pobednik turnira.)
        self.phase = 0
        self.players = {}

        self.infoLabel = QLabel()
        self.initUI()

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.setbackground()
        self.backbutton = StyleButton('PNG/Buttons/Close_BTN.png', 'Back', 40, 40)
        self.backbutton.clicked.connect(self.backbuttonClick)

        self.holder = QVBoxLayout()
        self.playerslayout3 = QHBoxLayout()
        self.playerslayout2 = QHBoxLayout()
        self.playerslayout1 = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        self.titleLabel = QLabel()
        self.titleLabel.setText("ENTER A NAME AND CHOOSE A CAR:")
        self.titleLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.playerslayout2.addWidget(self.winner1phase)
        self.playerslayout2.addWidget(self.winner2phase)
        self.playerslayout1.addWidget(self.winner)

        self.playerslayout2.setAlignment(Qt.AlignHCenter)
        self.playerslayout1.setAlignment(Qt.AlignHCenter)

        self.buttonsLayout.addWidget(self.backbutton)
        self.buttonsLayout.setAlignment(Qt.AlignCenter)

        self.holder.addWidget(self.titleLabel)
        self.holder.addLayout(self.playerslayout1)
        self.holder.addLayout(self.playerslayout2)
        self.holder.addLayout(self.playerslayout3)
        self.holder.addLayout(self.buttonsLayout)

        self.setLayout(self.holder)
        self.setScene(self.grafickascena)

    # make a specific amount of input player frames
    def setPlayers(self, playersdict):
        for i in range(self.playerslayout3.count()):
            okvir = self.playerslayout3.itemAt(i).widget()
            okvir.deleteLater()

        for player in playersdict: # dictionary playerName : car
            self.playerslayout3.addWidget(HUDOkvir(player, playersdict[player]))

        self.playerslayout3.setAlignment(Qt.AlignHCenter)

        self.players = playersdict
        self.resetWinners()

    def resetWinners(self):
        self.phase = 0
        self.winner1phase.setNameAndCar('?', '0')
        self.winner2phase.setNameAndCar('?', '0')
        self.winner.setNameAndCar('?', '0')

    def initNextPhase(self):

        self.phase += 1
        # ovom metodom se poziva boardgame sa igracima koji igraju tu sledecu fazu.

    def setPhaseWinner(self, winner):
        pass
        # ovoj metodi boardgame prosledjuje pobednika faze. Kako vec imamo gore
        # napravljene objekte winner1phase, winner2phase, winner kada dobijemo
        # pobednika neke faze, u tim winerima setujemo samo sliku i name,
        # novom metodom HUDOkvir-a setNameAndCar()
        # Na primer: self.winner1phase.setNameAndCar('Neko ime', "1")
        # Primetiti da je drugi parametar string, posto je u klasi player promenljiva self.Car takodje str.


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

    def backbuttonClick(self):
        # back to input number of players
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

    def resetPlayers(self):
        self.players = {}
