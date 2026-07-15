#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import os
import pathlib
from urllib.parse import urlparse

import xbmcvfs

from . import ADDON
from .kodilog import Log

def FileDownloader(url,dest):
	with xbmcvfs.File(dest, 'w') as f:
		response = requests.get(url, stream=True)
		if response.ok:
			for block in response.iter_content(1024):
				if not block:
					break
				result = f.write(block)
		else:
			Log(f'Error getting {url}')
	return result



def GetFiles(path,filetype=None,fullpath=True):
	path = TranslatePath(path)
	files = []
	if xbmcvfs.exists(path):
		for (root, dirs, file) in os.walk(path):
			for f in file:
				if filetype != None:
					if f.endswith(f'.{filetype}'):
						files.append(f)
				else:
					files.append(f)
	if fullpath:
		files = [os.path.join(path,f) for f in files]
	return files

def FileName(path,inc_extension=False):
	# Return file name from path minus file type
	path = TranslatePath(path)
	if xbmcvfs.exists(path):
		if inc_extension:
			return pathlib.Path(path).name
		else:
			return pathlib.Path(path).stem
	else:
		return None

def FileNameUrl(url):
	parsedurl = urlparse(url)
	return pathlib.Path(parsedurl.path).stem


def FolderName(path):
	path = TranslatePath(path)
	path = pathlib.Path(path)
	if path.is_dir():
		return path.name
	elif path.is_file():
		return path.parents[0].name
	else:
		return None


	
def JoinPath(items):
	if isinstance(items,list):
		return os.path.join(*items)




def TranslatePath(path):
	if path.startswith('special://'):
		path = xbmcvfs.translatePath(path)
	return path


def SpecialPath(absolute_path):
	# Converts real path to kodi special path
	# 1. Resolve your base special paths to their physical OS equivalents
	base_paths = {
		'special://home/': xbmcvfs.translatePath('special://home'),
		'special://temp/': xbmcvfs.translatePath('special://temp'),
		'special://masterprofile/': xbmcvfs.translatePath('special://masterprofile'),
		'special://xbmc/': xbmcvfs.translatePath('special://xbmc')
	}
	
	# Normalize paths to avoid slash and case mismatch issues
	abs_path_normalized = absolute_path.replace('\\', '/').lower()
	
	# 2. Check which base path the absolute path belongs to
	for special_prefix, physical_path in base_paths.items():
		phys_path_normalized = physical_path.replace('\\', '/').lower()
		
		if abs_path_normalized.startswith(phys_path_normalized):
			# 3. Replace the absolute prefix with the special protocol
			relative_part = absolute_path[len(physical_path):]
			# Ensure proper joining with a forward slash
			return f"{special_prefix}{relative_part}".replace('\\', '/')
			
	# Return the original path if no special mapping matches
	return absolute_path


def ExistandMake(path):
	path = TranslatePath(path)
	if xbmcvfs.exists(path):
		return True
	else:
		if xbmcvfs.mkdirs(path):
			return True
		else:
			Log(f'Unable to create dirs at {path}')
			return False


def DeleteFile(file):
	file = TranslatePath(file)
	if xbmcvfs.exists(file):
		return xbmcvfs.delete(file)


def MoveFile(file_path,folder_path):
	file_path = TranslatePath(file_path)
	folder_path = TranslatePath(folder_path)
	file_name = FileName(file_path,inc_extension=True)
	if xbmcvfs.exists(file_path) and ExistandMake(folder_path):
		new_file_path =JoinPath([folder_path,file_name])
		if not xbmcvfs.exists(new_file_path):
			if xbmcvfs.copy(file_path,new_file_path):
				if xbmcvfs.delete(file_path):
					Log(f'File:{file_path}\nMoved to:{new_file_path}\nSuccessfully')
					return True
				else:
					Log(f'File:{file_path}\nCopied to:{new_file_path}\nOriginal not deleted')
			else:
				Log(f'File:{file_path}\n Not copied to:{new_file_path}\nOriginal not deleted')
		else:
			if xbmcvfs.delete(file_path):
				Log(f'File:{new_file_path} already existed\n{file_path} original deleted')
	else:
		Log(f'File:{file_path}\nOr Folder path:{folder_path}\nDo not exist')


