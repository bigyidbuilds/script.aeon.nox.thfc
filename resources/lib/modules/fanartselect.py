#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xbmc
import xbmcgui

from . import ADDON

class _FanartSelect(xbmcgui.WindowXMLDialog):

	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self)

	def onInit(self):
		pass

	def onClick(self):
		pass



class FanartSelect(object):

	def __init__(self,path,properties):
		super(FanartSelect, self).__init__()
		self.path = path
		self.properties = properties


	def selectsingle(self):
		xbmc.executebuiltin("Dialog.Close(busydialognocancel)")
		w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH)
		w.doModal()
