#!usr/bin/env python3
# -*- utf8 -*-

import logging
from logging.handlers import RotatingFileHandler


class Logger:

    def __init__(self, path_file):
        self.__logger = logging.getLogger(path_file)
        self.__logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler(path_file, 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)
        steam_handler = logging.StreamHandler()
        steam_handler.setFormatter(formatter)
        steam_handler.setLevel(logging.DEBUG)
        self.__logger.addHandler(steam_handler)

    def info(self, message):
        self.__logger.info(message)

    def warning(self, message):
        self.__logger.warning(message)

    def debug(self, message):
        self.__logger.debug(message)

    def error(self, message):
        self.__logger.error(message)

    def critical(self, message):
        self.__logger.critical(message)
