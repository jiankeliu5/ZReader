#coding=utf-8
'''
Created on 2011-7-19

@author: monsterxx03
'''
import feedparser

class Item(object):
    
    def __init__(self):
        self.id = ''
        self.title = ''
        self.link = ''
        self.update_time = ''
        self.content = ''
        self.tags = []
        self.source_feed = ''
        
def setCenter(window):
    #将窗体置于屏幕中间
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    window.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

def feedParser(xml):
    #解析订阅条目
    d = feedparser.parse(xml)
    items_list = []
    for entry in d.entries:
        item = Item()
        if hasattr(entry, 'id'):
            item.id = entry.id
            print entry.id
        if hasattr(entry, 'updated'):
            item.update_time = entry.updated
        if hasattr(entry, 'link'):
            item.link = entry.link
        if hasattr(entry, 'title'):
            item.title = entry.title
        if hasattr(entry, 'summary'):
            item.content = entry.summary
        elif hasattr(entry, 'content'):
            item.content = entry.content[0]['value']
        if hasattr(entry, 'category'):
            item.tags = [tag['label'] for tag in entry.tags if tag['label']]
        if hasattr(entry, 'source'):
            item.source_feed = entry.source.id[27:]
        items_list.append(item)
    return items_list 

feedParser('moon.xml')
