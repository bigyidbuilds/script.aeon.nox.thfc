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
		self.call_handle = int(sys.argv[1])
		self.call_args = parse_qs(sys.argv[2][1:])
		Log(f'{self.call_url},{self.call_handle},{self.call_args}')
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
			if self.mode == 'dynamiclist':
				Log(f'Opening dynamic list with method={self.method} path={self.path} call_handle={self.call_handle} properties={self.properties}')
				from resources.lib.modules.dynamic_list import DynamicList
				d = DynamicList(self.method,self.path,self.call_handle,self.properties)
				d.Run()
				del d

		



if __name__ == '__main__':
	m=Main()
	m.Run()
		
