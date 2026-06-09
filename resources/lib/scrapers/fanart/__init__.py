#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from pathlib import Path
# import ast

# all_ = []
# p = Path('.')
# files = list(p.glob('[!__init__]*.py'))
# for file in files:
# 	with open(file) as f:
# 		node = ast.parse(f.read())
# 		for class_ in [n for n in node.body if isinstance(n, ast.ClassDef)]:
# 			all_.append(class_.name)

# print(all_)
# __all__ = ['Wallpaper']

from resources.lib.modules.scrapers.fanart import *