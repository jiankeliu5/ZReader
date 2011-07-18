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
    def __init__(self,parent=None):
        QThread.__init__(self,parent)

    def get_email_passwd(self,email,passwd):
        self.email = email
        self.passwd = passwd
        
    def run(self):
        try:
            GoogleApi.Google_Api.get_auth_headers(self.email,self.passwd)
            PublicFun.Is_Login = True
            self.emit(SIGNAL('login_success'))
        except Exception,e:
            print e
            self.emit(SIGNAL('login_failure'))
            
class GetListThread(QThread):
    """
    获取feed列表的线程
    """
    Feed_List = []
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        try:
            feed_addr_list,title_list,home_page_list = GoogleApi.Google_Api.get_subscription_list()
            self.Feed_List = zip(feed_addr_list,title_list,home_page_list)
            self.emit(SIGNAL('get_list_success'))
        except Exception,e:
            print e
            self.emit(SIGNAL('get_list_failure'))
