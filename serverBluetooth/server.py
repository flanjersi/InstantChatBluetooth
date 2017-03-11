#!/usr/bin/python3
# -*- coding: utf-8 -*-

from my_logger import Logger
from serverBluetooth.list_devices import ListDevices
from serverBluetooth.client import Client
from bluetooth import BluetoothSocket, advertise_service, lookup_name
from bluetooth import SERIAL_PORT_CLASS, SERIAL_PORT_PROFILE, OBEX_UUID, L2CAP
from queue import Queue
import threading
import select
import time

# raspberry pi maison : B8:27:EB:90:8C:81


class ServerBluetooth(threading.Thread):
    # Creation du serveur bluetooth
    # Protocole bluetooth = protocol ou L2CAP
    # Port du serveur : 4
    # Liste d'attente de connexion : 255
    def __init__(self, name="ServeurBluetooth", protocol=L2CAP):
        threading.Thread.__init__(self)
        self.__logger = Logger("log/server_bluetooth.log")

        self.__logger.info("Initialisation du serveur bluetooth")
        self._server_name = name
        self.__queue_from_client = Queue()
        self.__socket_server = BluetoothSocket(protocol)
        self.__socket_server.bind(("", 1))
        self.__socket_server.listen(10)
        self.__uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service(self.__socket_server, self._server_name,
                          service_id=self.__uuid,
                          service_classes=[self.__uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          protocols=[OBEX_UUID])

        self.__list_devices = ListDevices()
        self.__queueClients = {}
        self.__logger.info("Creation du serveur bluetooth d'adresse '{}' reussi".format(self.__socket_server.getsockname()))

    # Ajouter l'adresse d'un client à la liste à l'aide de son nom "name"
    # Renvoie vrai si le périphérique peux se connecte , sinon false
    # TODO: Prendre en compte l'adresse du périphérique
    def add_client(self, name, addr, socket):
        if not self.__list_devices.has_name(name):
            socket.send("Bienvenue sur le chat\n")
            self.__list_devices.add(name, addr, socket);
            return True
        return False
    # Attend la connection d'un périphérique
    def wait_connection(self):
        readable, writable, errored = select.select(
            [self.__socket_server], [], [], 0)

        for s in readable:
            if s is self.__socket_server:
                client_socket, client_addr = self.__socket_server.accept()
                client_name = lookup_name(client_addr[0], client_addr[1])
                self.__logger.debug("Connexion en cours du client bluetooth '{}' d'adresse'{}'".format(client_name, client_addr))
                if self.add_client(client_name, client_addr[0], client_socket):
                    self.__logger.debug("En attente de la connexion d'un peripherique bluetooth")
                    self.__queueClients[client_name] = Queue()
                    return client_socket, client_addr[0], client_name, self.__queueClients[client_name]
                else:
                    return None, None, None, None
        return None, None, None, None

    # Fonction de lancement du serveur
    def run(self):
        try:
            self.lunch()
        except Exception as exp:
            print(exp)
            self.close()

    def lunch(self):
        self.__logger.debug("En attente de la connexion d'un peripherique bluetooth")
        while True:
            client_socket, client_addr, client_name, queue = self.wait_connection()

            if client_socket != None and client_addr != None and client_name != None:
                Client(client_name, client_addr, client_socket, self.__queue_from_client, queue).start()
            elif not self.__queue_from_client.empty():
                dataMessage = self.__queue_from_client.get()
                self.__queue_from_client.task_done()
                self.broadcast(dataMessage)
            time.sleep(0.05)

    def broadcast(self, data):
        for socket in self.__list_devices.get_sockets().values():
            socket.send("{} : {}\n".format(data.client_name, data.message))

    def close(self):
        self.__logger.critical("Fermeture du serveur bluetooth")
        self.__socket_server.close()
