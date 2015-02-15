import sqlite3
import datetime
import json
import requests
import pysrt
import os

sqlite3.register_adapter(pysrt.srttime.SubRipTime, str)
sqlite3.register_converter('TIME', pysrt.srttime.SubRipTime.from_string)

BLUEMIX_ROOT = os.getenv('BLUEMIX_ROOT')

def get_paragraph_entities(paragraph):
	'''
	>>> get_paragraph_entities([u'Hello, World!'])
	[['...']]
	'''
	return requests.post(BLUEMIX_ROOT + '/entities', data=json.dumps(paragraph), headers={
		'Content-Type': 'application/json',
	}).json()

def srt_to_ffmpeg_time(time):
	return time.to_time().strftime('%H:%M:%S.%f')
