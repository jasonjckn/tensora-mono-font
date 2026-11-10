# Compare two OTFs glyph for glyph: glyph order, the cmap, hmtx, GDEF and GPOS tables (as ttx XML dumps) and every glyph's
# outline (fontTools RecordingPen, so no hints). Everything else is ignored, head's timestamps and checksum among it.
# Prints every difference; exits 0 only when all of it matches.
# Usage: compare.py A.otf B.otf
import difflib, io, sys
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

TABLES = ("cmap", "hmtx", "GDEF", "GPOS")
SHOWN = 6        # diff lines shown per differing table

def dump(font, table):
    buf = io.BytesIO()
    font.saveXML(buf, tables=[table])
    return buf.getvalue().decode("utf-8").splitlines()

def outline(glyphset, name):
    pen = RecordingPen()
    glyphset[name].draw(pen)
    return pen.value

def main(path_a, path_b):
    a, b = TTFont(path_a), TTFont(path_b)
    diffs = 0
    def report(msg):
        nonlocal diffs
        diffs += 1
        print(msg)
    if a.getGlyphOrder() != b.getGlyphOrder():
        report("glyph order differs (%d vs %d glyphs)" % (len(a.getGlyphOrder()), len(b.getGlyphOrder())))
    for t in TABLES:
        if (t in a) != (t in b):
            report("table %s only in %s" % (t, path_a if t in a else path_b))
        elif t in a:
            xa, xb = dump(a, t), dump(b, t)
            if xa != xb:
                d = [l for l in difflib.unified_diff(xa, xb, path_a, path_b, lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
                report("table %s differs (%d changed lines)" % (t, len(d)))
                for l in d[:SHOWN]:
                    print("    " + l)
    ga, gb = a.getGlyphSet(), b.getGlyphSet()
    names = a.getGlyphOrder()
    common = [n for n in names if n in gb]
    changed = [n for n in common if outline(ga, n) != outline(gb, n)]
    if changed:
        report("%d glyph outlines differ: %s" % (len(changed), " ".join(changed)))
    only_a, only_b = [n for n in names if n not in gb], [n for n in b.getGlyphOrder() if n not in ga]
    if only_a or only_b:
        report("glyphs only in A: %s; only in B: %s" % (" ".join(only_a), " ".join(only_b)))
    print("%s vs %s: %s" % (path_a, path_b, "%d differences" % diffs if diffs else "identical"))
    return 1 if diffs else 0

if len(sys.argv) != 3:
    sys.exit("usage: compare.py A.otf B.otf")
sys.exit(main(*sys.argv[1:]))
