# -*- coding: utf-8 -*-
import sqlite3
import os
import time
import tkinter
import tkinter.filedialog
import tkinter.messagebox

from utils import constant
from utils.windows.about import About


class Menubar(tkinter.Menu):
    def __init__(self, window_manager, **kw):
        super().__init__(**kw)
        self.window_manager = window_manager

        # File menu
        file_menu = tkinter.Menu(self, tearoff=0)
        file_menu.add_command(label='导入', command=self.import_data)
        file_menu.add_command(label='导出', command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(
            label='退出', command=self.window_manager.window.quit)
        self.add_cascade(label='选项', menu=file_menu)

        # Help menu
        help_menu = tkinter.Menu(self, tearoff=0)
        help_menu.add_command(label=f'关于 {constant.NAME}', command=About)
        self.add_cascade(label='帮助', menu=help_menu)

    def import_data(self):
        """Import data method"""
        path = tkinter.filedialog.askopenfilename(
            defaultextension='.db',
            filetypes=[('数据库文件', '.db')],
            initialfile='导出数据'
        )
        if path:
            start = time.time()
            db = sqlite3.connect(path)
            cursor = db.cursor()
            data = cursor.execute('select * from data').fetchall()
            for i in data:
                if not self.window_manager.database.name.is_name(i[1]):
                    self.window_manager.database.name.add(i[1], i[3])
                self.window_manager.database.express.add(*i[:3])
            db.close()
            message = '导入完成，共{}条数据，耗时{}s\n是否删除已导入数据？'.format(
                len(data), round(time.time() - start, 2))
            if tkinter.messagebox.askquestion(
                    title='导入完成', message=message) == 'yes':
                os.remove(path)

    def export_data(self):
        """Output data method"""
        path = tkinter.filedialog.asksaveasfilename(
            defaultextension='.db',
            filetypes=[('数据库文件', '.db'), ('所有文件', '.*')],
            initialfile='导出数据'
        )

        if path:
            start = time.time()
            if os.path.isfile(path):
                os.remove(path)
            db = sqlite3.connect(path)
            cursor = db.cursor()
            cursor.execute('''
                    create table if not exists data (
                    company varchar(255) not null,
                    name varchar(255) not null,
                    number varchar(255) not null,
                    phone integer
                )''')
            data = self.window_manager.database.express.list_all()
            for i in data:
                phone = self.window_manager.database.name.get_phone(i[3])
                if phone is None:
                    cursor.execute(
                        f'''insert into data (company, name, number) 
                        values (\'{i[2]}\', \'{i[3]}\', \'{i[4]}\')''')
                else:
                    cursor.execute(
                        f'''insert into data 
                        values (\'{i[2]}\', \'{i[3]}\', \'{i[4]}\', {phone})''')
            db.commit()
            db.close()
            message = '导出完成，共{}条数据，耗时{}s\n是否删除已导出数据？'.format(
                len(data), round(time.time() - start, 2))
            if tkinter.messagebox.askquestion(
                    title='导出完成', message=message) == 'yes':
                for i in data:
                    self.window_manager.database.express.remove(i[0])
