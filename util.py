import sqlite3
import datetime
import json
import requests
import pysrt

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

def get_paragraph_entities(paragraph):
	requests.post(BLUEMIX_ENDPOINT, 
