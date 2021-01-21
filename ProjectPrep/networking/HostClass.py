import socket
import os
import threading, multiprocessing
import json
from PyQt5 import Qt
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
import time
import re

class NetworkHost(QObject):

    signal = pyqtSignal(dict) # konektovati gde treba
    addPlayerFrameSignal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.ServerSocket = socket.socket()
        self.host = '127.0.0.1'
        self.id = True
        self.port = 7333
        self.name = ''
        self.car = 1
        self.ThreadCount = 0
        self.message = ""
        self.dict = []
        self.Clients = []

    def starthost(self):

        try:
            self.ServerSocket.bind((self.host, self.port))
            self.ServerSocket.setblocking(0)
        except socket.error as e:
            print(str(e))

        self.ServerSocket.listen(3)
        self.listenKill = False
        threading.Thread(target=self.startlistenloop).start()

    def startrecv(self, connection):

        while True:
            data = connection.recv(200)
            #reply = 'Server Says: ' + data.decode('utf-8')
            message : str = data.decode('utf-8')
            if message.startswith('s'):
                messageSplit = message.split(',')
                self.addPlayerFrameSignal.emit(messageSplit[1], messageSplit[2])
                print(messageSplit[1])
        print('closed')
        connection.close()

    def broadcastdictionary(self, dict):
        print("send to clients")
        jsondict = json.dumps(dict)
        for client in self.Clients:
            client.send(str.encode(jsondict))

    def startlistenloop(self):

        while self.listenKill == False: # kill me when you should.
            try:
                Client, address = self.ServerSocket.accept()
                self.Clients.append(Client)
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                Client.setblocking(1)
                clientThread = threading.Thread(target=self.startrecv, args=(Client, ))
                clientThread.start()
            except:
                #print('here')
                pass
            time.sleep(5)
        self.ServerSocket.close()