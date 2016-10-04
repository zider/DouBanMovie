#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

'''
homepage
'''

import requests
import json

from bs4 import BeautifulSoup as bs
from selenium import webdriver

from Movie import MovieDB

'''
通过webdriver可以获得豆瓣上通过JavaScript加载的相关列表
但是只有第一页啊，后面的呢？操作driver？没有尽头啊
'''

class MainPageDB(object):

    chartUrl = 'https://movie.douban.com/chart'
    
    def __init__(self, url='https://movie.douban.com'):
        #self.driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
        self.driver = webdriver.PhantomJS()
        self.driver.get(url)
        self.title = self.driver.title
        self.soup = bs(self.driver.page_source)
        
    def getHomeMovie(self):
        #screening-bd = screenMovie.find_element_by_class_name('screening-bd')
        result = {}
        screening_bd = self.soup.find('div', {'class': 'screening-bd'})
        items = screening_bd.findAll('li', {'class': 'ui-slide-item s'})
        items.extend(screening_bd.findAll('li', {'class': 'ui-slide-item'}))
        for item in items:
            name = item['data-title']
            release_time = item['data-release']
            rate = item['data-rate']
            rater = item['data-rater']
            trailer_url = item['data-trailer']
            duration = item['data-duration']
            region = item['data-region']
            director = item['data-director']
            actors = item['data-actors']
            url = item.find('a')['href']
            result[name] = [name, region, director, actors, release_time, rate, rater, duration, trailer_url,url]
        return json.dumps(result)
        
    def getHomeHot(self):
        result = {}
        items = self.soup.find('div', {'class': 'list'}).findAll('a', {'class': 'item'})
        for item in items:
            name, rate = item.find('p').text.split()
            url = item['href']
            result['name'] = [name, rate, url]
        return json.dumps(result)
        
    @classmethod
    def getChart(cls):
        url = cls.chartUrl
        soup = bs(requests.get(url).text)
        result = {}
        items = soup.findAll('tr', {'class': 'item'})
        for item in items:
            infos = item.find('div',{'class': 'pl2'})
            name = infos.find('a').text.replace('\n','').replace(' ','')
            info = infos.find('p').text
            rate = infos.find('span', {'class': 'rating_nums'}).text + 'By ' + infos.find('span', {'class': 'pl'}).text
            result['name'] = [name, info, rate]
        return json.dumps(result)
            