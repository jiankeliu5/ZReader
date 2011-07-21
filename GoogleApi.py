#coding=utf-8
'''
Created on 2011-7-18

@author: monsterxx03
'''
import urllib
import urllib2
import socket
import PublicFun
from xml.etree import ElementTree


socket.setdefaulttimeout(10)

class Google_Api(object):
    """Google Reader Api Function"""

    AUTH_URL = 'https://www.google.com/accounts/ClientLogin'
    TOKEN_URL = 'http://www.google.com/reader/api/0/token'
    ClIENT = 'ZReader'
    
    def __init__(self,host=None,type='http'):
        self.Author_Headers= {}
        self.token = ''
        self.host=host
        self.type=type

    def get_auth_headers(self,email,passwd):
        #获取认证后的http头

        """get http headers including auth"""

        postdata = urllib.urlencode({'Email':email,'Passwd':passwd,'service':'reader','source':self.ClIENT})
        req = urllib2.Request(self.AUTH_URL,postdata)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        auth_value = f.read().split()[2][5:]
        f.close()
        self.Author_Headers = {'Authorization':'GoogleLogin auth=%s'%auth_value}
        
    def get_token(self):
        #获取token用以进行编辑操作
        req = urllib2.Request(self.TOKEN_URL+'?client='+self.ClIENT,headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        self.token = f.read()
        f.close()

    def get_subscription_list(self):
        #获取订阅列表
        req = urllib2.Request("http://www.google.com/reader/api/0/subscription/list?client=%s"%self.ClIENT,headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        s = f.read()
        f.close()
        root = ElementTree.fromstring(s)
        object_list = root.iter('object')
        title_list = []
        feed_addr_list = []
        home_page_list = []
        for object in object_list:
            for item in object:
                if item.get('name')=='id':
                    feed_addr_list.append(item.text)
                if item.get('name')=='title':
                    title_list.append(item.text)
                if item.get('name')=='htmlUrl':
                    home_page_list.append(item.text)
        return zip(feed_addr_list,title_list,home_page_list)
    
    def get_read_list(self,n=20):
        #获取已读项列表
        req = urllib2.Request('http://www.google.com/reader/atom/user/-/state/com.google/read?client=%s&n=%d'%(self.ClIENT,n),
                              headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        xml = f.read()
        items_list = PublicFun.feedParser(xml)
        return items_list
    
    def get_unread_list(self):
        #获取所有未读计数列表
        #返回(feed地址,未读数)构成的列表和总未读数
        req = urllib2.Request("http://www.google.com/reader/api/0/unread-count?output=xml&all=true&client=%s"%self.ClIENT,headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        xml = f.read()
        f.close()
        root = ElementTree.fromstring(xml)
        object_list = root.iter('object')
        id_list = []
        count_list = []
        for object in object_list:
            id_list.append(object.iter('string').next().text)
            it = object.iter('number')
            tag = it.next()
            if tag.get('name')=='count':
                count_list.append(int(tag.text))
            else:
                it=it.next()
                count_list.append(int(it.text))
        total_count = max(count_list)
        id_count_list = zip(id_list,count_list)
        id_count_list = [ item for item in id_count_list if item[0].startswith('feed')]
        id_count_list = [(item[0],item[1]) for item in id_count_list]
        return dict(id_count_list),total_count
    
    def get_items(self,feed_url,n=20):
        #由指定的订阅地址，和返回条目数获取该站条目列表
        req_url = "http://www.google.com/reader/atom/%s?n=%d"%(urllib.quote(feed_url),n)
        req = urllib2.Request(req_url,headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        xml = f.read()
        f.close()
        items_list = PublicFun.feedParser(xml)
        return items_list
    
    def search_feed(self,item):
        #搜索供稿
        item = urllib.quote(item)
        req = urllib2.Request('http://www.google.com/reader/directory/search?q=%s&client=%s'%(item,self.ClIENT),
                              headers=self.Author_Headers)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
        return result
    
    def get_starred_items(self,n=9999):
        #获取加星条目列表
        req = urllib2.Request('http://www.google.com/reader/atom/user/-/state/com.google/starred?client=%s&n=%d'%(self.ClIENT,n),
                              headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        xml = f.read()
        f.close()
        items_list = PublicFun.feedParser(xml)
        return items_list
        
    def get_broadcast_items(self,n=9999):
        #获取共享的条目列表
        req = urllib2.Request('http://www.google.com/reader/atom/user/-/state/com.google/broadcast?client=%s&n=%d'%(self.ClIENT,n),
                              headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        xml = f.read()
        f.close()
        items_list = PublicFun.feedParser(xml)
        return items_list
        
    def get_reading_list(self,n=100):
        #获取阅读列表
        req = urllib2.Request('http://www.google.com/reader/atom/user/-/state/com.google/reading-list?client=%s&n=%d'%(self.ClIENT,n),
                              headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        xml = f.read()
        f.close()
        items_list = PublicFun.feedParser(xml)
        return items_list
        
    
    def add_a_feed(self,feed_url):
        #添加一个订阅
        if not self.token:
            self.get_token()
        req = urllib2.Request('http://www.google.com/reader/api/0/subscription/quickadd?client='%self.ClIENT,
                              data=urllib.urlencode({'quickadd':feed_url,'T':self.token}),headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
        print result
        if result.find('moreResults')!=-1:
            self.search_feed(feed_url)
        elif result.find('streamId')!=-1:
            return True
            
    def remove_a_feed(self,feed_url):
        #取消一个订阅
        if not self.token:
            self.get_token()
        req = urllib2.Request('https://www.google.com/reader/api/0/subscription/edit?client='%self.ClIENT,
                              data=urllib.urlencode({'s':feed_url,'T':self.token,'ac':'unsubscribe'}),headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
        if result=='OK':
            return True
        
    def starred_a_item(self,feed_url,id,a_or_r='a'):
        #给一个条目加注星标,a是添加星标，r是移除星标
        if not self.token:
            self.get_token()
        postdata = urllib.urlencode({a_or_r:'user/-/state/com.google/starred','async':'true','s':feed_url,'i':id,'T':self.token})
        req = urllib2.Request('http://www.google.com/reader/api/0/edit-tag?client=%s'%self.ClIENT,data=postdata,
                              headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
        if result=='OK':
            return True
        
    def broadcast_a_item(self,feed_url,id,a_or_r='a'):
        #共享一个条目,a是共享，r是取消共享
        if not self.token:
            self.get_token()
        postdata = urllib.urlencode({a_or_r:'user/-/state/com.google/starred','async':'true','s':feed_url,'i':id,'T':self.token})
        req = urllib2.Request('http://www.google.com/reader/api/0/edit-tag?client=%s'%self.ClIENT,data=postdata,
                              headers=self.Author_Headers)
        if self.host:
            req.set_proxy(self.host, self.type)
        f = urllib2.urlopen(req)
        result = f.read()
        f.close()
        if result=='OK':
            return True
        
    def set_proxy(self,host='127.0.0.1:8000',type='http'):
        self.host=host
        self.type=type
        
if __name__=='__main__':
    url= 'feed/http://feed.google.org.cn'
    g = Google_Api()
    g.get_auth_headers('xyj.asmy@gmail.com','19900608abc')
    print 1
    #g.set_proxy(host='127.0.0.1:8000',type='http')
    g.get_items('feed/http://feed.williamlong.info/')
            
        
    
