# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : start_main.py
# Time       ：2023-4-1 22:14
# Author     ：zsbcn
# version    ：python 3.10
# Description：
"""
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
            self.save_file_temp(file_name, '')

    def open_file_callback(self, event):
        """
        打开文件的回调函数
        :param event:
        """
        file_name, _ = QFileDialog.getOpenFileName(self, '打开文件')
        if file_name in self.tab_fileNames:
            reply = QMessageBox.information(self, '提示', '文件已打开，是否重新加载？',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                with open(file_name, mode='r', encoding='utf-8') as read_file:
                    self.tab_widget.currentWidget().setText(read_file.read())
                    self.save_file_temp(file_name, read_file.read())
            self.tab_widget.setCurrentWidget(self.tab_objects[self.tab_fileNames.index(file_name)])
        else:
            self.new_tab_callback(file_name)
            with open(file_name, mode='r', encoding='utf-8') as read_file:
                self.tab_widget.currentWidget().setText(read_file.read())
                self.save_file_temp(file_name, read_file.read())

    def save_file_callback(self, event):
        """
        保存文件的回调函数
        :param event:
        """
        current_file_name = self.tab_widget.tabText(self.tab_widget.currentIndex())
        temp_file_name = f'{get_temp_name(current_file_name)}.temp'
        if current_file_name.startswith('New File'):
            file_path, _ = QFileDialog.getSaveFileName(self, '保存文件', '.')
            if file_path:
                self.save_file_temp(temp_file_name,
                                    self.tab_widget.currentWidget().text())  # 保存临时文件
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_path)  # 更新Tab的名字
        # if os.path.exists(temp_file_name):
        #     if is_different(temp_file_name, self.tab_objects[self.tab_widget.currentIndex()].text()):
        #         file_path, _ = QFileDialog.getSaveFileName(self, '保存文件', '.')
        #         self.save_file_temp(temp_file_name,
        #                             self.tab_widget.currentWidget().text())  # 保存临时文件
        #         self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_path)  # 更新Tab的名字

        # if file_path and os.path.exists():
        # if current_file_name.startswith('New File') or (
        #         os.path.exists(temp_file_name) and is_different(temp_file_name, current_file_name)):
        #     file_path, _ = QFileDialog.getSaveFileName(self, '保存文件', '.')
        #     with open(file_path, mode='w', encoding='utf-8') as save_file:
        #         save_file.write(self.tab_objects[self.tab_widget.currentIndex()].text())
        #     self.tab_widget.setTabText(self.tab_widget.currentIndex(), file_path)

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

    def save_file_temp(self, temp_name, temp_content):
        """
        保存临时文件的回调函数
        :param temp_name: 临时文件的名字
        :param temp_content: 临时文件的内容
        """
        with open(f'{get_temp_name(temp_name)}.temp', mode='w', encoding='utf-8') as temp_file:
            temp_file.write(temp_content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMain()
    main_window.show()
    sys.exit(app.exec())
