#!/usr/bin/python3
# -*- coding: utf-8 -*-

import xbmcplugin
import json
import sys
from urllib.parse import parse_qs,urlencode
import routing
from resources.lib.modules.kodilog import Log
from resources.lib.modules.kodilistitem import ListItem 
from resources.lib.modules import ADDON,FOLDERPATHS,FILEPATHS
from resources.lib.modules.kodivfs import GetFiles,DeleteFile,FileName
from resources.lib.modules.encoding import Decode_B64


plugin = routing.Plugin()

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
		else:
			plugin.run()


@plugin.route('/')
def mainmenu():
	items = [
			(plugin.url_for(maintenance_menu),ListItem(label=ADDON.LocalStr(30500),icon="DefaultAddonProgram.png"),True)
			]		

	xbmcplugin.addDirectoryItems(plugin.handle, items)
	xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/maintenance_menu')
def maintenance_menu():
	items = [
			(plugin.url_for(maintenance_items,method="clearfolder",path=FOLDERPATHS.ImageBin),ListItem(label=ADDON.LocalStr(30501),icon="DefaultAddonProgram.png"),False),
			(plugin.url_for(maintenance_items,method="clearfolder_select",path=FOLDERPATHS.ImageBin),ListItem(label=ADDON.LocalStr(30502),icon="DefaultAddonProgram.png"),False),
			(plugin.url_for(maintenance_items,method="movecontents",properties=json.dumps({"pathfrom":FOLDERPATHS.ImageCache,"pathto":FOLDERPATHS.ImageBin})),ListItem(label=ADDON.LocalStr(30503),icon="DefaultAddonProgram.png"),False),
			(plugin.url_for(maintenance_items,method="movecontents",properties=json.dumps({"pathfrom":FOLDERPATHS.ImageBin,"pathto":FOLDERPATHS.ImageCache})),ListItem(label=ADDON.LocalStr(30509),icon="DefaultAddonProgram.png"),False),
			(plugin.url_for(maintenance_items,method="unusedimages",path=FOLDERPATHS.BackGrounds),ListItem(label=ADDON.LocalStr(30504),icon="DefaultAddonProgram.png"),False),
			(plugin.url_for(maintenance_items,method="deletefile",properties=json.dumps({"restart":True,"items":[{"path":FILEPATHS.ImageMeta},{"path":FILEPATHS.WallpaperScraperCache}]})),ListItem(label=ADDON.LocalStr(30505),icon="DefaultAddonProgram.png"),False),
			(plugin.url_for(maintenance_items,method="filemanger",path=ADDON.PROFILE),ListItem(label=xbmc.getLocalizedString(10003),icon="DefaultAddonProgram.png"),False)
			]
	xbmcplugin.addDirectoryItems(plugin.handle, items)
	xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/maintenance_menu/items/<method>')
def maintenance_items(method):
	try:
		path = plugin.args['path'][0]
	except:
		path = None
	try:
		properties = plugin.args['properties'][0]
	except:
		properties = None
	from resources.lib.modules.maintenance import Maintenance
	m = Maintenance(path,properties)
	getattr(m,method)()



if __name__ == '__main__':
	m=Main()
	m.Run()
		
