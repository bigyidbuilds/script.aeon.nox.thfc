#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

import xbmc

from .kodiaddon import Addon
from .kodivfs import GetFiles,JoinPath,SpecialPath 
from .kodilog import Log

clubbadge_settings = [
					"HomeMenuClubBadge_0",
					"HomeMenuClubBadge_1",
					"HomeMenuClubBadge_2",
					"HomeMenuClubBadge_3",
					"HomeMenuClubBadge_4",
					"HomeMenuClubBadge_5",
					"HomeMenuClubBadge_6",
					"HomeMenuClubBadge_7"
					]

class SkinSettings():
	"""docstring for SkinSettings"""
	def __init__(self,path,properties):
		super(SkinSettings, self).__init__()
		self.path = path
		self.properties = properties


	def randomclubbadge(self):
		Log(xbmc.getInfoLabel('Window(1135).Property(randomsetting)'))
		SKINADDON = Addon('skin.aeon.nox.thfc')
		path = [SKINADDON.PATH,'media','badges','']
		path = JoinPath(path)
		files = GetFiles(path,'png')
		for i in clubbadge_settings:
			xbmc.executebuiltin(f'Skin.SetString({i},{SpecialPath(random.choice(files))})')



