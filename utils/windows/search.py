# -*- coding: utf-8 -*-
import tkinter
import tkinter.messagebox
from tkinter import ttk
import time

from utils.data.database import DataBase
from utils import constant


class Search(tkinter.Frame):
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
        number_label = tkinter.Label(label_frame, text='运单号')
        number_label.pack()
        self.number_entry = tkinter.Entry(entry_frame)
        self.number_entry.bind('<Return>', self.take)
        self.number_entry.focus_set()
        self.number_entry.pack()

        # Button
        button_frame = tkinter.Frame(self)
        button_frame.pack()
        self.not_taken_mode = True

        def switch():
            if self.not_taken_mode:
                self.not_taken_mode = False
            else:
                self.not_taken_mode = True
            self.set_table()

        take_button = tkinter.Button(button_frame, text='领取',
                                     command=self.take)
        display_button = tkinter.Button(button_frame, text='显示/隐藏已领取',
                                        command=switch)
        take_button.pack(side='left')
        display_button.pack(side='right')

        # Data Frame
        data_frame = tkinter.Frame(self)
        data_frame.pack()

        # Table
        self.table = ttk.Treeview(data_frame, show='headings',
                                  selectmode='browse',
                                  columns=('时间', '快递公司',
                                           '收件人', '运单号', '状态'))
        self.table.column('时间', width=100, anchor='center')
        self.table.column('快递公司', width=100, anchor='center')
        self.table.column('收件人', width=100, anchor='center')
        self.table.column('运单号', width=100, anchor='center')
        self.table.column('状态', width=100, anchor='center')
        self.table.heading('时间', text='时间')
        self.table.heading('快递公司', text='快递公司')
        self.table.heading('收件人', text='收件人')
        self.table.heading('运单号', text='运单号')
        self.table.heading('状态', text='状态')
        self.table.bind('<Return>', self.take)
        self.table.pack(side='left')
        self.set_table()

        # Scrollbar
        scrollbar = tkinter.Scrollbar(data_frame, orient='vertical',
                                      command=self.table.yview)
        scrollbar.pack(side='right', fill='y')
        self.table.configure(yscrollcommand=scrollbar.set)

        tkinter.Label(self, text=constant.SEARCH_HELP, font=('宋体', 24)).pack()

    def set_table(self):
        # 清理
        self.table.delete(*self.table.get_children())

        # 仅显示未领取
        if self.not_taken_mode:
            data = self.database.express.list_not_taken()
        else:
            data = self.database.express.list_all()

        # 插入
        for i in data:
            date = time.strftime('%Y-%m-%d', time.localtime(i[1]))
            status = '已取' if i[5] == 1 else '未取'
            values = (date, i[2], i[3], i[4], status)
            self.table.insert('', 0, text=i[0], values=values)

    def take(self, event=None):
        number = self.number_entry.get()
        if number:
            # 查询并筛选数据
            data = [i for i in self.database.express.list_not_taken() if
                    i[4] == number]

            # 判断结果
            if len(data) == 1:
                self.database.express.take(data[0][0])
                self.number_entry.delete(0, 'end')
                self.set_table()
                tkinter.messagebox.showinfo(message=f'领取成功')
            elif len(data) > 1:
                tkinter.messagebox.showwarning(
                    message=f'查到多个运单号为"{number}"的快递，请在表中手动选择并领取')
                self.number_entry.delete(0, 'end')
            else:
                tkinter.messagebox.showerror(
                    message=f'没有运单号为"{number}"的快递')
        else:
            if not self.table.selection():
                return tkinter.messagebox.showerror(message='请选择要领取的快递')
            if tkinter.messagebox.askokcancel(
                    title='确认操作', message='请再次确认信息后点击确定'):
                self.database.express.take(
                    self.table.item(self.table.selection()[0])['text'])
                self.set_table()
