#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from urllib.parse import parse_qs

from resources.lib.modules.kodilog import Log

Log(sys.argv[1])

class Main():
	"""docstring for Main"""
	def __init__(self):
		super(Main, self).__init__()
		self.call_url = sys.argv[0]
		self.call_args = parse_qs(sys.argv[1][1:])
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
				d = SkinSettings(self.method,self.path,self.properties)
				d.Run()
				del d


		





if __name__ == '__main__':
	m=Main()
	m.Run()
