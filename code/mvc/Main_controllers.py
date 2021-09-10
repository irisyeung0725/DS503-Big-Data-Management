# -*- coding: utf-8 -*-

# System imports
import getopt
import sys, os
import re, time

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Data processing Imports
import numpy as np

# Custom Class Imports
import mvc.mvc_util as mvc_util
from mvc.mvc_util import Color as C 

import mvc.Main_view as main_view
import mvc.Main_model as main_model
import mvc.Main_controllers as controllers

import sql_to_hive
import hive_executor

class Process_Text_controller():
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def process(self, text):
        # text = re.sub('\"', '\\\"', text)
        text = re.sub('\n', ' ', text)
        text = re.sub('\r', ' ', text)
        text = re.sub('\t', ' ', text)
        text = re.sub("\s\s+", " ", text)

        text = text.split(";")

        return text

class Execute_controller():
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def process(self):
        text = self._view.get_text_contents()
        query = Process_Text_controller(self._model, self._view).process(text)
        self._view.set_button_stylesheet("RED")
        self._view.set_button_text("Processing...")
        time.sleep(0.1)

        queryBuilder = ""

        for q in query:
            q = q+";"
            if " recursive " in q.lower():
                if queryBuilder != "":
                    queryBuilder = "use {db};{qb}".format(db=self._model.database, qb=queryBuilder)
                    r = hive_executor.from_command(queryBuilder)
                    queryBuilder = ""
                r = sql_to_hive.convert_and_run(q, database=self._model.database)
            else:
                queryBuilder += " {q}".format(q=q)
                if "use " in q.lower():
                    _, _, after = q.partition("use ")
                    self._model.database = after[:after.find(" ")]
                    print(self._model.database)
                
        if queryBuilder != "":
            queryBuilder = "use {db};{qb}".format(db=self._model.database, qb=queryBuilder)
            r = hive_executor.from_command(queryBuilder)
            queryBuilder = ""

        self._view.set_button_stylesheet("GREEN")
        self._view.set_button_text("Execute!")
        return r