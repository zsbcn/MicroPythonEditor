# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : main_window.py
# Time       ：2023-4-2 22:47
# Author     ：zsbcn
# version    ：python 3.10
# Description：
"""
import os
import sys
from abc import abstractmethod
from typing import List

from PyQt6 import QtGui
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QMenu, QTabWidget

from ui.ui_editor import MyEditor


class ThonnyMainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tab_objects: List['MyEditor'] = []
        self.tab_fileNames: List[str] = []
        self.resize(self.width(), self.height())

        # 状态栏设置
        self.status = self.statusBar()
        self.status.showMessage('这是状态栏提示', 3000)
        self.setWindowTitle('测试')

        # 菜单栏设置
        self.menu = self.menuBar()

        # “文件”菜单
        self.file = QMenu(parent=self.menu)
        self.file.setTitle('文件')

        # “文件-新建”菜单
        self.new_file = QAction(parent=self.menu)
        self.new_file.setText('新建')

        # "文件-打开"菜单
        self.open_file = QAction(parent=self.menu)
        self.open_file.setText('打开')

        # "文件-保存"菜单
        self.save_file = QAction(parent=self.menu)
        self.save_file.setText('保存')

        # “文件-关闭”菜单
        self.quite_exe = QAction(parent=self.menu)
        self.quite_exe.setText('关闭')

        # 给菜单关联动作
        self.menu.addAction(self.file.menuAction())
        self.file.addAction(self.new_file)
        self.file.addAction(self.open_file)
        self.file.addAction(self.save_file)
        self.file.addAction(self.quite_exe)
        self.new_file.triggered.connect(self.new_file_callback)
        self.open_file.triggered.connect(self.open_file_callback)
        self.save_file.triggered.connect(self.save_file_callback)
        self.quite_exe.triggered.connect(self.close)

        self.menu.addMenu('编辑')
        self.menu.addMenu('视图')
        self.menu.addMenu('运行')
        self.menu.addMenu('工具')
        self.menu.addMenu('帮助')

        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        self.tab_widget = QTabWidget()
        self.v_layout.addWidget(self.tab_widget)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab_callback)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.currentChanged.connect(self.reload_file)

    @abstractmethod
    def new_file_callback(self, event):
        pass

    @abstractmethod
    def open_file_callback(self, event):
        pass

    @abstractmethod
    def save_file_callback(self, event):
        pass

    @abstractmethod
    def close_tab_callback(self, index: int):
        pass

    @abstractmethod
    def new_tab_callback(self, tab_name: str):
        pass

    @abstractmethod
    def reload_file(self):
        pass

    def close(self) -> None:
        super().close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        for file in os.listdir():
            if file.endswith('.temp'):
                os.remove(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ThonnyMainWindow()
    main_window.show()
    sys.exit(app.exec())
