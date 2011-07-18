#coding=utf-8
'''
Created on 2011-7-18

@author: monsterxx03
'''
import urllib
import urllib2
from xml.etree import ElementTree

class Google_Api(object):
    """Google Reader Api Function"""

    AUTH_URL = 'https://www.google.com/accounts/ClientLogin'
    TOKEN_URL = 'http://www.google.com/reader/api/0/token'
    host=None
    type='http'

    @classmethod
    def get_auth_headers(self,email,passwd,host=host,type=type):
        #获取认证后的http头

        """get http headers including auth"""

        postdata = urllib.urlencode({'Email':email,'Passwd':passwd,'service':'reader'})
        req = urllib2.Request(self.AUTH_URL,postdata)
        if host:
            req.set_proxy(host, type)
        f = urllib2.urlopen(req)
        auth_value = f.read().split()[2][5:]
        f.close()
        self.Author_Headers = {'Authorization':'GoogleLogin auth=%s'%auth_value}
        
    @classmethod
    def get_token(self,host=host,type=type):
        #获取token用以进行编辑操作
        req = urllib2.Request(self.TOKEN_URL,self.Author_Headers)
        if host:
            req.set_proxy(host, type)
        f = urllib2.urlopen(req)
        self.token = f.read()
        f.close()

    @classmethod
    def get_subscription_list(self,host=host,type=type):
        #获取订阅列表
        req = urllib2.Request("http://www.google.com/reader/api/0/subscription/list",headers=self.Author_Headers)
        if host:
            req.set_proxy(host, type)
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
        return feed_addr_list,title_list,home_page_list
    
    @classmethod
    def get_all_unread_list(self,host=host,type=type):
        #获取所有未读计数列表
        #返回(feed地址,未读数)构成的列表和总未读数
        req = urllib2.Request("http://www.google.com/reader/api/0/unread-count?output=xml&all=true",headers=self.Author_Headers)
        if host:
            req.set_proxy(host, type)
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
        return id_count_list,total_count
    
    @classmethod
    def get_items(self,feed_url,n=20,host=host,type=type):
        #由指定的订阅地址，和返回条目数获取该站条目列表
        req_url = "http://www.google.com/reader/atom/%s?n=%d"%(feed_url,n)
        req = urllib2.Request(req_url,headers=self.Author_Headers)
        if host:
            req.set_proxy(host, type)
        f = urllib2.urlopen(req)
        xml = f.read()
        f.close()
    
