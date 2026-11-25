"""Shared drawing library for the riemann diagrams.

Taken from the TOPAK diagram family (Apache-2.0, same author) by way of riemann-diagrams, whose copy this is, at
riemann-diagrams f87256e (NOTICE). There, the brand, date, generator and state line differ from TOPAK's, the fonts
are embedded Noto where TOPAK names system fonts, and the light theme's page is a grey matched to the content.
Here, only BRAND, DATE, HOME_ORDER, the light page (`page`, measured again here: diagrams/PAGE.md) the style
that shows a link's target (`.rd-target`, `.rd-row`), and `table`'s optional row anchors differ from that copy. A fix in riemann-diagrams reaches this copy only when
it is copied again, on purpose.

Dependency-free. Every diagram is a Canvas; primitives measure their own text with the advance
widths in metrics.py, wrap it, and return the height they used, so layouts are computed rather
than hand-tuned. The widths are those of the Noto faces in fonts/, which every poster embeds
(tools/build-fonts.py writes both), so the text is drawn in the font it was measured in.

Theming: every colour is written twice, once as a presentation attribute (the light theme, for
renderers without CSS) and once as a class whose CSS custom property switches under
`prefers-color-scheme: dark`. CSS beats presentation attributes, so browsers adapt and
everything else falls back to light.

Inline markup in any text: **bold**, `code`, and [[accent|text]] for an accent-coloured run.
"""
import base64
import collections
import pathlib
import re
from xml.sax.saxutils import escape, unescape

from metrics import W as _W

# The embedded faces, as tools/build-fonts.py subset them: (file, family, weight, style). Noto Sans Math is second
# in both stacks, so a symbol the text face lacks is drawn from it, as metrics.py assumes. The system names after
# the embedded ones serve renderers that do not read @font-face.
FONTS = pathlib.Path(__file__).resolve().parent / "fonts"
FACES = [
    ("sans-regular", "RD Noto Sans", 400, "normal"),
    ("sans-bold", "RD Noto Sans", 700, "normal"),
    ("sans-italic", "RD Noto Sans", 400, "italic"),
    ("mono-regular", "RD Noto Sans Mono", 400, "normal"),
    ("mono-bold", "RD Noto Sans Mono", 700, "normal"),
    ("math-regular", "RD Noto Sans Math", 400, "normal"),
]
SANS = "'RD Noto Sans', 'RD Noto Sans Math', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "'RD Noto Sans Mono', 'RD Noto Sans Math', 'Noto Sans Mono', Menlo, Consolas, monospace"
MONO_EM = _W["m"]["0"]   # Noto Sans Mono's cell, 0.6 em; symbols it lacks come from Math at their own width
MONO_SCALE = 0.92        # code runs are set slightly smaller than the surrounding text
# style of a run -> its table in metrics.py. A bold run in an italic line is the italic face emboldened by the
# browser, which keeps the italic advances.
_TABLE = {"r": "r", "b": "b", "i": "i", "bi": "i", "m": "m", "mb": "mb"}
# what every style can draw from the embedded faces, its own or Math; anything else is a WARNING (Canvas.check)
COVERED = set.intersection(*(set(t) for t in _W.values()))
_FALLBACK_EM = 0.62      # the width of a character in no table; the generator warns about every such character

BRAND = "RIEMANN-MASULLO-DIAGRAMS"
DATE = "2026.11.25"
GENERATOR = "diagrams/gen-diagrams.py"
STATE = "State drawn: see each diagram's state line"

# ---------------------------------------------------------------------------------------------
# Theme tokens: name -> (light, dark)
BASE = {
    "bg":    ("#ffffff", "#12151b"),
    "page":  ("#e8e8e8", "#12151b"),   # the page behind the cards: in light, the mean luminance of M1's content (PAGE.md)
    "ink":   ("#1e2430", "#e6e9ef"),
    "muted": ("#4a5262", "#b0b8c6"),
    "faint": ("#7d8596", "#7f8898"),
    "panel": ("#f5f6f8", "#1a1e26"),
    "line":  ("#d4d8e0", "#363d4a"),
    "zebra": ("#fafbfc", "#161a21"),
}
# accent -> (stroke light, tint light, stroke dark, tint dark)
ACCENTS = {
    "blue":   ("#2f5aa8", "#edf2fb", "#8fb0ec", "#1a2540"),   # authority, ratified
    "teal":   ("#166b5b", "#e8f5f1", "#6cc7b0", "#12302a"),   # mechanism, verified object
    "amber":  ("#a35a00", "#fdf3e4", "#f0b15c", "#33260f"),   # Proposed
    "violet": ("#6b46a8", "#f3eefb", "#b9a0e8", "#261d38"),   # draft
    "red":    ("#a4262c", "#fcefef", "#f08a8f", "#3a1a1d"),   # gap, deny, refused
    "grey":   ("#5f6878", "#f1f2f4", "#a3abb9", "#22262e"),   # neutral, external, withdrawn
    "brown":  ("#8a4b14", "#f9f0e6", "#e0a56b", "#2f2215"),   # humans, custody
    "pink":   ("#9d2f6e", "#fbeef5", "#ec8cc2", "#351a2a"),   # detection, Observer
    "green":  ("#2e7d32", "#edf6ee", "#85c98a", "#17291a"),   # subtraction, safe direction
}

