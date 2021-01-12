# -*- coding: utf-8 -*-
import tkinter

from utils import constant


class About(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title(constant.NAME)
        self.geometry('300x200')

        name_info = f'{constant.NAME} v{constant.VERSION}'
        version_info = f'Built on {constant.BUILD_DATE}'
        self.name = tkinter.Label(self, text=name_info, font=('黑体', 20))
        self.version = tkinter.Label(self, text=version_info)
        self.author = tkinter.Label(self, text=f'by {constant.AUTHOR}')
        self.name.pack()
        self.version.pack()
        self.author.pack()
