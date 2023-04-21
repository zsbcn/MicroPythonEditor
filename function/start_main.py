# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : start_main.py
# Time       ：2023-4-1 22:14
# Author     ：zsbcn
# version    ：python 3.10
# Description：
"""
import os
import sys

from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog, QMessageBox

from ui.main_window import ThonnyMainWindow
from ui.ui_editor import MyEditor
from utils.cipher import *


class MyMain(ThonnyMainWindow):
    def new_file_callback(self, event):
        """
        新建文件的回调函数
        :param event:
        """
        file_name, status = QInputDialog.getText(self, '新建文件', '请输入文件名')
        if status:
            if len(file_name) == 0:
                file_name = f'New File {len(self.tab_fileNames) + 1}'
            self.new_tab_callback(file_name)
            self.save_file2temp(file_name, '')

    def open_file_callback(self, event):
        """
        打开文件的回调函数
        :param event:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, '打开文件')
        if file_name in self.tab_fileNames:
            self.tab_widget.setCurrentWidget(self.tab_objects[self.tab_fileNames.index(file_name)])
            reply = QMessageBox.information(self, '提示', '文件已打开，是否重新加载？',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.load_file(file_name)
        elif file_name:
            self.load_file(file_name, new_tab=True)

    def load_file(self, file_name, new_tab=False):
        """
        加载文件
        :param file_name: 加载文件的路径
        :param new_tab: 是否新建Tab页
        """
        if new_tab:
            self.new_tab_callback(file_name)
        with open(file_name, mode='r', encoding='utf-8') as read_file:
            self.tab_widget.currentWidget().setText(read_file.read())
            self.save_file2temp(file_name, read_file.read())

    def save_file_callback(self, event):
        """
        保存文件的回调函数
        :param event:
        """
        current_file_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        current_content = self.tab_objects[self.tab_widget.currentIndex()].text()
        temp_file_name = f'{get_temp_name(current_file_name)}.temp'
        if current_file_name.startswith('New File') \
                or (os.path.exists(temp_file_name) and is_different(temp_file_name, current_content)):
            self.update_file(current_content)

    def close_tab_callback(self, index):
        """
        关闭Tab的回调函数
        :param index: 待关闭的Tab的编号
        """
        self.tab_widget.removeTab(index)
        self.tab_objects.pop(index)
        self.tab_fileNames.pop(index)

    def new_tab_callback(self, tab_name):
        """
        新增Tab的回调函数
        :param tab_name:
        """
        self.tab_objects.append(MyEditor(tab_name))
        self.tab_fileNames.append(tab_name)
        tab_nums = self.tab_widget.count()
        self.tab_widget.addTab(self.tab_objects[tab_nums], tab_name)
        self.tab_widget.setCurrentWidget(self.tab_objects[tab_nums])

    def save_file2temp(self, temp_name, temp_content):
        """
        保存临时文件的回调函数
        :param temp_name: 临时文件的名字
        :param temp_content: 临时文件的内容
        """
        with open(f'{get_temp_name(temp_name)}.temp', mode='w', encoding='utf-8') as temp_file:
            temp_file.write(temp_content)

    def update_file(self, new_content: str):
        file_path, _ = QFileDialog.getOpenFileName(self, '保存文件')
        if file_path in self.tab_fileNames and file_path != self.tab_widget.tabText(self.tab_widget.currentIndex()):
            QMessageBox.warning(self, '提示', '文件已打开，无法保存')
        elif file_path:
            with open(file_path, mode='w', encoding='utf-8') as save_file:
                save_file.write(new_content)
            self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_path)
            self.save_file2temp(file_path, new_content)
            self.tab_fileNames[self.tab_widget.currentIndex()] = file_path

    def reload_file(self):
        current_file_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        current_content = self.tab_objects[self.tab_widget.currentIndex()].text()
        if is_different(current_file_name, current_content):
            reply = QMessageBox.information(self, '提示', '文件已被修改，是否更新？',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.load_file(current_file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMain()
    main_window.show()
    sys.exit(app.exec())
