#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pathlib

import xbmcvfs

from .kodilog import Log

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

def FileName(path):
	# Return file name from path minus file type
	path = TranslatePath(path)
	return pathlib.Path(path).stem


	
def JoinPath(items):
	if isinstance(items,list):
		return os.path.join(*items)




def TranslatePath(path):
	if path.startswith('special://'):
		path = xbmcvfs.translatePath(path)
	return path
	

# C:\Users\Andy\AppData\Roaming\Kodi\addons\skin.aeon.nox.thfc\media\badges
# C:\Users\Andy\AppData\Roaming\Kodi\addons\skin.aeon.nox.thfc\media\badges