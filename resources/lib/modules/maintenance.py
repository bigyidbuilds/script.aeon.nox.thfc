#!/usr/bin/python3
# -*- coding: utf-8 -*-
from operator import itemgetter 
import json 

import xbmc
import xbmcvfs
import xbmcgui

from .kodijson import SettingSkin
from .kodivfs import GetFiles,DeleteFile,FileName,MoveFile,GetDirs,SpecialPath,TranslatePath,PathType,FileFolderPath,PathCompare,ExistandMake
from .kodilog import Log
from .kodilistitem import ListItem
from .skinsettings import setting_groups
from . import ADDON,FOLDERPATHS,FILEPATHS


class Maintenance(object):
	"""docstring for Maintenance"""
	def __init__(self,path,properties):
		super(Maintenance, self).__init__()
		self.path = path
		self.properties = properties
		if isinstance(self.properties,str):
			self.properties = json.loads(self.properties)


	def clearfolder(self):
		files = GetFiles(self.path)
		for f in files:
			DeleteFile(f)

	def clearfolder_select(self):
		items = list()
		files = GetFiles(self.path)
		for file in files:
			items.append(ListItem(label=file,icon=file,fanart=file))
		ret = xbmcgui.Dialog().multiselect(ADDON.LocalStr(30507), items, useDetails=True)
		del_items = itemgetter(*ret)(items)
		for del_item in del_items:
			DeleteFile(del_item.getArt('fanart'))

	def movecontents(self):
		files = GetFiles(self.properties.get("pathfrom"))
		pathto = self.properties.get("pathto")
		for f in files:
			MoveFile(f,pathto)
		ok = xbmcgui.Dialog().ok(ADDON.NAME,f'{len(files)} {ADDON.LocalStr(30508)} {pathto}')

	def unusedimages(self):
		excempt_dirs = [(TranslatePath(d)) for d in [FOLDERPATHS.SingleImage,FOLDERPATHS.ImageCache,FOLDERPATHS.ImageBin]]
		dirs = [d for d in GetDirs(self.path) if d not in excempt_dirs]
		si_files = GetFiles(FOLDERPATHS.SingleImage)
		settings = list()
		counter = 0
		for hm in setting_groups.get('homemenugroup'):
			s = f'{hm}.MultiFanart'
			setting = SettingSkin(s)
			if setting:
				rp_setting = TranslatePath(setting)
				if PathType(rp_setting) == 'dir':
					if rp_setting in dirs:
						dirs.remove(rp_setting)
				elif PathType(rp_setting) == 'file':
					fp = FileFolderPath(rp_setting)
					if PathCompare(fp,FOLDERPATHS.SingleImage):
						if rp_setting in si_files:
							si_files.remove(rp_setting)
		for d in dirs:
			for f in GetFiles(d):
				counter += 1
				MoveFile(f,FOLDERPATHS.ImageBin)
		for f in si_files:
			MoveFile(f,FOLDERPATHS.ImageBin)
			counter += 1
		ok = xbmcgui.Dialog().ok(ADDON.NAME, f'{counter} {ADDON.LocalStr(30508)} {FOLDERPATHS.ImageBin}')


	def deletefile(self):
		items = self.properties.get('items')
		restart = self.properties.get('restart')
		to_delete = list()
		if self.path:
			to_delete.append(self.path)
		elif items:
			li = list()
			for i in items:
				path = i.get('path')
				li.append(ListItem(label=FileName(path,inc_extension=True),properties={"path":path}))
			ret = xbmcgui.Dialog().multiselect(ADDON.LocalStr(30507),li)
			if ret:
				del_items = itemgetter(*ret)(li)
				for del_item in del_items:
					to_delete.append(del_item.getProperty('path'))
		if restart:
			#Creates a json file containing paths of files to be deleted 
			#delete action coded into load_actions.py home()
			if ExistandMake(FOLDERPATHS.Cache):
				self.WriteJson({"filepaths":to_delete},FILEPATHS.FilesToDelete)
			if (xbmc.getCondVisibility('System.Platform.Windows')) or (xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.android')):
				xbmc.executebuiltin('RestartApp')
			else:
				xbmc.executebuiltin('Quit')
				
		else:
			for d in to_delete:
				DeleteFile(d)


	def WriteJson(self,content,file):
		json_str = json.dumps(content, indent=4)
		with xbmcvfs.File(file,'w') as f:
			f.write(json_str)
		f.close()



	def filemanger(self):
		xbmc.executebuiltin(f"ActivateWindow(filemanager,{self.path},{self.path})")




		

