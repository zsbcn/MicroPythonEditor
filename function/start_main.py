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


class MyMain(ThonnyMainWindow):
    def new_file_callback(self, event):
        file_name, status = QInputDialog.getText(self, '新建文件', '请输入文件名')
        if status:
            if len(file_name) == 0:
                file_name = 'New File'
            self.new_tab_callback(file_name)

    def open_file_callback(self, event):
        file_name, _ = QFileDialog.getOpenFileName(self, '打开文件')
        if file_name:
            if file_name in self.tab_fileNames:
                reply = QMessageBox.information(self, '标题', '消息对话框正文',
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                                | QMessageBox.StandardButton.Cancel,
                                                QMessageBox.StandardButton.Yes)
                print(reply)
                self.tab_widget.setCurrentWidget(self.tab_objects[self.tab_fileNames.index(file_name)])
            else:
                self.new_tab_callback(file_name)
                with open(file_name, mode='r', encoding='utf-8') as f:
                    self.tab_widget.currentWidget().setText(f.read())

    def close_tab_callback(self, index):
        self.tab_widget.removeTab(index)
        self.tab_objects.pop(index)
        self.tab_fileNames.pop(index)

    def new_tab_callback(self, tab_name):
        self.tab_objects.append(MyEditor(tab_name))
        self.tab_fileNames.append(tab_name)
        tab_nums = self.tab_widget.count()
        self.tab_widget.addTab(self.tab_objects[tab_nums], tab_name)
        self.tab_widget.setCurrentWidget(self.tab_objects[tab_nums])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMain()
    main_window.show()
    sys.exit(app.exec())
