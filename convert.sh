#!/bin/bash
# usage: ./convert.sh file.mp4 file.gif start_time duration_time
# time format: HH:MM:SS.SSSSSS
set -e
set -o pipefail
input_file="$1"
output_file="$2"
sub_file="$3"
start_time="$4"
duration_time="$5"
ffmpeg=ffmpeg
command -v "$ffmpeg" &>/dev/null || ffmpeg=avconv
"$ffmpeg" -ss "$start_time" -i "$input_file" -vf "scale=320:-1,subtitles=$sub_file:force_style='FontName=DejaVu Serif,FontSize=36,Outline=3'" -t "$duration_time" -r 10 -f image2pipe -vcodec ppm - | convert -delay 10 -loop 0 ppm:- gif:"$output_file"
