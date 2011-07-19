#!/usr/bin/python
#coding=utf-8

import PublicFun
import NetThread
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Login import Login
from ui_ZReader import  Ui_ZReader

class ZReader(QMainWindow):
    
    subscription_list = []
    unread_list = []
    reading_list = []
    read_list = []
    starred_list = []
    broadcast_list = []
    
    def __init__(self,parent=None):
        super(ZReader,self).__init__(parent)

        self.ui = Ui_ZReader()
        self.ui.setupUi(self)

        self.updateUi()
        
        self.loadingThread = NetThread.LoadingThread()
        self.login = Login()
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
        for item in self.reading_list:
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
        print len(item_list)
        for index, item in enumerate(item_list):
            starredButton = QPushButton()
            broadcastButton = QPushButton()
            self.ui.tableWidget.setCellWidget(index,0,starredButton)
            self.ui.tableWidget.setCellWidget(index,1,broadcastButton)
            self.ui.tableWidget.setItem(index,2,QTableWidgetItem(item_list[index][1]))
            self.ui.tableWidget.setItem(index,3,QTableWidgetItem(item_list[index][3]))
                
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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    zReader = ZReader()
    zReader.show()
    sys.exit(app.exec_())
        
