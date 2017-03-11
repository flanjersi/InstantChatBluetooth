#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Objet représentant une liste de périphériques bluetooth
# Pour autoriser ou non la connexion de periphériques au serveur
class ListDevices:

    def __init__(self):
        self._devices = {}
        self.__tab_device_connected = {}
        self.__tab_device_socket = {}

    def add(self, name, addr, socket):
        self._devices[name] = addr
        self.__tab_device_socket[name] = socket

    def get_sockets(self):
        return self.__tab_device_socket

    def get_device_connected(self, name):
        device_connected = ""
        for key, value in self.__tab_device_connected.items():
            if value is True:
                device_connected = device_connected + key + "\n"
        return device_connected

    # Renvoie vrai si le périphérique "name" ayant l'adresse "addr"
    # est présent dans le dictionnaire
    # Sinon false
    def has_device(self, name, addr):
        if self.has_name(name):
            if self._devices.get(name) == addr:
                return True

        return False

    # Renvoie vrai si il existe le nom du périphérique dans la liste
    # des périphériques autorisé à se connecter
    def has_name(self, name="none"):
        return name in self._devices

    # Supprime un périphérique de la liste a l'aide de son nom
    # Si la supression c'est executé renvoie vrai sinon faux
    def remove_device(self, name):
        if name in self._devices:
            del self._devices[name]
            del self.__tab_device_socket[name]
            return True
        return False

    def print_devices(self):
        print("--- Liste des périphériques actuellement stocké ---")
        for name, addr in self._devices.items():
            print(" | --> Nom : '", name, "' / Adresse mac : '", addr, "'")
        print("--- Fin de la liste ---")
