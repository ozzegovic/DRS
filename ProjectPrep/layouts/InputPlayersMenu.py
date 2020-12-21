from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.CustomWidgets.InputOkvir import InputOkvir
from ProjectPrep.CustomWidgets.CustomButton import StyleButton


players = {}  # dictionary {"username" : carNumber}


class InputPlayersView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget, number):
        super(InputPlayersView, self).__init__()

        self.viewlist = centralWidget
        self.players = []  # array of inputOkvir, get inputs from previous view
        self.infoLabel = QLabel()
        self.initUI(number)

    def initUI(self, number):

        for i in range(number):
            self.players.append(InputOkvir(i))

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

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

        for i in range(number):
            self.playersLayout.addWidget(self.players[i])
        self.playersLayout.setAlignment(Qt.AlignCenter)

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
        for i in range(len(self.players)):
            if self.players[i].playerName != '':
                global players
                if players.get(self.players[i].playerName) == None:
                    players[self.players[i].playerName] = self.players[i].Car
                else:
                    # key already exists
                    self.validated = False
            else:
                self.validated = False

        if self.validated == False:
            self.infoLabel.setText('All players must have a unique name.')
            self.infoLabel.adjustSize()
        else:
            self.viewlist.setCurrentWidget(self.viewlist.widget(2))

    def backbuttonClick(self):
        #remove created widget
        self.viewlist.removeWidget(self.viewlist.widget(4))
        # back to input number of players
        self.viewlist.setCurrentWidget(self.viewlist.widget(3))

