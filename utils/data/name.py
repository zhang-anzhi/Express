# -*- coding: utf-8 -*-
import sqlite3
from pypinyin import pinyin, Style


class Name:

    def __init__(self, database):
        self.cursor = database.cursor
        self.connection = database.connection

        # Creat table
        self.cursor.execute('''
                    create table if not exists name (
                    name varchar(255) not null unique,
                    phone integer,
                    pinyin varchar(255) not null
                )'''
                            )
        self.connection.commit()

    # ---------------
    # List and search
    # ---------------

    def is_name(self, name: str) -> bool:
        """
        Return a boolean where name is in name list.
        :param name: The person name.
        """
        return name in [i[0] for i in self.list_all()]

    def list_all(self) -> list:
        """Return the name list."""
        return self.cursor.execute(
            'select * from name order by pinyin').fetchall()

    def get_phone(self, name: str) -> int or None:
        """
        Get the phone number from data where name is name.
        :param name: The person name.
        :return: The phone number, if cannot find return None.
        """
        try:
            return self.cursor.execute(
                'select * from name where name=?', (name,)).fetchall()[0][1]
        except IndexError:
            return None

    # -------------
    # Data operator
    # -------------

    def add(self, name: str, phone: int = None) -> bool:
        """
        Add new person to data.
        :param name: The name of the person.
        :param phone: The phone of the person.
        :return: Boolean value where operator success.
        """
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

    def remove(self, name: str):
        """
        Remove a express data.
        :param name: Person name.
        """
        self.cursor.execute('delete from name where name=?', (name,))
        self.connection.commit()
