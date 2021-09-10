# -*- coding: utf-8 -*-

# System imports
import getopt
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Data processing Imports
import numpy as np

# PyQt Imports
from PyQt5 import QtCore, QtGui, Qt, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QTextEdit

# Custom Class Imports
import mvc.mvc_util as mvc_util
from mvc.mvc_util import Color as C

import mvc.Main_model as main_model
import mvc.Main_controllers as controllers

# from dataLabelerMVC.v2_models import *
# from dev_utils.cloud_storage_util import QuerySwideo_controller, PostLabel_controller, \
#     QueryFrame_controller


class Main_view(QWidget):
    """The core view of the util, entry point view
    """

    resized = QtCore.pyqtSignal()

    def __init__(self, model):
        """Init primariliy limited to declaring variables.

        Args:
            model (Main_model): Core state holder for core view.
        """
        super().__init__()

        # declare model
        self._model = model

        self._textBox = QTextEdit(self)

        self._executeButton = QPushButton("Execute!", self)
        # self._userBox = QLineEdit(self)
        # self._frameTextLabel = QLabel("Frame Number: %s" % (None), self)

    def setup(self):
        """Setup the UI.

        Components:
            - Setup the window
            - Set the layout
            - Set styles and capabilities of elements
            - Setup Action listeners
            - Set alignments
            - Setup grid layout
        """

        # set window properties
        self.setMinimumSize(800, 400)
        self.setWindowTitle("Hive Executor")

        # set grid layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)


        # self._threadPool = QtCore.QThreadPool()
        # self._threadPool.setMaxThreadCount(1)

        self._BUTTON_RED_STYLESHEET = """
            QPushButton { min-height: 40px; border-radius: 4px; padding: 0.4em 0.4em 0.4em 0.4em; border: 1px; color: white; background-color: red; }
            QPushButton:focus { border: 0px; selection-background-color: red; background-color: red; }
            QPushButton:hover { border: 1px solid white; selection-background-color: red; background-color: red; }
            """
        self._BUTTON_GREEN_STYLESHEET = """
            QPushButton { min-height: 40px; border-radius: 4px; padding: 0.4em 0.4em 0.4em 0.4em; border: 1px; color: white; background-color: green; }
            QPushButton:focus { border: 0px; selection-background-color: green; background-color: green; }
            QPushButton:hover { border: 1px solid white; selection-background-color: green; background-color: green; }
            """

        self._executeButton.setStyleSheet(self._BUTTON_GREEN_STYLESHEET)

        self._executeButton.clicked.connect(self._on_click_execute_button)

        self.resized.connect(self._on_resize)

        self._textBox.setPlaceholderText("USE testDB;\nSELECT * FROM testDB;")#\n<font color=\"\#red\">text text text</font>

        # set fonts
        commonFont = QtGui.QFont("Calibri", 11, QtGui.QFont.Normal)
        executeButtonFont = QtGui.QFont("Calibri", 12, QtGui.QFont.Normal)

        self._textBox.setFont(commonFont)
        self._executeButton.setFont(executeButtonFont)

        #                                               Y, X, H, W
        leftLayout = QGridLayout()
        leftLayout.addWidget(self._textBox,             0, 0, 1, 1)

        #                                               Y, X, H, W
        rightLayout = QGridLayout()
        rightLayout.addWidget(self._executeButton,      0, 0, 1, 1)

        #                                               Y, X, H, W
        self.grid.addLayout(leftLayout,                 0, 0, 0, 2)
        self.grid.addLayout(rightLayout,                0, 2, 0, 2)

    def updateDisplay(self):
        """Update the display
        """

        self.show()

    def get_text_contents(self):
        return self._textBox.toPlainText()

    def _on_click_execute_button(self):
        controllers.Execute_controller(self._model, self).process()

    def set_button_stylesheet(self, color="RED"):
        if color == "RED":
            self._executeButton.setStyleSheet(self._BUTTON_RED_STYLESHEET)
        else:
            self._executeButton.setStyleSheet(self._BUTTON_GREEN_STYLESHEET)

        time.sleep(0.1)

    def set_button_text(self, text):
        self._executeButton.setText(text)

    def _on_resize(self):
        pass

    def resizeEvent(self, event):
        """Event handling of when a window is resized.

        Keyword arguments:
            event (Event): event that occured
        """
        super().resizeEvent(event)
        self.resized.emit()

    def keyPressEvent(self, event):
        """Keyboard listener actions.

        Args:
            event (PyQtEvent): Internal event of KeyPress
        """
        super().keyPressEvent(event)




# class WorkerSignals(QtCore.QObject):
#     '''
#     Defines the signals available from a running worker thread.

#     Supported signals are:

#     finished
#         No data

#     error
#         `tuple` (exctype, value, traceback.format_exc() )

#     result
#         `object` data returned from processing, anything

#     progress
#         `int` indicating % progress

#     '''
#     error = QtCore.pyqtSignal(Exception)
#     result = QtCore.pyqtSignal(bool)
#     finished = QtCore.pyqtSignal()


# class Worker(QtCore.QRunnable):
#     '''
#     Worker thread

#     Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

#     :param callback: The function callback to run on this worker thread. Supplied args and
#                      kwargs will be passed through to the runner.
#     :type callback: function
#     :param args: Arguments to pass to the callback function
#     :param kwargs: Keywords to pass to the callback function

#     '''

#     def __init__(self, fn, *args, **kwargs):
#         super(Worker, self).__init__()

#         # Store constructor arguments (re-used for processing)
#         self.fn = fn
#         self.args = args
#         self.kwargs = kwargs
#         self.signals = WorkerSignals()

#     @QtCore.pyqtSlot()
#     def run(self):
#         '''
#         Initialise the runner function with passed args, kwargs.
#         '''

#         # Retrieve args/kwargs here; and fire processing using them
#         try:
#             result = self.fn(*self.args, **self.kwargs)
#         except Exception as e:
#             self.signals.error.emit(e)
#         else:
#             self.signals.result.emit(True)
#         finally:
#             self.signals.finished.emit()

#     @QtCore.pyqtSlot()
#     def stop(self):
#         return