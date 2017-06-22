# -*- encoding:UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
import time
import re
import sys
from models import News
from mongoalchemy.session import Session
from celery import Celery
from kombu import Queue

app = Celery("bbc")
app.config_from_object("celeryconfig")

app.conf.task_queues = (
    Queue('default',  routing_key='task.#'),
    Queue('bbc',  routing_key='bbc.#'),
    
)
task_default_exchange = 'bbc'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'


def route_task(name, args, kwargs, options, task=None, **kw):
  if name == 'bbc_task':
    return{'exchange': 'bbc',
           'exchange_type': 'topic',
           'routing_key': 'bbc.compress'}
              

def download(url,user_agent="wswp"):
  headers = {"User-agent":user_agent}
  request = urllib2.Request(url,headers=headers)
  html = None
  try:
      html = urllib2.urlopen(request).read()
  except urllib2.URLError as e:
      print e
  return html
  
def get_news_url(url):
  html = download(url)
  soup = BeautifulSoup(html,'html.parser')
  # print soup.prettify('utf-8')
  promo = soup.find(attrs={"class":"module module--promo module--highlight"})
  print promo
  print "promo"
  links = promo.find_all("a")
  for link in links:
    url = link.get("href")
    if not url.startswith("http"):
      url = "http://www.bbc.com"+url
    print "链接：%s",url
    article = download(url)
    article_detail = BeautifulSoup(article, 'html.parser')
    title = article_detail.find(attrs={"class":"story-body__h1"})
    content =  article_detail.find(attrs={"class":"story-body__inner"})
    if title is not None:
      print "标题:%s", title.text
    if content is not None:
      print "内容："
      for p in content.find_all("p"):
        print  p.text
    time.sleep(3)
@app.task    
def bbc_task():
  print "开始获取"
  get_news_url("http://www.bbc.com") 
  #get_news_url(url) 
