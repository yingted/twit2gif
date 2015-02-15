CREATE TABLE movies(
	video_path TEXT NOT NULL,
	subtitle_path TEXT NOT NULL
);
-- We need custom pysqlite adapter and converter for datetime.time
CREATE TABLE subtitles(
	FOREIGN KEY(movie) REFERENCES movies(rowid),
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	quote TEXT NOT NULL,
	gif_path TEXT
);
CREATE TABLE sentences(
	FOREIGN KEY(subtitle) REFERENCES subtitles(rowid),
	entities TEXT NOT NULL
);
CREATE INDEX sentences_entities_index ON sentences(entities);
