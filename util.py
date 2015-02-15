import sqlite3
import datetime
SQLITE_TIME_FORMAT = '%H:%M:%S.%f'
def adapt_time(time):
	return time.strftime(SQLITE_TIME_FORMAT)
def convert_time(time):
	return datetime.datetime.strptime(time, SQLITE_TIME_FORMAT).time()
sqlite3.register_adapter(datetime.time, adapt_time)
sqlite3.register_converter('TIME', convert_time)

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
