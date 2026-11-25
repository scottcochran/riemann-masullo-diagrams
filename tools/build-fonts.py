#!/usr/bin/env python3
"""Build the fonts the posters embed, and the advance widths the generator lays text out with.

    uv run --with fonttools==4.68.0 --with brotli==1.2.0 python tools/build-fonts.py SRC_DIR

SRC_DIR holds the four Noto files named in SOURCES, downloaded from google/fonts at the commit given there; the
script checks each against its SHA-256 before it reads it. It writes, from them:

- diagrams/src/fonts/*.woff2: six faces, subset to the characters in WANT. Noto Sans in regular, bold and italic,
  and Noto Sans Mono in regular and bold, are instanced from the variable fonts at wdth 100 (no poster sets bold
  italic: a bold run in an italic line is drawn with the italic face, emboldened by the browser);
  Noto Sans Math, which has one weight, is subset to the characters of WANT that one of the other faces lacks,
  since that is all a browser will draw from it. Hinting is dropped (the posters are read zoomed in); the name
  table is kept whole, so each file carries its copyright and licence.
- diagrams/src/metrics.py: the advance width, in em, of every character of WANT in every style the generator
  sets (r, b, i, m, mb), taken from the face the browser will draw it with: the style's own face where it
  has the glyph, Noto Sans Math where it does not (and for the arrows in code; see MONO_FROM_MATH). Kerning and ligatures are left out of the subsets, so these
  advances are exactly what the browser lays out. A character a poster uses that is in no table is reported by
  the generator as a WARNING, so a new symbol fails CI here instead of falling back to a system font.

Run it only to change the fonts or WANT; the generator itself reads the committed files and needs nothing outside
the standard library. The committed WOFF2 files, not this script, are what the posters' bytes depend on: a
different fontTools or Brotli may write different bytes from the same sources.
"""
import hashlib
import io
import pathlib
import sys

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "diagrams" / "src" / "fonts"
METRICS = ROOT / "diagrams" / "src" / "metrics.py"

GOOGLE_FONTS = "06bfe0d62a98375cb09c942fa18e68bd32cff057"   # google/fonts main, 2026.11.22
SOURCES = {
    "sans": ("ofl/notosans/NotoSans[wdth,wght].ttf",
             "bfb7bb691513f12e734dc346c03a03f784912432d7e3fa8e56efcf906fe86b3d"),
    "italic": ("ofl/notosans/NotoSans-Italic[wdth,wght].ttf",
               "58e6e0ebd1931b29a365aa2d3e2ee9a9e831a3af7cf3ad1462d4e72154f0b291"),
    "mono": ("ofl/notosansmono/NotoSansMono[wdth,wght].ttf",
             "2cb2adb378a8f574213e23df697050b83c54c27df465a2015552740b2769a081"),
    "math": ("ofl/notosansmath/NotoSansMath-Regular.ttf",
             "3f495fe933c06786e4d5f6d86b8ee70b6753a68ee3b9d87528726de0f6e2c47d"),
}

# (file stem, source, wght, style key of metrics.py); math has no style of its own
FACES = [
    ("sans-regular", "sans", 400, "r"),
    ("sans-bold", "sans", 700, "b"),
    ("sans-italic", "italic", 400, "i"),
    ("mono-regular", "mono", 400, "m"),
    ("mono-bold", "mono", 700, "mb"),
]


def _ranges(*pairs):
    return {chr(c) for a, b in pairs for c in range(a, b + 1)}


# What the posters may set: Latin with its accents, Greek, the punctuation, and the symbols of mathematics and
# Lean that the posters use or plausibly will, about 600 characters. The posters used 187 at 2026.11.22, all of
# them here. Kept this small because every poster carries every face: wider ranges (all of the arrows and
# operators blocks, Cyrillic, the script and fraktur alphabets) came to 506 KB of WOFF2, more than most posters.
# Anything outside it is a WARNING from the generator; add it here and rebuild.
WANT = _ranges(
    (0x0020, 0x007E),   # ASCII
    (0x00A0, 0x017F),   # Latin-1 and Latin Extended-A
    (0x0391, 0x03A9),   # Greek capitals
    (0x03B1, 0x03C9),   # Greek small letters
    (0x2010, 0x2027),   # dashes, quotes, bullets, ellipsis
    (0x2030, 0x203A),   # per mille, primes, angle quotes
    (0x2070, 0x209C),   # super- and subscripts
    (0x2190, 0x2199),   # the plain arrows
    (0x21D0, 0x21D5),   # the double arrows
    (0x2200, 0x2233),   # the first operators: quantifiers, sets, sums, roots, integrals
    (0x2260, 0x228B),   # relations: ≠ ≡ ≤ ≥ ≪ ≫ ⊂ ⊃ ⊆ ⊇
    (0x2295, 0x22A5),   # ⊕ ⊗ ⊙ ⊢ ⊣ ⊤ ⊥
    (0x2308, 0x230B),   # ceiling and floor
    (0x27E6, 0x27EB),   # ⟦ ⟧ ⟨ ⟩ ⟪ ⟫
    (0x27F5, 0x27FA),   # long arrows
) | set(
    "ϕϵϑϖϱ"                                  # Greek letter variants
    "ˣ\u0304\u0302\u0303\u0307"             # modifier x, combining macron, hat, tilde, dot
    "ШЖДЛПФ"                                 # Cyrillic letters used as names (Ш)
    "ℂℍℕℙℚℝℤℓℵ℘ℜℑ"                          # letterlike
    "↦↤↪↠⇢⇝↺↻"                              # maps-to, hooks, dashed
    "≃≅≈≍≺≻⋆⋅⋯⋮⋱⋂⋃⋀⋁⨁⨂⧸∣∤∥∦"                 # relations and big operators
    "⟶⟹⟼■□▶▸◀○●★⚠✓✗"                       # long arrows; the legend marks
    "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"        # script capitals
    "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"        # bold script capitals
    "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"        # fraktur capitals
    "𝔸𝔹𝔻𝔼𝔽𝔾𝕀𝕁𝕂𝕃𝕄𝕆𝕊𝕋𝕌𝕍𝕎𝕏𝕐𝟙"               # double-struck capitals not in letterlike, and 𝟙
)


