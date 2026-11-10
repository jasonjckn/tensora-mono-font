#!/bin/sh
# Render a release preview: white on black, large enough to stay sharp when zoomed.
# Usage: scripts/preview.sh FONT.otf TEXT.txt OUT.png
set -eu
exec hb-view --font-size=160 --margin=96 --line-space=72 \
  --background=000000 --foreground=FFFFFF \
  -O png -o "$3" --text-file="$2" "$1"
