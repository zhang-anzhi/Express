# -*- coding: utf-8 -*-
import sqlite3
import time
import uuid


class Express:

    def __init__(self, database):
        self.cursor = database.cursor
        self.connection = database.connection

        # Create table
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

    # ---------------
    # List and search
    # ---------------

    def list_all(self) -> list:
        """List all data"""
        return self.cursor.execute(
            'select * from express order by time').fetchall()

    def list_not_taken(self) -> list:
        """List all data where status column is False"""
        return self.cursor.execute(
            'select * from express where status=? order by time',
            (False,)).fetchall()

    def search_by_name(self, name: str, not_taken: bool = True) -> list:
        """
        Return the data if name column is name.
        :param name: A str, the name.
        :param not_taken: A boolean value, if is true only return the status column is False.
        """
        if not_taken:
            return self.cursor.execute(
                'select * from express where name=? and status=False', (name,)
            ).fetchall()
        else:
            return self.cursor.execute(
                'select * from express where name=?', (name,)).fetchall()

    def search_by_number(self, number: str) -> list:
        """
        Return the data if the data column is number.
        :param number: Express number.
        """
        return self.cursor.execute(
            'select * from express where number=?', (number,)).fetchall()

    # -------------
    # Data operator
    # -------------

    def add(self, company: str, name: str, number: str) -> bool:
        """
        Add new express data.
        :param company: The express company.
        :param name: The receiver name.
        :param number: The express number.
        :return: Boolean value where operator success.
        """
        try:
            self.cursor.execute(f'''insert into express values (
                \'{uuid.uuid4()}\', {int(time.time())},
                \'{company}\', \'{name}\', \'{number}\', False)''')
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def take(self, id: str):
        """
        Mark a express status to True
        :param id: Express id, a uuid value.
        """
        self.cursor.execute('update express set status=? where id=?',
                            (True, id))
        self.connection.commit()

    def remove(self, id: str):
        """
        Remove a express data.
        :param id: Express id, a uuid value.
        """
        self.cursor.execute('delete from express where id=?', (id,))
        self.connection.commit()
