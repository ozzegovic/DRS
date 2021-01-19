from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QStackedLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.layouts.hostView import HostView
import  sys


class menuView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        super(menuView, self).__init__()

        self.viewlist = centralWidget
        self.initUI()

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.setbackground()
        self.playbutton = StyleButton('PNG/Buttons/Play_BTN.png', 'Play', 40, 40)
        self.playbutton.clicked.connect(self.playbuttonclick)
        self.tourney2button = StyleButton('PNG/You_Win/Play_Tournament_1.png', '2 Player tournament', 40, 40)
        self.tourney2button.clicked.connect(self.tournament2click)
        self.tourney4button = StyleButton('PNG/You_Win/Play_Tournament_2.png', '4 Player tournament', 40, 40)
        self.tourney4button.clicked.connect(self.tournament4click)
        self.connectroombutton = StyleButton('PNG/Buttons/Play_BTN.png', 'Connect to host', 40, 40)
        self.connectroombutton.clicked.connect(self.connectRoomButtonClick)
        self.hostbutton = StyleButton('PNG/You_Win/Play_BTN.png', 'Host a game', 40, 40)
        self.hostbutton.clicked.connect(self.hostgame)
        self.exitbtn = StyleButton('PNG/Buttons/Close_BTN.png', 'Exit', 40, 40)
        self.exitbtn.clicked.connect(self.closeThis)

        self.grafickascena.addWidget(self.playbutton)
        self.grafickascena.addWidget(self.tourney2button)
        self.grafickascena.addWidget(self.tourney4button)
        self.grafickascena.addWidget(self.hostbutton)
        self.grafickascena.addWidget(self.connectroombutton)
        self.grafickascena.addWidget(self.exitbtn)

        self.playbutton.move(150, 250)
        self.tourney2button.move(150, 300)
        self.tourney4button.move(150, 350)
        self.hostbutton.move(150, 400)
        self.connectroombutton.move(150, 450)
        self.exitbtn.move(150, 500)

        self.setScene(self.grafickascena)

    def hostgame(self):
        self.hostview = self.viewlist.widget(7)
        self.viewlist.setCurrentWidget(self.hostview)

    def tournament2click(self):
        self.turnir = self.viewlist.widget(4)
        self.turnir.initFrames(2, 1)
        self.viewlist.setCurrentWidget(self.turnir)

    def tournament4click(self):

        self.turnir = self.viewlist.widget(4)
        self.turnir.initFrames(4, 2)
        self.viewlist.setCurrentWidget(self.turnir)

    def setbackground(self):
        tempImg = QPixmap('PNG/9c49087c09fd07a10ae3887a7825f389.jpg')
        tempImg = tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        self.graphicsPixmapItem = QGraphicsPixmapItem(tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)

    def playbuttonclick(self):

        self.viewlist.setCurrentWidget(self.viewlist.widget(3))

    def gotoSettingsMenu(self):

        self.viewlist.setCurrentWidget(self.viewlist.widget(5))

    def connectRoomButtonClick(self):
        self.viewlist.setCurrentWidget(self.viewlist.widget(8))

    def closeThis(self):
        sys.exit()
