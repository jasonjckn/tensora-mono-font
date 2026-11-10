# Render the README's banner and specimens, each in a dark and a light version for
# GitHub's <picture> prefers-color-scheme sources. Backgrounds are transparent outside
# the banner panel, so the images sit on any theme.
#
# Usage: uv run --with pillow --with pygments python scripts/readme-images.py [FONT_DIR]
# FONT_DIR defaults to the newest font_releases/* directory.
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else sorted(
    (ROOT / "font_releases").iterdir(), key=lambda p: p.name)[-1]
OUT = ROOT / "assets" / "readme"
OUT.mkdir(parents=True, exist_ok=True)

# GitHub's own palette (Primer), so the images match the page around them.
THEMES = {
    "dark":  dict(fg="#e6edf3", muted="#9198a1", accent="#f78166", panel="#161b22", border="#30363d"),
    "light": dict(fg="#1f2328", muted="#59636e", accent="#bc4c00", panel="#f6f8fa", border="#d0d7de"),
}
# Draw at 4x the displayed size, then downsample with Lanczos to 2x: the saved PNGs are
# twice their display size (sharp on Retina screens), with smoother edges than drawing at 2x.
SCALE = 4
SAVE_SCALE = 2


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size * SCALE)


def text_width(f, s):
    return f.getbbox(s)[2]


def downsample(img):
    w, h = img.size
    return img.resize((w * SAVE_SCALE // SCALE, h * SAVE_SCALE // SCALE), Image.Resampling.LANCZOS)


def save(img, name, theme):
    downsample(img).save(OUT / f"{name}-{theme}.png", optimize=True)


def banner(theme, c):
    w, h, pad = 1200, 400, 64
    img = Image.new("RGBA", (w * SCALE, h * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w * SCALE - 1, h * SCALE - 1], radius=20 * SCALE,
                        fill=c["panel"], outline=c["border"], width=2 * SCALE)
    title, sub = font("TensoraMonoN.otf", 128), font("TensoraMonoN.otf", 26)
    sample = font("TensoraMonoN.otf", 30)
    d.text((pad * SCALE, 70 * SCALE), "Tensora Mono", font=title, fill=c["fg"])
    d.text((pad * SCALE + 6 * SCALE, 232 * SCALE),
           "a monospace font for code  ·  Nerd Fonts inside", font=sub, fill=c["muted"])
    # One line of what sets it apart: code punctuation, then the Unicode it covers.
    x, y = pad * SCALE + 6 * SCALE, 300 * SCALE
    for s, col in (("{ } => != 0O 1lI", c["fg"]), ("   ", c["fg"]),
                   ("⏺ ✻ ⎿ ✓ ⚠ → x² H₂O ᴀʙᴄ ⓐⓑⓒ 𝗕𝗼𝗹𝗱", c["accent"])):
        d.text((x, y), s, font=sample, fill=col)
        x += text_width(sample, s)
    save(img, "banner", theme)


def lines_image(name, theme, c, rows, size=34, gap=18, width=1200):
    """Rows of (text, colour key, font file) on a transparent background."""
    fonts = {f: font(f, size) for _, _, f in rows}
    asc, desc = fonts[rows[0][2]].getmetrics()
    lh = asc + desc + gap * SCALE
    img = Image.new("RGBA", (width * SCALE, lh * len(rows) + 8 * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (s, col, f) in enumerate(rows):
        d.text((4 * SCALE, i * lh + 4 * SCALE), s, font=fonts[f], fill=c[col])
    save(img, name, theme)


SPECIMEN = [
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "fg"),
    ("abcdefghijklmnopqrstuvwxyz", "fg"),
    ("0123456789  !@#$%^&*()[]{}<>?", "fg"),
    ("-> => != <= >= :: |> // /* */ ~ ` ' \"", "muted"),
    ("0O  1lI|  rn m  {[( )]}  ,.;:", "accent"),
]

VARIANTS = [
    ("Tensora Mono     fn len(n) = n + 1  # Nothing", "fg", "TensoraMono.otf"),
    ("Tensora Mono N   fn len(n) = n + 1  # Nothing", "fg", "TensoraMonoN.otf"),
]

CODE = ROOT / "assets" / "readme" / "code"
# Pygments styles for the syntax colours, picked to sit on the window colours below.
CODE_STYLES = {"dark": "github-dark", "light": "xcode"}
WINDOW = {
    "dark":  dict(bg="#0d1117", bar="#161b22", border="#30363d", gutter="#6e7681", title="#9198a1"),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", gutter="#8c959f", title="#59636e"),
}


def code_window(path, theme, size=28):
    """An editor window: title bar with traffic lights and the file name, line numbers, highlighted code."""
    from pygments.lexers import get_lexer_for_filename
    from pygments.styles import get_style_by_name
    style, w = get_style_by_name(CODE_STYLES[theme]), WINDOW[theme]
    f = font("TensoraMono.otf", size)
    src = path.read_text()
    lines = src.rstrip("\n").split("\n")
    cell = text_width(f, "M")
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 1.35)
    bar, pad, gut = 44 * SCALE, 28 * SCALE, cell * 4
    width = pad * 2 + gut + cell * max(82, max(map(len, lines)))
    height = bar + pad * 2 + lh * len(lines)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = 12 * SCALE
    d.rounded_rectangle([0, 0, width - 1, height - 1], radius=r, fill=w["bg"], outline=w["border"], width=2 * SCALE)
    d.rounded_rectangle([0, 0, width - 1, bar], radius=r, fill=w["bar"], outline=w["border"], width=2 * SCALE)
    d.rectangle([2 * SCALE, bar - r, width - 3 * SCALE, bar - 1], fill=w["bar"])  # square off the bar's bottom
    d.line([0, bar, width, bar], fill=w["border"], width=2 * SCALE)
    for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        cx, cy = (24 + 22 * i) * SCALE, bar // 2
        d.ellipse([cx - 7 * SCALE, cy - 7 * SCALE, cx + 7 * SCALE, cy + 7 * SCALE], fill=col)
    tf = font("TensoraMono.otf", 18)
    d.text((width // 2, bar // 2), path.name, font=tf, fill=w["title"], anchor="mm")
    x0, y = pad + gut, bar + pad
    for n in range(len(lines)):
        d.text((pad + cell * 2, y + n * lh), str(n + 1), font=f, fill=w["gutter"], anchor="ra")
    x, row = x0, 0
    for tok, val in get_lexer_for_filename(path.name).get_tokens(src):
        hexcol = style.style_for_token(tok)["color"]  # already inherited from parent tokens
        colour = "#" + hexcol if hexcol else THEMES[theme]["fg"]
        for k, part in enumerate(val.split("\n")):
            if k:
                x, row = x0, row + 1
            if part:
                d.text((x, y + row * lh), part, font=f, fill=colour)
                x += cell * len(part)
    save(img, f"code-{path.stem}", theme)


for theme, c in THEMES.items():
    for path in sorted(p for p in CODE.iterdir() if p.suffix in (".clj", ".jl", ".rs")):
        code_window(path, theme)
    banner(theme, c)
    lines_image("specimen", theme, c, [(s, col, "TensoraMono.otf") for s, col in SPECIMEN], size=40)
    lines_image("variants", theme, c, VARIANTS, size=34)
print("wrote", OUT)
