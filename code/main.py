# System imports
import getopt
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Data processing Imports
import numpy as np

# PyQt Imports
from PyQt5.QtWidgets import QApplication

import mvc.mvc_util as mvc_util
from mvc.mvc_util import Color as C 

import mvc.Main_view as view
import mvc.Main_model as model
import mvc.Main_controllers as controllers

class Main_controller():
    """Setup the application and model then execute
    """
    
    def __init__(self, input_folder=None):
        self._app = QApplication(sys.argv)
        self._mainModel = model.Main_model()
        self._mainView = view.Main_view(self._mainModel)

    def launch(self):
        self._mainView.setup()
        self._mainView.show()

        return self._app.exec_()

#--------------------------- Main routines----------------------------------
if __name__=='__main__':

    #Setting up app locally within function helps work with Spyder for debug
    def run_app():
        Main_controller().launch()
    run_app()

# with recursive ancestor as (select * from people
# where Name = "Hannah" union all select people.* from people
# inner join ancestor on ancestor.father = people.ID or ancestor.mother = people.ID)
# select * from ancestor;

