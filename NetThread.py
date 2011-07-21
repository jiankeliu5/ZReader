#coding=utf-8
'''
Created on 2011-7-18

@author: monsterxx03
'''
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
    subscription_list = []
    unread_list = []
    reading_list = []
    read_list = []
    starred_list = []
    broadcast_list = []
    
    def __init__(self,google_api):
        QThread.__init__(self)
        self.google_api = google_api

    def run(self):
        try:
            self.subscription_list = self.google_api.get_subscription_list()
            self.unread_list = self.google_api.get_unread_list()[0]
            self.reading_list = self.google_api.get_reading_list()
            self.read_list = self.google_api.get_read_list()
            self.starred_list = self.google_api.get_starred_items()
            self.broadcast_list = self.google_api.get_broadcast_items()
            self.emit(SIGNAL('get_list_success'))
        except Exception,e:
           print e
           self.emit(SIGNAL('get_list_failure'))

class GetItemsThread(QThread):
    """
    由feed地址获取条目列表的线程
    """
    pass