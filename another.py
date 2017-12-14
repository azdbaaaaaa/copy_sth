#!/usr/bin/env/python
#-*- coding=utf-8 -*-

import xlrd
import unittest
import requests


class Test(unittest.TestCase):

    def duqu(self, filename='test.xlsx'):
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        parameter = table.row_values(1)
        jsoninfo = eval(parameter[3])
        url = 'http://XXX' + parameter[2]