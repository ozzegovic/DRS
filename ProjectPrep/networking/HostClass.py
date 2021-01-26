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
    updateposition = pyqtSignal(str, float, float, int)

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
            elif message.startswith('m'):
                info = message.split(',')
                self.updateposition.emit(info[1], float(info[2]), float(info[3]), int(info[4]))
                self.broadcastMovement(info[1], float(info[2]), float(info[3]), int(info[4]))
            elif message.startswith('e'):
                break
        print('closed')
        connection.close()

    def getName(self):
        return self.name

    def broadcastdictionary(self, dict):
        print("send to clients")
        jsondict = json.dumps(dict)
        for client in self.Clients:
            client.send(str.encode(jsondict))

        self.listenKill = True

    def broadcastObstacles(self, index, x, y, pic, visible):
        # Ovom metodom poslati upakovan string broadcast klijentima o prepreci.
        message = str.encode('o,' + str(index) + ',' + str(x) + ',' + str(y) + ',' + str(pic) + ',' + str(visible))
        for client in self.Clients:
            client.send(message)

    def broadcastMovement(self, player, x, y, keyindex):
        pass # TODO
        # Ovde prvo emitovati kod sebe player poziciju, a zatim i broadcastovati klijentima.
        # Ovo je pomeraj klijenta, koji se broadcastoju ostalim klijentima.
        # Poziva se iz startrecva.
        for client in self.Clients:
            client.send(str.encode('m,' + str(player) + ',' + str(x) + ',' + str(y) + ',' + str(keyindex)))

    def broadcastServerMoveToClients(self, player, x, y, keyindex):
        pass # TODO
        # Ovde broadcastovati samo klijentima ne emitovati kod sebe, jer je
        # ovo samo pomeraj koji host pravi.

    def startlistenloop(self):

        while self.listenKill == False: # kill me when you should.
            try:
                Client, address = self.ServerSocket.accept()
                print('Connected to: ' + address[0] + ':' + str(address[1]))
                Client.setblocking(1)
                self.Clients.append(Client)
                clientThread = threading.Thread(target=self.startrecv, args=(Client, ))
                clientThread.start()
            except:
                #print('here')
                pass
            time.sleep(5)
        self.ServerSocket.close()

    def stopNetworkThreads(self):
        for client in self.connectionlist:
            client.send(str.encode('e'))
