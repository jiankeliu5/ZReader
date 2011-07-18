#!/usr/bin/python
#coding=utf-8
import os
import urllib
import urllib2
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

