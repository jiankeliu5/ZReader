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
    
    def __init__(self, parent=None):
        super(ZReader, self).__init__(parent)
        
        self.current_list = []#tabWidget当前显示的列表
        self.subscription_list = [] #订阅地址的列表
        self.unread_list = [] #未读数统计列表

        self.ui = Ui_ZReader()
        self.ui.setupUi(self)

        self.updateUi()
        
        self.google_api = GoogleApi.Google_Api()
        self.login = Login(self.google_api)
        self.loadingThread = NetThread.LoadingThread(self.google_api)
        #订阅列表上的右键菜单
        self.feed_list_con_menu = Menu.Feed_list_Menu(self.ui.feedList)
        
        self.connect(self.loadingThread, SIGNAL('get_list_failure'), self.loadingFailure)
        self.connect(self.loadingThread, SIGNAL('get_list_success(QString)'), self.loadingSuccess)
        #登入成功后开始刷新订阅列表
        self.connect(self.login.loginThread, SIGNAL('login_success'), self.loading)
        

    def updateUi(self):
        PublicFun.setCenter(self)
        self.ui.progressBar.hide()
            
    def loading(self):
        self.ui.progressBar.show()
        self.loadingThread.flag='loading'
        self.loadingThread.start()
            
    def loadingFailure(self):
        self.ui.progressBar.hide()
        QMessageBox.information(self, u'failure', u'网络太差或遭遇GFW T T', buttons=QMessageBox.Ok)
        
    def loadingSuccess(self,flag):
        #登入成功或切换显示视图的线程成功后加载到tableWidget
        if flag=='loading':
            self.ui.feedList.clear()
            self.subscription_list = self.loadingThread.subscription_list
            self.unread_list = self.loadingThread.unread_list
            self.current_list = self.loadingThread.reading_list
            for item in self.subscription_list:
                title = item[1]
                if item[0] in self.unread_list.keys():
                    title += '(%d)' % self.unread_list[item[0]]
                self.ui.feedList.addItem(QListWidgetItem(QIcon(PublicFun.Rss_Image), title))
            #加载reading-list到table中
            self.fill_table(self.current_list)
        elif flag=='reading_list':
            self.current_list = self.loadingThread.reading_list
            self.fill_table(self.current_list)
        elif flag=='read_list':
            self.current_list = self.loadingThread.read_list
            self.fill_table(self.current_list)
        elif flag=='starred_list':
            self.current_list = self.loadingThread.starred_list
            self.fill_table(self.current_list)
        elif flag== 'broadcast_list':
            self.current_list = self.loadingThread.broadcast_list
            self.fill_table(self.current_list)
        elif flag=='items':
            self.current_list=self.loadingThread.items
            self.fill_table(self.current_list)
        self.ui.progressBar.hide()
        
    def fill_table(self, item_list):
    #用传入的条目列表填充tableWidget控件
        self.current_list = item_list
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(len(item_list))
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setColumnWidth(0, 50)
        self.ui.tableWidget.setColumnWidth(1, 50)
        self.ui.tableWidget.setColumnWidth(2, 450)
        self.ui.tableWidget.setColumnWidth(3, 200)
        for index, item in enumerate(item_list):
            starred_item = QTableWidgetItem(QIcon(PublicFun.Unstarred_Image), '')
            broadcast_item = QTableWidgetItem(QIcon(PublicFun.Unbroadcast_Image), '')
            if 'starred' in item.tags:
                starred_item.setIcon(QIcon(PublicFun.Starred_Image))
            if 'broadcast' in item.tags:
                broadcast_item.setIcon(QIcon(PublicFun.Broadcast_Image))
            title_item = QTableWidgetItem(item_list[index].title)
            time_item = QTableWidgetItem(item_list[index].update_time)
            if 'read' not in item.tags:
                font = QFont()
                #font.setBold(True)
                font.setItalic(True)
                title_item.setFont(font)
                time_item.setFont(font)
            self.ui.tableWidget.setItem(index, 0, starred_item)
            self.ui.tableWidget.setItem(index, 1, broadcast_item)
            self.ui.tableWidget.setItem(index, 2, title_item)
            self.ui.tableWidget.setItem(index, 3, time_item)
    
    def star_item(self,column,row):
        #给条目加星
        item = self.current_list[row]
        starred_item = self.ui.tableWidget.item(row, column)
        if 'starred' not in item.tags: #给条目加星
            starred_item.setIcon(QIcon(PublicFun.Starred_Image))
            item.tags.append('starred')
            flag = self.google_api.starred_a_item(item.source_feed, item.id, 'a')
            if flag:
                self.current_list[row] = item
        else: #取消条目加星
            starred_item.setIcon(QIcon(PublicFun.Unstarred_Image))
            item.tags.remove('starred')
            flag = self.google_api.starred_a_item(item.source_feed, item.id, 'r')
            if flag:
                self.current_list[row] = item
                
    def broadcast_item(self,column,row):
        #共享条目
        item = self.current_list[row]
        broadcast_item = self.ui.tableWidget.item(row, column)
        if 'broadcast' not in item.tags: #共享条目
            broadcast_item.setIcon(QIcon(PublicFun.Broadcast_Image))
            item.tags.append('broadcast')
            flag = self.google_api.broadcast_a_item(item.source_feed, item.id, 'a')    
            if flag:
                self.current_list[row] = item
        else:#取消共享
            broadcast_item.setIcon(QIcon(PublicFun.Unbroadcast_Image))
            item.tags.remove('broadcast')
            flag = self.google_api.broadcast_a_item(item.source_feed, item.id, 'r')
            if flag:
                self.current_list[row] = item
        
    @pyqtSlot()
    def on_actionLogin_Google_Account_triggered(self):
        #登入google账户
        if not PublicFun.Is_Login:
            self.login.show()
        else:
            QMessageBox.information(self, u'information', u'you have already logined', buttons=QMessageBox.Ok)
            
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        #显示视图中选择项改变时决定用loadingThread来更新哪个列表
        if not PublicFun.Is_Login:
            return
        self.ui.progressBar.show()
        if index == 0:
            self.loadingThread.flag='reading_list'
            self.loadingThread.start()
        elif index == 1:
            self.loadingThread.flag ='read_list'
            self.loadingThread.start()
        elif index == 2:
            self.loadingThread.flag='starred_list'
            self.loadingThread.start()
        elif index == 3:
            self.loadingThread.flag='broadcast_list'
            self.loadingThread.start()
            
    @pyqtSlot(QListWidgetItem)
    def on_feedList_itemClicked(self, item):
        #feed列表中的项被点击时发生
        self.ui.progressBar.show()
        index = self.ui.feedList.currentRow()
        feed_url = self.subscription_list[index][0]
        self.loadingThread.flag="items"
        self.loadingThread.feed_url = feed_url
        self.loadingThread.start()
        
    @pyqtSlot(QPoint)
    def on_feedList_customContextMenuRequested(self, point):
        point = self.ui.feedList.mapToGlobal(point)
        self.feed_list_con_menu.popup(point)

    @pyqtSlot(QTableWidgetItem)
    def on_tableWidget_itemClicked(self, item):
        #tableWidget中项被点击时发生
        column = item.column()
        row = item.row()
        if column == 0: #点击加星按钮
            self.star_item(column, row)
        if column == 1: #点击共享按钮
            self.broadcast_item(column, row)
        if column == 2:
            #浏览条目
            pass

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    zReader = ZReader()
    zReader.show()
    sys.exit(app.exec_())
        
