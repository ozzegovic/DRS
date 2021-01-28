from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.CustomWidgets.InputOkvir import InputOkvir
from ProjectPrep.networking.ClientClass import NetworkClientCode

class ConnectRoom(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        self.isFullScreen = False
        super(ConnectRoom, self).__init__()
        self.inputFrame = InputOkvir(1)
        self.viewlist = centralWidget
        self.client = None
        self.connected = False
        self.initUI()

    def initUI(self):

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.setbackground()
        self.backbutton = StyleButton('PNG/Buttons/Close_BTN.png', 'Back', 40, 40)
        self.backbutton.clicked.connect(self.backtomenu)
        self.playbutton = StyleButton('PNG/Buttons/Play_BTN.png', 'Play', 40, 40)
        self.playbutton.clicked.connect(self.play)

        self.holder = QVBoxLayout()
        self.playerLayout = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()
        self.hostLayout = QHBoxLayout()

        self.ipLabel = QLabel()
        self.ipLabel.setText("ENTER HOST ADDRESS: ")
        self.ipLabel.setFixedWidth(150)
        self.ipLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')

        self.hostText = QLineEdit()
        self.hostText.setFixedWidth(150)
        self.hostText.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.hostText.setAlignment(Qt.AlignLeft)

        self.hostLayout.addWidget(self.ipLabel)
        self.hostLayout.addWidget(self.hostText)
        self.hostLayout.setAlignment(Qt.AlignJustify)

        self.titleLabel = QLabel()
        self.titleLabel.setText("ENTER A NAME AND CHOOSE A CAR:")
        self.titleLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.playerLayout.addWidget(self.inputFrame)

        self.buttonsLayout.addWidget(self.playbutton)
        self.buttonsLayout.addWidget(self.backbutton)
        self.buttonsLayout.setAlignment(Qt.AlignCenter)

        self.infoLabel = QLabel() # moze da se doda kasnije ako bude neka greska, npr server posalje da je vec je poslao neko taj username, da ne moze da se konektuje itd
        self.infoLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.infoLabel.setAlignment(Qt.AlignCenter)

        self.holder.addLayout(self.hostLayout)
        self.holder.addWidget(self.titleLabel)
        self.holder.addLayout(self.playerLayout)
        self.holder.addWidget(self.infoLabel)
        self.holder.addLayout(self.buttonsLayout)

        self.setLayout(self.holder)
        self.setScene(self.grafickascena)

    @pyqtSlot(dict)
    def setGameDictionary(self, players):
        pass
        self.boardgame = self.viewlist.widget(2)
        self.boardgame.initPlayers(players, 3, self.client)
        self.client.updateobstacles.connect(self.boardgame.networkSetObstacles)
        self.viewlist.setCurrentWidget(self.boardgame)

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
        self.setInfoLabelText(0)
        if self.client is not None:
            self.client.disconnect()
        self.connected = False
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

    def play(self):
        self.resetLabelStyle()
        if self.connected == True:
            return
        self.client = NetworkClientCode()
        self.client.host = self.hostText.text() # get input address
        print(self.hostText.text())
        self.client.signal.connect(self.setGameDictionary)
        board = self.viewlist.widget(2)
        self.client.updateposition.connect(board.networkPlayerPosition)
        self.connected = self.client.setnameandCar(self, self.inputFrame.playerName, self.inputFrame.Car)
        #self.client.sendSignUpMessage()

    def setInfoLabelText(self, error):
        if error == 0:
            self.infoLabel.setText("")
            self.hostText.setText("")
            self.resetLabelStyle()

        elif error == 1:
            self.hostText.setStyleSheet('color: yellow; font-weight: bold; background: transparent; border: 3px solid red;')
            self.infoLabel.setText("Cannot connect to host. Check input fields.")
            self.infoLabel.adjustSize()
        elif error == 2:
            self.hostText.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
            self.infoLabel.setText("Connected. Waiting...")
            self.infoLabel.adjustSize()
        elif error == 3:
            self.inputFrame.playerNameEdit.setStyleSheet('color: yellow; font-weight: bold; background: transparent; border: 3px solid red;')
            self.infoLabel.setText("Cannot connect to host. Check input fields.")
            self.infoLabel.adjustSize()

    def resetLabelStyle(self):
            self.hostText.setStyleSheet(
                'color: yellow; font-weight: bold; background: transparent;')
            self.inputFrame.playerNameEdit.setStyleSheet(
                'color: yellow; font-weight: bold; background: transparent;')
            self.infoLabel.adjustSize()