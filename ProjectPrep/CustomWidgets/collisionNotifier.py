from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time

class CollisionNotifier(QObject):

    finished = pyqtSignal()
    update = pyqtSignal()

    def __init__(self):
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

    def start(self):
        # Start the thread
        self.killThread = False
        self.thread.start()

    @pyqtSlot()
    def work(self):  # A slot with no params

        while True:
            if self.killThread == True:
                self.finished.emit()
                return

            self.update.emit()
            time.sleep(0.01)

        # notify all
        # in this case: kill the thread
        self.finished.emit()