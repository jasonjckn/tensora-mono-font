# Generate an OTF from an SFD.  Usage: gen.py IN.sfd OUT.otf   (same as v14's)
import fontforge, sys
fontforge.open(sys.argv[1]).generate(sys.argv[2])
