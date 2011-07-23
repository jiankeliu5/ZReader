#coding=utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Feed_list_Menu(QMenu):
    
    def __init__(self,parent=None):
        QMenu.__init__(self,parent)
        
        self.add_feed_action = self.addAction(u"添加订阅")
        self.delete_feed_action = self.addAction(u"删除订阅")