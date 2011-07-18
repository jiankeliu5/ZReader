#!/usr/bin/python
#coding=utf-8
import os
import urllib
import urllib2
from xml.etree import ElementTree
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

class Google_Api():
    """Google Reader Api Function"""

    AUTH_URL = 'https://www.google.com/accounts/ClientLogin'

    @classmethod
    def get_auth_headers(self,email,passwd):
        #获取认证后的http头
        global Author_Headers

        """get http headers including auth"""

        postdata = urllib.urlencode({'Email':email,'Passwd':passwd,'service':'reader'})
        req = urllib2.Request(self.AUTH_URL,postdata)
        auth_value = urllib2.urlopen(req).read().split()[2][5:]
        Author_Headers = {'Authorization':'GoogleLogin auth=%s'%auth_value}

    @classmethod
    def get_subscription_list(self):
        #获取订阅列表
        req = urllib2.Request("http://www.google.com/reader/api/0/subscription/list",headers=Author_Headers)
        s = urllib2.urlopen(req).read()
        root = ElementTree.fromstring(s)
        object_list = root.getiterator('object')
        title_list = []
        feed_addr_list = []
        home_page_list = []
        for object in object_list:
            for item in object:
                if item.get('name')=='id':
                    feed_addr_list.append(item.text)
                if item.get('name')=='title':
                    title_list.append(item.text)
                if item.get('name')=='htmlUrl':
                    home_page_list.append(item.text)
        return feed_addr_list,title_list,home_page_list