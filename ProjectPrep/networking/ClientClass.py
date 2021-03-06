import socket
import threading
import time, json, re
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
        self.clientThread = None

    def setnameandCar(self, connectroom, name, car):

        if name != "":
            self.name = name
            self.car = car
        else:
            connectroom.setInfoLabelText(3)

        try:
            self.ClientSocket.connect((self.host, self.port))
            self.sendSignUpMessage()
            connectroom.setInfoLabelText(2)
            return True
        except socket.error as e:
            connectroom.setInfoLabelText(1)
            return False


    def disconnect(self):
        try:
            self.ClientSocket.send(str.encode('d,' + str(self.name)))
        except:
            self.ClientSocket.close()

        #start thread to send sign up message
    def sendSignUpMessage(self):
        self.ClientSocket.send(str.encode('s,' + str(self.name) + ',' + str(self.car))) # salje se prijava korisnika.
        print("Poslato")
        self.clientThread = threading.Thread(target=self.serverResponce, args=(self.ClientSocket,))
        self.clientThread.start()

    def getName(self):
        return self.name

        # nakon prijema emitovati signal metodi Client viewa da zapocne igru s tim recnikom.

    def serverResponce(self, connection):
        print("LISTENING")
        try:
            data = connection.recv(1000)
            message : str = data.decode('utf-8')
            dict = json.loads(message)
            self.signal.emit(dict)
        except:
            return

        while True:
            message = self.ClientSocket.recv(200).decode('utf-8')
            if message.startswith('m'):
                msg = message.split(',')
                keyindex = int(re.sub("[^0-9]", "", msg[4]))
                if msg[1] != self.name:
                    self.updateposition.emit(msg[1], float(msg[2]), float(msg[3]), keyindex)
            elif message.startswith('o'):
                self.parseObstacleMessage(message)
            elif message.startswith('e'):
                self.ClientSocket.send(str.encode('e'))
                break
        #self.ClientSocketshutdown(socket.SHUT_RDWR)
        self.ClientSocket.close()

    def sendplayerPosition(self, name, x, y, keyindex):
        try:
            self.ClientSocket.send(str.encode('m,' + name + ',' + str(x) + ',' + str(y) + ',' + str(keyindex)))
        except:
            pass

    def parseObstacleMessage(self, message):
        parts = message.split(',')
        if len(parts) != 6:
            print('Obstacles message - invalid format.')
            return
        else:
            visible = True if parts[5] == 'True' else False
            self.updateobstacles.emit(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), visible)
