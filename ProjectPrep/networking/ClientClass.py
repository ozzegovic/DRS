import socket
import threading
import time, json
from threading import Thread
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from ProjectPrep.layouts.boardNotifier import Worker

class NetworkClientCode(QObject):

    signal = pyqtSignal(dict) # konektovati gde treba

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

        # nakon prijema emitovati signal metodi Client viewa da zapocne igru s tim recnikom.

    def serverResponce(self,connection):
        print("LISTENING")
        data = connection.recv(1000)
        message : str = data.decode('utf-8')
        dict = json.loads(message)
        self.signal.emit(dict)