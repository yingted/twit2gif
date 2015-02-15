#!/usr/bin/env python
import cherrypy
import importer
import util
class Server(object):
	def query(self):
		return 'Hello World!'
	query.exposed = True

if __name__ == '__main__':
	cherrypy.quickstart(Server())
