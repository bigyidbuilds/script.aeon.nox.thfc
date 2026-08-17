#!/usr/bin/python3
# -*- coding: utf-8 -*-
import ast
import json

import xbmc
import xbmcgui

from.kodilog import Log

class ExecuteBuiltin(object):
	"""docstring for ExecuteBuiltin"""
	def __init__(self,path,properties):
		super(ExecuteBuiltin, self).__init__()
		self.path = path
		self.properties = ast.literal_eval(properties)

		


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
		xbmc.sleep(300)
		current_window = xbmcgui.getCurrentWindowDialogId()
		Log(current_window)
		Log(categorystart-int(categoryfocus))
		while True:
			if current_window == 100140:
				break
		if categoryfocus != None:
			xbmcgui.Window(current_window).setFocusId(categorystart-int(categoryfocus))
			# xbmc.executebuiltin(f'SetFocus(3,{categorystart-int(categoryfocus)})')
		if settingfocus != None:
			xbmc.executebuiltin(f'SetFocus(5,{settingstart-int(settingfocus)})') 
