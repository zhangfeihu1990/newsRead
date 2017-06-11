# -*- encoding:UTF-8 -*-
import urllib2
import urllib
from bs4 import BeautifulSoup
import json
import re
import time
import simplejson
import sys

from model import News
from mongoalchemy.session import Session

reload(sys)
sys.setdefaultencoding('utf-8')

#下载网页内容
def download(url, user_agent="wswp"):
  print "开始获取"
  headers = {"User-agent":user_agent}  #设置用户代理
  request = urllib2.Request(url,headers=headers)
  html = None
  try:
      html = urllib2.urlopen(request).read()
  except urllib2.URLError as e:
      print e
  return html

#url链接的获取新闻
def get_news_content(url):
    html = download(url)
    soup = BeautifulSoup(html,"html.parser")
   # print soup.prettify("utf-8")
    print soup.find(attrs={"class":"pg-headline"})
    title = soup.find(attrs={"class":"pg-headline"})
    print soup.find(attrs={"class":"metadata__byline__author"})
    author = soup.find(attrs={"class":"metadata__byline__author"})
    print soup.find(attrs={"class":"update-time"})
    update_time = soup.find(attrs={"class":"update-time"})
    contents = soup.find_all(attrs={"class":"zn-body__paragraph"})
    content = ""
    for i in contents:
      print i.text
      content += i.text

    #存入mongoDB
    session = Session.connect('runoob')
    #session.clear_collection(News)

    news = News(title=str(title), author=str(author), update_time=str(update_time),content=str(content))
    print news.title
    session.save(news)
    print '查询结果'

    result = session.query(News).skip(3).limit(2)
    for news in session.query(News).skip(3).limit(2):
      print news.title,news.update_time

#crow_cnn()

#获取首页中所有新闻的url
def get_news_url(url,site):
    html = download(url)     #获取网站首页
    soup = BeautifulSoup(html,"html.parser")
    print soup.prettify("utf-8")
    if site=="wp":
      print "源自wp"
      storys = soup.find_all(attrs={"moat-id":"homepage/story"})
      print storys
      for story in storys:
        web_headline = story.find(attrs={"data-pb-field":"web_headline"})
        summary = story.find(attrs={"data-pb-field":"summary"})
        if web_headline:
          print "标题：",web_headline.text
        if summary:
          print "简介：",summary.text
    elif site=='cnn':
      print "源自cnn"
      cnn = soup.find_all("script")
      for i in cnn:            #打印所有js
          print "i type:",type(i)
          data=re.findall(r".*contentModel = (.*)\;\<\/script\>",str(i)) #新闻相关的json，获取后是字符串
          if data:
            dd = re.sub(r'\s+', ' ', data[0])     #去除掉多余空格
            data= simplejson.dumps(dd)
            print "-------data type:" ,type(data)
            content = simplejson.loads(data,encoding='utf-8')
            print content
            a = content.split(',')
            print "个数%d",len(a)

            uri_list=[]    #存放页面中所有uri
            url_list = []     #存放html为后缀的url
            for k in range(0,len(a)):
                print a[k]
                b = a[k].split(":")
                if '{"uri"' in str(b[0]):  #到页面中所有uri放到uri_list
                    uri_list.append(b[1])
            print "mydic:",uri_list

            #构成绝对路径，并只保留html
            for j in range(0,len(uri_list)):
                url = "http://edition.cnn.com/"+str(uri_list[j]).strip('"') #去除uri两侧双引号，构成完整url
                if url.endswith("html"):
                  url_list.append(url)

            print len(uri_list),len(url_list),url_list
            #获取每个路径页面的新闻内容
            for index in range(0,len(url_list)):
                get_news_content(url_list[index])
                time.sleep(3)

class ScrapeCallback:
    def __init__(self):
        pass
    def __call__(self, url, html):
        print url
        print html

get_news_url("http://edition.cnn.com/","cnn")
#urllib.urlretrieve("http://edition.cnn.com/politics/2017/06/09/trump-comey-leaker-tapes-murray-pkg-lead.cnn")

#print download('http://www.reuters.com/')

