"""Drawing helpers the posters share: a declaration as a card, a layered graph of cards, a chain of cards.

Layout is computed from the data and the measured text, never placed by hand, and every tie is broken by name, so
the same inputs give the same bytes.
"""
import re

import lib

GAP_X, GAP_Y = 26, 92        # between cards in a row, and between rows


def pages(paper):
    item, p0, p1 = paper
    return f"{item}, p. {p0}" if p0 == p1 else f"{item}, pp. {p0}–{p1}"


def accent_of(d, targets):
    if d.open:
        return "red"
    if d.i in targets:
        return "blue"
    return "amber"


def decl_card(c, x, y, d, accent, draw=True, w=None, extra=()):
    """A declaration: its name as code, its file and line, its Paper: reference. Returns (w, h)."""
    title = f"`{d.show}`"
    body = [f"`{d.where}`"]
    if d.paper:
        body.append("Paper: " + pages(d.paper))
    body += list(extra)
    w = w or max([230, lib.text_width(title, 13.5, bold=True) + 34] +
                 [min(lib.text_width(b, 12.5) + 34, 420) for b in body if not b.startswith("Item:")])
    h = c.card(x, y, w, title, body, accent=accent, size=12.5, tsize=13.5, bullets=False, draw=draw, pad=13,
               dash="6 4" if d.open else None)
    if draw:
        c.blocks[-1] = c.blocks[-1][:4] + ("node " + d.name,)
    return w, h


def item_line(c, d):
    """`Item: <its card>` for a declaration that belongs to a paper item, or nothing."""
    import items as I
    X = I.load()
    k = X.item_of.get(d.i)
    if k is None:
        return []
    it = X.items[k]
    return [f"Item: {to_anchor(c, it.anchor, it.label)}"]


def layered(c, y0, layers, edges, accent, extra=None):
    """Draw `layers` (lists of Decls, lowest layer first) as rows, the lowest at the foot, and an arrow for each
    (used, user) pair in `edges`, from the top of the used card to the foot of the user card. Returns the height
    used. The order in each row is by name, then two passes of barycentres against the rows next to it."""
    extra = extra or {}
    rows = [sorted(L, key=lambda d: d.name) for L in layers]
    nbr_up = {d.i: [] for L in rows for d in L}
    nbr_dn = {d.i: [] for L in rows for d in L}
    for a, b in edges:
        nbr_up[a].append(b)
        nbr_dn[b].append(a)
    pos = {d.i: k for L in rows for k, d in enumerate(L)}
    for _ in range(2):
        for r in range(1, len(rows)):
            rows[r].sort(key=lambda d: (sum(pos[j] for j in nbr_dn[d.i]) / len(nbr_dn[d.i]) if nbr_dn[d.i]
                                        else pos[d.i], d.name))
            pos.update({d.i: k for k, d in enumerate(rows[r])})
        for r in range(len(rows) - 2, -1, -1):
            rows[r].sort(key=lambda d: (sum(pos[j] for j in nbr_up[d.i]) / len(nbr_up[d.i]) if nbr_up[d.i]
                                        else pos[d.i], d.name))
            pos.update({d.i: k for k, d in enumerate(rows[r])})
    size = {d.i: decl_card(c, 0, 0, d, accent(d), draw=False, extra=extra.get(d.i, ())) for L in rows for d in L}
    width = c.x1 - c.x0
    box, y = {}, y0
    for L in reversed(rows):                       # the highest layer first, at the top
        tot = sum(size[d.i][0] for d in L) + GAP_X * (len(L) - 1)
        if tot > width:
            raise ValueError(f"a row of {len(L)} cards is {tot:.0f} wide, the poster {width:.0f}")
        x = c.x0 + (width - tot) / 2
        hmax = max(size[d.i][1] for d in L)
        for d in L:
            w, h = size[d.i]
            box[d.i] = (x, y, w, h)
            x += w + GAP_X
        y += hmax + GAP_Y
    layer_of = {d.i: r for r, L in enumerate(rows) for d in L}
    # ports: spread each card's arrows along its edge, in the order of the cards at their other ends
    outs = {i: sorted(nbr_up[i], key=lambda j: (box[j][0], j)) for i in box}
    ins = {i: sorted(nbr_dn[i], key=lambda j: (box[j][0], j)) for i in box}

    def port(i, j, side):
        x, yy, w, h = box[i]
        lst = outs[i] if side == "top" else ins[i]
        k = lst.index(j)
        px = x + w * (k + 1) / (len(lst) + 1)
        return px, (yy if side == "top" else yy + h)

    for a, b in sorted(edges, key=lambda e: (box[e[0]][0], box[e[1]][0], e)):
        p0 = port(a, b, "top")
        p1 = port(b, a, "bottom")
        pts = [p0]
        for r in range(layer_of[a] + 1, layer_of[b]):   # an arrow that skips a row passes between its cards
            L = rows[r]
            ry = box[L[0].i][1]
            rh = max(box[d.i][3] for d in L)
            t = (ry - p0[1]) / (p1[1] - p0[1])
            want = p0[0] + (p1[0] - p0[0]) * t
            xs = [box[L[0].i][0] - GAP_X / 2] + [box[d.i][0] + box[d.i][2] + GAP_X / 2 for d in L]
            gx = min(xs, key=lambda g: (abs(g - want), g))
            pts += [(gx, ry - 10), (gx, ry + rh + 10)]
        pts.append(p1)
        c.arrow(pts, accent="muted", sw=1.6)
    for L in rows:
        for d in L:
            x, yy, w, h = box[d.i]
            decl_card(c, x, yy, d, accent(d), w=w, extra=extra.get(d.i, ()))
    return y - GAP_Y - y0


