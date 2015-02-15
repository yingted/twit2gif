#!/usr/bin/env python

import sqlite3
import pysrt
import sys

con = sqlite3.connect('twit2gif.db', detect_types=sqlite3.PARSE_DECLTYPES)

with open("schema.sql") as schema_file:
    cur.executescript(schema_file.read())

def main(mp4, srt):
    cur = con.cursor()
    raw_subs = pysrt.open(srt)
    text_subs = [raw_sub.text for raw_sub in raw_subs]

    # TODO: FIX_ME(text_subs)
    entities_subs = FIX_ME(text_subs)
    subs = zip(raw_subs, entities_subs)

    with cur:
        cur.execute("INSERT INTO movies VALUES (?, ?)", (mp4, srt))
        movie_id = cur.lastrowid

        for meta, entities in subs:
            cur.execute("INSERT INTO subtitles VALUES (?, ?, ?, ?, ?, ?)", (meta.start, meta.end, meta.text, None, movie_id))
            sub_id = cur.lastrowid
            sentences = [(entity, sub_id) for entity in entities]
            cur.executemany("INSERT INTO sentences VALUES (?, ?)", sentences)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Usage: ./importer.py file.mp4 file.srt')
    main(*sys.argv[1:])
