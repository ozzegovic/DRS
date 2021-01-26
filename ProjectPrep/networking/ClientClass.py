import socket
import threading
import time, json
from threading import Thread
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from ProjectPrep.layouts.boardNotifier import Worker

class NetworkClientCode(QObject):

    signal = pyqtSignal(dict) # konektovati gde treba
    updateobstacles = pyqtSignal(int, int, int, int, bool)
    updateposition = pyqtSignal(str, float, float, int)

    def __init__(self):
        super().__init__()
        self.ClientSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 7333
        self.id = False
        self.name = ''
        self.car = 1

    def setnameandCar(self, name, car):

        self.name = name
        self.car = car

        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))


        #start thread to send sign up message
    def sendSignUpMessage(self):
        self.ClientSocket.send(str.encode('s,' + str(self.name) + ',' + str(self.car))) # salje se prijava korisnika.
        print("Poslato")
        clientThread = threading.Thread(target=self.serverResponce, args=(self.ClientSocket,))
        clientThread.start()

    def getName(self):
        return self.name

        # nakon prijema emitovati signal metodi Client viewa da zapocne igru s tim recnikom.

    def serverResponce(self, connection):
        print("LISTENING")
        data = connection.recv(1000)
        message : str = data.decode('utf-8')
        dict = json.loads(message)
        self.signal.emit(dict)

        while True:
            message = self.ClientSocket.recv(200).decode('utf-8')
            if message.startswith('m'):
                msg = message.split(',')
                self.updateposition.emit(msg[1], float(msg[2]), float(msg[3]), int(msg[4]))
            elif message.startswith('o'):
                self.parseObstacleMessage(message)
            elif message.startswith('e'):
                self.ClientSocket.send(str.encode('e'))
                break
        self.ClientSocket.close()

    def sendplayerPosition(self, name, x, y, keyindex):
        self.ClientSocket.send(str.encode('m,' + name + ',' + str(x) + ',' + str(y) + ',' + str(keyindex)))

    def parseObstacleMessage(self, message):
        parts = message.split(',')
        if len(parts) != 6:
            print('Obstacles message - invalid format.')
            return
        else:
            visible = True if parts[5] == 'True' else False
            self.updateobstacles.emit(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), visible)