STATUS = {
    # key: (label, accent, dash)
    "accepted":   ("Accepted", "blue", None),
    "proposed":   ("Proposed", "amber", "6 4"),
    "draft":      ("Draft, not ratified", "violet", "6 4"),
    "notbuilt":   ("Not built", "red", "2 3"),
    "built":      ("Built at reference", "teal", None),
    "superseded": ("Superseded", "grey", "2 3"),
    "withdrawn":  ("Withdrawn", "grey", "2 3"),
    "open":       ("Open", "red", "6 4"),
    # ratified and in force, subject to redesign (ADR-0029 A4); dashed so it never reads as settled
    "provisional": ("Accepted · provisional", "blue", "4 3"),
    # gated, pinned and enforced, ratified only when the bootstrap reviewer finds it fit (ADR-0030 A3)
    "genprov":    ("Genesis-provisional", "violet", "4 3"),
}


def _font_faces():
    out = []
    for stem, family, weight, style in FACES:
        data = base64.b64encode((FONTS / f"{stem}.woff2").read_bytes()).decode("ascii")
        out.append(f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};"
                   f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return out


_FONT_FACES = _font_faces()


def _css():
    lines = list(_FONT_FACES)
    def block(idx_base, idx_s, idx_t):
        out = []
        for k, v in BASE.items():
            out.append(f"--{k}:{v[idx_base]};")
        for k, v in ACCENTS.items():
            out.append(f"--{k}:{v[idx_s]};--{k}-t:{v[idx_t]};")
        return "".join(out)
    lines.append("svg{" + block(0, 0, 1) + "}")
    lines.append("@media (prefers-color-scheme: dark){svg:not([data-theme=light]){" + block(1, 2, 3) + "}}")
    lines.append("svg[data-theme=dark]{" + block(1, 2, 3) + "}")
    lines.append("a:hover tspan,a:focus tspan,a:hover>text{text-decoration:underline} a:hover>rect{stroke-width:3.4}")
    # The card or block a link opened: its halo (drawn hidden, behind it) shows while it is the address's #fragment,
    # and pulses three times. A renderer without CSS keeps it hidden.
    lines.append(".rd-target{opacity:0} g:target>.rd-target{opacity:1;animation:rd-pulse 0.9s ease-in-out 3}"
                 " @keyframes rd-pulse{50%{stroke-width:9}} g[id]{scroll-margin-top:90px}"
                 " g.rd-row:target>rect:first-child{fill:var(--amber-t);stroke:var(--amber);stroke-width:3;"
                 "animation:rd-pulse 0.9s ease-in-out 3}")
    for k in BASE:
        lines.append(f".f-{k}{{fill:var(--{k})}} .s-{k}{{stroke:var(--{k})}}")
    for k in ACCENTS:
        lines.append(f".f-{k}{{fill:var(--{k})}} .ft-{k}{{fill:var(--{k}-t)}} .s-{k}{{stroke:var(--{k})}}")
    return "\n".join(lines)


def light(name):
    if name in BASE:
        return BASE[name][0]
    if name.endswith("-t"):
        return ACCENTS[name[:-2]][1]
    return ACCENTS[name][0]


def fill(name):
    """fill attribute + class for a token ('ink', 'blue', 'blue-t')."""
    cls = f"ft-{name[:-2]}" if name.endswith("-t") else f"f-{name}"
    return f'fill="{light(name)}" class="{cls}"'


def stroke(name):
    return f'stroke="{light(name)}"'


def fs(fill_name, stroke_name):
    """fill + stroke on one element (classes combined)."""
    fcls = f"ft-{fill_name[:-2]}" if fill_name.endswith("-t") else f"f-{fill_name}"
    return (f'fill="{light(fill_name)}" stroke="{light(stroke_name)}" '
            f'class="{fcls} s-{stroke_name}"')


def sonly(stroke_name):
    return f'fill="none" stroke="{light(stroke_name)}" class="s-{stroke_name}"'


# ---------------------------------------------------------------------------------------------
# Text measurement and rich-text wrapping

_RUN = re.compile(r"(\*\*.+?\*\*|`.+?`|\[\[[a-z]+\|.+?\]\]|\[\[@[^|\]]+\|.+?\]\])")


