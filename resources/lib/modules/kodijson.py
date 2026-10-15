#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

import xbmc

from .kodilog import Log



info = { "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "params": { "filter": { "id": "AudioLibrary.GetAlbums", "type": "method" } }, "id": 1 }

info2 ={"jsonrpc": "2.0", "method": "Textures.GetTextures", "params": {  "properties":["url", "cachedurl", "lasthashcheck", "imagehash", "sizes"] , "filter": {"field": "url", "operator": "is", "value":"http://assets.fanart.tv/fanart/music/db008806-16f6-48fc-8521-3d953709689d/artistbackground/a-day-to-remember-4f235569da7d7.jpg"}}, "id": 1}

def GetTextures(field=None,operator=None,value=None):
	method = "Textures.GetTextures"
	params = {  "properties":["url", "cachedurl", "lasthashcheck", "imagehash", "sizes"] }
	if field and operator and value:
		params.update({"filter":{"field":field,"operator":operator,"value":value}})
	data = get_json(method,params)
	return data

def FavouritesDetails():
	method = "Favourites.GetFavourites"
	permission = "ReadData"
	params = {"properties": ["window","path","thumbnail","windowparameter"]}
	data = get_json(method,params,permission=permission)
	return data

def SettingsSkin():
	method = "Settings.GetSkinSettings"
	permission ="ReadData"
	data = get_json(method,permission=permission)
	results = data.get('results')
	if results:
		settings = results.get('settings')
		if settings:
			return settings
		else:
			return None
	else:
			return None

def SettingSkin(setting_id):
	""" {'type': 'boolean'}, {'type': 'string'}
	"""
	method = "Settings.GetSkinSettingValue"
	permission = 'ReadData'
	params = {"setting": setting_id}
	data =	get_json(method,params,permission=permission)
	result = data.get('result')
	if result:
		value = result.get('value')
		if value:
			return value
		else:
			return None
	else:
		return None


def get_json(method:str, params=[],**kwargs) -> dict:
	"""communicate with kodi JSON-RPC

	Args:
		method (str): the JSON-RPC method
		params (dict): the JSON_RPC params

	Returns:
		dict: JSON_RPC results
	"""
	base_query = {"jsonrpc":"2.0" , "method":method , "id":1}
	base_query.update({"params":params})
	if len(kwargs)>0:
		base_query.update(kwargs)
	query = xbmc.executeJSONRPC(json.dumps(base_query))
	return json.loads(query)




