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
