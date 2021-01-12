# -*- coding: utf-8 -*-
import tkinter


class Statistics(tkinter.Frame):
    def __init__(self, window_manager, **kw):
        super().__init__(**kw)
        self.window_manager = window_manager
        self.database = window_manager.database

        tkinter.Label(self, text='开发中', font=('宋体', 72)).pack()
