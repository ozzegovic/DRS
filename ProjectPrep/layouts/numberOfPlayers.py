from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStackedWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from ProjectPrep.CustomWidgets.CustomButton import StyleButton
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView

class NumberOfPlayersView(QGraphicsView):

    def __init__(self, centralWidget: QStackedWidget):

        super(NumberOfPlayersView, self).__init__()

        self.viewlist = centralWidget
        self.initUI()

    def initUI(self):

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, 1000, 850)

        self.setbackground()
        self.oneplayerbutton = StyleButton('PNG/Buttons/Play_BTN.png', '1 player', 40, 40)
        self.oneplayerbutton.clicked.connect(self.oneplayerbuttonclick)
        self.twoplayerbutton = StyleButton('PNG/Buttons/Play_BTN.png', '2 players', 40, 40)
        self.twoplayerbutton.clicked.connect(self.twoplayerbuttonclick)

        self.threeplayerbutton = StyleButton('PNG/Buttons/Play_BTN.png', '3 players', 40, 40)
        self.threeplayerbutton.clicked.connect(self.threeplayerbuttonclick)

        self.fourplayerbutton = StyleButton('PNG/Buttons/Play_BTN.png', '4 players', 40, 40)
        self.fourplayerbutton.clicked.connect(self.fourplayerbuttonclick)

        self.backbutton = StyleButton('PNG/Buttons/Close_BTN.png', 'Back', 40, 40)
        self.backbutton.clicked.connect(self.backbuttonclick)

        self.holder = QVBoxLayout()
        self.playersLayout1 = QHBoxLayout()
        self.playersLayout2 = QHBoxLayout()


        self.playersLayout1.addWidget(self.oneplayerbutton)
        self.playersLayout1.addWidget(self.twoplayerbutton)
        self.playersLayout1.setAlignment(Qt.AlignCenter)

        self.playersLayout2.addWidget(self.threeplayerbutton)
        self.playersLayout2.addWidget(self.fourplayerbutton)
        self.playersLayout2.setAlignment(Qt.AlignCenter)

        self.titleLabel = QLabel()
        self.titleLabel.setText("CHOOSE NUMBER OF PLAYERS:")
        self.titleLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.holder.addWidget(self.titleLabel)
        self.holder.addLayout(self.playersLayout1)
        self.holder.addLayout(self.playersLayout2)

        self.holder.addWidget(self.backbutton, alignment=Qt.AlignCenter)

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

    def oneplayerbuttonclick(self):
        # create widget with 1 car
        self.input = self.viewlist.widget(4)
        self.input.initFrames(1, 0)
        self.viewlist.setCurrentWidget(self.input) # 4. element view liste

    def twoplayerbuttonclick(self):
        # create widget with 2 cars
        self.input = self.viewlist.widget(4)
        self.input.initFrames(2, 0)
        self.viewlist.setCurrentWidget(self.input)  # 4. element view liste
    def threeplayerbuttonclick(self):
        # create widget with 3 cars
        self.input = self.viewlist.widget(4)
        self.input.initFrames(3, 0)
        self.viewlist.setCurrentWidget(self.input) # 4. element view liste
    def fourplayerbuttonclick(self):
        # create widget with 4 cars
        self.input = self.viewlist.widget(4)
        self.input.initFrames(4, 0)
        self.viewlist.setCurrentWidget(self.input)  # 4. element view liste

    def backbuttonclick(self):
        # back to main menu
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

