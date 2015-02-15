#!/usr/bin/env python
import cherrypy
class Server(object):
	def index(self):
		return 'Hello World!'
	index.exposed = True

if __name__ == '__main__':
	cherrypy.quickstart(Server())
