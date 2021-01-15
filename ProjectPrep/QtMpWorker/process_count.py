from multiprocessing import Process, Pipe
import sys

import time


class ProcessCount(Process):

    def __init__(self, pipe: Pipe, perioda):
        self.pipe = pipe
        self.period = perioda

    def startprocess(self):
        super().__init__(target=self.__count__, args=[self.pipe, self.period], daemon=True)
        self.start()

    def __count__(self, pipe: Pipe, perioda):
        while True:
            pipe.recv()
            pipe.send('go')
            time.sleep(perioda)