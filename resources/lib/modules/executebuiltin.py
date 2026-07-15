#!/usr/bin/python3
# -*- coding: utf-8 -*-
import ast
import json

import xbmc

from.kodilog import Log

class ExecuteBuiltin(object):
	"""docstring for ExecuteBuiltin"""
	def __init__(self,path,properties):
		super(ExecuteBuiltin, self).__init__()
		self.path = path
		Log(properties)
		self.properties = ast.literal_eval(properties)
		# self.properties = json.loads(json.dumps(properties))
		Log(self.properties)
		Log(type(self.properties))
		


	def opensettings(self):
		''' 
		category counting starts at -200 and counts up
		1st item is -200
		2nd item is -199 
		and so on
		setting menu items starts at -180 and counts up 
		Group labels are still inc in this list so 
		-180 could be a group and so 1st focus-able item could be -179 which could be 1st item in this group
		'''
		addon = self.properties.get('addon')
		categoryfocus = self.properties.get('category')
		settingfocus = self.properties.get('setting')
		categorystart = -200
		settingstart = -180

		xbmc.executebuiltin(f'Addon.OpenSettings({addon})')
		if categoryfocus != None:
			xbmc.executebuiltin(f'SetFocus(3,{categorystart-int(categoryfocus)})')
		if settingfocus != None:
			xbmc.executebuiltin(f'SetFocus(5,{settingstart-int(settingfocus)})') 
