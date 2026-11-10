#!/bin/sh
# Render every PNG the README and the release pages use, with the newest release's fonts:
# each release preview (assets/tensora-mono-vN-<topic>.txt -> .png) and the README images.
# Usage: scripts/render-all.sh
set -eu
cd "$(dirname "$0")/.."
latest=$(ls -d font_releases/*/ | sort | tail -1)
for txt in assets/tensora-mono-v*-*.txt; do
  scripts/preview.sh "${latest}TensoraMonoN.otf" "$txt" "${txt%.txt}.png"
  echo "rendered ${txt%.txt}.png"
done
uv run --with pillow --with pygments python -I scripts/readme-images.py "$latest"
