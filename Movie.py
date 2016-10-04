#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

'''
分析单独的一部电影info
'''

import requests
import json

from bs4 import BeautifulSoup as bs
from selenium import webdriver

class MovieDB(object):
    
    KEY_INFO = ['导演', '编剧', '主演', '类型:', 'IMDb链接:']
    EXCEPT_KEY = ['制片国家/地区:', '语言:', '上映日期:', '片长:', '又名:']
    
    def __init__(self, url='https://movie.douban.com/subject/25986180/'):
        self.url = url
        self.soup = bs(requests.get(self.url).text)
        # 豆瓣电影有时候会自动跳转回首页
        # 暂时原因未判别，加个验证
        if self.soup.title.text.split() == ['豆瓣电影']:
            self.url = url + '?from=showing'
            self.soup = bs(requests.get(self.url).text)
        
    def getInfo(self):
        info = self.soup.find('div',{'id':'info'}).text.split()
        info = [i for i in info if i != '/']
        length = len(info)
        i = 0
        result = {}
        result['title'] = self.soup.title.text.split()[0] + '-' + self.soup.find('span',{'class':'year'}).text[1:-1]
        result['rate'] = getRate()
        result['summary'] = self.soup.find('span',{'property':'v:summary'}).text.replace(' ','').replace('\\u3000','')
        key = ''
        while i < length:
            if info[i] in KEY_INFO:
                key = info[i]
                result[key] = ''
                i += 1
            elif info[i] in EXCEPT_KEY:
                i += 2
            else:
                result[key].append(info[i])
                i += 1
        return json.dumps(result)
            
    def getRate(self):
        return self.soup.find('strong',{'class':'ll rating_num'}).text + ' Rating By ' + self.soup.find('span',{'property':'v:votes'}).text + ' Peoples.'
            
    def getComment(self):
        comments = self.soup.findAll('div',{'class':'comment'})
        result = {}
        user, rate, time, comment = '', '', '', ''
        for i in comments:
            comment = i.find('p').text
            i = i.find('span', {'class': 'comment-info'})
            user = i.find('a').text
            info = i.findAll('span')
            if len(info) == 1:
                rate = ''
                time = info[0].text.split()[0]
            elif len(info) == 2:
                rate = info[0]['title']
                time = info[1].text.split()[0]
            result[user] = [user, rate, time, comment]
        return json.dumps(result)
        
    def getReview(self, review):
        review = self.soup.findAll('div', {'class': 'review'})
        result = {}
        user, userUrl, rate, title, shortReview, time = '', '', '', '', '', ''
        for i in review:
            info = i.find('div', {'class': 'review-hd'}).find('h3').findAll('a')
            user = info[0]['title']
            userUrl = info[0]['href']
            title = info[len(info)-1].text
            rate = i.find('div', {'class': 'review-hd-info'}).find('span')['title']
            time = i.find('div', {'class': 'review-hd-info'}).text.split()[1]
            shortReview = i.find('div', {'class': 'review-short'}).find('span').text.replace('\n', '')
            result[user] = [user, userUrl, rate, title, shortReview, time]
        return json.dumps(result)