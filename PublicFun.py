#!/usr/bin/python
#coding=utf-8
import os
import urllib
import urllib2
import feedparser
from PyQt4.QtCore import *
from PyQt4.QtGui import *

Is_Login = False
Data_Base = 'ZReader_DataBase.db'
Rss_Image='image'+os.sep+'rss.png'
Unstarred_Image = 'image'+os.sep+'unstarred.png'
Unbroadcast_Image = 'image'+os.sep+'unbroadcast.png'
Starred_Image = 'image'+os.sep+'starred.png'
Broadcast_Image = 'image'+os.sep+'broadcast.png'
Cache_Dir = 'cache'

class Item(object):
    """从一个订阅feed地址获取的条目类，
    有id号，标题，原文链接，更新时间，内容，
    打上的标签，原feed地址"""
    
    def __init__(self):
        self.id = ''
        self.title = ''
        self.link = ''
        self.update_time = ''
        self.content = ''
        self.tags = []
        self.source_feed = ''
        
def setCenter(window):
    #将窗体置于屏幕中间
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    window.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

def feedParser(xml):
    #解析订阅条目
    d = feedparser.parse(xml)
    items_list = []
    for entry in d.entries:
        item =  Item()
        if hasattr(entry, 'id'):
            item.id = entry.id
        if hasattr(entry, 'updated'):
            item.update_time = entry.updated
        if hasattr(entry, 'link'):
            item.link = entry.link
        if hasattr(entry, 'title'):
            item.title = entry.title
        if hasattr(entry, 'summary'):
            item.content = entry.summary
        elif hasattr(entry, 'content'):
            item.content = entry.content[0]['value']
        if hasattr(entry, 'category'):
            item.tags = [tag['label'] for tag in entry.tags if tag['label']]
        if hasattr(entry, 'source'):
            item.source_feed = entry.source.id[27:]
        items_list.append(item)
    return items_list    

if __name__=='__main__':
    feedParser('src/moon.xml')