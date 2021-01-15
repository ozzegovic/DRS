from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time
import threading


class Worker(QObject):

    finished = pyqtSignal()
    update = pyqtSignal()

    def __init__(self, calldynamic):
        super().__init__()
        self.thread = QThread()
        self.killThread = False
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Worker Signals to the Thread slots
        self.finished.connect(self.thread.quit)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.work)
        self.milisecperioda = calldynamic

    def start(self):
        # Start the thread
        self.killThread = False
        self.thread.start()

    def stop(self):
        self.killThread = True

    @pyqtSlot()
    def work(self):  # A slot with no params

        while True:
            if self.killThread == True:
                self.finished.emit()
                return

            self.update.emit()
            self.thread.msleep(self.milisecperioda)

        # notify all
        # in this case: kill the thread
        self.finished.emit()