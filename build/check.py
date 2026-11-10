# Release invariants of a Tensora Mono OTF. Prints every failure, exits 1 if there is any.
#  - every glyph mapped from U+0300..U+036F (combining marks) has advance 0 and GDEF glyph class 3 (mark)
#  - every other glyph, .notdef included, has advance 600
#  - GPOS has a MarkBase (lookup type 4) lookup, which places the marks over the base letter
#  - post.isFixedPitch is 1
# Usage: check.py OTF...
import sys
from fontTools.ttLib import TTFont

CELL = 600
MARK_BASE, EXTENSION = 4, 9

def lookup_types(gpos):
    # a lookup of type 9 (extension) wraps the real type in each subtable
    for lk in gpos.LookupList.Lookup:
        yield from ((st.ExtensionLookupType if lk.LookupType == EXTENSION else lk.LookupType) for st in lk.SubTable)

def failures(path):
    f = TTFont(path)
    marks = {g for cp, g in f.getBestCmap().items() if 0x300 <= cp <= 0x36F}
    if not marks:
        yield "no glyph is mapped from U+0300..U+036F"
    hmtx = f["hmtx"]
    classes = f["GDEF"].table.GlyphClassDef.classDefs if "GDEF" in f and f["GDEF"].table.GlyphClassDef else {}
    for g in sorted(marks):
        if hmtx[g][0] != 0:
            yield "mark %s has advance %d, not 0" % (g, hmtx[g][0])
        if classes.get(g) != 3:
            yield "mark %s has GDEF glyph class %s, not 3" % (g, classes.get(g))
    for g in f.getGlyphOrder():
        if g not in marks and hmtx[g][0] != CELL:
            yield "glyph %s has advance %d, not %d" % (g, hmtx[g][0], CELL)
    if "GPOS" not in f:
        yield "no GPOS table"
    elif MARK_BASE not in lookup_types(f["GPOS"].table):
        yield "GPOS has no MarkBase (type 4) lookup"
    if f["post"].isFixedPitch != 1:
        yield "post.isFixedPitch is %s, not 1" % f["post"].isFixedPitch

if len(sys.argv) < 2:
    sys.exit("usage: check.py OTF...")
bad = 0
for path in sys.argv[1:]:
    fails = list(failures(path))
    for msg in fails:
        print("%s: FAIL %s" % (path, msg))
    print("%s: %s" % (path, "%d failures" % len(fails) if fails else "ok"))
    bad += len(fails)
sys.exit(1 if bad else 0)
