#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xbmcplugin

from .kodiaddon import Addon 
from .kodivfs import GetFiles,JoinPath,FileName,SpecialPath
from .Kodilistitem import ListItem
from .kodilog import Log

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
		SKINADDON = Addon('skin.aeon.nox.thfc')
		path = [SKINADDON.PATH,'media','badges','']
		path = JoinPath(path)
		files = GetFiles(path,'png')
		Log(files)
		for file in files:
			label = FileName(file)
			icon = SpecialPath(file)
			Log(icon)
			content.append(('',ListItem(label=label,icon=icon,properties={'label':label,'icon':icon}),False))
		xbmcplugin.addDirectoryItems(self.handle,content)
		xbmcplugin.endOfDirectory(self.handle)

