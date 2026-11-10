# Convert a finished CFF OTF to TrueType outlines: every glyph's cubic Béziers become quadratics (fontTools cu2qu, at most
# MAX_ERR units off), with the contours reversed because TrueType winds them the other way. The CFF table becomes glyf + loca,
# maxp becomes version 1.0 and post format 2 (the glyph names stay). Every other table (cmap, GDEF, GPOS, name, OS/2, ...) is
# kept; hmtx keeps its advances, and a left side bearing becomes the glyph's new xMin, which TrueType rasterizers expect.
# The result has no TrueType hinting: no fpgm, prep, cvt or glyph instructions.
# Usage: otf2ttf.py IN.otf OUT.ttf
import sys
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

MAX_ERR = 1.0        # font units

def quadratic_glyphs(font):
    glyphset = font.getGlyphSet()
    glyphs = {}
    for name in font.getGlyphOrder():
        pen = TTGlyphPen(glyphset)
        glyphset[name].draw(Cu2QuPen(pen, MAX_ERR, reverse_direction=True))
        glyphs[name] = pen.glyph()
    return glyphs

def convert(font):
    assert font.sfntVersion == "OTTO" and "CFF " in font, "not a CFF OTF"
    order = font.getGlyphOrder()
    font["loca"] = newTable("loca")
    font["glyf"] = glyf = newTable("glyf")
    glyf.glyphOrder = order
    glyf.glyphs = quadratic_glyphs(font)
    del font["CFF "]
    if "VORG" in font:
        del font["VORG"]
    hmtx = font["hmtx"]
    moved = 0
    for name, g in glyf.glyphs.items():
        if g.numberOfContours:
            g.recalcBounds(glyf)
            moved += hmtx[name][1] != g.xMin
            hmtx[name] = (hmtx[name][0], g.xMin)
    # the unhinted font needs one zone and no twilight points, storage, functions, stack or instructions; fontTools fills in
    # the point, contour and component counts when it saves
    maxp = font["maxp"] = newTable("maxp")
    maxp.tableVersion = 0x00010000
    maxp.maxZones = 1
    maxp.maxTwilightPoints = maxp.maxStorage = maxp.maxFunctionDefs = maxp.maxInstructionDefs = 0
    maxp.maxStackElements = maxp.maxSizeOfInstructions = 0
    post = font["post"]
    post.formatType = 2.0
    post.extraNames, post.mapping, post.glyphOrder = [], {}, order
    font["head"].glyphDataFormat = 0
    font.sfntVersion = "\000\001\000\000"
    return moved

if len(sys.argv) != 3:
    sys.exit("usage: otf2ttf.py IN.otf OUT.ttf")
src, out = sys.argv[1:]
f = TTFont(src)
moved = convert(f)
f.save(out)
print(out, "| glyphs", len(f.getGlyphOrder()), "| left side bearings moved", moved)
