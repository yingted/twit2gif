import sqlite3
import datetime
import json
import requests
import pysrt
import os

sqlite3.register_adapter(pysrt.srttime.SubRipTime, str)
sqlite3.register_converter('TIME', pysrt.srttime.SubRipTime.from_string)

orig_sqlite3_connect = sqlite3.connect
def sqlite3_connect(*args, **kwargs):
	if 'detect_types' not in kwargs and 2 <= len(args):
		args = list(args)
		args[2] = sqlite3.PARSE_DECLTYPES
		args = tuple(args)
	else:
		kwargs['detect_types'] = sqlite3.PARSE_DECLTYPES
	return orig_sqlite3_connect(*args, **kwargs)
sqlite3.connect = sqlite3_connect

BLUEMIX_ROOT = os.getenv('BLUEMIX_ROOT')

def get_paragraph_entities(paragraph):
	'''
	>>> get_paragraph_entities([u'Hello, World!'])
	[['...']]
	'''
	return requests.post(BLUEMIX_ROOT + '/entities', data=json.dumps(paragraph), headers={
		'Content-Type': 'application/json',
	}).json()
