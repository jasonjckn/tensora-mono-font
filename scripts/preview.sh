#!/bin/sh
# Render a release preview: white on black, large enough to stay sharp when zoomed.
# hb-view draws at twice the size and ImageMagick downsamples with Lanczos, for smoother
# edges than drawing at the final size; hb-view (HarfBuzz) also places combining marks.
# Usage: scripts/preview.sh FONT.otf TEXT.txt OUT.png
set -eu
tmp=$(mktemp "${TMPDIR:-/tmp}/preview.XXXXXX")
trap 'rm -f "$tmp"' EXIT
hb-view --font-size=320 --margin=192 --line-space=144 \
  --background=000000 --foreground=FFFFFF \
  -O png -o "$tmp" --text-file="$2" "$1"
magick "$tmp" -filter Lanczos -resize 50% -strip "$3"
