# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : cipher.py
# Time       ：2023-4-15 2:16
# Author     ：zsbcn
# version    ：python 3.10
# Description：
"""
from hashlib import md5


def get_temp_name(row_name: str):
    """
    获取临时的名字
    :param row_name: 临时名字的原始内容
    :return: MD5编码生成的临时名字
    """
    return md5(row_name.encode('utf-8')).hexdigest()


def is_different(temp_file_name, current_content):
    """
    判断两个文本是否有变更
    :param temp_file_name: 临时文件的名字
    :param current_content: 新文本的内容
    :return: 没有变更：False; 变更：True
    """
    try:
        with open(temp_file_name, mode='r', encoding='utf-8') as temp_file_handle:
            if md5(temp_file_handle.read().encode('utf-8')).hexdigest() == md5(
                    current_content.encode('utf-8')).hexdigest():
                return False
            return True
    except FileNotFoundError:
        return False


if __name__ == '__main__':
    with open('test.txt', mode='r', encoding='utf-8') as f:
        if md5(f.read().encode('utf-8')).hexdigest() == md5('1'.encode('utf-8')).hexdigest():
            print(True)
        else:
            print(False)
