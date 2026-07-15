#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json
import wallpaper

import xbmcvfs

from . import ADDON,FOLDERPATHS,FILEPATHS
from .skinsettings import setting_groups
from .kodijson import SettingSkin
from .kodivfs import TranslatePath,PathType,GetFiles,FileNameUrl,FileName,SpecialPath,FolderName,ExistandMake
from .encoding import Encode_B64,Decode_B64

class backGrounds():

	def __init__(self):
		self.includecache = ADDON.SETTINGS.getBool('background.include.localfiles')
		self.content = self.getcontent()

	def getcontent(self):
		s = ADDON.SETTINGS.getInt('background.scarper.cache.clear')
		ft = xbmcvfs.exists(FILEPATHS.WallpaperScraperCache)
		wf = False
		if s == 0 and not ft:
			wf = True
		elif s == 1:
			if ft:
				st_file = xbmcvfs.Stat(FILEPATHS.WallpaperScraperCache)
				if datetime.datetime.fromtimestamp(st_file.st_mtime(),tz=datetime.timezone.utc)+datetime.timedelta(hours=24) < datetime.datetime.now(datetime.timezone.utc):
					wf = True
			else:
				wf = True
		elif s == 2:
			if ft:
				st_file = xbmcvfs.Stat(FILEPATHS.WallpaperScraperCache)
				if datetime.datetime.fromtimestamp(st_file.st_mtime(),tz=datetime.timezone.utc)+datetime.timedelta(hours=48) < datetime.datetime.now(datetime.timezone.utc):
					wf = True
			else:
				wf = True
		if wf:
			if ExistandMake(FOLDERPATHS.ScraperCache):
				json_str = json.dumps(wallpaper.GetWallPapers('tottenham hotspur'), indent=4)
				with xbmcvfs.File(FILEPATHS.WallpaperScraperCache,'w') as f:
					f.write(json_str)
		if xbmcvfs.exists(FILEPATHS.WallpaperScraperCache):
			with xbmcvfs.File(FILEPATHS.WallpaperScraperCache,'r') as f:
				content = json.load(f)
		if self.includecache:
			localitemcounter = 0
			items_to_add = []
			paths_checked = []
			for hm in setting_groups.get('homemenugroup'):
				path = SettingSkin(f'{hm}.MultiFanart')
				if path:
					paths_checked.append(TranslatePath(path))
					pathtype = PathType(path)
					if pathtype == 'dir':
						files = GetFiles(path)
						for file in files:
							localitemcounter += 1
							items_to_add.append({'label':FileNameUrl(Decode_B64(FileName(file))),'url':SpecialPath(file),'source':FolderName(path),'keywords':['local file']})
					elif pathtype == 'file':
						localitemcounter += 1
						items_to_add.append({'label':FileNameUrl(Decode_B64(FileName(path))),'url':SpecialPath(path),'source':FolderName(path),'keywords':['local file']})
					else:
						continue
			for hm in setting_groups.get('homemenugroup'):
				path = getattr(FOLDERPATHS,hm)
				if path not in paths_checked and xbmcvfs.exists(path):
					paths_checked.append(TranslatePath(path))
					pathtype = PathType(path)
					if pathtype == 'dir':
						files = GetFiles(path)
						for file in files:
							localitemcounter += 1
							items_to_add.append({'label':FileNameUrl(Decode_B64(FileName(file))),'url':SpecialPath(file),'source':FolderName(path),'keywords':['local file']})
			for folder in ['SingleImage','ImageCache']:
				path = getattr(FOLDERPATHS,folder)
				if path not in paths_checked and xbmcvfs.exists(path):
					pathtype = PathType(path)
					if pathtype == 'dir':
						files = GetFiles(path)
						for file in files:
							localitemcounter += 1
							items_to_add.append({'label':FileNameUrl(Decode_B64(FileName(file))),'url':SpecialPath(file),'source':FolderName(path),'keywords':['local file']})

			results = content.get('results')
			if results:
				if len(items_to_add)>0:
					items = results.get('items')
					total_item = results.get('total_items')
					keywords = results.get('keywords')
					new_total_items = len(items)+len(items_to_add)
					for i in items_to_add:
						items.append(i)
					results.update({'total_items':new_total_items})
					keywords.update({'local file':localitemcounter})		
		return content





