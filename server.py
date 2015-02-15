#!/usr/bin/env python
import cherrypy
import cherrypy_cors
import importer
import util
import os
import tempfile
import flock
import subprocess

class Server(object):
	gif_dir = 'rendered_gifs/'
	@cherrypy.expose
	@cherrypy_cors.tools.expose()
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in(force=False)
	def query(self, text=''):
		print repr(text)
		paragraph = util.get_paragraph_entities([text])[0]
		with importer.cursor() as c:
			c.execute('CREATE TEMP TABLE query_sentences(query_entities TEXT NOT NULL UNIQUE)')
			try:
				c.executemany('INSERT OR IGNORE INTO query_sentences VALUES (?)', [(sentence,) for sentence in paragraph])
				res = list(c.execute('''
					SELECT subtitle, quote
						FROM query_sentences
						INNER JOIN sentences
							ON entities=query_entities
						INNER JOIN subtitles
							ON subtitles.rowid=subtitle
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
			ret['url'] = cherrypy.url('/render/%d.gif' % subtitle)
		return ret
	@cherrypy.expose
	@cherrypy.tools.response_headers(headers=[('Content-Type', 'image/gif')])
	def render(self, gif):
		if not gif.endswith('.gif'):
			raise cherrypy.NotFound()
		subtitle = int(gif[:-4])
		try:
			os.makedirs(self.gif_dir)
		except OSError:
			pass
		#with tempfile.NamedTemporaryFile(suffix='.gif', prefix='render_', dir=self.gif_dir, delete=False) as gif_f:
		with open(os.path.join(self.gif_dir, 'render_%d.gif' % subtitle), 'w+b') as gif_f:
			with flock.Flock(gif_f, flock.LOCK_EX):
				gif_f.seek(0, 2)
				size = gif_f.tell()
				#print 'subtitle', subtitle, 'size', size
				if not size:
					#print 'new file', gif_f.name
					with importer.cursor() as c:
						for video_path, start_time, end_time in c.execute('''
							SELECT video_path, start_time, end_time
								FROM subtitles
								INNER JOIN movies
									ON movies.rowid=movie
								WHERE subtitles.rowid=?
						''', (subtitle,)):
							break
						else:
							raise cherrypy.NotFound()
					subprocess.check_call((
						'./convert.sh',
						os.path.abspath(video_path),
						gif_f.name,
						util.srt_to_ffmpeg_time(start_time),
						util.srt_to_ffmpeg_time(end_time - start_time),
					))
			gif_f.seek(0)
			return gif_f.read()
	#render._cp_config = {
	#	'response.stream': True,
	#}

if __name__ == '__main__':
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.quickstart(Server())
