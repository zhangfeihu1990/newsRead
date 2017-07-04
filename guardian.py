# -*- encoding:UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
import time 
import sys

def download(url, user_agent="wasp"):
  headers = {"User-agent":user_agent}
  request = urllib2.Request(url ,headers=headers)
  html = None
  try:
    html = urllib2.urlopen(request).read()
    print html
  except urllib2.URLError as e:
    print e
  return html

def get_news_url( url ):
  html = download( url )
  soup = BeautifulSoup(html, 'html.parser')
  ws = soup.find(attrs={"class":"fc-slice-wrapper"})
  print "ws:",ws
  links = ws.find_all("a")
  url_list = []
  for link in links:
    if not link in url_list:
      href = link.get("href")
      print "link:%s" % href
      url_list.append( href )
      #url_list =  set(url_list)
  urlset = set(url_list)
  for j in urlset:
    print "url:----",j
  return urlset
get_news_url("http://www.theguardian.com")  
