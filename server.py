#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import threading
from serverBluetooth.server import ServerBluetooth
from my_logger import Logger
from queue import Queue
from bluetooth import RFCOMM


class MainServer(threading.Thread):

    def __init__(self, name):
        self.__logger = Logger("log/main_log.log")
        self.__logger.info("Initialisation serveur principal")
        threading.Thread.__init__(self, name=name)
        self.__data_receive_from_module = Queue()
        self.__alive = True

        self.__server_bluetooth = ServerBluetooth(protocol=RFCOMM)

        self.__logger.info("Serveur principal initialiser")

    def run(self):
        self.start_module()

        while self.__alive:
            try:
                data = self.receive_data()
                self.analyse(data)
            except Exception as exp:
                self.__logger.critical(exp.args[0])
                self.__alive = False
        self.__logger.info("Arret centrale communication")

    def start_module(self):
        self.__logger.info("Lancement du serveur principal")
        self.__server_bluetooth.start()
        self.__logger.info("Serveur Principal démarrer")

    def receive_data(self):
        while True:
            if self.__data_receive_from_module.empty() is not True:
                data = self.__data_receive_from_module.get()
                self.__data_receive_from_module.task_done()
                return data
            time.sleep(0.01)

    def analyse(self, data):
        self.__analyser.analyse(data)


if __name__ == '__main__':
    main_server = MainServer("serveur principal")
    main_server.start()


__author__ = "Jérémy GROS"
__version__ = "1.0.0"
__email__ = "contact@jeremygros.fr"
