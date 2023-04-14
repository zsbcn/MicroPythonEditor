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

if __name__ == '__main__':
    with open('test.txt', mode='r', encoding='utf-8') as f:
        if md5(f.read().encode('utf-8')).hexdigest() == md5('1'.encode('utf-8')).hexdigest():
            print(True)
        else:
            print(False)
