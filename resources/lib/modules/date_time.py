#!/usr/bin/python3
# -*- coding: utf-8 -*-



import datetime



# stat_result = path.stat()
# modified = datetime.fromtimestamp(stat_result.st_mtime, tz=timezone.utc)
# print('modified', modified)


def Datetime_now_utc():
	return  datetime.datetime.now(datetime.timezone.utc)

def Datetime_fromtimestamp(timestamp,tz=None):
	tz = getattr(datetime.timestamp,tz)
	return datetime.datetime.fromtimestamp(timestamp, tz=tz)

def Timedelta(**time):
	return datetime.timedelta(time)
