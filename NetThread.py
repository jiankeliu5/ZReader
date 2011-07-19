#coding=utf-8
'''
Created on 2011-7-18

@author: monsterxx03
'''
import PublicFun
import GoogleApi
from PyQt4.QtCore import *

google_api = GoogleApi.Google_Api()

class LoginThread(QThread):
    """登入用线程"""
    def __init__(self,parent=None):
        QThread.__init__(self,parent)

    def get_email_passwd(self,email,passwd):
        self.email = email
        self.passwd = passwd
        
    def run(self):
        try:
            google_api.get_auth_headers(self.email,self.passwd)
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
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        try:
            self.subscription_list = google_api.get_subscription_list()
            self.unread_list = google_api.get_unread_list()[0]
            self.reading_list = google_api.get_reading_list()
            self.read_list = google_api.get_read_list()
            self.starred_list = google_api.get_starred_items()
            self.broadcast_list = google_api.get_broadcast_items()
            self.emit(SIGNAL('get_list_success'))
        except Exception,e:
            print e
            self.emit(SIGNAL('get_list_failure'))
