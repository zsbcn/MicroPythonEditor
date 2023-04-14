# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : uir.py
# Time       ：2023-4-2 22:09
# Author     ：zsbcn
# version    ：python 3.10
# Description：自定义的代码编辑器
"""

from PyQt6 import QtGui, QtCore
from PyQt6.Qsci import QsciScintilla, QsciAPIs, QsciLexerPython


class MyEditor(QsciScintilla):
    def __init__(self, file_name: str):
        super().__init__()
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, 15)
        self.ctrlPressed = False
        self.__file_name = file_name

        self._lexer = QsciLexerPython()

        self.setLexer(self._lexer)  # 设置python的语法高亮
        self.setUtf8(True)  # 设置编辑器编码
        self.setCaretLineVisible(True)  # 高亮显示当前行
        self.setIndentationsUseTabs(False)  # 设置使用空格替代Tab
        self.setTabWidth(4)  # 一个Tab宽度是4
        self.setIndentationGuides(True)
        self.setAutoIndent(True)  # 设置自动缩进

        self._apis = QsciAPIs(self._lexer)
        kwlist = self._lexer.keywords(True).split()
        for i in kwlist:
            self._apis.add(i)
        self._apis.prepare()

        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionUseSingle(QsciScintilla.AutoCompletionUseSingle.AcusNever)

    @property
    def file_name(self):
        return self.__file_name

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        super().wheelEvent(event)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key.Key_Control:
            self.ctrlPressed = False
        super().keyReleaseEvent(a0)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key.Key_Control:
            self.ctrlPressed = True
        super().keyPressEvent(e)
