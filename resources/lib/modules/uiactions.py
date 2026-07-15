#!/usr/bin/python3
# -*- coding: utf-8 -*-

class uiActions(object):
	"""docstring for uiActions wrapper for keyboard & remote inputs"""
	def __init__(self):
		super(uiActions, self).__init__()
		self.ACTION_LEFT = 1
		self.ACTION_RIGHT = 2
		self.ACTION_UP = 3
		self.ACTION_DOWN = 4
		self.ACTION_PAGE_UP = 5
		self.ACTION_PAGE_DOWN = 6
		self.ACTION_SELECT_ITEM = 7
		self.ACTION_PARENT_DIR = 9
		self.ACTION_PREVIOUS_MENU = 10
		self.ACTION_SHOW_INFO = 11
		self.ACTION_STOP = 13
		self.ACTION_NEXT_ITEM = 14
		self.ACTION_PREV_ITEM = 15
		self.ACTION_SHOW_CODEC = 27
		self.ACTION_SHOW_FULLSCREEN = 36
		self.ACTION_DELETE_ITEM = 80
		self.ACTION_NAV_BACK = 92
		self.ACTION_MENU = 163
		self.ACTION_LAST_PAGE = 160
		self.ACTION_RECORD = 170

		self.ACTION_CREATE_BOOKMARK = 96

		self.ACTION_PAUSE = 12
		self.ACTION_PLAY = 68
		self.ACTION_PLAYER_FORWARD = 77
		self.ACTION_PLAYER_PLAY = 79
		self.ACTION_PLAYER_PLAYPAUSE = 229
		self.ACTION_PLAYER_REWIND = 78

		self.ACTION_MOUSE_WHEEL_UP = 104
		self.ACTION_MOUSE_WHEEL_DOWN = 105
		self.ACTION_MOUSE_MOVE = 107
		self.ACTION_MOUSE_LEFT_CLICK = 100
		self.ACTION_MOUSE_RIGHT_CLICK = 101

		self.KEY_CONTEXT_MENU = 117
		self.KEY_HOME = 159
		self.KEY_ESC = 61467

		self.REMOTE_0 = 58
		self.REMOTE_1 = 59
		self.REMOTE_2 = 60
		self.REMOTE_3 = 61
		self.REMOTE_4 = 62
		self.REMOTE_5 = 63
		self.REMOTE_6 = 64
		self.REMOTE_7 = 65
		self.REMOTE_8 = 66
		self.REMOTE_9 = 67

		self.ACTION_JUMP_SMS2 = 142
		self.ACTION_JUMP_SMS3 = 143
		self.ACTION_JUMP_SMS4 = 144
		self.ACTION_JUMP_SMS5 = 145
		self.ACTION_JUMP_SMS6 = 146
		self.ACTION_JUMP_SMS7 = 147
		self.ACTION_JUMP_SMS8 = 148
		self.ACTION_JUMP_SMS9 = 149
