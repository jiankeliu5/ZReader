#coding=utf-8
'''
Created on 2011-7-19

@author: monsterxx03
'''
import feedparser

d = feedparser.parse('reading-list.xml')
title_list = []
link_list = []
time_list = []
content_list = []
for entry in d.entries:
    time_list.append(entry.updated)
    print entry.title
    link_list.append(entry.link)
    title_list.append(entry.title)
    if hasattr(entry, 'summary'):
        content_list.append(entry.summary)
    elif hasattr(entry, 'content'):
        content_list.append(entry.content[0]['value'])
    else:
        content_list.append('')
