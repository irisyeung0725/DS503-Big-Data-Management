# -*- coding: utf-8 -*-

# System imports
import glob
from enum import Enum

# Data processing Imports
import numpy as np

# PyQt Imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QSlider, QLabel
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QImage, QPixmap, QValidator, QRegExpValidator

# Custom Class Imports

class Color:
    """Class for color printing to terminal.
    
    Usage:
    ```
        >>> print(Color.GREEN + "HI", Color.RESET)
        HI <in green text>
    ```
    """
    # all colors bold unless otherwise noted
    GREEN = "\033[;1m\033[1;32m"
    RED = "\033[;1m\033[1;31m"
    YELLOW = "\033[;1m\033[1;33m"
    BLUE = "\033[;1m\033[1;34m"
    RESET = "\033[;0m\033[0;0m" # not bold
    
class Alignments(Enum):
    CENTER = 1
    LEFT = 2
    RIGHT = 3
    TOP = 4
    BOTTOM = 5

class HorizontalColorbar_widget(QLabel):

    def __init__(self, mx=10):
        """initiallize horizontal colorbar.
        This is a a bar that can be set to different colors at different positions.

        Note:
            The width is likely significantly greater than number of elements in list.
            This is to provide a long and skinny strip instead of of a too small to read,
            or even rectangular shape.

        Args:
            mx (int, optional): max value of colorbar. Defaults to 10.
        """
        super().__init__()

        self.__width = 500
        self.__height = 10

        self.bar = np.zeros((self.__height,self.__width,3), dtype=np.uint8)     
        self.mx = mx   
        self.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored,
            QtWidgets.QSizePolicy.Ignored))
        self.update()
    
    def setMax(self, mx):
        self.mx = mx
        self.bar = np.zeros((self.__height,self.__width,3), dtype=np.uint8)
        self.update()

    def reset(self):
        self.bar = np.zeros((self.__height,self.__width,3), dtype=np.uint8)
        self.update()


    def setCellValues(self, x, values):
        """Set the value at a specific location.
        Inherently this likely sets the value at more locations than specified.

        Args:
            x (int): cell location (horizontally)
            values (list): 3 length list for of rgb color
        """

        assert x >= 0 and x < self.mx, "Cell out of bounds"

        trans1 = int(x / self.mx * self.__width)
        trans2 = int((x+1) / self.mx * self.__width)

        values = np.reshape(values, (1, 1, 3))
        values = np.repeat(values, trans2-trans1, 1)
        values = np.repeat(values, self.__height, 0)
        self.bar[:,trans1:trans2,:] = values
        self.update()

    def update(self):
        height, width, rgbChannels = self.bar.shape
        qimg = QImage(self.bar.tostring(), width, height, rgbChannels * width, QImage.Format_RGB888)
        self.colorbarPixmap = QPixmap(QPixmap.fromImage(qimg))
        lw, lh = self.width(), self.height()
        self.setPixmap(self.colorbarPixmap.scaled(lw, lh, Qt.KeepAspectRatio))
        self.show()

class HorizontalSlider_widget(QSlider):
    """
    Creates a horizontal slider of the style used in the locked mirror analyzer; includes self.setVals(), which helps
    quickly set up the tick range of the sliders
    """

    def __init__(self, parent=Qt.Horizontal):
        super().__init__(parent)
        self.setTickPosition(self.TicksBothSides)
        self.maxTick = 0
        self.minTick = 0
        self.tickinterval = 0

    def setVals(self, maxTick, maxWidth=None, minTick=0, tickInterval=1):
        self.maxTick = maxTick
        self.minTick = minTick
        self.tickInterval = tickInterval
        self.setMinimum(self.minTick)
        self.setMaximum(self.maxTick)
        self.setTickInterval(self.tickInterval)
        self.setMaximumWidth(maxWidth if maxWidth is not None else self.maximumWidth())

class DateValidator_controller(QRegExpValidator):
    def __init__(self, parent=None):
        self.regexStr = "[0-1]{0,1}[0-9]/[0-3]{0,1}[0-9]/[1-2]{0,1}[0-9]{1,3}"
        super().__init__(QRegExp(self.regexStr), parent)

    def validate(self, string, pos):
        """Override the validate function of the RegExpValidator.
        This will setup the correct formatting for a date.

        Args:
            string (str): the text to be validated
            pos (int): position of the most recent character

        Returns:
            tuple: (res, string, pos)
                res: result of the validating
                string: new string after manipulation
                pos: new position of the cursor
        """
        res, string, pos = super().validate(string, pos)

        if res == 0:
            if string[pos-1].isdigit() and string.count('/') < 2:
                string = string[0:pos-1] + "/" + string[pos-1]
                res = 1
                pos = pos+1


        # get the mo/da/yr as array
        date = string.split("/")

        # init to something that cannot be entered
        mo = da = yr = "-1"

        # update vars based on array
        try:
            mo = date[0]
            da = date[1]
            yr = date[2]
        except:
            pass

        # change arr len of date based on overwritten values
        if mo == "-1":
            date = []
        elif da == "-1":
            date = date[:1]
        elif yr == "-1":
            date = date[:2]

        # if entering date that doesnt exist, stop it
        try:
            if int(mo) > 12:
                date[0] = "1"
                pos -= 1
            if int(da) > 31:
                date[1] = "3"
                pos -= 1

        except Exception as e:
            pass

        # reform the date
        string = '/'.join(date)

        return res, string, pos