#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import json

import xbmc
import xbmcgui
import xbmcvfs
import os
import wallpaper

from . import ADDON,FOLDERPATHS,FILEPATHS
from .kodijson import SettingSkin
from .kodilog import Log
from .kodivfs import FileName,SpecialPath,JoinPath,ExistandMake,FileDownloader,GetFiles,FileNameUrl,MoveFile,CopyFile
from .Kodilistitem import ListItem
from .uiactions import uiActions
from .encoding import Encode_B64,Decode_B64
from .backgrounds import backGrounds

class _FanartSelect(xbmcgui.WindowXMLDialog):

	BACKGROUND_LIST = 9000
	FILTER_LIST = 9100
	CLEAR_LIST = 9200
	CLEAR_BUTTON = 9210
	SELECTED_BUTTON = 9310
	SET_IMAGE_BUTTON = 9311
	SELECTD_GROUP = 9400
	SELECTED_LIST = 9410


	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self)
		self.UIACTIONS = uiActions()
		self.kwargs = kwargs
		self.content = self.kwargs.get('content')
		self.results = self.content.get('results')
		self.singleimage = self.kwargs.get('singleimage')
		self.multiimage = self.kwargs.get('multiimage')
		self.randomimage = self.kwargs.get('randomimage')
		self.existing_content = self.kwargs.get('existing_content',list())
		if self.results:
			self.backgroundlist =self.backgroundBuilder(self.results.get('items'))
			self.filterlist = self.filterBuilder(self.results.get('keywords'))
		else:
			self.backgroundlist = self.filterlist = None
		self.selecteditem = None
		self.selectedmulti = self.existing_content
		self.setimages = False



	def onInit(self):
		self.BACKGROUND_LIST_CTRL = self.getControl(self.BACKGROUND_LIST)
		self.FILTER_LIST_CTRL = self.getControl(self.FILTER_LIST)
		self.CLEAR_LIST_CTRL = self.getControl(self.CLEAR_LIST)
		self.SELECTED_BUTTON_CTRL = self.getControl(self.SELECTED_BUTTON)
		self.SELECTED_LIST_CTRL = self.getControl(self.SELECTED_LIST)
		self.SELECTED_GROUP_CTRL = self.getControl(self.SELECTD_GROUP)
		self.SET_IMAGE_BUTTON_CTRL = self.getControl(self.SET_IMAGE_BUTTON)
		self.CLEAR_LIST_CTRL.setVisible(False)
		if self.singleimage:
			self.SELECTED_BUTTON_CTRL.setVisible(False)
			self.SELECTED_GROUP_CTRL.setVisible(False)
			self.SET_IMAGE_BUTTON_CTRL.setVisible(False)
		elif self.multiimage or self.randomimage:
			self.SELECTED_BUTTON_CTRL.setLabel(ADDON.LocalStr(32000))
			if len(self.selectedmulti)>0:
				self.SELECTED_BUTTON_CTRL.setVisible(True)		
				self.SELECTED_GROUP_CTRL.setVisible(False)
				self.SET_IMAGE_BUTTON_CTRL.setVisible(True)
				self.SelectedLoader()
			else:
				self.SELECTED_BUTTON_CTRL.setVisible(False)		
				self.SELECTED_GROUP_CTRL.setVisible(False)
				self.SET_IMAGE_BUTTON_CTRL.setVisible(False)
		else:
			pass
		if self.backgroundlist:
			self.BACKGROUND_LIST_CTRL.addItems(self.backgroundlist)
		if self.filterlist:
			self.FILTER_LIST_CTRL.addItems(self.filterlist)
		self.setFocusId(self.BACKGROUND_LIST)



	def onClick(self,controlId):
		if controlId == self.CLEAR_BUTTON:
			self.setFocusId(self.BACKGROUND_LIST)
			self.CLEAR_LIST_CTRL.setVisible(False)
			self.FILTER_LIST_CTRL.setVisible(True)
			self.Reload(keyword=None)
		elif controlId == self.SELECTED_BUTTON:
			self.selectedButton()
		elif controlId == self.SET_IMAGE_BUTTON:
			self.setimages = True
			self.Close()


			

	def onAction(self,action):
		actionid = action.getId()
		if actionid in [self.UIACTIONS.ACTION_NAV_BACK,self.UIACTIONS.ACTION_PREVIOUS_MENU ]:
			self.Close()
		elif actionid in [self.UIACTIONS.ACTION_SELECT_ITEM,self.UIACTIONS.ACTION_MOUSE_LEFT_CLICK]:
			if self.getFocusId() == self.FILTER_LIST:
				item = self.FILTER_LIST_CTRL.getSelectedItem()
				keyword = item.getProperty('keyword')
				self.setFocusId(self.BACKGROUND_LIST)
				self.FILTER_LIST_CTRL.setVisible(False)
				self.CLEAR_LIST_CTRL.setVisible(True)
				self.Reload(keyword=keyword)
			elif self.getFocusId() == self.BACKGROUND_LIST:
				item = self.BACKGROUND_LIST_CTRL.getSelectedItem()
				if self.singleimage:
					self.selecteditem = item
					self.setimages = True
					self.close()
				elif self.multiimage or self.randomimage:
					self.AddSelected(item)
					self.SelectedLoader()
					if len(self.selectedmulti)>0:
						self.SELECTED_BUTTON_CTRL.setVisible(True)
						self.SET_IMAGE_BUTTON_CTRL.setVisible(True)
			elif self.getFocusId() == self.SELECTED_LIST:
				pos = self.SELECTED_LIST_CTRL.getSelectedPosition()
				self.selectedmulti.pop(pos)
				if len(self.selectedmulti)>=1:
					self.SelectedLoader()
				else:
					self.SELECTED_GROUP_CTRL.setVisible(False)
					self.SELECTED_BUTTON_CTRL.setVisible(False)
					self.SET_IMAGE_BUTTON_CTRL.setVisible(False)
					self.setFocusId(self.BACKGROUND_LIST)
				

				


	def Reload(self,keyword=None):
		self.BACKGROUND_LIST_CTRL.reset()
		items = self.backgroundBuilder(self.results.get('items'),keyword=keyword)
		self.BACKGROUND_LIST_CTRL.addItems(items)

	def SelectedLoader(self):
		self.SELECTED_LIST_CTRL.reset()
		self.SELECTED_LIST_CTRL.addItems(self.selectedmulti)

	def AddSelected(self,item):
		self.selectedmulti.append(ListItem(label=item.getLabel(),icon=item.getArt('icon'),fanart=item.getArt('fanart'),properties={'keywords':item.getProperty('keywords'),'source':item.getProperty('source')}))


	def Close(self):
		super(_FanartSelect,self).close()


	def backgroundBuilder(self,content,keyword=None):
		listitems = []
		for i in content:
			label = i.get('label')
			image = i.get('url')
			source = i.get('source')
			keywords = i.get('keywords')
			if keyword:
				if keyword in keywords:
					listitems.append(ListItem(label=label,icon=image,fanart=image,properties={'keywords':keywords,'source':source}))
			else:
				listitems.append(ListItem(label=label,icon=image,fanart=image,properties={'keywords':keywords,'source':source}))
		return listitems



	def filterBuilder(self,content):
		listitems = []
		for k,v in content.items():
			label = f'{k}({v})'
			name = k
			count = v
			listitems.append(ListItem(label=label,properties={'keyword':name,'count':count}))
		return listitems


	def selectedButton(self):
		button_label = self.SELECTED_BUTTON_CTRL.getLabel()
		show_str = ADDON.LocalStr(32000)
		hide_str = ADDON.LocalStr(32001)
		if button_label == show_str:
			label = hide_str
			vis = True
		elif button_label == hide_str:
			label = show_str
			vis = False
		self.SELECTED_GROUP_CTRL.setVisible(vis)
		self.SELECTED_BUTTON_CTRL.setLabel(label)
		if vis:
			self.setFocusId(self.SELECTED_LIST)	

	def toggleButton(self,controlid,label):
		control = self.getControl(controlid)


	def addItems(self,controlid,items):
		control = self.getControl(controlid)
		control.addItems(items)



