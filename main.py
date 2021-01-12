# -*- coding: utf-8 -*-
from utils.data.database import DataBase
from utils.windows.window_manager import WindowManager

database = DataBase('data.db')
window_manager = WindowManager(database)
database.close()