def parse(s):
    """-> list of (text, style, accent) runs. style in r/b/m (regular, bold, mono). The accent of a run inside
    [[@url|text]] is the url with its @, and render_line makes the run a link; text may hold code runs."""
    runs = []
    for part in _RUN.split(s):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            # code inside bold: the code run is set in mono (which has no bold), the rest stays bold
            for sub in re.split(r"(`[^`]+`)", part[2:-2]):
                if sub.startswith("`") and sub.endswith("`") and len(sub) > 2:
                    runs.append((sub[1:-1], "m", None))
                elif sub:
                    runs.append((sub, "b", None))
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            runs.append((part[1:-1], "m", None))
        elif part.startswith("[[@") and part.endswith("]]"):
            url, txt = part[2:-2].split("|", 1)
            runs.extend((t, st, url) for t, st, _ in parse(txt))
        elif part.startswith("[[") and part.endswith("]]"):
            acc, txt = part[2:-2].split("|", 1)
            runs.append((txt, "b", acc))
        else:
            runs.append((part, "r", None))
    return runs


def em(s, style="r"):
    """The advance of s in em, in one of the styles r, b, i, bi, m, mb."""
    tbl = _W[_TABLE[style]]
    return sum(tbl.get(c, _FALLBACK_EM) for c in s)


def mono_width(s, size, bold=False):
    """A run of code at its own size (no MONO_SCALE), as the Lean panels set it."""
    return em(s, "mb" if bold else "m") * size


def width(s, size, style="r"):
    if style in ("m", "mb"):
        return em(s, style) * size * MONO_SCALE
    return em(s, style) * size


def restyle(st, bold=False, italic=False):
    """The style of a run of style st set in a bold or an italic line."""
    if bold:
        st = {"r": "b", "m": "mb", "i": "bi"}.get(st, st)
    if italic:
        st = {"r": "i", "b": "bi"}.get(st, st)
    return st


def text_width(s, size, bold=False, italic=False):
    return sum(width(t, size, restyle(st, bold, italic)) for t, st, _ in parse(s))


def wrap(s, maxw, size, bold=False, italic=False):
    """Greedy wrap of rich text. Returns list of lines, each a list of runs. '\n' forces a break."""
    lines_out = []
    for para in s.split("\n"):
        words = []  # (text, style, accent) with trailing space info
        for txt, st, acc in parse(para):
            st = restyle(st, bold, italic)
            parts = re.split(r"( )", txt)
            for p in parts:
                if p == "":
                    continue
                words.append((p, st, acc))
        line, lw = [], 0.0
        for w in words:
            ww = width(w[0], size, w[1])
            if w[0] == " ":
                if line:
                    line.append(w)
                    lw += ww
                continue
            if line and lw + ww > maxw:
                while line and line[-1][0] == " ":
                    lw -= width(" ", size, line[-1][1]); line.pop()
                lines_out.append(line)
                line, lw = [], 0.0
            line.append(w)
            lw += ww
        while line and line[-1][0] == " ":
            line.pop()
        lines_out.append(line)
    return lines_out


def _merge(line):
    out = []
    for t, st, acc in line:
        if out and out[-1][1] == st and out[-1][2] == acc:
            out[-1] = (out[-1][0] + t, st, acc)
        else:
            out.append((t, st, acc))
    return out


def line_width(line, size):
    return sum(width(t, size, st) for t, st, _ in line)


TEXT_BOXES = []   # (x0, y0, x1, y1, text) of every line drawn, for the overlap check

# The registry of the links between posters: the set's manifest.json, loaded by the generator before any poster is
# built. POSTERS: id -> file; ANCHORS_OF: file -> the blueprint ids it anchors; REGISTRY: blueprint id -> the file
# of the poster that draws it in full, the first in HOME_ORDER that anchors it. A map poster's manifest names map
# posters, so each set links only within itself.
HOME_ORDER = []
POSTERS, ANCHORS_OF, REGISTRY = {}, {}, {}
# The links out, set by bp.load: EXTERNAL, every blueprint id to its file in the blueprint repository at BP_COMMIT;
# PINNED, the prefixes an absolute href may have, the blueprint and the mirror at their pinned commits.
EXTERNAL, PINNED = {}, []
# PAPERS, set by bp.load from src/papers.toml: a reference id to the paper itself, the diagram's own data; F4 links
# each reference's title to it. SOURCES, set by bp.read_checks from src/checks.toml: the pages R1's band 5 rests on.
# An absolute href must be under a PINNED prefix or be one of these.
PAPERS, SOURCES = {}, {}


def load_registry(manifest):
    POSTERS.clear(); ANCHORS_OF.clear(); REGISTRY.clear()
    for pid, m in manifest.items():
        POSTERS[pid] = m["file"]
        ANCHORS_OF[m["file"]] = set(m.get("anchors", ()))
    order = [p for p in HOME_ORDER if p in POSTERS] + sorted(p for p in POSTERS if p not in HOME_ORDER)
    for pid in reversed(order):
        for a in ANCHORS_OF[POSTERS[pid]]:
            REGISTRY[a] = POSTERS[pid]


