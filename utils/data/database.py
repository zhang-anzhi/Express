# -*- coding: utf-8 -*-
import sqlite3

from utils.data.express import Express
from utils.data.name import Name


class DataBase:

    def __init__(self, name):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('vacuum')
        self.express = Express(self)
        self.name = Name(self)

    def close(self):
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None
