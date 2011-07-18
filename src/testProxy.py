'''
Created on 2011-7-18

@author: monsterxx03
'''
import urllib2

req = urllib2.Request('http://www.google.com/reader/view/feed/http%3A%2F%2Fwww.appinn.com%2Ffeed%2F')
host = "127.0.0.1:8000"
req.set_proxy(host, 'http')
print urllib2.urlopen(req).read()
