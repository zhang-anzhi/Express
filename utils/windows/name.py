# -*- coding: utf-8 -*-
import tkinter
import tkinter.messagebox
from tkinter import ttk

from utils.data.database import DataBase
from utils import functions
from utils import constant


class Name(tkinter.Frame):
    def __init__(self, window_manager, **kw):
        super().__init__(**kw)
        self.window_manager = window_manager
        self.database: DataBase = window_manager.database

        # Frame
        input_frame = tkinter.Frame(self)
        label_frame = tkinter.Frame(input_frame)
        entry_frame = tkinter.Frame(input_frame)
        input_frame.pack()
        label_frame.pack(side='left')
        entry_frame.pack(side='right')

        # Input
        name_label = tkinter.Label(label_frame, text='姓名(必填)')
        phone_label = tkinter.Label(label_frame, text='电话')
        name_label.pack()
        phone_label.pack()
        self.name_entry = tkinter.Entry(entry_frame)
        self.phone_entry = tkinter.Entry(entry_frame)
        self.name_entry.bind('<KeyRelease>', self.set_table)
        self.name_entry.bind('<Return>', self.add)
        self.name_entry.focus_set()
        self.name_entry.pack()
        self.phone_entry.pack()

        # Button
        button_frame = tkinter.Frame(self)
        button_frame.pack()
        register_button = tkinter.Button(button_frame, text='添加',
                                         command=self.add)
        remove_button = tkinter.Button(button_frame, text='删除',
                                       command=self.remove)
        register_button.pack(side='left')
        remove_button.pack(side='right')

        # Table
        table_frame = tkinter.Frame(self)
        table_frame.pack()
        self.table = ttk.Treeview(table_frame, show='headings',
                                  selectmode='browse',
                                  columns=('姓名', '电话'))
        self.table.bind('<KeyRelease-Delete>', self.remove)
        self.table.column('姓名', width=100, anchor='center')
        self.table.column('电话', width=100, anchor='center')
        self.table.heading('姓名', text='姓名')
        self.table.heading('电话', text='电话')
        self.table.pack(side='left')
        self.set_table()
        scrollbar = tkinter.Scrollbar(table_frame, orient='vertical',
                                      command=self.table.yview)
        scrollbar.pack(side='right', fill='y')
        self.table.configure(yscrollcommand=scrollbar.set)

        tkinter.Label(self, text=constant.NAME_HELP, font=('宋体', 24)).pack()

    def set_table(self, event=None):
        functions.set_table(
            self.table,
            functions.simplify_name_list(self.database.name.list_all(),
                                         self.name_entry.get())
        )

    def add(self, event=None):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        phone = None if phone == '' else phone
        self.database.name.add(name, phone)
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.set_table()

    def remove(self, event=None):
        name = self.table.item(self.table.selection()[0])
        if tkinter.messagebox.askokcancel(
                title='确认操作', message=f'确认删除"{name["text"]}"吗？'):
            self.database.name.remove(name['text'])
            self.set_table()
