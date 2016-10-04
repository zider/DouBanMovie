#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

'''
真的必须开始了
豆瓣影评爬一个
'''

import json
import re
import arrow
import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver

from Main import MainPageDB
from Movie import MovieDB
from VarType import MovieType

__version__ = '0.0.1'
__author__ = 'uzjY'
__time__ = '16-09-30'

TIMEOUT = 10

def testShow():
    test = MainPageDB()
    infos = json.loads(test.getHomeMovie())
    print(infos)
    
if __name__ == '__main__':
    testShow()