# Characters the code face draws from Noto Sans Math instead of its own glyph: Noto Sans Mono's arrows are a
# third of an em tall and hard to see at panel size, and Lean signatures are made of them. Math's are full size,
# and about 1.7 cells wide, which the Lean panels' line breaking measures (bp.cells).
MONO_FROM_MATH = {c for c in WANT if 0x2190 <= ord(c) <= 0x21FF or 0x27F0 <= ord(c) <= 0x27FF}


def load(src_dir, key):
    rel, digest = SOURCES[key]
    path = src_dir / pathlib.PurePosixPath(rel).name
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        sys.exit(f"build-fonts: {path} is not google/fonts@{GOOGLE_FONTS[:10]}:{rel}")
    return TTFont(io.BytesIO(data))


def instance(font, wght):
    if "fvar" not in font:
        return font
    return instancer.instantiateVariableFont(font, {"wght": wght, "wdth": 100}, updateFontNames=True)


def write_subset(font, chars, stem):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.hinting = False
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    # no kerning and no ligatures: the posters are drawn with exactly the advances in metrics.py, and the kern
    # tables of Latin-1 and Extended-A were a third of each sans face. Marks stay, for the combining accents.
    opts.layout_features = ["ccmp", "locl", "mark", "mkmk"]
    opts.drop_tables += ["MATH", "STAT", "DSIG"]   # MATH serves MathML layout only, which an SVG never does
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=sorted(ord(c) for c in chars))
    sub.subset(font)
    font.recalcTimestamp = False      # keep the source's head.modified, so a rebuild writes the same bytes
    path = OUT / f"{stem}.woff2"
    subset.save_font(font, str(path), opts)
    return path


def advances(font):
    upem = font["head"].unitsPerEm
    hmtx = font["hmtx"]
    return {chr(cp): hmtx[g][0] / upem for cp, g in font.getBestCmap().items()}


def main(src_dir):
    src_dir = pathlib.Path(src_dir)
    OUT.mkdir(parents=True, exist_ok=True)
    built = {}
    for stem, key, wght, style in FACES:
        font = instance(load(src_dir, key), wght)
        adv = {c: w for c, w in advances(font).items()
               if c in WANT and not (key == "mono" and c in MONO_FROM_MATH)}
        built[style] = adv
        print(write_subset(font, adv, stem).relative_to(ROOT), len(adv), "characters")
    lacking = {c for c in WANT if any(c not in adv for adv in built.values())}
    math = load(src_dir, "math")
    madv = {c: w for c, w in advances(math).items() if c in lacking}
    print(write_subset(math, madv, "math-regular").relative_to(ROOT), len(madv), "characters")

    out = ['# Advance widths (fraction of 1 em) of the embedded Noto faces, for every character the posters may set.',
           '# Written by tools/build-fonts.py from the fonts in diagrams/src/fonts/; do not edit. A character missing',
           "# from a style's own face has the width of its Noto Sans Math glyph, which is what the browser draws.",
           "W = {"]
    for _, _, _, style in FACES:
        table = dict(madv)
        table.update(built[style])
        items = [f"{c!r}: {round(w, 4)}" for c, w in sorted(table.items())]
        out.append(f"    {style!r}: {{")
        line = "       "
        for it in items:
            if len(line) + len(it) + 2 > 118:
                out.append(line.rstrip())
                line = "       "
            line += " " + it + ","
        out.append(line.rstrip())
        out.append("    },")
    out.append("}")
    METRICS.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(METRICS.relative_to(ROOT), {s: len(t) for s, t in built.items()}, "math", len(madv))
    missing = sorted(c for c in WANT if c not in madv and any(c not in adv for adv in built.values()))
    if missing:
        print(f"build-fonts: {len(missing)} characters of WANT are in no face of some style:",
              "".join(missing[:80]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
