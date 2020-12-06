from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, QEvent, pyqtSlot
import time
from ProjectPrep.CustomWidgets.ButtonNotifier import Worker

class StyleButton(QPushButton):

    def __init__(self, file, text, width, height):

        super().__init__()

        self.setText("  " + text)
        self.setStyleSheet("*{background-color: transparent; font: 24px Arial, sans-serif; "
                           "color: white; width: 200px; Text-align:left;} "
                           "StyleButton:hover "
                           "{ color: purple; border-radius: 22px; background: rgba(255, 150, 0, 0.3);}")

        self.setIcon(QtGui.QIcon(file))
        self.setIconSize(QSize(width, height))

        self.worker = Worker()
        self.defSize = QSize(width, height)
        self.animSize = self.defSize

        self.worker.update.connect(self.animationButton)

    def enterEvent(self, a0: QEvent):
        self.worker.killThread = False
        self.animSize = self.defSize
        self.worker.start()

    def leaveEvent(self, a0: QEvent):

        self.worker.killThread = True
        self.setIconSize(self.defSize)

    @pyqtSlot(str)
    def animationButton(self, i):
        if i == '+':
            self.animSize = QSize(self.animSize.width() + 1, self.animSize.height() + 1)
            self.setIconSize(QSize(self.animSize))
        else:
            self.animSize = QSize(self.animSize.width() - 1, self.animSize.height() - 1)
            self.setIconSize(QSize(self.animSize))
