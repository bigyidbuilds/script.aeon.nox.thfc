#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS
import requests

from .kodijson import GetTextures
from .kodilog import Log
from .kodivfs import FileExtUrl

class imageMeta():

	def __init__(self,path,**kwargs):
		self.FILENAME = None
		self.SIZE = None
		self.HEIGHT = kwargs.get('height',None)
		self.WIDTH = kwargs.get('width',None)
		self.FORMAT = None
		self.MODE = None
		self.IS = False
		self.RATIO = 1
		self._image(path)

	def _image(self,path):
		if path.endswith(('.jpg','.png')):
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
		else:
			image = GetTextures(field="url",operator="is",value=path)
			if path.startswith('http://') or path.startswith('https://'):
				response = requests.get(path, stream=True)
				if response.ok:
					self.IS = True
				if self.HEIGHT and self.WIDTH:
					self.HEIGHT = int(self.HEIGHT)
					self.WIDTH = int(self.WIDTH)
				else:
					self.HEIGHT,self.WIDTH = _textures(image)
			else:
				if xbmcvfs.exists(path):
					self.IS = True 
				self.HEIGHT,self.WIDTH = _textures(image)
			self.FORMAT = (FileExtUrl(path)).lstrip('.').upper()
			self.SIZE = [int(self.WIDTH),int(self.HEIGHT)]
			self.RATIO = self._ratio(self.WIDTH,self.HEIGHT)
				

	def _textures(self,data):
		height = None
		width = None
		result = data.get('result')
		if result:
			textures = result.get('textures')
			if textures and len(textures)>=1:
				for texture in textures:
					sizes = texture.get('sizes')
					if sizes and len(sizes)>=1:
						for size in sizes:
							width = size.get('width')
							height = size.get('height')
		return height,width


	def _ratio(self,width,height):
		# ratio higher then 1 is a landscape less the 1 is a portrait
		return width/height