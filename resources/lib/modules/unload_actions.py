#!/usr/bin/python3
# -*- coding: utf-8 -*-

from . import ADDON,FOLDERPATHS,FILEPATHS

from .kodivfs import DeleteFile

class UnloadActions(object):
	"""docstring for UnloadActions"""
	def __init__(self,path,properties):
		super(UnloadActions, self).__init__()
		self.path = path
		self.properties = properties


	def home(self):
		self.clearscrapercache()


	def clearscrapercache(self):
		if ADDON.SETTINGS.getInt('background.scarper.cache.clear') == 0:
			DeleteFile(FILEPATHS.WallpaperScraperCache)