def chain(c, x, y, decls, accent, maxw=None):
    """A chain of declarations as cards left to right, lowest first, an arrow between each pair, wrapping to a new
    row when the next card does not fit. Returns the height used."""
    maxw = maxw or (c.x1 - x)
    sizes = [decl_card(c, 0, 0, d, accent(d), draw=False) for d in decls]
    cx, cy, rowh, placed = x, y, 0, []
    for d, (w, h) in zip(decls, sizes):
        if placed and cx + w > x + maxw:
            cx, cy, rowh = x, cy + rowh + 54, 0
        placed.append((d, cx, cy, w, h))
        cx += w + 54
        rowh = max(rowh, h)
    for (d, px, py, pw, ph), (e, qx, qy, qw, qh) in zip(placed, placed[1:]):
        if qy == py:
            c.arrow([(px + pw, py + ph / 2), (qx, py + ph / 2)], accent="muted", sw=1.6)
        else:
            mid = py + ph + 27
            c.arrow([(px + pw / 2, py + ph), (px + pw / 2, mid), (qx + qw / 2, mid), (qx + qw / 2, qy)],
                    accent="muted", sw=1.6)
    for d, px, py, pw, ph in placed:
        decl_card(c, px, py, d, accent(d), w=pw)
    return cy + rowh - y


def quote(c, x, y, w, s, size=14, color="ink"):
    """A quotation: the whole paragraph in italics (the library's inline markup has bold and code, not italics),
    so that a reader can tell it from the poster's own words. Markdown emphasis inside the quotation (`*title*`) is
    dropped, since the whole is already italic. Returns the height used."""
    s = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"\1", s)
    lead = round(size * 1.42, 1)
    lines = lib.wrap(s, w, size, italic=True)
    for k, ln in enumerate(lines):
        c.add(lib.render_line(x, y + size + k * lead, ln, size, color, italic=True))
    c.ymax = max(c.ymax, y + size * 0.35 + (len(lines) - 1) * lead + size)
    return (len(lines) - 1) * lead + size * 1.35


# -- links between posters. A link is made only to what exists: an anchor of the poster being drawn, an anchor the
# committed manifest gives another poster, or a poster the manifest lists. Anything else stays plain text, and the
# generator's second run (when anchors moved) makes the link. Canvas.check fails the build on a link that does
# not resolve.

def to_anchor(c, anchor, text, own=()):
    """`text` linked to the card `anchor`, on this poster (`own`, the anchors it will draw) or on the poster that
    draws it."""
    if anchor in own:
        return f"[[@#{anchor}|{text}]]"
    if anchor in lib.REGISTRY:
        return f"[[@{lib.REGISTRY[anchor]}#{anchor}|{text}]]"
    return text


def to_poster(pid, text, anchor=None):
    """`text` linked to poster `pid`: to `anchor` on it, or else to its title block (`top`), so that every link has a
    target to frame."""
    f = lib.POSTERS.get(pid)
    if not f:
        return text
    if anchor and anchor in lib.ANCHORS_OF.get(f, ()):
        return f"[[@{f}#{anchor}|{text}]]"
    if "top" in lib.ANCHORS_OF.get(f, ()):
        return f"[[@{f}#top|{text}]]"
    return f"[[@{f}|{text}]]"


def to_url(url, text):
    return f"[[@{url}|{text}]]"


