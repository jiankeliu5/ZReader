#!/usr/bin/python
#coding=utf-8

import urllib2
import socket
import PublicFun
import GoogleApi
import NetThread
import Menu
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Login import Login
from ui_ZReader import  Ui_ZReader

socket.setdefaulttimeout(10)

class ZReader(QMainWindow):
    
    subscription_list = [] #订阅项的列表
    unread_list = []#未读项目统计列表
    reading_list = []#阅读列表
    read_list = [] #已读列表
    starred_list = [] #加星条目列表
    broadcast_list = [] #共享条目的列表
    
    def __init__(self,parent=None):
        super(ZReader,self).__init__(parent)

        self.ui = Ui_ZReader()
        self.ui.setupUi(self)

        self.updateUi()
        
        self.google_api = GoogleApi.Google_Api()
        self.login = Login(self.google_api)
        self.loadingThread = NetThread.LoadingThread(self.google_api)
        
        #订阅列表上的右键菜单
        self.feed_list_con_menu = Menu.Feed_list_Menu(self.ui.feedList)
        
        self.connect(self.loadingThread,SIGNAL('get_list_failure'),self.loadingFailure)
        self.connect(self.loadingThread,SIGNAL('get_list_success'),self.loadingSuccess)
        #登入成功后开始刷新订阅列表
        self.connect(self.login.loginThread, SIGNAL('login_success'),self.loading)
        

    def updateUi(self):
        PublicFun.setCenter(self)
        self.ui.progressBar.hide()
            
    def loading(self):
        self.ui.progressBar.show()
        self.loadingThread.start()
            
    def loadingFailure(self):
        self.ui.progressBar.hide()
        QMessageBox.information(self,u'failure',u'get the feed list failure',buttons=QMessageBox.Ok)
        
    def loadingSuccess(self):
        self.ui.feedList.clear()
        self.subscription_list = self.loadingThread.subscription_list
        self.unread_list = self.loadingThread.unread_list
        self.reading_list = self.loadingThread.reading_list
        self.read_list = self.loadingThread.read_list
        self.starred_list = self.loadingThread.starred_list
        self.broadcast_list = self.loadingThread.broadcast_list
        for item in self.subscription_list:
            title = item[1]
            if item[0] in self.unread_list.keys():
                title += '(%d)'%self.unread_list[item[0]]
            self.ui.feedList.addItem(QListWidgetItem(QIcon(PublicFun.Rss_Image),title))
        #加载reading-list到table中
        self.fill_table(self.reading_list)
        
        self.ui.progressBar.hide()   
        
    def fill_table(self,item_list):
    #用传入的条目列表填充tableWidget控件
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(len(item_list))
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setColumnWidth(0,50)
        self.ui.tableWidget.setColumnWidth(1,50)
        self.ui.tableWidget.setColumnWidth(2,450)
        self.ui.tableWidget.setColumnWidth(3,200)
        for index, item in enumerate(item_list):
            starredButton = QPushButton(QIcon(PublicFun.Unstarred_Image),'')
            starredButton.setFlat(True)
            broadcastButton = QPushButton(QIcon(PublicFun.Unbroadcast_Image),'')
            broadcastButton.setFlat(True)
            starredButton.setCheckable(True)
            broadcastButton.setCheckable(True)
            if 'starred' in item.tags:
                starredButton.setChecked(True)
                starredButton.setIcon(QIcon(PublicFun.Starred_Image))
            if 'broadcast' in item.tags:
                broadcastButton.setChecked(True)
                broadcastButton.setIcon(QIcon(PublicFun.Broadcast_Image))
            title_item = QTableWidgetItem(item_list[index].title)
            time_item = QTableWidgetItem(item_list[index].update_time)
            if 'read' not in item.tags:
                font = QFont()
                #font.setBold(True)
                font.setItalic(True)
                title_item.setFont(font)
                time_item.setFont(font)
            self.ui.tableWidget.setCellWidget(index,0,starredButton)
            self.ui.tableWidget.setCellWidget(index,1,broadcastButton)
            self.ui.tableWidget.setItem(index,2,title_item)
            self.ui.tableWidget.setItem(index,3,time_item)
                
    @pyqtSlot()
    def on_actionLogin_Google_Account_triggered(self):
        if not PublicFun.Is_Login:
            self.login.show()
        else:
            QMessageBox.information(self,u'information',u'you have already logined',buttons = QMessageBox.Ok)
            
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self,index):
        if index==0:
            self.fill_table(self.reading_list)
        elif index==1:
            self.fill_table(self.read_list)
        elif index==2:
            self.fill_table(self.starred_list)
        elif index==3:
            self.fill_table(self.broadcast_list)
            
    @pyqtSlot(QListWidgetItem)
    def on_feedList_itemClicked(self,item):
        index = self.ui.feedList.currentRow()
        feed_url = self.subscription_list[index][0]
        try:
            item_list = self.google_api.get_items(feed_url)
            self.fill_table(item_list)
        except urllib2.HTTPError,e:
            print e.code
        
    @pyqtSlot(QPoint)
    def on_feedList_customContextMenuRequested(self,point):
        point = self.ui.feedList.mapToGlobal(point)
        self.feed_list_con_menu.popup(point)
        

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    zReader = ZReader()
    zReader.show()
    sys.exit(app.exec_())
        
