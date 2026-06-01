#!/usr/bin/python3
# -*- coding: utf-8 -*-


import xbmcaddon


class Addon():
	"""docstring for Addon"""
	def __init__(self, *args):
		super(Addon, self).__init__()
		self.addon = xbmcaddon.Addon(*args)
		self.SETTINGS = self.addon.getSettings()
		self.AUTHOR = self.addon.getAddonInfo('author')
		self.CHANGELOG = self.addon.getAddonInfo('changelog')
		self.DESCRIPTION = self.addon.getAddonInfo('description')
		self.DISCLAIMER = self.addon.getAddonInfo('disclaimer')
		self.FANART = self.addon.getAddonInfo('fanart')
		self.ICON = self.addon.getAddonInfo('icon')
		self.ID = self.addon.getAddonInfo('id')
		self.NAME = self.addon.getAddonInfo('name')
		self.PATH = self.addon.getAddonInfo('path')
		self.PROFILE = self.addon.getAddonInfo('profile')
		self.STARS = self.addon.getAddonInfo('stars')
		self.SUMMARY = self.addon.getAddonInfo('summary')
		self.TYPE = self.addon.getAddonInfo('type')
		self.VERSION = self.addon.getAddonInfo('version')


	def LocalStr(self,stringID):
		return self.addon.getLocalizedString(stringID)

	def Reload(self):
		self.addon = xbmcaddon.Addon(self.ID)
		self.SETTINGS = self.addon.getSettings()