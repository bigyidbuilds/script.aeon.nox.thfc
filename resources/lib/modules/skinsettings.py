#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

import xbmc

from .kodiaddon import Addon
from .kodivfs import GetFiles,JoinPath,SpecialPath 
from .kodilog import Log

setting_groups = {
					"homemenugroup": [
						"VideosHomeItem",
						"Custom5HomeItem",
						"ProgramsHomeItem",
						"Custom6HomeItem",
						"Custom4HomeItem",
						"ShutdownHomeItem",
						"GamesHomeItem",
						"MusicVideoHomeItem",
						"WeatherHomeItem",
						"Custom3HomeItem",
						"MovieHomeItem",
						"TVShowHomeItem",
						"SettingsHomeItem",
						"FavoritesHomeItem",
						"MusicHomeItem",
						"LiveTVHomeItem",
						"PicturesHomeItem",
						"Custom2HomeItem",
						"Custom1HomeItem"
					],
					"HomeMenuClubBadge": [
						"HomeMenuClubBadge_0",
						"HomeMenuClubBadge_1",
						"HomeMenuClubBadge_2",
						"HomeMenuClubBadge_3",
						"HomeMenuClubBadge_4",
						"HomeMenuClubBadge_5",
						"HomeMenuClubBadge_6",
						"HomeMenuClubBadge_7"
					]
				}

class SkinSettings():
	"""docstring for SkinSettings"""
	def __init__(self,path,properties):
		super(SkinSettings, self).__init__()
		self.path = path
		self.properties = properties


	def randomclubbadge(self):
		SKINADDON = Addon('skin.aeon.nox.thfc')
		path = [SKINADDON.PATH,'media','badges','']
		path = JoinPath(path)
		files = GetFiles(path,'png')
		for i in setting_groups.get('HomeMenuClubBadge'):
			xbmc.executebuiltin(f'Skin.SetString({i},{SpecialPath(random.choice(files))})')



