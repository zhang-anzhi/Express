# -*- coding: utf-8 -*-
import time
import re

from pypinyin import pinyin, Style


def list_all_as_table(data):
    for i in data:
        print('| {} | {} | {} | {} | {} | {} |'.format(
            i[0].ljust(36),
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i[1])).ljust(10),
            i[2].ljust(8), i[3].ljust(10),
            str(i[4]).ljust(16), ('已取' if i[5] == 1 else '').ljust(2)
        ))


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


def simplify_name_list(name_list, name_now):
    if name_now == '':
        return [(i[0], i[1]) for i in name_list]
    elif re.fullmatch('[a-zA-z]*', name_now):
        return [(i[0], i[1]) for i in name_list if i[2].startswith(name_now)]
    else:
        return [(i[0], i[1]) for i in name_list if i[0].startswith(name_now)]


def set_table(table, data_list):
    table.delete(*table.get_children())
    for i in reversed(data_list):
        table.insert('', 0, text=i[0], values=i)
