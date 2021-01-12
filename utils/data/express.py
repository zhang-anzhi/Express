# -*- coding: utf-8 -*-
import sqlite3
import time
import uuid


class Express:

    def __init__(self, database):
        self.cursor = database.cursor
        self.connection = database.connection
        self.cursor.execute('''
                    create table if not exists express (
                    id varchar(255) not null primary key unique,
                    time integer not null,
                    company varchar(255) not null,
                    name varchar(255) not null,
                    number varchar(255) not null,
                    status integer not null
                )'''
                            )
        self.connection.commit()

    # List and search

    def list_all(self):
        return self.cursor.execute(
            'select * from express order by time').fetchall()

    def list_not_taken(self):
        return self.cursor.execute(
            'select * from express where status=? order by time',
            (False,)).fetchall()

    def search_by_name(self, name, not_taken=True):
        if not_taken:
            return self.cursor.execute(
                'select * from express where name=? and status=False', (name,)
            ).fetchall()
        else:
            return self.cursor.execute(
                'select * from express where name=?', (name,)).fetchall()

    def search_by_number(self, number):
        return self.cursor.execute(
            'select * from express where number=?', (number,)).fetchall()

    # Express operator

    def add(self, company, name, number):
        try:
            self.cursor.execute(f'''insert into express values (
                \'{uuid.uuid4()}\', {int(time.time())},
                \'{company}\', \'{name}\', \'{number}\', False)''')
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def take(self, id):
        self.cursor.execute('update express set status=? where id=?',
                            (True, id))
        self.connection.commit()

    def remove(self, id):
        self.cursor.execute('delete from express where id=?', (id,))
        self.connection.commit()
