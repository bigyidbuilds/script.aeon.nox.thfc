#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xbmcplugin

from .kodiaddon import Addon 
from .kodivfs import GetFiles,JoinPath,FileName,SpecialPath,FileNameUrl
from .kodilistitem import ListItem
from .kodilog import Log
from .resource import GetAssets

class DynamicList():
	"""docstring for DynamicList"""
	def __init__(self,method,path,handle,properties):
		super(DynamicList, self).__init__()
		self.method = method
		self.path = path
		self.handle = handle
		self.properties = properties

	def Run(self):
		Log(f'Run with method {self.method}')
		if self.method == 'clubbadgelist':
			self.ClubBadgeList()



	def ClubBadgeList(self):
		content = list()
		assets = GetAssets('resource.images.footballbadges','tottenhamhotspur')
		for asset in assets:
			label = FileNameUrl(asset)
			icon = asset
			content.append(('',ListItem(label=label,icon=icon,properties={'label':label,'icon':icon}),False))
		xbmcplugin.addDirectoryItems(self.handle,content)
		xbmcplugin.endOfDirectory(self.handle)

