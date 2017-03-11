from .command import *


class ListCommand:

	def __init__(self):
		self.__list_command = {}


	def add(self, command):
		if isinstance(command, CommandBluetooth):
			self.__list_command[command.name] = command
		else:
			raise BadType("Is not a command bluetooth")

	def get(self, name):
		if self.hasKey(name) is True:
			return self.__list_command[name]
		else:
			raise ValueError("Don't have command '{}' for bluetooth".format(name))

	def hasKey(self, name):
		"""Renvoie vrai si la commande de nom 'name' existe sinon false"""
		if name in self.__list_command:
			return True
		return False

	def items(self):
		return self.__list_command.items()
