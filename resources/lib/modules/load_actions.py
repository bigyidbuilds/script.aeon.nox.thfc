#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import json

import xbmc
import xbmcgui
import xbmcvfs

from . import ADDON,FOLDERPATHS,FILEPATHS

from .kodivfs import DeleteFile,ExistandMake,FileNameUrl
from .backgrounds import backGrounds
from .kodilog import Log
from .skinsettings import setting_groups
from .images import imageMeta

class LoadActions(object):
	"""docstring for LoadActions"""
	def __init__(self,path,properties):
		super(LoadActions, self).__init__()
		self.path = path
		self.properties = properties
		self.window = None
		self.monitor = xbmc.Monitor()


	def home(self):
		self.window = xbmcgui.Window(10000)
		self.menus = setting_groups.get('homemenugroup')
		ExistandMake(FOLDERPATHS.Cache)
		self.clearscrapercache()
		self.randomfanart()


	def clearscrapercache(self):
		if ADDON.SETTINGS.getInt('background.scarper.cache.clear') == 0:
			DeleteFile(FILEPATHS.WallpaperScraperCache)


	def randomfanart(self):
		self.window.setProperty('wallpaper.random.fixed.updated','true')
		totalrandom = 'background.random.random.{}'
		fixedrandom = 'background.random.fixed.{}'
		random_backgrounds = backGrounds().content.get('results').get('items')
		self.fixed_content = None
		
		while(not self.monitor.abortRequested()):
			#fixed random
			Log('awake')
			if self.window.getProperty('wallpaper.random.fixed.updated') == 'true':
				self.fixed_content = self.fixedcontent()
			results = self.fixed_content.get('results')
			if results:
				fixed_backgrounds = results.get('items')
				if len(fixed_backgrounds)>0:
					wallpapers =[ x.get('fanart') for x in fixed_backgrounds]
					for menu in self.menus:
						self.window.setProperty(fixedrandom.format(menu),random.choice(wallpapers))
			if len(random_backgrounds)>0:
				for menu in self.menus:
					max_retry = 0
					window_prop = None
					images_meta = self.imagemetacontent()
					while max_retry<10 or window_prop == None:
						background = random.choice(random_backgrounds)
						background_path = background.get('url')
						if background_path.startswith('http://') or background_path.startswith('https://'):
							max_retry += 1
							filename = FileNameUrl(background_path)
							image_meta = images_meta.get(filename)
							if image_meta:
								ratio = images_meta.get('ratio')
								ok = images_meta.get('ok')
								if ok:
									if ADDON.SETTINGS.getBool('background.random.filter'):
										if ratio >= ADDON.SETTINGS.getNumber('background.random.ratio'):
											window_prop = background_path
								else:
									window_prop = background_path
							else:
								IMAGE = imageMeta(background_path)
								images_meta.update({filename:{'ratio':IMAGE.RATIO,'ok':IMAGE.IS,'height':IMAGE.HEIGHT,'width':IMAGE.WIDTH,'filename':IMAGE.FILENAME,'size':IMAGE.SIZE,'mode':IMAGE.MODE,'format':IMAGE.FORMAT}})
								if IMAGE.IS:
									if ADDON.SETTINGS.getBool('background.random.filter'):
										if IMAGE.RATIO >= ADDON.SETTINGS.getNumber('background.random.ratio'):
											window_prop = background_path
									else:
										window_prop = background_path
						else:
							window_prop = background_path
					self.imagemetaWrite(images_meta)
					self.window.setProperty(totalrandom.format(menu),window_prop)
			self.monitor.waitForAbort(ADDON.SETTINGS.getInt('background.random.refresh'))
			Log('sleeping')






	def fixedcontent(self):
		if xbmcvfs.exists(FILEPATHS.WallpaperRandom):
			with xbmcvfs.File(FILEPATHS.WallpaperRandom,'r') as f:
				content = json.load(f)
		self.window.setProperty('wallpaper.random.fixed.updated','false')
		return content


	def imagemetacontent(self):
		content = None
		if xbmcvfs.exists(FILEPATHS.ImageMeta):
			with xbmcvfs.File(FILEPATHS.ImageMeta,'r') as f:
				content = json.load(f)
		if bool(content):
			return content
		else:
			return {}

	def imagemetaWrite(self,content):
		json_str = json.dumps(content, indent=4)
		with xbmcvfs.File(FILEPATHS.ImageMeta,'w') as f:
			f.write(json_str)
		f.close()


