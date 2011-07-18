#!/usr/bin/python
#coding=utf-8
import socket
import sqlite3
import NetThread
import PublicFun
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_Login import Ui_Login

socket.setdefaulttimeout(10)

class Login(QWidget):
    def __init__(self,parent=None):
        super(Login,self).__init__(parent)

        self.ui = Ui_Login()
        self.ui.setupUi(self)
        
        self.updateUi()
        self.setValidator()
        
        #登入线程
        self.loginThread = NetThread.LoginThread()
        self.connect(self.loginThread,SIGNAL('login_failure'),self.login_failure)
        self.connect(self.loginThread, SIGNAL('login_success'),self.login_success)
        

    def updateUi(self):
        PublicFun.setCenter(self)
        
    def setValidator(self):
        email_rx = QRegExp("[\\w\.?]+@\\w+\.\\w+")
        email_valid = QRegExpValidator(email_rx,self)
        self.ui.emailLineEdit.setValidator(email_valid)
        passwd_rx = QRegExp("\\w{6,}")
        passwd_valid = QRegExpValidator(passwd_rx,self)
        self.ui.passwdLineEdit.setValidator(passwd_valid)
        
    def  login_failure(self):
        QMessageBox.warning(self,u'waring!',u'Sorry,login failure',buttons=QMessageBox.Ok)
        self.ui.loginButton.setEnabled(True)
        self.ui.exitButton.setEnabled(True)
        self.ui.loginButton.setText(u'Login')
        
    def login_success(self):
        if self.ui.checkBox.isChecked():
            con = sqlite3.connect(PublicFun.Data_Base)
            cursor = con.cursor()
            sql ="insert into account values(?,?)"
            cursor.execute(sql,(str(self.email),str(self.passwd)))
            con.commit()
            cursor.close()
            con.close()
        self.close()
        
    def showEvent(self,event):
        con = sqlite3.connect(PublicFun.Data_Base)
        cursor = con.cursor()
        cursor.execute('select * from account')
        ep = cursor.fetchone()
        if ep:
            email,passwd = ep
            self.ui.emailLineEdit.setText(email)
            self.ui.passwdLineEdit.setText(passwd)
        con.close()
        
    @pyqtSlot()
    def on_loginButton_clicked(self):
        self.email = self.ui.emailLineEdit.text()
        self.passwd = self.ui.passwdLineEdit.text()
        if self.email=='' or self.passwd=='':
            QMessageBox.warning(self,u'waring!',u'email and password can\'t be empty',buttons=QMessageBox.Ok)
            return
        self.ui.loginButton.setDisabled(True)
        self.ui.loginButton.setText(u'waiting....')
        self.ui.exitButton.setDisabled(True)
        self.loginThread.get_email_passwd(self.email,self.passwd)
        self.loginThread.start()
        

if __name__=='__main__':
    import sys

    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())
