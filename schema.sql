CREATE TABLE IF NOT EXISTS movies(
	video_path TEXT NOT NULL,
	subtitle_path TEXT NOT NULL
);
-- We need custom pysqlite adapter and converter for datetime.time
CREATE TABLE IF NOT EXISTS subtitles(
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	quote TEXT NOT NULL,
	gif_path TEXT,
	movie INTEGER,
	FOREIGN KEY(movie) REFERENCES movies(rowid)
);
CREATE TABLE IF NOT EXISTS sentences(
	entities TEXT NOT NULL,
	subtitle INTEGER,
	FOREIGN KEY(subtitle) REFERENCES subtitles(rowid)
);
CREATE INDEX IF NOT EXISTS sentences_entities_index ON sentences(entities);
