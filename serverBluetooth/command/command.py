import time
import re


class CommandBluetooth:
    """
    Classe abstraite commande possédant un nom et un client bluetooth

    La méthode à implémenter est 'execute()'
    """
    def __init__(self, name, client_bluetooth):
        self.name = name
        self.__client_bluetooth = client_bluetooth

    @property
    def client_bl(self):
        return self.__client_bluetooth

    def execute(self, data=None):
        pass
