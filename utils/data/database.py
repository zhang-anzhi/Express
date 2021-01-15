# -*- coding: utf-8 -*-
import sqlite3

from utils.data.express import Express
from utils.data.name import Name


class DataBase:

    def __init__(self, name):
        # Database connection
        self.connection = sqlite3.connect(name)

        # Cursor
        self.cursor = self.connection.cursor()
        self.cursor.execute('vacuum')

        # Table object
        self.express = Express(self)
        self.name = Name(self)

    def close(self):
        # Close cursor
        self.cursor.close()
        self.cursor = None

        # Close Connection
        self.connection.close()
        self.connection = None
