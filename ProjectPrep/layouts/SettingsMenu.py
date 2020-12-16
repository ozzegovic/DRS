from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.uic.properties import QtWidgets

from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
import ctypes



class SettingsView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        self.isFullScreen = False
        super(SettingsView, self).__init__()

        self.viewlist = centralWidget
        self.initUI()

    def initUI(self):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1200, 630)

        self.setbackground()
        self.backbtn = StyleButton('PNG/Buttons/Close_BTN.png', 'Back', 40, 40)
        self.backbtn.clicked.connect(self.backtomenu)

        self.grafickascena.addWidget(self.backbtn)
        self.backbtn.move(500, 500)

        self.fullscreenBtn = StyleButton('PNG/Settings/Indicator_OFF.png', '', 40, 40)
        self.fullscreenBtn.clicked.connect(self.fullscreenIt)
        self.grafickascena.addWidget(self.fullscreenBtn)
        self.fullscreenBtn.move(500, 400)

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
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

    def fullscreenIt(self):
        if not self.isFullScreen:
            user32 = ctypes.WinDLL('user32')
            SW_MAXIMISE = 3
            hWnd = user32.GetForegroundWindow()
            user32.ShowWindow(hWnd, SW_MAXIMISE)
            self.showFullScreen()
            self.showMaximized()
            self.isFullScreen = True
        else:
            user32 = ctypes.WinDLL('user32')
            SW_MAXIMISE = 1
            hWnd = user32.GetForegroundWindow()
            user32.ShowWindow(hWnd, SW_MAXIMISE)
            self.showFullScreen()
            self.showMaximized()
            self.isFullScreen = False