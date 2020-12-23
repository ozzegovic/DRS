from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QStackedLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
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
        self.settingsbutton = StyleButton('PNG/Buttons/Settings_BTN.png', 'Settings', 40, 40)
        self.settingsbutton.clicked.connect(self.gotoSettingsMenu)
        self.exitbtn = StyleButton('PNG/Buttons/Close_BTN.png', 'Exit', 40, 40)
        self.exitbtn.clicked.connect(self.closeThis)

        self.grafickascena.addWidget(self.playbutton)
        self.grafickascena.addWidget(self.settingsbutton)
        self.grafickascena.addWidget(self.exitbtn)

        self.playbutton.move(150, 250)
        self.settingsbutton.move(150, 300)
        self.exitbtn.move(150, 350)

        self.setScene(self.grafickascena)

    def setbackground(self):
        tempImg = QPixmap('PNG/9c49087c09fd07a10ae3887a7825f389.jpg')
        tempImg = tempImg.scaled(self.grafickascena.width(), self.grafickascena.height())

        self.graphicsPixmapItem = QGraphicsPixmapItem(tempImg)
        self.grafickascena.addItem(self.graphicsPixmapItem)

    def playbuttonclick(self):

        self.viewlist.setCurrentWidget(self.viewlist.widget(3))

    def gotoSettingsMenu(self):

        self.viewlist.setCurrentWidget(self.viewlist.widget(1))

    def closeThis(self):
        sys.exit()
