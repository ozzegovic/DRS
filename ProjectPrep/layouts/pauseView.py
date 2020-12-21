from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap,  QPainter
from ProjectPrep.CustomWidgets.CustomButton import StyleButton


class pauseView(QGraphicsView):

    def __init__(self, viewlist, width, height):
        super(pauseView, self).__init__()
        self.viewlist = viewlist
        self.initUI(width, height)

    def initUI(self, width, height):

        self.grafickascena = QGraphicsScene()
        self.grafickascena.setSceneRect(0, 0, width, height)

        self.setbackground()
        self.resumebutton = StyleButton('PNG/Buttons/Play_BTN.png', 'Resume', 40, 40)
        self.resumebutton.clicked.connect(self.resumebuttonclick)
        self.mainmenubutton = StyleButton('PNG/Buttons/Settings_BTN.png', 'Main menu', 40, 40)
        self.mainmenubutton.clicked.connect(self.mainmenubuttonclick)

        self.holder = QVBoxLayout()
        self.buttonsLayout = QVBoxLayout()

        self.buttonsLayout.addWidget(self.resumebutton)
        self.buttonsLayout.addWidget(self.mainmenubutton)
        self.buttonsLayout.setAlignment(Qt.AlignCenter)

        self.titleLabel = QLabel()
        self.titleLabel.setText("GAME PAUSED")
        self.titleLabel.setStyleSheet('color: yellow; font-weight: bold; background: transparent;')
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.holder.addWidget(self.titleLabel)
        self.holder.addLayout(self.buttonsLayout)

        self.setLayout(self.holder)
        self.setScene(self.grafickascena)

    def resumebuttonclick(self):
        #self.viewlist.widget(2).grafickascena.removeItem(self.viewlist.widget(3).backgroundItem)
        self.viewlist.widget(2).pauseButton.setEnabled(True)
        self.viewlist.widget(2).worker.start()
        self.hide()

    def mainmenubuttonclick(self):
        #self.viewlist.widget(2).grafickascena.removeItem(self.viewlist.widget(3).backgroundItem)
        self.viewlist.widget(2).pauseButton.setEnabled(True)
        self.viewlist.widget(2).worker.start()
        self.hide()
        # back to main menu
        self.viewlist.setCurrentWidget(self.viewlist.widget(0))

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

