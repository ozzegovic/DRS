from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QMainWindow, QWidget, QStackedWidget, QStackedLayout
import sys
from ProjectPrep.layouts.menuLayout import menuView
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.SettingsMenu import SettingsView
from ProjectPrep.layouts.Boardgame import Boardgame
from ProjectPrep.layouts.pauseView import pauseView
from ProjectPrep.layouts.numberOfPlayers import NumberOfPlayersView


class MainWindow(QMainWindow):

    def __init__(self):


        super().__init__()
        self.centralWidget = QStackedWidget()

        self.board = Boardgame(self.centralWidget)
        self.mainmenu = menuView(self.centralWidget)
        self.Settings = SettingsView(self.centralWidget)
        #self.InputSettings = InputPlayersView(self.centralWidget, 0) # nema potrebe praviti ovde ovaj view
        self.NumberOfPlayers = NumberOfPlayersView(self.centralWidget)

        self.initUI()
        self.show()

    def initUI(self):
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.addWidget(self.mainmenu) # 0. element view liste
        self.centralWidget.addWidget(self.Settings) # 1. element view liste
        self.centralWidget.addWidget(self.board) # 2. element view liste
        self.centralWidget.addWidget(self.NumberOfPlayers) # 3. element view liste

        #self.centralWidget.addWidget(self.InputSettings) # 4. element view liste, kreira se u numberOfPlayers.py

        self.centralWidget.setCurrentWidget(self.mainmenu)
        self.setWindowTitle('Crazy Cars')


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec_())
