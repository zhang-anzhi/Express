# -*- coding: utf-8 -*-
import tkinter
import tkinter.messagebox
from tkinter import ttk

from utils import functions
from utils import constant


class Register(tkinter.Frame):
    def __init__(self, window_manager, **kw):
        super().__init__(**kw)
        self.window_manager = window_manager
        self.database = window_manager.database

        # Input
        input_frame = tkinter.Frame(self)
        label_frame = tkinter.Frame(input_frame)
        entry_frame = tkinter.Frame(input_frame)
        input_frame.pack()
        label_frame.pack(side='left')
        entry_frame.pack(side='right')
        company_label = tkinter.Label(label_frame, text='快递公司')
        number_label = tkinter.Label(label_frame, text='运单号')
        name_label = tkinter.Label(label_frame, text='收件人')
        company_label.pack()
        number_label.pack()
        name_label.pack()
        self.company_combobox = ttk.Combobox(
            entry_frame, values=constant.COMPANY)
        self.number_entry = tkinter.Entry(entry_frame)
        self.name_entry = tkinter.Entry(entry_frame)
        self.company_combobox.pack()
        self.number_entry.pack()
        self.name_entry.pack()
        self.number_entry.focus_set()
        self.number_entry.bind('<Return>',
                               lambda _: self.name_entry.focus_set())
        self.company_combobox.bind('<<ComboboxSelected>>', self.select_company)
        self.name_entry.bind('<KeyRelease>', self.set_table)
        self.name_entry.bind('<Return>', self.register)

        table_frame = tkinter.Frame(self)
        table_frame.pack()

        # Table
        self.table = ttk.Treeview(table_frame, height=3, show='headings',
                                  selectmode='browse', columns=('姓名',))
        self.table.bind('<ButtonRelease-1>', self.select_table)
        self.table.column('姓名', width=100, anchor='center')
        self.table.heading('姓名', text='姓名')
        self.table.pack(side='left')
        self.set_table()

        # Scrollbar
        scrollbar = tkinter.Scrollbar(table_frame, orient='vertical',
                                      command=self.table.yview)
        scrollbar.pack(side='right', fill='y')
        self.table.configure(yscrollcommand=scrollbar.set)

        # Checkbutton
        self.check_var = tkinter.BooleanVar()
        check_button = tkinter.Checkbutton(self, text='自动清空',
                                           variable=self.check_var,
                                           onvalue=True, offvalue=False)
        check_button.select()
        check_button.pack()

        # Button
        button_frame = tkinter.Frame(self)
        register_button = tkinter.Button(button_frame, text='登记',
                                         command=self.register)
        button_frame.pack()
        register_button.pack()

        # Text
        self.text_var = tkinter.StringVar()
        self.text_var.set('请输入信息')
        text_label = tkinter.Label(self, textvariable=self.text_var,
                                   font=('宋体', 24), fg='blue')
        text_label.pack()
        tkinter.Label(self,
                      text=constant.REGISTER_HELP, font=('宋体', 24)).pack()

    def register(self, event=None):
        company = self.company_combobox.get()
        name = self.name_entry.get()
        number = self.number_entry.get()

        # 完整填写
        if not (company and name and number):
            return self.text_var.set('请填写完整信息')

        # 公司姓名填写正确
        if company == '其它（请直接填写）' or name == '其它（请直接填写）':
            return self.text_var.set('请填写完整信息')

        # 收件人未存储
        if name not in [i[0] for i in self.database.name.list_all()]:
            message = f'收件人"{name}"不在数据库中，请前往收件人管理页面添加'
            return tkinter.messagebox.showinfo(title='姓名错误', message=message)

        info = f'快递公司”{company}“，收件人“{name}”，运单号“{number}”'
        self.window_manager.database.express.add(company, name, number)
        self.text_var.set('已登记\n' + info)
        if self.check_var.get():
            self.number_entry.delete(0, 'end')
            self.name_entry.delete(0, 'end')
        self.number_entry.focus_set()
        self.set_table()

    def set_table(self, event=None):
        functions.set_table(
            self.table,
            functions.simplify_name_list(self.database.name.list_all(),
                                         self.name_entry.get())
        )

    def select_company(self, event):
        if self.company_combobox.get() != '其它（请直接填写）':
            self.number_entry.focus_set()

    def select_table(self, event):
        name = self.table.item(self.table.selection()[0])['text']
        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, name)
        self.name_entry.focus_set()