def paper_label(url):
    """A paper's link as ERRATA.md gives it -> its identifier: `arXiv:1002.4127`, `doi:10.1000/x`."""
    m = re.match(r"https://arxiv\.org/(?:abs|pdf)/(.+?)(?:\.pdf)?$", url)
    if m:
        return f"arXiv:{m.group(1)}"
    if url.startswith("https://doi.org/"):
        return f"doi:{url[len('https://doi.org/'):]}"
    raise ValueError(f"ERRATA.md links a paper at {url}, which draw.paper_label cannot name")


def paper_links(cited):
    """{url: entry ids} -> `arXiv:1002.4127`, each opening the paper, for a narrow cell."""
    return ", ".join(to_url(u, paper_label(u)) for u in cited)


def errata_papers(m, cited):
    """{url: entry ids} -> a card line: each paper the entries' rows link, in ERRATA.md's words, and the entries."""
    return "Papers the errata link: " + "; ".join(
        f"{m.paper_text[u]}, {to_url(u, paper_label(u))} ({', '.join(ids)})" for u, ids in cited.items())


NAV = [("M1", "what the targets rest on"), ("M2", "the steps with no known repair"), ("M3", "the paper by depth"),
       ("M4", "every chapter"), ("M5", "the refutations")]


def nav(c, ident, y):
    """The line under the title that links the overviews; M4 lists every chapter poster. Returns the height used.
    Also makes the title block an anchor, `top`, which a link to the whole poster opens and frames."""
    c.out.insert(0, '<g id="top">')
    c.anchors.append("top")
    close(c, 1, c.x0, c.pad - 10, c.x1 - c.x0, y - c.pad - 12, pad=10)
    parts = [f"**{pid}**, {what}" if pid == ident else to_poster(pid, f"{pid}, {what}") for pid, what in NAV]
    return c.para(c.x0, y, c.x1 - c.x0, "Posters: " + " · ".join(parts) + ". Names, items, files, entries and "
                  "posters are links, underlined under the pointer: a card's title or a Lean name opens the source "
                  "at the pin.", size=13.5, color="faint") + 16


def anchored(c, anchor):
    """Open a group with id `anchor` around what is drawn next. Returns the mark that `close` takes."""
    c.add(f'<g id="{anchor}">')
    c.anchors.append(anchor)
    return len(c.out)


def close(c, mark, x, y, w, h, pad=7):
    """Close the group `anchored` opened, with its halo behind everything in it: a frame around the box (x, y, w, h)
    that lib's CSS shows only while the group is the target of the address (`:target`), so that a link's
    destination stands out when it is opened."""
    c.out.insert(mark, f'<rect x="{x - pad:.1f}" y="{y - pad:.1f}" width="{w + 2 * pad:.1f}" '
                       f'height="{h + 2 * pad:.1f}" rx="12" fill="{lib.light("amber-t")}" stroke="{lib.light("amber")}" '
                       f'class="rd-target ft-amber s-amber" stroke-width="3.5" opacity="0"/>')
    c.add("</g>")


def coverable(text):
    """A quotation the embedded fonts can draw: the text, or, if it has a character the fonts lack, the text cut
    before the sentence that holds the first one and marked ` …`. Returns (text, whether it was cut)."""
    bad = [i for i, ch in enumerate(text) if ch not in lib.COVERED and ch != "\n"]
    if not bad:
        return text, False
    start = max((i for i in range(bad[0]) if text[i - 1:i + 1] in (". ", ".\n")), default=0)
    return (text[:start].rstrip() + " …") if start else "…", True


def m2_card(d):
    """The anchor of an open declaration's card on M2, for the ones no open row names."""
    import re
    return "open-" + re.sub(r"[^\w.-]+", "_", d.key)


def m2_target(m, d):
    """Where M2 names the open declaration `d`: the row of ERRATA.md's open rows that names it in code
    (`row-<line>`), else its own card there."""
    for r in m.rows:
        if not r.settled and any((x := m.resolve(n)) is not None and x.i == d.i for n in r.names):
            return f"row-{r.line}"
    return m2_card(d)


def described(d, limit=280):
    """The first sentence of a declaration's docstring description, to quote on a card; one longer than `limit`
    characters is cut at a word and marked ` …`, as is one with a character the fonts lack. None when there is none."""
    if not d.summary:
        return None
    first = re.split(r"(?<=[.!?])\s+(?=[A-Z(`$])", d.summary)[0]
    if len(first) > limit:
        cut = first[:limit].rsplit(" ", 1)[0].rstrip(",;:")
        if cut.count("`") % 2:                  # never leave a code run open
            cut = cut[:cut.rindex("`")].rstrip()
        first = cut + " …"
    text, _ = coverable(first)
    return text if text != "…" else None
