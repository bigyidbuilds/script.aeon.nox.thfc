#!/usr/bin/python3
# -*- coding: utf-8 -*-


import base64



def Encode_B64(string):
	return base64.b64encode(string.encode()).decode()

def Decode_B64(string):
	return base64.b64decode(string).decode()
