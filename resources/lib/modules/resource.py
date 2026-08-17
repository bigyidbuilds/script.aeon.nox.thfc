#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xbmcvfs

import xml.etree.ElementTree as ET

from .kodiaddon import Addon
from .kodivfs import JoinPath 


def GetAssets(addon_id,dir_name):
	# full string details ="resource://<add-on-id>/<path-to-file>"
	asset_str = "resource://{}/{}/{}"
	assets = []
	RESOURCE_ADDON = Addon(addon_id)
	file_path = JoinPath([RESOURCE_ADDON.PATH,'assets.xml'])
	if xbmcvfs.exists(file_path):
		tree =ET.parse(file_path)
		root = tree.getroot()
		for asset in root.find(f"./dir[@name='{dir_name}']"):
			assets.append(asset_str.format(RESOURCE_ADDON.ID,dir_name,asset.text))
	return assets


