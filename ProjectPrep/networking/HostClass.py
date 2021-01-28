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
    disconnectplayer = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ServerSocket = socket.socket()
        hostname = socket.gethostname()
        self.host = socket.gethostbyname(hostname)
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

            self.ServerSocket.listen(3)
            self.listenKill = False
            threading.Thread(target=self.startlistenloop).start()

        except socket.error as e:
            print(str(e))

    def startrecv(self, connection):

        while True:
            try:
                data = connection.recv(200)
            except:
                return
            #reply = 'Server Says: ' + data.decode('utf-8')
            message : str = data.decode('utf-8')
            if message.startswith('s'):
                # if connection in self.Clients:
                #     return
                messageSplit = message.split(',')
                self.addPlayerFrameSignal.emit(messageSplit[1], messageSplit[2])
                print(messageSplit[1])
            elif message.startswith('m'):
                info = message.split(',')
                keyindex = int(re.sub("[^0-9]", "", info[4]))
                self.updateposition.emit(info[1], float(info[2]), float(info[3]), keyindex)
                self.broadcastMovement(info[1], float(info[2]), float(info[3]), keyindex)
            elif message.startswith('d'):
                name = message.split(',')[1]
                for client in self.Clients:
                    if client == connection:
                        client.close()
                self.disconnectplayer.emit(name)
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
            try:
                client.send(str.encode(jsondict))
            except:
                continue
        self.listenKill = True

    def broadcastObstacles(self, index, x, y, pic, visible):
        # Ovom metodom poslati upakovan string broadcast klijentima o prepreci.
        message = str.encode('o,' + str(index) + ',' + str(x) + ',' + str(y) + ',' + str(pic) + ',' + str(visible))
        for client in self.Clients:
            try:
                client.send(message)
            except:
                continue
    def broadcastMovement(self, player, x, y, keyindex):
        pass # TODO
        # Ovde prvo emitovati kod sebe player poziciju, a zatim i broadcastovati klijentima.
        # Ovo je pomeraj klijenta, koji se broadcastoju ostalim klijentima.
        # Poziva se iz startrecva.
        for client in self.Clients:
            try:
                client.send(str.encode('m,' + str(player) + ',' + str(x) + ',' + str(y) + ',' + str(keyindex)))
            except:
                continue

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
                pass
            time.sleep(1)
        #self.ServerSocket.shutdown(socket.SHUT_RDWR)
        self.ServerSocket.close()

    def stopNetworkThreads(self):
        for client in self.Clients:
            try:
                client.send(str.encode('e'))
            except:
                pass
