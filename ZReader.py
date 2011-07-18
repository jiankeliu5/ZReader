#!/usr/bin/python
#coding=utf-8

import PublicFun
import NetThread
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Login import Login
from ui_ZReader import  Ui_ZReader

class ZReader(QMainWindow):
    def __init__(self,parent=None):
        super(ZReader,self).__init__(parent)

        self.ui = Ui_ZReader()
        self.ui.setupUi(self)

        self.updateUi()
        
        self.refreshListThread = NetThread.GetListThread()
        self.login = Login()
        self.connect(self.refreshListThread,SIGNAL('get_list_failure'),self.refreshListFailure)
        self.connect(self.refreshListThread,SIGNAL('get_list_success'),self.refreshListSuccess)
        #登入成功后开始刷新订阅列表
        self.connect(self.login.loginThread, SIGNAL('login_success'),self.refreshList)
        

    def updateUi(self):
        PublicFun.setCenter(self)
        self.ui.progressBar.hide()
        tableList = [self.ui.ReadingTable,self.ui.StarredTable,self.ui.SharedTable]
        for table in tableList:
            table.setColumnWidth(0,15)
            table.setColumnWidth(1,15)
            table.setColumnWidth(2,self.width()/2)
            
    def refreshList(self):
        self.ui.progressBar.show()
        self.refreshListThread.start()
            
    def refreshListFailure(self):
        self.ui.progressBar.hide()
        QMessageBox.information(self,u'failure',u'get the feed list failure',buttons=QMessageBox.Ok)
        
    def refreshListSuccess(self):
        self.ui.feedList.clear()
        for item in self.refreshListThread.Feed_List:
            self.ui.feedList.addItem(QListWidgetItem(QIcon(PublicFun.Rss_Image),item[1]))
        self.ui.progressBar.hide()    
            
    @pyqtSlot()
    def on_actionLogin_Google_Account_triggered(self):
        if not PublicFun.Is_Login:
            self.login.show()
        else:
            QMessageBox.information(self,u'information',u'you have already logined',buttons = QMessageBox.Ok)




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    zReader = ZReader()
    zReader.show()
    sys.exit(app.exec_())
        
