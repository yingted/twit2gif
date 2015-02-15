#!/bin/bash
set -ex
rm -rf twit2gif.db rendered_gifs
find movies -name \*.srt -exec bash -c '
       shopt -s nullglob;
       set -x;
       ./importer.py "${0%srt}"{[^s]*,s[^r]*,sr[^t]*,srt?*} "$0"
' {} \;
