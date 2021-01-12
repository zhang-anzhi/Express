# -*- coding: utf-8 -*-
import sqlite3
from pypinyin import pinyin, Style


class Name:

    def __init__(self, database):
        self.cursor = database.cursor
        self.connection = database.connection
        self.cursor.execute('''
                    create table if not exists name (
                    name varchar(255) not null unique,
                    phone integer,
                    pinyin varchar(255) not null
                )'''
                            )
        self.connection.commit()

    def is_name(self, name):
        return name in [i[0] for i in self.list_all()]

    def list_all(self):
        return self.cursor.execute(
            'select * from name order by pinyin').fetchall()

    def get_phone(self, name):
        try:
            return self.cursor.execute(
                'select * from name where name=?', (name,)).fetchall()[0][1]
        except IndexError:
            return None

    def add(self, name, phone=None):
        py = ''.join([i[0] for i in pinyin(name, style=Style.NORMAL)])
        try:
            if phone is None:
                self.cursor.execute(f'''insert into name (name, pinyin) values 
                (\'{name}\', \'{py}\')''')
            else:
                self.cursor.execute(f'''insert into name values 
                (\'{name}\', {phone}, \'{py}\')''')
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove(self, name):
        self.cursor.execute('delete from name where name=?', (name,))
        self.connection.commit()
