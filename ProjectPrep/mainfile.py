from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QMainWindow, QWidget, QStackedWidget, QStackedLayout
import sys
from ProjectPrep.layouts.menuLayout import menuView
from ProjectPrep.layouts.InputPlayersMenu import InputPlayersView
from ProjectPrep.layouts.Boardgame import Boardgame
from ProjectPrep.layouts.pauseView import pauseView
from ProjectPrep.layouts.numberOfPlayers import NumberOfPlayersView
from ProjectPrep.layouts.WinnerMenu import  WinnerView
from ProjectPrep.layouts.tournament import TournamentTree
from ProjectPrep.layouts.ConnectRoom import ConnectRoom
from ProjectPrep.layouts.hostView import HostView

class MainWindow(QMainWindow):

    def __init__(self):


        super().__init__()
        self.centralWidget = QStackedWidget()

        self.board = Boardgame(self.centralWidget)
        self.mainmenu = menuView(self.centralWidget)
        self.hostview = HostView(self.centralWidget)
        self.InputSettings = InputPlayersView(self.centralWidget)
        self.NumberOfPlayers = NumberOfPlayersView(self.centralWidget)
        self.tournament = TournamentTree(self.centralWidget)
        self.Winner = WinnerView(self.centralWidget)
        self.connectRoom = ConnectRoom(self.centralWidget)

        self.setGeometry(0, 0, 1000, 850)

        self.initUI()
        self.show()

    def initUI(self):
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.addWidget(self.mainmenu) # 0. element view liste
        self.centralWidget.addWidget(self.hostview) # 1. element view liste
        self.centralWidget.addWidget(self.board) # 2. element view liste
        self.centralWidget.addWidget(self.NumberOfPlayers) # 3. element view liste
        self.centralWidget.addWidget(self.InputSettings) # 4. element view liste
        self.centralWidget.addWidget(self.tournament) # 5. element view liste
        self.centralWidget.addWidget(self.Winner) # 6. element view liste
        self.centralWidget.addWidget(self.connectRoom) # 7. element view liste

        self.centralWidget.setCurrentWidget(self.mainmenu)
        self.setWindowTitle('Crazy Cars')


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec_())
