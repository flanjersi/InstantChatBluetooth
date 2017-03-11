#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .command.list_command import ListCommand
from my_logger import Logger
from .command.command import *
from bluetooth import *
from queue import Queue
import threading
import time
import socket

class Message:
    def __init__(self, client_name, message):
        self.__client_name = client_name
        self.__message = message

    @property
    def message(self):
        return self.__message

    @property
    def client_name(self):
        return self.__client_name


class Client(threading.Thread):

    def __init__(self, name, addr, socket, queue_to_server_bluetooth, queue):

        threading.Thread.__init__(self)
        self.__logger = Logger("log/server_bluetooth.log")
        self.__client_name = name
        self.__addr = addr
        self.__socket = socket
        self.__socket.settimeout(0.5)
        self.__alive = True
        self.__queue_from_server_bluetooth = queue
        self.__queue_to_server_bluetooth = queue_to_server_bluetooth
        self.__list_command = ListCommand()
        self.add_all_commands()

    def stop(self):
        self.__alive = False

    def run(self):
        self.__logger.info("Client bluetooth '{}' d'adresse '{}' en cours de traitement ".format(self.__client_name, self.__addr))

        while self.__alive:
            data = self.receive()
            if data is not None:
                self.__queue_to_server_bluetooth.put(Message(self.__client_name, data))
            time.sleep(0.05)

        self.__logger.info("Deconnexion du client bluetooth '{}' d'adresse '{}'".format(self.__client_name, self.__addr))
        self.__socket.close()

    def search_and_execute_command(self, data_bluetooth):
        if len(data_bluetooth) == 0:
            return

        data_name = data_bluetooth.split(" ")[0]

        if self.has_command(data_name):
            self.execute_command(data_name, data_bluetooth)
        else:
            self.no_command_found(data_bluetooth)

    def no_command_found(self, data):
            data_format = data.replace("\r", " ").replace("\n", " ")
            self.send("Je ne reconnais pas ce que vous me demandez, vous avez le choix entre: \n")
            for key, value in self.__list_command.items():
                self.send(" - {}\n".format(key))
            time_now = time.strftime("%H:%M:%S")
            self.__logger.info("Serveur -> Recu :'{}' depuis le client '{}'".format(data_format, self.__client_name))

    def send(self, data):
        """Envoie une donnée"""
        self.__socket.send(data)

    def receive(self):
        """Receptionne une donnée"""
        try:
            data = self.__socket.recv(256).decode()
        except socket.error as exp:
            if exp.args[0] == "timed out":
                return None
            else:
                self.__alive = False
        else:
            return data

    def get_data_from_server(self):
        """Recupere une donée de la file si celle-çi n'est pas vide"""
        while True:
            if self.__queue_from_server_bluetooth.empty() is not True:
                data = self.__queue_from_server_bluetooth.get()
                self.__queue_from_server_bluetooth.task_done()
                return data
            time.sleep(0.01)

    def send_data_to_server(self, data):
        pass

    def execute_command(self, name, data):
        self.__list_command.get(name).execute(data)

    def has_command(self, name):
        return self.__list_command.hasKey(name)

    @property
    def name(self):
        return self.__client_name

    def add_all_commands(self):
        pass
