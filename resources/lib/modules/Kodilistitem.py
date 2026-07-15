#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

import xbmcgui



def ListItem(label='',icon=None,fanart=None,properties=None):
	li = xbmcgui.ListItem(label)
	art = {}
	if icon:
		art.update({'icon':icon})
	if fanart:
		art.update({'fanart':fanart})
	if art:
		li.setArt(art)
	if properties:
		for k,v in properties.items():
			if isinstance(v,str):
				li.setProperty(k,v)
			else:
				li.setProperty(k,json.dumps(v))
	return li


# thumb	string - image filename
# poster	string - image filename
# banner	string - image filename
# fanart	string - image filename
# clearart	string - image filename
# clearlogo	string - image filename
# landscape	string - image filename
# icon	string - image filename
