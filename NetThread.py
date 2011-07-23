#coding=utf-8
'''
Created on 2011-7-18

@author: monsterxx03
'''
import os
import urllib
import PublicFun
import GoogleApi
from PyQt4.QtCore import *

class LoginThread(QThread):
    """登入用线程"""
    def __init__(self,google_api,parent=None):
        QThread.__init__(self,parent)
        self.google_api = google_api

    def get_email_passwd(self,email,passwd):
        self.email = email
        self.passwd = passwd
        
    def run(self):
        try:
            self.google_api.get_auth_headers(self.email,self.passwd)
            PublicFun.Is_Login = True
            self.emit(SIGNAL('login_success'))
        except Exception,e:
            print e
            self.emit(SIGNAL('login_failure'))
            
class LoadingThread(QThread):
    """
    登入成功后进行加载的线程
    """
    
    def __init__(self,google_api):
        QThread.__init__(self)
        self.google_api = google_api
        self.flag = ''
        self.feed_url = ''
        self.subscription_list = []
        self.unread_list = []
        self.reading_list = []
        self.read_list = []
        self.starred_list = []
        self.broadcast_list = []
        self.items = []

    def run(self):
        try:
            if self.flag=="loading":
                self.subscription_list = self.google_api.get_subscription_list()
                self.unread_list = self.google_api.get_unread_list()[0]
                self.reading_list =self.google_api.get_reading_list()
            elif self.flag=="reading_list":
                self.read_list = self.google_api.get_reading_list()
            elif self.flag=="read_list":
                self.read_list = self.google_api.get_read_list()
            elif self.flag=="starred_list":
                self.starred_list = self.google_api.get_starred_items()
            elif self.flag=="broadcast_list":
                self.broadcast_list = self.google_api.get_broadcast_items()
            elif self.flag=='items':
                self.items = self.google_api.get_items(self.feed_url)
            self.emit(SIGNAL('get_list_success(QString)'),self.flag)
        except Exception,e:
           print e
           self.emit(SIGNAL('get_list_failure'))
           
class ImageThread(QThread):
    """下载一个条目中图片的线程"""
    def __init__(self,google_api):
        QThread.__init__(self)
        self.link_list = []
        self.img_list = []
        self.item= None
        self.google_api = google_api
        
    def run(self):
        self.img_list = []
        self.google_api.set_read(self.item.source_feed,self.item.id,'a')
        for link in self.link_list:
            filename = link[link.rfind('/')+1:]
            filename = os.path.join(os.getcwd(),PublicFun.Cache_Dir,filename)
            if os.path.exists(filename):
                self.img_list.append(filename)
                continue
            try:
                urllib.urlretrieve(link, filename)
                self.img_list.append(filename)
            except Exception,e:
                print e
                self.img_list.append("")
                continue
