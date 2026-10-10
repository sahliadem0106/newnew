#!/usr/bin/env bash
# Burn a CCTV-style camera label and running clock onto a generated clip.
# AI video models garble on-screen text, so the label is added afterwards.
#
# Usage: ./cctv_overlay.sh input.mp4 output.mp4 "CAM-03 ESCALATOR UP" "2026-10-12 14:07:30"
set -euo pipefail

in="$1"; out="$2"; label="$3"; start="$4"
epoch=$(date -u -d "$start" +%s)

ffmpeg -y -loglevel error -i "$in" -vf "\
format=yuv420p,\
eq=saturation=0.75:contrast=1.05,\
noise=alls=6:allf=t,\
drawbox=x=0:y=0:w=iw:h=44:color=black@0.55:t=fill,\
drawtext=text='${label}':x=16:y=12:fontsize=24:fontcolor=white,\
drawtext=text='%{pts\:gmtime\:${epoch}\:%Y-%m-%d %H\\\\\:%M\\\\\:%S}':x=w-tw-16:y=12:fontsize=24:fontcolor=white,\
drawtext=text='● REC':x=16:y=h-36:fontsize=20:fontcolor=red" \
  -c:a copy "$out"
