#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup 
import re
import urllib
from urllib.parse import urlunparse,urlencode,quote_plus


class Wallpapercat(object):
	"""docstring for Wallpaper"""
	def __init__(self,query):
		super(Wallpaper, self).__init__()
		self.scheme = 'https'
		self.netloc = 'wallpapercat.com'
		self.searchpath = 'search?term={}'
		self.query = quote_plus(query)
		self.useragent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36'
		self.accept = '*/*'
		self.acceptlanguage = 'en-US,en;q=0.9'
		self.referer = urlunparse((self.scheme,self.netloc,'',None,None,None))
		self.headers = {
						'user-agent':self.useragent,
						'accept':self.accept,
						'accept-language':self.acceptlanguage,
						'referer':self.referer
						}

	def searchurl(self):
		url = urlunparse((self.scheme,self.netloc,self.searchpath.format(self.query),None,None,None))
		print(url)
		res = requests.get(url,headers=self.headers)
		soup = BeautifulSoup(res.content, 'html.parser')	
		place_end = soup.find('div',{'class':'_place_end'})
		return place_end.find('a').get('href')


	def scrape(self):
		url = self.searchurl()
		items = []
		res = requests.get(url,headers=self.headers)
		soup = BeautifulSoup(res.content, 'html.parser')
		regex = re.compile('white_bord is_desktop.*')
		content =  soup.find_all("div",{'class':regex})
		for c in content:
			meta = c.find('meta',{"itemprop":"name"})
			name = meta.attrs.get("content")
			link = c.find('link')
			imglink = link.attrs.get("href")
			img_url = urlunparse((self.scheme,self.netloc,imglink,None,None,None))
			items.append({'label':name,'url':img_url,'source':self.netloc})
		return items


if __name__ == '__main__':
	s=Scaper('tottenham hotspur')
	print(s.content())