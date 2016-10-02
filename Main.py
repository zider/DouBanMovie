#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

'''
homepage
'''

import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver

from Movie import MovieDB

'''
通过webdriver可以获得豆瓣上通过JavaScript加载的相关列表
但是只有第一页啊，后面的呢？操作driver？没有尽头啊
'''

class MainPage(object):
    def __init__(self, url='https://movie.douban.com'):
        #self.driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.title = self.driver.title
        self.page_source = self.driver.page_source
        self.soup = bs(self.page_source)
        self.HomeMovie = getHomeMovie(self.soup)
        self.HomeHot = getHomeHot(self.soup)
        
    @staticmethod
    def getHomeMovie(screenMovie):
        #screening-bd = screenMovie.find_element_by_class_name('screening-bd')
        result = {}
        screening-bd = soup.find('div', {'class': 'screening-bd'})
        items = screening-bd.findAll('li', {'class': 'ui-slide-item s'})
        items.extend(screening-bd.findAll('li', {'class': 'ui-slide-item'}))
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
            result['name'] = [name, region, director, actors, release_time, rate, rater, duration, trailer_url,url]
        return result
        
    @staticmethod
    def getHomeHot(hotMovie):
        result = {}
        items = hotMovie.find('div', {'class': 'list'}).findAll('a', {'class': 'item'})
        for item in items:
            name, rate = item.find('p').text.split()
            url = item['href']
            result['name'] = [name, rate, url]
        return result
        