def CopyFile(file_path,folder_path):	
	file_path = TranslatePath(file_path)
	folder_path = TranslatePath(folder_path)
	file_name = FileName(file_path,inc_extension=True)
	if xbmcvfs.exists(file_path) and xbmcvfs.exists(folder_path):
		new_file_path =JoinPath([folder_path,file_name])
		if not xbmcvfs.exists(new_file_path):
			if xbmcvfs.copy(file_path,new_file_path):
				Log(f'File:{file_path}\nCopied to:{new_file_path}')
			else:
				Log(f'File:{file_path}\n Not copied to:{new_file_path}')
		else:
			Log(f'File:{new_file_path} already exists not copied')
	else:
		Log(f'File:{file_path}\nOr Folder path:{folder_path}\nDo not exist')



def PathType(path):
	path = TranslatePath(path)
	if pathlib.Path(path).is_file():
		_type = 'file'
	else:
		if pathlib.Path(path).is_dir():
			_type = 'dir'
		else:
			_type = None
	return _type


class FolderPaths(object):
	"""docstring for FolderPaths wrapper for predefined folder paths"""
	def __init__(self):
		super(FolderPaths, self).__init__()
		self.VideosHomeItem     = JoinPath([ADDON.PROFILE,'backgrounds','VideosHomeItem',''])
		self.Custom5HomeItem    = JoinPath([ADDON.PROFILE,'backgrounds','Custom5HomeItem',''])
		self.ProgramsHomeItem   = JoinPath([ADDON.PROFILE,'backgrounds','ProgramsHomeItem',''])
		self.Custom6HomeItem    = JoinPath([ADDON.PROFILE,'backgrounds','Custom6HomeItem',''])
		self.Custom4HomeItem    = JoinPath([ADDON.PROFILE,'backgrounds','Custom4HomeItem',''])
		self.ShutdownHomeItem   = JoinPath([ADDON.PROFILE,'backgrounds','ShutdownHomeItem',''])
		self.GamesHomeItem      = JoinPath([ADDON.PROFILE,'backgrounds','GamesHomeItem',''])
		self.MusicVideoHomeItem = JoinPath([ADDON.PROFILE,'backgrounds','MusicVideoHomeItem',''])
		self.WeatherHomeItem    = JoinPath([ADDON.PROFILE,'backgrounds','WeatherHomeItem',''])
		self.Custom3HomeItem    = JoinPath([ADDON.PROFILE,'backgrounds','Custom3HomeItem',''])
		self.MovieHomeItem      = JoinPath([ADDON.PROFILE,'backgrounds','MovieHomeItem',''])
		self.TVShowHomeItem     = JoinPath([ADDON.PROFILE,'backgrounds','TVShowHomeItem',''])
		self.SettingsHomeItem   = JoinPath([ADDON.PROFILE,'backgrounds','SettingsHomeItem',''])
		self.FavoritesHomeItem  = JoinPath([ADDON.PROFILE,'backgrounds','FavoritesHomeItem',''])
		self.MusicHomeItem      = JoinPath([ADDON.PROFILE,'backgrounds','MusicHomeItem',''])
		self.LiveTVHomeItem     = JoinPath([ADDON.PROFILE,'backgrounds','LiveTVHomeItem',''])
		self.PicturesHomeItem   = JoinPath([ADDON.PROFILE,'backgrounds','PicturesHomeItem',''])
		self.Custom2HomeItem    = JoinPath([ADDON.PROFILE,'backgrounds','Custom2HomeItem',''])
		self.Custom1HomeItem    = JoinPath([ADDON.PROFILE,'backgrounds','Custom1HomeItem',''])
		self.Cache              = JoinPath([ADDON.PROFILE,'cache',''])
		self.Random             = JoinPath([self.Cache,'Random',''])
		self.SingleImage        = JoinPath([ADDON.PROFILE,'backgrounds','SingleImage',''])
		self.ImageCache         = JoinPath([ADDON.PROFILE,'backgrounds','ImageChace',''])
		self.ScraperCache       = JoinPath([self.Cache,'scraper',''])
		self.ImageBin           = JoinPath([ADDON.PROFILE,'backgrounds','ImageBin',''])



class FilePaths(object):
	"""docstring for FilePaths wrapper for predefined file paths"""
	def __init__(self):
		super(FilePaths, self).__init__()
		self.FOLDERPATHS = FolderPaths()
		self.WallpaperScraperCache = JoinPath([self.FOLDERPATHS.ScraperCache,'wallpaper.json'])
		self.WallpaperRandom = JoinPath([self.FOLDERPATHS.Random,'random.json'])
		self.ImageMeta = JoinPath([self.FOLDERPATHS.Cache,'imagemeta.json'])
		
