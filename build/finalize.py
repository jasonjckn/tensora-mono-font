# Post-process a Nerd-patched OTF: restore the unpatched font's names (the patcher renames to "… Nerd Font
# Mono"), its OS/2 typo metrics and fsSelection (keep v12 line spacing), set the version string, mark the
# font monospaced, and set blue zones measured from the outlines.
# Usage: finalize.py UNPATCHED.otf PATCHED.otf VERSION OUT.otf
import sys
from fontTools.ttLib import TTFont
src, pat, ver, out = sys.argv[1:]
a, b = TTFont(src), TTFont(pat)
b["name"] = a["name"]
for nid in (3, 5):   # unique ID and version: FontForge truncated "3.5.1" to "3.5." in name 5
    old = a["name"].getDebugName(nid)
    for rec in b["name"].names:
        if rec.nameID == nid: rec.string = ("Version " + ver) if nid == 5 else old.replace(old.split(" : ")[0], "FontForge 2.0") 
for k in ("sTypoAscender", "sTypoDescender", "sTypoLineGap", "fsSelection"):
    setattr(b["OS/2"], k, getattr(a["OS/2"], k))
# v15: the combining marks (U+0300..U+036F) are zero-advance glyphs drawn over the preceding cell (negative bearings).
# The patcher's --mono pass keeps those bearings but sets every glyph's advance to the cell width, marks included, so
# put their zero advance back (after checking the patcher left their outlines alone). Every other glyph has the same advance.
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
def shape(f, n):
    # bounds and signed area: the patcher's save/reload rounds control points and may drop a collinear point
    gs = f.getGlyphSet(); bp = BoundsPen(gs); gs[n].draw(bp); ap = AreaPen(gs); gs[n].draw(ap); return bp.bounds, ap.value
def same(s1, s2, tol=0.05):
    (b1, a1), (b2, a2) = s1, s2
    return (b1 is None and b2 is None) or (b1 is not None and b2 is not None and all(abs(u - v) <= tol for u, v in zip(b1, b2)) and abs(a1 - a2) <= 1)
marks = {g for c, g in a.getBestCmap().items() if 0x300 <= c <= 0x36F}
for g in sorted(marks):
    assert a["hmtx"][g][0] == 0 and same(shape(a, g), shape(b, g)), "patcher changed the mark " + g
    b["hmtx"][g] = (0, b["hmtx"][g][1])
assert len({b["hmtx"][g][0] for g in b.getGlyphOrder() if g not in marks}) == 1, "not every glyph has the same advance"
assert all(b["hmtx"][g][0] == 0 for g in marks), "a combining mark has an advance"
b["post"].isFixedPitch = 1
b["OS/2"].panose.bProportion = 9
cff = b["CFF "].cff; td = cff.topDictIndex[0]; ta = a["CFF "].cff.topDictIndex[0]
cff.fontNames = list(a["CFF "].cff.fontNames)
for k in ("FullName", "FamilyName", "Weight", "Notice", "Copyright"):
    if hasattr(ta, k): setattr(td, k, getattr(ta, k))
td.version = ver.split(";")[0]
p = td.Private
p.BlueValues = [-12, 0, 530, 542, 719, 743, 770, 782]    # baseline, x-height, caps+digits, ascender
p.OtherBlues = [-237, -236, -208, -193]                  # descenders: p/q, then g/j/y
# v15: pin the marks where they are drawn. Without a GPOS mark lookup, HarfBuzz and CoreText (so Emacs) place a mark from
# the base letter's ink: CoreText also widens the cluster when the mark's ink is off-centre (x + U+0300 measured 609.5)
# and moves a low line under g to y -335, below the descent. One mark-to-base lookup with the same anchors for every
# base letter, base (600, 0) and mark (0, 0), puts each mark's origin at the pen position after the base, which is
# where its zero-advance outline is drawn (ink over the preceding cell): HarfBuzz and CoreText then leave it as drawn.
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
order = b.getGlyphOrder(); encoded = set(b.getBestCmap().values())
fea = "markClass [%s] <anchor 0 0> @MARKS;\nfeature mark { pos base [%s] <anchor 600 0> mark @MARKS; } mark;\n" % (
    " ".join(g for g in order if g in marks), " ".join(g for g in order if g in encoded and g not in marks))
addOpenTypeFeaturesFromString(b, fea, tables=["GPOS"])
b["OS/2"].usMaxContext = 2             # base + mark (fontTools does not count mark-to-base lookups, FontForge had 1)
b.save(out)
print(out, b["name"].getDebugName(1), "|", b["name"].getDebugName(4), "|", b["name"].getDebugName(5), "| glyphs", len(b.getGlyphOrder()), "| isFixedPitch", b["post"].isFixedPitch)
