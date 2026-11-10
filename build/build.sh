#!/bin/zsh
# Build a release's two OTFs from its two SFDs: FontForge generate (build/gen.py), Nerd Fonts 3.5.1 patch, finalize
# (build/finalize.py: the marks get their zero advance back after the patcher's --mono pass, and a GPOS mark-to-base lookup pins
# them where they are drawn), then hint the font's own glyphs with otfautohint.
# Reads src/TensoraMono_vN.sfd and src/TensoraMono_N_vN.sfd, stages in build/.cache/out/, and writes
# font_releases/DATE-vN/TensoraMono.otf and TensoraMonoN.otf (an existing directory of that name is overwritten).
# build/.cache/ also holds the Nerd Fonts font patcher: downloaded and unpacked on the first run.
# Usage: build/build.sh N DATE        e.g. build/build.sh 17 2026-11-09        (any working directory)
set -e
B=${0:A:h}; REPO=${B:h}; C=$B/.cache; O=$C/out; P=$C/FontPatcher
NERD=3.5.1; SHA=42bcb32145499a35732274c7fc48deb434ad0d2e0e118f98527c1479c6fa251a
PY="--python 3.13"       # uv's default here is an x86_64 Python 3.15, where afdko's pyclipper does not build
die() { print -u2 "build.sh: $*"; exit 1 }
need() { command -v $1 >/dev/null || die "$1 not found on PATH ($2)" }
[[ $# == 2 && $1 == <-> && -n $2 && $2 != */* ]] || { print -u2 "usage: build/build.sh N DATE   (e.g. build/build.sh 17 2026-11-09)"; exit 2 }
N=$1; VER="0.$N;Nerd Fonts $NERD"; REL=$REPO/font_releases/$2-v$N
need fontforge "install FontForge, e.g. brew install fontforge"
need uv "install uv, e.g. brew install uv"
for sfd in TensoraMono_v$N TensoraMono_N_v$N; do
  [[ -f $REPO/src/$sfd.sfd ]] || die "$REPO/src/$sfd.sfd not found"
done

# The font patcher: download once, check the hash on every run, unpack once.
ZIP=$C/dl/FontPatcher.zip
if [[ ! -f $ZIP ]]; then
  need curl "needed to download the font patcher"
  mkdir -p $C/dl
  curl -fsSL -o $ZIP.part https://github.com/ryanoasis/nerd-fonts/releases/download/v$NERD/FontPatcher.zip
  mv $ZIP.part $ZIP      # a failed download leaves no $ZIP behind
fi
[[ $(shasum -a 256 < $ZIP) == $SHA\ * ]] || die "$ZIP does not match SHA-256 $SHA; delete it (and $P) and rerun to download it again"
if [[ ! -f $P/font-patcher ]]; then
  need unzip "needed to unpack the font patcher"
  unzip -qo $ZIP -d $P.part
  mv $P.part $P
fi

# FontForge's startup banner and warnings are noise; a failure prints everything.
F() {
  local out
  out=$(fontforge -lang=py -script "$@" 2>&1) || { print -u2 -r -- $out; print -u2 "build.sh: fontforge failed: $*"; return 1 }
  print -r -- $out | grep -v -e pkg_resources -e Copyright -e License -e 'with many' -e 'Based on' -e '^ ' || true
}
mkdir -p $O/unpatched $O/patched $O/final
for u sfd in TensoraMono TensoraMono_v$N TensoraMonoN TensoraMono_N_v$N; do
  F $B/gen.py $REPO/src/$sfd.sfd $O/unpatched/$u.otf
  rm -f $O/patched/${u}NerdFontMono-Regular.otf       # so a patcher that wrote nothing cannot leave an old file for finalize
  fontforge -script $P/font-patcher --complete --mono --careful --no-progressbars -ext otf --outputdir $O/patched $O/unpatched/$u.otf > $O/patched/$u.log 2>&1 \
    || die "font-patcher failed, see $O/patched/$u.log"
  uv run -q $=PY --with fonttools python -I $B/finalize.py $O/unpatched/$u.otf $O/patched/${u}NerdFontMono-Regular.otf "$VER" $O/final/$u.unhinted.otf
  # hint only the font's own glyphs (otfautohint crashes on some Nerd icons)
  G=$(uv run -q $=PY --with fonttools python -I -c "import sys; from fontTools.ttLib import TTFont; print(','.join(TTFont(sys.argv[1]).getGlyphOrder()))" $O/unpatched/$u.otf)
  uv run -q $=PY --with afdko otfautohint -a -g "$G" --log $O/final/$u.hint.log -o $O/final/$u.otf $O/final/$u.unhinted.otf
done
mkdir -p $REL
cp $O/final/TensoraMono.otf $O/final/TensoraMonoN.otf $REL/
echo "built: $REL/"