def chapter_poster(stmts):
    """The file of the chapter poster (R3 to R8) that anchors every one of `stmts`, else None."""
    for pid in HOME_ORDER[:6]:
        f = POSTERS.get(pid)
        if f and all(k in ANCHORS_OF[f] for k in stmts):
            return f
    return None


def render_line(x, y, line, size, color="ink", anchor="start", bold=False, italic=False):
    """One line of wrap() output. bold and italic must be what the line was wrapped with."""
    line = [(t, restyle(st, bold, italic), acc) for t, st, acc in line]
    lw = line_width(line, size)
    bx = x if anchor == "start" else (x - lw / 2 if anchor == "middle" else x - lw)
    TEXT_BOXES.append((bx, y - size * 0.75, bx + lw, y + size * 0.2, "".join(t for t, _, _ in line)))
    spans, link, linked = [], None, []
    def flush():
        if linked:
            spans.append(f'<a href="{escape(link[1:])}">{"".join(linked)}</a>')
            linked.clear()
    for t, st, acc in _merge(line):
        attrs = []
        if st in ("b", "bi", "mb"):
            attrs.append('font-weight="bold"')
        if st in ("m", "mb"):
            attrs.append(f'font-family="{MONO}" font-size="{size * MONO_SCALE:.1f}"')
        url = acc if acc and acc.startswith("@") else None
        if acc and not url:
            attrs.append(fill(acc))
        span = f'<tspan {" ".join(attrs)}>{escape(t)}</tspan>' if attrs else escape(t)
        if url != link:
            flush()
            link = url
        (linked if url else spans).append(span)
    flush()
    it = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SANS}" font-size="{size}"{it} '
            f'{fill(color)} text-anchor="{anchor}">{"".join(spans)}</text>')


# ---------------------------------------------------------------------------------------------

