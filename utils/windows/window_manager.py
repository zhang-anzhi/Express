# -*- coding: utf-8 -*-
import tkinter
from tkinter import ttk

from utils import constant
from utils.data.database import DataBase
from utils.windows.menubar import Menubar
from utils.windows.register import Register
from utils.windows.search import Search
from utils.windows.name import Name
from utils.windows.statistics import Statistics


class WindowManager:
    def __init__(self, database: DataBase):
        self.database = database
        self.window = tkinter.Tk()
        self.window.title(constant.NAME)
        self.window.wm_iconphoto(True, tkinter.PhotoImage(data=constant.ICON))
        self.window.config(menu=Menubar(self))
        self.window.state('zoomed')
        # self.window.attributes('-fullscreen', True)

        def e(_):
            select = self.notebook.select()[2:]
            if select == 'register':
                self.register.company_combobox.delete(0, 'end')
                self.register.number_entry.delete(0, 'end')
                self.register.name_entry.delete(0, 'end')
                self.register.number_entry.focus_set()
                self.register.set_table()
            elif select == 'search':
                self.search.number_entry.delete(0, 'end')
                self.search.not_taken_mode = True
                self.search.number_entry.focus_set()
                self.search.set_table()
            elif select == 'name':
                self.name.name_entry.delete(0, 'end')
                self.name.phone_entry.delete(0, 'end')
                self.name.name_entry.focus_set()
                self.name.set_table()

        # Notebook
        self.notebook = ttk.Notebook(self.window)
        self.window.bind('<<NotebookTabChanged>>', e)
        self.notebook.pack()

        self.register = Register(self)
        self.search = Search(self)
        self.name = Name(self)
        self.statistics = Statistics(self)
        self.notebook.add(self.register, text='登记')
        self.notebook.add(self.search, text='查询/领取')
        self.notebook.add(self.name, text='收件人管理')
        self.notebook.add(self.statistics, text='统计数据')

        self.window.mainloop()
