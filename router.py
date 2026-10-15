#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from urllib.parse import parse_qs
import traceback

from resources.lib.modules.kodilog import Log

import xbmc

class Main():
	"""docstring for Main"""
	def __init__(self):
		super(Main, self).__init__()
		self.call_url = sys.argv[0]
		try:
			Log(sys.argv[1])
			self.call_args = parse_qs(sys.argv[1])
		except:
			self.call_args = None
		Log(self.call_args)
		self.Args()

	def Args(self):
		try:
			self.mode = self.call_args.get('mode')[0]
		except:
			self.mode = None
		try:
			self.method = self.call_args.get('method')[0]
		except:	
			self.method = None
		try:
			self.path = self.call_args.get('path')[0]
		except:
			self.path = None
		try:
			self.properties = self.call_args.get('properties')[0]
		except Exception as e:
			self.properties = dict()
			Log(F'{e} {traceback.print_exc()}')

	def Run(self):
		if self.mode != None:
			if self.mode == 'settings':
				from resources.lib.modules.skinsettings import SkinSettings
				c = SkinSettings(self.path,self.properties)		
			elif self.mode == 'fanartselect':
				from resources.lib.modules.fanartselect import FanartSelect
				c = FanartSelect(self.path,self.properties)
			elif self.mode == 'unloadaction':
				from resources.lib.modules.unload_actions import UnloadActions
				c = UnloadActions(self.path,self.properties)
			elif self.mode == 'loadaction':
				from resources.lib.modules.load_actions import LoadActions
				c = LoadActions(self.path,self.properties)
			elif self.mode == 'executebuiltin':
				from resources.lib.modules.executebuiltin import ExecuteBuiltin
				c = ExecuteBuiltin(self.path,self.properties)
			elif self.mode == 'maintenance':
				from resources.lib.modules.maintenance import Maintenance
				c = Maintenance(self.path,self.properties)
			getattr(c,self.method)()
		else:
			xbmc.executebuiltin('RunAddon(script.aeon.nox.thfc)')


		





if __name__ == '__main__':
	m=Main()
	m.Run()
