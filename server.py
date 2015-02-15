#!/usr/bin/env python
import cherrypy
import importer
import util

class Server(object):
	@cherrypy.expose
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in(force=False)
	def query(self):
		try:
			text = cherrypy.request.json
		except AttributeError:
			text = cherrypy.request.body.params['text']
		paragraph = util.get_paragraph_entities([text])[0]
		with importer.cursor() as c:
			c.execute('CREATE TEMP TABLE query_sentences(query_entities UNIQUE TEXT NOT NULL)')
			try:
				c.executemany('INSERT OR IGNORE INTO query_sentences VALUES (?)', [(sentence,) for sentence in paragraph])
				res = list(c.execute('''
					SELECT subtitle, quote
						FROM query_sentences
						INNER JOIN sentences
							ON entities=query_entities
						LIMIT 1
				'''))
			finally:
				c.execute('DROP TABLE query_sentences')
		ret = {
			'quote': None,
			'url': None,
		}
		if res:
			subtitle, quote = res[0]
			ret['quote'] = quote
			ret['url'] = cherrypy.url('/render.gif?subtitle=%d' % subtitle)
		return ret
	@cherrypy.expose
	def render(self, gif):
		if not gif.endswith('.gif'):
			raise cherrypy.NotFound()
		subtitle = int(gif[:-4])
		return 'subtitle = %d' % subtitle

if __name__ == '__main__':
	cherrypy.quickstart(Server())
