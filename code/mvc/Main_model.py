# -*- coding: utf-8 -*-

# System imports
import getopt
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Data processing Imports
import numpy as np

# Custom Class Imports
import mvc.mvc_util as mvc_util
from mvc.mvc_util import Color as C 

import mvc.Main_view as view
import mvc.Main_model as model
import mvc.Main_controllers as controllers

class Main_model():
    """Core model for use by the Main_view
    """
    def __init__(self):
        self.database = "recursivedb"

    def reset_all(self):
        self.__init__()

    def get_database(self):
        return self.database

    def set_database(self, db):
        self.database = db
        return True