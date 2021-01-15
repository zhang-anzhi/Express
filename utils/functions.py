# -*- coding: utf-8 -*-
import re
from tkinter.ttk import Treeview

from pypinyin import pinyin, Style


def screen_name(name_list, key):
    """
    :param name_list: The all name list
    :param key: The key to screen in name list
    :return: Name list after screen
    """
    result = []
    for i in name_list:
        if key in i:
            result.append(i)
        elif re.fullmatch('[a-zA-z]*', key):
            py = ''.join([i[0] for i in pinyin(i, style=Style.NORMAL)])
            if py.startswith(key):
                result.append(i)
    return result


def simplify_name_list(name_list: list, name_now: str):
    """
    To simplify a full name list to a small list that relate to name_now
    :param name_list: A name list.
    :param name_now: The name that will be use to simplify, can be pinyin/character.
    :return: The name list after simplify.
    """
    if name_now == '':
        return [(i[0], i[1]) for i in name_list]
    elif re.fullmatch('[a-zA-z]*', name_now):
        return [(i[0], i[1]) for i in name_list if i[2].startswith(name_now)]
    else:
        return [(i[0], i[1]) for i in name_list if i[0].startswith(name_now)]


def set_table(table: Treeview, data_list: list):
    """
    :param table: A Tkinter table object will be fill in data.
    :param data_list: The list of data, each data should be a tuple.
    """
    table.delete(*table.get_children())
    for i in reversed(data_list):
        table.insert('', 0, text=i[0], values=i)