class FanartSelect(object):

	def __init__(self,path,properties):
		super(FanartSelect, self).__init__()
		self.path = path
		self.properties = properties
		self.includecache = ADDON.SETTINGS.getBool('background.include.localfiles')
		self.home_window = xbmcgui.Window(10000)


	def selectsingle(self):
		xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
		content = backGrounds().content
		xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
		w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=content,singleimage=True)
		w.doModal()
		selecteditem = w.selecteditem
		setimages = w.setimages
		if setimages:
			if isinstance(selecteditem,xbmcgui.ListItem):
				wallpaper = selecteditem.getArt('fanart')
				if not wallpaper.startswith('special://'):
					if ADDON.SETTINGS.getBool('background.cache.singleimage'):
						filename = Encode_B64(wallpaper)
						if ExistandMake(FOLDERPATHS.SingleImage):
							full_path = JoinPath([FOLDERPATHS.SingleImage,f'{filename}.jpg'])
							if FileDownloader(wallpaper,full_path):
								wallpaper_path = full_path
							else:
								wallpaper_path = wallpaper
						else:
							wallpaper_path = wallpaper
					else:
						wallpaper_path = wallpaper
				else:
					wallpaper_path = wallpaper
				xbmc.executebuiltin('Skin.SetString(ItemToEdit.BGType,1)')
				xbmc.executebuiltin(f'Skin.SetString(ItemToEdit.MultiFanart,{wallpaper_path})')
		xbmc.executebuiltin('Dialog.Close(1122)')
		del w

	def selectmulti(self):
		xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
		filename = self.home_window.getProperty("FanartSelector.Folder.Name")
		filepath = getattr(FOLDERPATHS,filename)
		existing_content = []
		content = backGrounds().content
		if xbmcvfs.exists(filepath):
			files = GetFiles(filepath)
			if len(files)>0:
				xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
				ret = xbmcgui.Dialog().yesnocustom(xbmc.getLocalizedString(31977), ADDON.LocalStr(32002),ADDON.LocalStr(32005),ADDON.LocalStr(32003),ADDON.LocalStr(32004))
				if ret == 1:
					Log('Clear existing list')
					for file in files:
						MoveFile(file,FOLDERPATHS.ImageBin) 
					w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=content,multiimage=True)
					xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
				elif ret == 0:
					Log('Use existing list')
					for file in files:
						file_path = JoinPath([FOLDERPATHS.ImageCache,FileName(file,inc_extension=True)])
						MoveFile(file,FOLDERPATHS.ImageCache)
						# set new path to file in imagecache after move
						existing_content.append(ListItem(label=FileNameUrl(Decode_B64(FileName(file_path))),icon=SpecialPath(file_path),fanart=SpecialPath(file_path),properties={'keywords':['local file'],'source':filename}))
					w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=content,multiimage=True,existing_content=existing_content)
					xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
				else:
					return
			else:
				w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=content,multiimage=True)
				xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
		else:
			w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=content,multiimage=True)
			xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
		w.doModal()
		selectedmulti = w.selectedmulti
		setimages = w.setimages
		if setimages:
			if ExistandMake(filepath):
				for li in selectedmulti:
					if isinstance(li,xbmcgui.ListItem):
						wallpaper = li.getArt('fanart')
						if wallpaper.startswith('special://'):
							Log(filepath)
							MoveFile(wallpaper,filepath)
						elif wallpaper.startswith("https:") or wallpaper.startswith("http:"):
							filename = Encode_B64(wallpaper)
							full_path = JoinPath([filepath,f'{filename}.jpg'])
							FileDownloader(wallpaper,full_path)
			xbmc.executebuiltin('Skin.SetString(ItemToEdit.BGType,2)')
			xbmc.executebuiltin(f'Skin.SetString(ItemToEdit.MultiFanart,{filepath})')
		elif not setimages and len(existing_content)>0:
			for li in existing_content:
				if isinstance(li,xbmcgui.ListItem):
					wallpaper = li.getArt('fanart')
					if wallpaper.startswith('special://'):
						MoveFile(wallpaper,filepath)
		xbmc.executebuiltin('Dialog.Close(1122)')
		del w

	def selectrandom(self):
		xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
		if ExistandMake(FOLDERPATHS.Random):
			imagecontent =  backGrounds().content
			if xbmcvfs.exists(FILEPATHS.WallpaperRandom):
				with xbmcvfs.File(FILEPATHS.WallpaperRandom,'r') as f:
					content = json.load(f)
			else:
				content = {"results":{"items":[]}}
			results = content.get('results')
			items = results.get('items')
			copyitems = items.copy()
			if len(items)>0:
				xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
				ret = xbmcgui.Dialog().yesnocustom(xbmc.getLocalizedString(31977), ADDON.LocalStr(32006),ADDON.LocalStr(32005),ADDON.LocalStr(32003),ADDON.LocalStr(32004))
				if ret == 1:
					Log('Clear existing list')
					items.clear()
					w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=imagecontent,randomimage=True)
				elif ret == 0:
					Log('Use existing list')
					existing_content = []
					for item in items:
						label = item.get('label')
						icon = item.get('icon')
						fanart = item.get('fanart')
						existing_content.append(ListItem(label=label,icon=icon,fanart=fanart))
					w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=imagecontent,randomimage=True,existing_content=existing_content)
					items.clear()
				else:
					return
			else:
				w = _FanartSelect('custom_1100_FanartSelector.xml', ADDON.PATH,content=imagecontent,randomimage=True)
				xbmc.executebuiltin('Dialog.Close(busydialognocancel, true)')
			w.doModal()
			selectedmulti = w.selectedmulti
			setimages = w.setimages
			if setimages:
				for sel in selectedmulti:
					if isinstance(sel,xbmcgui.ListItem):
						items.append({'label':sel.getLabel(),'icon':sel.getArt('icon'),'fanart':sel.getArt('fanart')})
				json_str = json.dumps(content, indent=4)
				with xbmcvfs.File(FILEPATHS.WallpaperRandom,'w') as f:
					f.write(json_str)
				self.home_window.setProperty('wallpaper.random.fixed.updated','true')
			elif not setimages and len(copyitems)>0:
				for copyitem in copyitems:
					items.append({'label':copyitem.get('label'),'icon':copyitem.get('icon'),'fanart':copyitem.get('fanart')})
				json_str = json.dumps(content, indent=4)
				with xbmcvfs.File(FILEPATHS.WallpaperRandom,'w') as f:
					f.write(json_str)		
			del w

