from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time
import threading


class Worker(QObject):

    finished = pyqtSignal()
    update = pyqtSignal()

    def __init__(self, calldynamic):
        super().__init__()
        self.thread = QThread()
        self.startdynamic = calldynamic
        self.killThread = False
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Worker Signals to the Thread slots
        self.finished.connect(self.thread.quit)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.work)
        self.perioda = calldynamic

    def start(self):
        # Start the thread
        self.killThread = False
        self.thread.start()

    def stop(self):
        self.killThread = True

    def decreaseperiod(self, period):
        if self.perioda - period > 0:
            self.perioda = self.perioda - period
        print('Perioda je: {0}.'.format(self.perioda))

    def restart(self):
        self.perioda = self.startdynamic

    @pyqtSlot()
    def work(self):  # A slot with no params

        while True:
            if self.killThread == True:
                self.finished.emit()
                return

            self.update.emit()
            time.sleep(self.perioda)

        # notify all
        # in this case: kill the thread
        self.finished.emit()