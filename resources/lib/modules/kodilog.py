#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xbmc

from . import ADDON

def Log(msg):
	if ADDON.SETTINGS.getBool('general.debug'):
		from inspect import getframeinfo, stack
		fileinfo = getframeinfo(stack()[1][0])
		xbmc.log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(ADDON.NAME,ADDON.VERSION,msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)