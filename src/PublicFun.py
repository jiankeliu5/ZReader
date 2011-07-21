#!/usr/bin/python
#coding=utf-8
import os
import urllib
import urllib2
import feedparser
from PyQt4.QtCore import *
from PyQt4.QtGui import *

Author_Headers = ''
Is_Login = False
Data_Base = 'ZReader_DataBase.db'
Rss_Image = 'image' + os.sep + 'rss.jpg'

class Item(object):
    
    def __init__(self):
        self.id = ''
        self.title = ''
        self.link = ''
        self.update_time = ''
        self.content = ''
        self.tags = []
        
    

def setCenter(window):
    #将窗体置于屏幕中间
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    window.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

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
        items_list.append(item)
    return items_list

if __name__=='__main__':
    items_list = feedParser('Gis.xml')
    for item in items_list:
        print item.tags