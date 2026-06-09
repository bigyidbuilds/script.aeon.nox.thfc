#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from urllib.parse import parse_qs

from resources.lib.modules.kodilog import Log



class Main():
	"""docstring for Main"""
	def __init__(self):
		super(Main, self).__init__()
		self.call_url = sys.argv[0]
		Log(sys.argv[1])
		self.call_args = parse_qs(sys.argv[1])
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
		except:
			self.properties = {}

	def Run(self):
		if self.mode != None:
			if self.mode == 'settings':
				from resources.lib.modules.skinsettings import SkinSettings
				c = SkinSettings(self.path,self.properties)		
			elif self.mode == 'fanartselect':
				from resources.lib.modules.fanartselect import FanartSelect
				c = FanartSelect(self.path,self.properties)
			getattr(c,self.method)()


		





if __name__ == '__main__':
	m=Main()
	m.Run()
