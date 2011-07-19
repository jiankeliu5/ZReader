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
Rss_Image='image'+os.sep+'rss.jpg'

def setCenter(window):
    #将窗体置于屏幕中间
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    window.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

def feedParser(xml):
    #解析订阅条目
    d = feedparser.parse(xml)
    id_list = []
    title_list = []
    link_list = []
    time_list = []
    content_list = []
    for entry in d.entries:
        if hasattr(entry, 'id'):
            id_list.append(entry.id)
        if hasattr(entry, 'updated'):
            time_list.append(entry.updated)
        else:
            time_list.append('')
        if hasattr(entry, 'link'):
            link_list.append(entry.link)
        else:
            link_list.append('')
        if hasattr(entry,'title'):
            title_list.append(entry.title)
        else:
            title_list.append('')
        if hasattr(entry, 'summary'):
            content_list.append(entry.summary)
        elif hasattr(entry, 'content'):
            content_list.append(entry.content[0]['value'])
        else:
            content_list.append('')
    return id_list,title_list,link_list,time_list,content_list
