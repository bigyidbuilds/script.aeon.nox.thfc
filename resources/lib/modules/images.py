#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS
import requests


class imageMeta():

	def __init__(self,path):
		self.FILENAME = None
		self.SIZE = None
		self.HEIGHT = None
		self.WIDTH = None
		self.FORMAT = None
		self.MODE = None
		self.IS = False
		self.RATIO = 1
		self._image(path)

	def _image(self,path):
		if path.startswith('http://') or path.startswith('https://'):
			response = requests.get(path, stream=True)
			if response.ok:
				image = response.raw
				self.IS = True
				im = Image.open(image)
			else:
				return
		else:
			if xbmcvfs.exists(path):
				self.IS = True
				im = Image.open(path)
			else:
				return
		self.FILENAME = im.filename
		self.SIZE = im.size
		self.HEIGHT = im.height
		self.WIDTH = im.width
		self.FORMAT = im.format
		self.MODE = im.mode
		self.RATIO = self._ratio(self.WIDTH,self.HEIGHT)

	def _ratio(self,width,height):
		# ratio higher then 1 is a landscape less the 1 is a portrait
		return width/height