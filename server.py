#!/usr/bin/env python
import cherrypy
import cherrypy_cors
import importer
import util
import os
import urllib
import tempfile
import flock
import subprocess
import pyshorteners.shorteners
import pysrt
import hashlib

class Server(object):
	gif_dir = 'rendered_gifs/'
	@cherrypy.expose
	@cherrypy_cors.tools.expose()
	@cherrypy.tools.json_out()
	@cherrypy.tools.json_in(force=False)
	def query(self, text=''):
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
                        shortener = pyshorteners.shorteners.Shortener('TinyurlShortener')
                        temp_url = cherrypy.url('/render/%d.gif' % subtitle, 'text=' + urllib.quote(text.encode('utf-8')))
			#print 'shorten', temp_url
			ret['url'] = shortener.short(temp_url)
		return ret
	@cherrypy.expose
	@cherrypy.tools.response_headers(headers=[('Content-Type', 'image/gif')])
	def render(self, gif, text=''):
		if not gif.endswith('.gif'):
			raise cherrypy.NotFound()
		subtitle = int(gif[:-4])
		try:
			os.makedirs(self.gif_dir)
		except OSError:
			pass
		text_hash = hashlib.sha224(text).hexdigest()
		#with tempfile.NamedTemporaryFile(suffix='.gif', prefix='render_', dir=self.gif_dir, mode='r+b', delete=False) as gif_f:
		with open(os.path.join(self.gif_dir, 'render_%d_%s.gif' % (subtitle, text_hash)), 'r+b') as gif_f:
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
					with tempfile.NamedTemporaryFile(suffix='.srt', prefix='sub_', dir=self.gif_dir) as srt_f:
						time_diff = end_time - start_time
						srt_item = pysrt.SubRipItem(index=1, start=pysrt.srttime.SubRipTime(), end=(time_diff + pysrt.srttime.SubRipTime(0,0,1,0)), text=text)
						srt_file = pysrt.SubRipFile(items=[srt_item], path=srt_f.name)
						srt_file.save()
						subprocess.check_call((
							'./convert.sh',
							os.path.abspath(video_path),
							gif_f.name,
							srt_f.name,
							util.srt_to_ffmpeg_time(start_time),
							util.srt_to_ffmpeg_time(time_diff),
						))
			gif_f.seek(0)
			return gif_f.read()
	#render._cp_config = {
	#	'response.stream': True,
	#}

if __name__ == '__main__':
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.quickstart(Server())