class Canvas:
    """One diagram. Primitives append SVG and track the lowest y used so height is computed."""

    def __init__(self, ident, title, subtitle, width, sources, pad=56, note=None, state=None):
        self.ident, self.title, self.subtitle, self.W = ident, title, subtitle, width
        self.sources = sources
        self.note, self.state = note, state
        self.pad = pad
        self.out = []
        self.ymax = 0
        self.x0, self.x1 = pad, width - pad
        self.blocks = []   # (x0, y0, x1, y1, name) of cards and tables, for the overlap check
        self.n_arrows = 0  # for the manifest
        self.anchors = []  # blueprint ids set as the id of a card's group, for the manifest and the link check
        self.links = 0     # code runs that name a card on this poster, made links to it by link()
        self.links_out = 0 # and those that name a card on another poster of the set, linked there
        self.links_ext = 0 # and those that name a blueprint id no poster draws, linked to its file at the pin
        self.overflow = [] # table cells whose text is wider than the cell, which Canvas.check warns about
        self.y = self._header()

    def stats(self):
        """What the release notes report: the cards that are statements, and the arrows."""
        return {"cards": sum(1 for b in self.blocks if b[4].startswith("node ")), "arrows": self.n_arrows}

    # -- bookkeeping
    def add(self, s, bottom=None):
        self.out.append(s)
        if bottom is not None:
            self.ymax = max(self.ymax, bottom)

    def _header(self):
        p = self.pad
        self.add(f'<text x="{p}" y="{p + 8}" font-family="{SANS}" font-size="13" letter-spacing="1.5" '
                 f'font-weight="bold" {fill("faint")}>{BRAND} · {escape(self.ident)}</text>')
        y = p + 44
        for ln in wrap(self.title, self.W - 2 * p, 30, bold=True):
            self.add(render_line(p, y, ln, 30, "ink", bold=True))
            y += 38
        y += 2
        for ln in wrap(self.subtitle, self.W - 2 * p, 16):
            self.add(render_line(p, y, ln, 16, "muted"))
            y += 23
        y += 10
        self.add(f'<line x1="{p}" y1="{y}" x2="{self.W - p}" y2="{y}" {sonly("line")} stroke-width="1.5"/>', y)
        return y + 34

    # -- primitives
    def text(self, x, y, s, size=14, color="ink", anchor="start", bold=False):
        self.add(render_line(x, y, _merge([(t, "b" if bold and st == "r" else st, a) for t, st, a in parse(s)]),
                             size, color, anchor), y + size * 0.3)

    def para(self, x, y, w, s, size=14, color="ink", lead=None, bold=False, anchor="start", draw=True):
        lead = lead or round(size * 1.42, 1)
        lines = wrap(s, w, size, bold)
        if draw:
            for i, ln in enumerate(lines):
                ax = x if anchor == "start" else (x + w / 2 if anchor == "middle" else x + w)
                self.add(render_line(ax, y + size + i * lead, ln, size, color, anchor, bold))
            self.ymax = max(self.ymax, y + size * 0.35 + (len(lines) - 1) * lead + size)
        return (len(lines) - 1) * lead + size * 1.35

    def rect(self, x, y, w, h, accent="grey", tint=True, dash=None, rx=8, sw=1.6, fill_token=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        f = fill_token or (f"{accent}-t" if tint else "bg")
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                 f'{fs(f, accent)} stroke-width="{sw}"{d}/>', y + h)

    def pill(self, x, y, label, accent="grey", size=12, dash=None, solid=False, anchor="start"):
        w = text_width(label, size, bold=True) + 18
        h = size + 10
        if anchor == "end":
            x -= w
        elif anchor == "middle":
            x -= w / 2
        d = f' stroke-dasharray="{dash}"' if dash else ""
        if solid:
            self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
                     f'{fs(accent, accent)} stroke-width="1.2"/>')
            self.add(render_line(x + 9, y + size + 2.5, [(label, "b", None)], size, "bg"), y + h)
        else:
            self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
                     f'{fs(accent + "-t", accent)} stroke-width="1.2"{d}/>')
            self.add(render_line(x + 9, y + size + 2.5, [(label, "b", None)], size, accent), y + h)
        return w

    def status(self, x, y, key, extra="", size=11.5, anchor="start"):
        label, acc, dash = STATUS[key]
        return self.pill(x, y, label + (f" · {extra}" if extra else ""), acc, size, dash, anchor=anchor)

    def card(self, x, y, w, title, body=(), accent="grey", status=None, status_extra="", dash=None,
             h=None, size=14, tsize=16, tint=True, draw=True, sub=None, pad=16, bullets=True, lead=None):
        """A titled box. body: list of rich strings (bulleted when bullets=True). Returns height."""
        inner = w - 2 * pad
        lead = lead or round(size * 1.42, 1)
        tlines = wrap(title, inner - (0 if not status else 0), tsize, bold=True) if title else []
        hh = pad
        hh += len(tlines) * (tsize + 6)
        if sub:
            sublines = wrap(sub, inner, size - 1)
            hh += len(sublines) * round((size - 1) * 1.4, 1) + 2
        else:
            sublines = []
        status_h = 0
        if status:
            status_h = 11.5 + 10 + 8
            hh += status_h
        if tlines and body:
            hh += 6
        blines = []
        bul = "•  " if bullets else ""
        indent = width(bul, size) if bullets else 0
        for item in body:
            ls = wrap(item, inner - indent, size)
            blines.append(ls)
            hh += len(ls) * lead + 3
        hh += pad - 4
        if h is not None:
            hh = max(h, hh)
        if not draw:
            return hh
        if dash is None and status:
            dash = STATUS[status][2]
        self.blocks.append((x, y, x + w, y + hh, "card " + (title or "")[:40]))
        self.rect(x, y, w, hh, accent, tint=tint, dash=dash)
        cy = y + pad
        for ln in tlines:
            self.add(render_line(x + pad, cy + tsize - 2, ln, tsize, accent, bold=True))
            cy += tsize + 6
        for ln in sublines:
            self.add(render_line(x + pad, cy + size - 3, ln, size - 1, "muted"))
            cy += round((size - 1) * 1.4, 1)
        if sublines:
            cy += 2
        if status:
            cy += 2
            self.status(x + pad, cy, status, status_extra)
            cy += status_h - 2
        if tlines and body:
            cy += 6
        for ls in blines:
            for i, ln in enumerate(ls):
                if i == 0 and bullets:
                    self.add(render_line(x + pad, cy + size, [("•", "b", None)], size, accent))
                self.add(render_line(x + pad + indent, cy + size, ln, size, "ink"))
                cy += lead
            cy += 3
        return hh

    def region(self, x, y, w, h, label, accent="grey", dash="10 6", sw=2.2, tint=False, size=14, rx=14):
        """A boundary container with a label tab on its top edge."""
        self.rect(x, y, w, h, accent, tint=tint, dash=dash, sw=sw, rx=rx, fill_token=None if tint else "bg")
        if tint is False:
            # transparent fill: overwrite the bg fill with none so nested content shows the canvas
            self.out[-1] = self.out[-1].replace(f'fill="{light("bg")}" ', 'fill="none" ').replace("f-bg ", "")
        if label:
            tw = text_width(label, size, bold=True) + 20
            self.add(f'<rect x="{x + 18:.1f}" y="{y - size / 2 - 6:.1f}" width="{tw:.1f}" height="{size + 12}" rx="6" '
                     f'{fs("bg", accent)} stroke-width="1.4"/>')
            self.add(render_line(x + 28, y + size / 2 - 1.5, parse(label), size, accent, bold=True))

    def arrow(self, pts, accent="grey", dash=None, sw=2, label=None, lsize=12.5, lpos=0.5, head=True,
              both=False, loff=(0, 0), lw=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        if head:
            self.n_arrows += 1
        me = f' marker-end="url(#arw-{accent})"' if head else ""
        ms = f' marker-start="url(#arw-{accent})"' if both else ""
        self.add(f'<path d="{path}" {sonly(accent)} stroke-width="{sw}"{d}{me}{ms} '
                 f'stroke-linejoin="round"/>', max(p[1] for p in pts))
        if label:
            # label at fraction lpos along the polyline length
            segs = list(zip(pts, pts[1:]))
            lens = [abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in segs]
            tgt = sum(lens) * lpos
            for (a, b), L in zip(segs, lens):
                if tgt <= L or (a, b) == segs[-1]:
                    f = 0 if L == 0 else min(1, tgt / L)
                    mx, my = a[0] + (b[0] - a[0]) * f + loff[0], a[1] + (b[1] - a[1]) * f + loff[1]
                    break
                tgt -= L
            self.label(mx, my, label, accent, lsize, lw)

    def label(self, cx, cy, s, accent="grey", size=12.5, maxw=None):
        maxw = maxw or 10_000
        lines = wrap(s, maxw, size)
        lw = max(line_width(ln, size) for ln in lines)
        lead = size * 1.35
        h = len(lines) * lead + 6
        self.add(f'<rect x="{cx - lw / 2 - 7:.1f}" y="{cy - h / 2:.1f}" width="{lw + 14:.1f}" height="{h:.1f}" '
                 f'rx="5" {fs("bg", accent)} stroke-width="1"/>')
        for i, ln in enumerate(lines):
            self.add(render_line(cx, cy - h / 2 + 3 + size + i * lead - 2, ln, size, accent, "middle"))

    def line(self, x1, y1, x2, y2, accent="line", sw=1.4, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {sonly(accent)} '
                 f'stroke-width="{sw}"{d}/>', max(y1, y2))

    def heading(self, x, y, s, accent="ink", size=19, w=None):
        """A section heading with a short rule under it. Returns height used."""
        self.text(x, y + size, s, size, accent, bold=True)
        return size + 16

    def table(self, x, y, cols, rows, size=13.5, header=True, hsize=13.5, pad=9, zebra=True, draw=True,
              accent="grey"):
        """cols: list of (title, width[, opts]) where opts may hold mono/bold/accent/align.
        rows: list of lists of rich strings; or {'group': label, 'accent': a}; or
        {'cells': [...], 'accent': a, 'dash': bool} to tint a row. Returns height."""
        lead = round(size * 1.38, 1)
        tw = sum(c[1] for c in cols)
        cy = y
        parts = []

        def cell_lines(s, cw, opt):
            s = s if s is not None else ""
            if opt.get("mono") and s:
                s = f"`{s}`"
            out = wrap(s, cw - 2 * pad, size, bold=opt.get("bold", False))
            if draw:     # a word wider than its cell is not broken: it runs into the next cell, so Canvas.check warns
                self.overflow += [ln for ln in out if line_width(ln, size) > cw - 2 * pad + 0.5]
            return out

        if header:
            hl = [wrap(c[0], c[1] - 2 * pad, hsize, bold=True) for c in cols]
            hh = max(len(l) for l in hl) * round(hsize * 1.35, 1) + 2 * pad - 2
            if draw:
                parts.append(f'<rect x="{x}" y="{cy:.1f}" width="{tw}" height="{hh:.1f}" {fs(accent, accent)} '
                             f'stroke-width="1"/>')
                cx = x
                for (c, ls) in zip(cols, hl):
                    for i, ln in enumerate(ls):
                        parts.append(render_line(cx + pad, cy + pad + hsize - 1 + i * round(hsize * 1.35, 1),
                                                 ln, hsize, "bg", bold=True))
                    cx += c[1]
            cy += hh
        for ri, r in enumerate(rows):
            if isinstance(r, dict) and "group" in r:
                gacc = r.get("accent", accent)
                gl = wrap(r["group"], tw - 2 * pad, size, bold=True)
                gh = len(gl) * lead + 2 * pad - 4
                if draw:
                    parts.append(f'<rect x="{x}" y="{cy:.1f}" width="{tw}" height="{gh:.1f}" '
                                 f'{fs(gacc + "-t", "line")} stroke-width="1"/>')
                    for i, ln in enumerate(gl):
                        parts.append(render_line(x + pad, cy + pad + size - 2 + i * lead, ln, size, gacc, bold=True))
                cy += gh
                continue
            racc, rdash, ranchor = None, False, None
            if isinstance(r, dict):
                racc, rdash, ranchor, r = r.get("accent"), r.get("dash", False), r.get("anchor"), r["cells"]
            ls = [cell_lines(s, c[1], c[2] if len(c) > 2 else {}) for s, c in zip(r, cols)]
            rh = max(max(len(l), 1) for l in ls) * lead + 2 * pad - 4
            if draw:
                if ranchor:                 # a row a link can open: lib's CSS frames it while it is the target
                    parts.append(f'<g id="{ranchor}" class="rd-row">')
                    self.anchors.append(ranchor)
                bgtok = f"{racc}-t" if racc else ("zebra" if zebra and ri % 2 else "bg")
                parts.append(f'<rect x="{x}" y="{cy:.1f}" width="{tw}" height="{rh:.1f}" {fs(bgtok, "line")} '
                             f'stroke-width="1"/>')
                if racc:
                    parts.append(f'<rect x="{x}" y="{cy:.1f}" width="5" height="{rh:.1f}" {fill(racc)}/>')
                cx = x
                for c, cl in zip(cols, ls):
                    opt = c[2] if len(c) > 2 else {}
                    col = opt.get("accent", "ink")
                    for i, ln in enumerate(cl):
                        parts.append(render_line(cx + pad, cy + pad + size - 2 + i * lead, ln, size, col,
                                                 bold=opt.get("bold", False)))
                    cx += c[1]
                if ranchor:
                    parts.append("</g>")
            cy += rh
        if draw:
            self.blocks.append((x, y, x + tw, cy, "table " + cols[0][0][:30]))
            # column rules
            cx = x
            for c in cols[:-1]:
                cx += c[1]
                parts.append(f'<line x1="{cx}" y1="{y}" x2="{cx}" y2="{cy:.1f}" {sonly("line")} stroke-width="1"/>')
            parts.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{cy - y:.1f}" {sonly(accent)} '
                         f'stroke-width="1.4"/>')
            self.add("\n".join(parts), cy)
        return cy - y

    def legend(self, x, y, items, title="Legend", size=13, maxw=None):
        """items: list of (kind, accent, label, dash[, stroke width]) where kind is 'box', 'line', 'arrow',
        'status'."""
        maxw = maxw or (self.x1 - x)
        cx, cy = x, y
        self.text(cx, cy + size, title, size, "faint", bold=True)
        cx += text_width(title, size, True) + 18
        for it in items:
            kind, acc, lab = it[0], it[1], it[2]
            dash = it[3] if len(it) > 3 else None
            sw = it[4] if len(it) > 4 else 2
            iw = 34 + text_width(lab, size) + 26
            if cx + iw > x + maxw:
                cx = x + text_width(title, size, True) + 18
                cy += size + 16
            d = f' stroke-dasharray="{dash}"' if dash else ""
            if kind == "box":
                self.add(f'<rect x="{cx}" y="{cy + 1}" width="26" height="{size + 3}" rx="4" {fs(acc + "-t", acc)} '
                         f'stroke-width="1.6"{d}/>')
            elif kind == "line":
                self.add(f'<line x1="{cx}" y1="{cy + size / 2 + 2}" x2="{cx + 26}" y2="{cy + size / 2 + 2}" '
                         f'{sonly(acc)} stroke-width="2.2"{d}/>')
            elif kind == "arrow":
                self.add(f'<path d="M {cx} {cy + size / 2 + 2} L {cx + 24} {cy + size / 2 + 2}" {sonly(acc)} '
                         f'stroke-width="{sw}"{d} marker-end="url(#arw-{acc})"/>')
            self.text(cx + 34, cy + size, lab, size, "muted")
            cx += iw
        self.ymax = max(self.ymax, cy + size + 6)
        return cy + size + 6 - y

    # -- output
    _MONO_TSPAN = re.compile(r'<tspan ((?:[^<>]*? )?font-family="' + re.escape(MONO) + r'"[^<>]*)>([^<>]+)</tspan>')

    def link(self):
        """A code run whose text is exactly one of the poster's anchors becomes a link to that card: in a Stated
        with, Proof uses or Used by footer, in a card's text, in a key. One that names a card on another poster of
        the set links there, by a relative href that resolves in the tree, on the Pages site and among a release's
        assets alike. Plain href, SVG's own <a> inside <text>; no glyph is added, so the measured widths and the
        overlap check are unchanged."""
        anchors = set(self.anchors)
        def repl(m):
            t = m.group(2)
            if t in anchors:
                self.links += 1
                return f'<a href="#{t}">{m.group(0)}</a>'
            if t in REGISTRY:
                self.links_out += 1
                return f'<a href="{REGISTRY[t]}#{t}">{m.group(0)}</a>'
            if t in EXTERNAL:
                self.links_ext += 1
                return f'<a href="{escape(EXTERNAL[t])}">{m.group(0)}</a>'
            return m.group(0)
        def line(s):   # the runs render_line has already made links are left alone: SVG does not nest <a>
            parts = re.split(r'(<a href="[^"]*">.*?</a>)', s)
            return "".join(p if i % 2 else self._MONO_TSPAN.sub(repl, p) for i, p in enumerate(parts))
        self.out = [line(s) if "<tspan" in s else s for s in self.out]

    def check(self):
        """Warn about text lines whose boxes intersect, or that leave the canvas, and about characters the
        embedded fonts do not have, which a browser would draw from a system font at an unmeasured width.
        Returns the warnings."""
        boxes = [b for b in TEXT_BOXES if b[4].strip()]
        warn = [f"wider than its table cell: {''.join(t for t, _, _ in ln)!r}" for ln in self.overflow]
        ids = re.findall(r' id="([^"]*)"', "\n".join(self.out))
        for i in sorted(i for i, n in collections.Counter(ids).items() if n > 1):
            warn.append(f"id drawn twice: {i!r}")
        files = set(POSTERS.values())
        for h in sorted(set(re.findall(r' href="([^"]*)"', "\n".join(self.out)))):
            f, _, frag = h.partition("#")
            if f.startswith("http"):
                if not any(f.startswith(p) for p in PINNED) and h not in PAPERS.values() and h not in SOURCES.values():
                    warn.append(f"link out neither at a pinned commit, a paper of src/papers.toml nor a source of "
                                f"src/checks.toml: {h}")
            elif not f and frag not in self.anchors:
                warn.append(f"link to no card on this poster: #{frag}")
            elif f and f not in files:
                warn.append(f"link to a poster the manifest does not list: {f}")
            elif f and frag and frag not in ANCHORS_OF[f]:
                warn.append(f"link to a card {f} does not draw: #{frag}")
        for a in self.anchors:
            if not re.fullmatch(r"[A-Za-z_][\w.-]*", a) or a in ("t", "d") or a.startswith("arw-"):
                warn.append(f"not usable as an anchor: {a!r}")
        drawn = set()
        for t in re.findall(r">([^<]+)<", "\n".join(self.out)):
            drawn |= set(unescape(t))
        for ch in sorted(drawn - COVERED - {"\n"}):
            warn.append(f"not in the embedded fonts: {ch!r} (U+{ord(ch):04X}); add it to WANT in "
                        f"tools/build-fonts.py and rebuild the fonts")
        for b in boxes:
            if b[0] < 0 or b[2] > self.W + 0.5:
                warn.append(f"off-canvas: {b[4][:60]!r} x={b[0]:.0f}..{b[2]:.0f}")
        bl = self.blocks
        for i, a in enumerate(bl):
            for b in bl[i + 1:]:
                inter = a[0] < b[2] - 1 and b[0] < a[2] - 1 and a[1] < b[3] - 1 and b[1] < a[3] - 1
                if not inter:
                    continue
                a_in_b = b[0] <= a[0] and a[2] <= b[2] and b[1] <= a[1] and a[3] <= b[3]
                b_in_a = a[0] <= b[0] and b[2] <= a[2] and a[1] <= b[1] and b[3] <= a[3]
                if not (a_in_b or b_in_a):
                    warn.append(f"block overlap: {a[4]!r} and {b[4]!r}")
        boxes.sort(key=lambda b: b[1])
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                if b[1] >= a[3] - 1:
                    break
                if a[0] < b[2] - 1 and b[0] < a[2] - 1 and a[1] < b[3] - 1 and b[1] < a[3] - 1:
                    warn.append(f"overlap: {a[4][:50]!r} @({a[0]:.0f},{a[1]:.0f}) with {b[4][:50]!r} "
                                f"@({b[0]:.0f},{b[1]:.0f})")
        return warn

    def svg(self):
        p = self.pad
        y = self.ymax + 44
        self.add(f'<line x1="{p}" y1="{y}" x2="{self.W - p}" y2="{y}" {sonly("line")} stroke-width="1.2"/>')
        y += 26
        src = "Sources: " + self.sources
        for ln in wrap(src, self.W - 2 * p, 13):
            self.add(render_line(p, y, ln, 13, "faint"))
            y += 19
        foot = (f"{self.state or STATE}{' · ' + self.note if self.note else ''} · generated {DATE} by "
                f"{GENERATOR}")
        for ln in wrap(foot, self.W - 2 * p, 13):
            self.add(render_line(p, y, ln, 13, "faint"))
            y += 19
        H = int(y + p - 20)
        markers = "".join(
            f'<marker id="arw-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="13" markerHeight="13" '
            f'orient="auto-start-reverse" markerUnits="userSpaceOnUse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" {fill(k)}/></marker>'
            for k in list(ACCENTS) + ["ink", "muted", "faint"])
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{H}" '
                f'viewBox="0 0 {self.W} {H}" aria-labelledby="t d">\n'
                f'<title id="t">{BRAND} {escape(self.ident)} — {escape(re.sub(r"[*`]", "", self.title))}</title>\n'
                f'<desc id="d">{escape(re.sub(r"[*`]", "", self.subtitle))}</desc>\n'
                f'<style>\n{_css()}\n</style>\n<defs>{markers}</defs>\n'
                f'<rect width="{self.W}" height="{H}" {fill("page")}/>\n')
        self.link()
        self.warnings = self.check()
        TEXT_BOXES.clear()
        return head + "\n".join(self.out) + "\n</svg>\n"
