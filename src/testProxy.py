'''
Created on 2011-7-18

@author: monsterxx03
'''
import urllib2
import GoogleApi

google = GoogleApi.Google_Api()
google.get_auth_headers('','')
print 1
req = urllib2.Request('http://www.google.com/reader/atom/user/-/state/com.google/reading-list',
                      headers=google.Author_Headers)
print urllib2.urlopen(req).read()
