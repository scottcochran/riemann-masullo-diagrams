"""A chapter poster: one module directory of riemann-masullo's library, item by item.

The view riemann-masullo's own progress map gives per section, pinned. Each module of the directory is a band,
and each paper item a card in the band of the module that holds most of its declarations. A card gives the item's
pages, its declarations, its state, how many of its declarations state something other than the print, the
printed claims kept for it, its errata entries by Checked value, the items of the chapter it uses and is used by
(with redundant edges dropped), and how many items of other chapters it uses.

Each chapter module (`d_c*.py`) records what it expects and passes it to `build()`, which compares every value
with what the sources say and fails on a difference:

- ITEMS: band (a module's file, or in ForMathlib a directory) -> the item keys drawn in it, in the paper's order;
- EXPECTED: the item edges drawn, (used, user), after the redundant ones are dropped;
- OUTSIDE: item -> chapter -> how many items of that chapter it uses directly, for the items that use any;
- STATES: the items that are open, and those that rest on an open declaration;
- DEVIATIONS: item -> (declarations with a `Deviation:` line, declarations), for the items that have one;
- ERRATA: item -> Checked value -> the entries placed on it.
- CITES: item -> the keys of the bibliography the manuscript cites on the item's pages (diagrams/src/paper.py).
- ERRATA_PAPERS: item -> the URL of each paper those entries' rows of ERRATA.md link -> the entries that link it.
"""
import collections
import re

import draw
import items as I
import lib
import paper
import rm

W = 2400
COLS = 6
GAP = 22
ACCENT = {"open": "red", "rests": "amber", "proved": "teal"}
STATE_LABEL = {"open": "open: a declaration of the item uses sorryAx",
               "rests": "proved, but rests on an open declaration",
               "proved": "proved, with nothing open below"}


def short_module(module, chapter):
    """The band an item is drawn in: its module's file under the directory, or, in `ForMathlib`, where each file is
    one item, the first directory under it."""
    rest = module.split(".", 2)[2] if module.count(".") >= 2 else module
    if chapter == "ForMathlib":
        parts = rest.split(".")
        return f"ForMathlib/{parts[0]}/" if len(parts) > 1 else "ForMathlib/"
    return rest.replace(".", "/") + ".lean"


def plural(n, word):
    if n == 1:
        return f"1 {word}"
    return f"{n:,} " + (word[:-1] + "ies" if word.endswith("y") else word + "s")


def paper_order(it):
    """Items in the paper's order: by number, then kind; an item with no number after, by its text."""
    kind, _, rest = it.key.partition(":")
    num = I.NUMBER.fullmatch(rest)
    return (0, I.natural(rest), kind) if num else (1, I.natural(rest), kind)


def poster_id(chapter):
    """The id of a directory's chapter poster: C5 for Ch05_ThetaZSpaces, CA for AppA_AlgebraicNT, L1 for ForMathlib."""
    m1, m2 = re.match(r"Ch(\d+)_", chapter), re.match(r"App([A-E])_", chapter)
    return f"C{int(m1.group(1))}" if m1 else f"C{m2.group(1)}" if m2 else "L1"


def chapter_title(chapter):
    name = rm.chapter_label(chapter)
    return f"{name} · `{chapter}`" if name != chapter else f"`{chapter}`"


def read(chapter):
    """Everything a chapter poster draws, as the values its literals are compared with."""
    X = I.load()
    its = sorted(X.chapter(chapter), key=lambda it: (I.natural(it.module), paper_order(it)))
    keys = {it.key for it in its}
    items = collections.defaultdict(list)
    for it in its:
        items[short_module(it.module, chapter)].append(it.key)
    edges = I.reduce([(it.key, u) for it in its for u in it.uses if u in keys])
    outside = {}
    for it in its:
        cnt = collections.Counter(X.items[u].chapter for u in it.uses if u not in keys)
        if cnt:
            outside[it.key] = dict(sorted(cnt.items(), key=lambda kv: rm.chapter_order(kv[0])))
    states = {s: [it.key for it in its if it.state == s] for s in ("open", "rests")}
    devs = {it.key: (it.deviations, len(it.decls)) for it in its if it.deviations}
    errata = {it.key: it.errata for it in its if it.errata}
    m = rm.load()
    papers = {k: cited for k, v in errata.items() if (cited := m.papers_of([i for ids in v.values() for i in ids]))}
    P = paper.load()
    cites = {it.key: ks for it in its if it.pages and (ks := P.keys_on(*it.pages))}
    return its, {"ITEMS": {k: items[k] for k in sorted(items, key=I.natural)},
                 "EXPECTED": sorted((b, a) for a, b in edges), "OUTSIDE": outside, "STATES": states,
                 "DEVIATIONS": devs, "ERRATA": errata, "ERRATA_PAPERS": papers,
                 "CITES": cites}


def build(ident, chapter, **expected):
    m = rm.load()
    its, got = read(chapter)
    for name in ("ITEMS", "EXPECTED", "OUTSIDE", "STATES", "DEVIATIONS", "ERRATA", "ERRATA_PAPERS", "CITES"):
        rm.require(f"{ident} {name}", expected[name], got[name], f"{ident}'s cards for {chapter}")
    by_key = {it.key: it for it in its}
    uses = collections.defaultdict(list)
    used_by = collections.defaultdict(list)
    for b, a in got["EXPECTED"]:
        uses[a].append(b)
        used_by[b].append(a)
    n_decls = sum(len(it.decls) for it in its)
    st = collections.Counter(it.state for it in its)
    n_dev = len(got["DEVIATIONS"])
    n_err = len({e for v in got["ERRATA"].values() for ids in v.values() for e in ids})
    paper_items = sum(1 for it in its if not it.key.startswith(("helpers:", "file:")))
    what = "files" if chapter == "ForMathlib" else "items"
    c = lib.Canvas(
        ident, f"{chapter_title(chapter)}, {what[:-1]} by {what[:-1]}",
        f"riemann-masullo at {rm.SHORT}: {plural(len(its), what[:-1])}"
        + ("" if chapter == "ForMathlib" else f" in {plural(len({it.module for it in its}), 'module')}")
        + f", {plural(n_decls, 'declaration')}. "
        f"{st['open']} open, {st['rests']} resting on an open declaration, {st['proved']} proved. "
        f"{plural(n_dev, what[:-1])} {'has' if n_dev == 1 else 'have'} a declaration that states something other "
        f"than the print" + (f"; {plural(n_err, 'errata entry').replace('entrys', 'entries')} "
                             f"{'is' if n_err == 1 else 'are'} on them." if n_err else "."),
        W, rm.sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += draw.nav(c, ident, y)
    own = {it.anchor for it in its}
    entry_line = {e["id"]: e["line"] for e in m.entries}
    intro = ("**How to read it.** One band per module of the directory, one card per paper item: the declarations "
             "whose docstrings cite it, and the helpers before them in the same file, as riemann-masullo's progress "
             "map groups them. " if chapter != "ForMathlib" else
             "**How to read it.** One card per file, and one band per directory under `ForMathlib`, with the rest "
             "of the path on the card: the paper does not number this material, so each file is one item, as "
             "riemann-masullo's progress map has it. ")
    intro += ("The line in italics is quoted from the Lean source (Apache-2.0): the first sentence of the docstring of the "
              "declaration the card's title opens, after its `Paper:` reference, cut and marked “…” where long. It is "
              "the formalisers' description of what the Lean states, not the manuscript's. "
              "“Uses” and “Used by” name the items of this directory whose declarations a card's declarations "
              "use directly, with each use that another path between the same items already implies left out. "
              "Uses of other directories are counted, not named. A use is what the elaborated terms reach at the "
              "pin, a fact about the Lean and not about the paper.")
    if n_err:
        intro += (" Errata are ERRATA.md's entries, placed by the item numbers their “Where” column names, with "
                  "their Checked value and nothing stronger. They were reported and checked by AI agents; in "
                  "ERRATA.md's words, “No entry has been reviewed by a specialist.”")
    if got["CITES"]:
        intro += (" “Its pages cite” names the works the manuscript cites, by their keys in its bibliography, on the "
                  "pages of the card's `Paper:` references, read from riemann-masullo's transcription of it; each "
                  "opens the work's row on B1. They are the paper's citations, not the Lean's, which cites none of "
                  "them, and say nothing of what the Lean rests on.")
    if got["ERRATA_PAPERS"]:
        intro += (" A paper named under the errata is one an entry's row of ERRATA.md links, named in that row's "
                  "words; the linked paper was not read here.")
    y += c.para(x0, y, x1 - x0, intro, size=14.5, color="muted") + 26
    cw = (x1 - x0 - GAP * (COLS - 1)) / COLS

    def body(it):
        out = []
        printed = (f"{it.printed} printed claim{'s' if it.printed != 1 else ''} kept" if it.printed else "")
        decl_poster = "D" + poster_id(chapter)[1:] if chapter != "ForMathlib" else "DL"
        n = plural(len(it.decls), "declaration")
        out.append(draw.to_poster(decl_poster, n, anchor=I.anchor(it.key, "d"))
                   + (", " + draw.to_poster(decl_poster, f"{it.deviations} deviating from the print",
                                            anchor=I.anchor(it.key, "v")) if it.deviations else "")
                   + (", " + draw.to_poster("M5", printed, anchor=f"refuted-{chapter}") if printed else ""))
        if it.state != "proved":
            opened = sorted((d for d in it.decls if d.open), key=lambda d: d.key)
            below = sorted({o.key: o for d in it.decls for o in m.open_below(d.i)}.values(), key=lambda d: d.key)
            opens = opened if it.state == "open" else below
            floor = any(o.key == "RiemannMasullo.traceFormula_exteriorZeros" for o in opened + below)
            words = (f"{plural(len(opened), 'declaration')} of the item {'is' if len(opened) == 1 else 'are'} open"
                     if it.state == "open" else f"rests on {plural(len(below), 'open declaration')}")
            # each open declaration opens where M2 names it: its row, or its card
            targets = sorted({draw.m2_target(m, o) for o in opens}, key=I.natural)
            m2 = ", ".join(draw.to_poster("M2", "M2" if len(targets) == 1 else f"M2 ({n + 1})", anchor=t)
                           for n, t in enumerate(targets))
            out.append(words[0].upper() + words[1:] + ", named on " + m2
                       + (" and " + draw.to_poster("M1", "M1", anchor="floor") if floor else ""))
        if it.key in got["ERRATA"]:
            out.append("Errata: " + "; ".join(
                ", ".join(draw.to_url(m.errata_url(entry_line[i]), i) for i in ids) + f" ({chk})"
                for chk, ids in got["ERRATA"][it.key].items()))
        if it.key in got["ERRATA_PAPERS"]:
            out.append(draw.errata_papers(m, got["ERRATA_PAPERS"][it.key]))
        if it.key in got["CITES"]:
            P = paper.load()
            out.append("Its pages cite: " + ", ".join(draw.to_poster("B1", k, anchor=P.by_key[k][0].anchor)
                                                      for k in got["CITES"][it.key]))
        if uses[it.key]:
            out.append("**Uses:** " + ", ".join(draw.to_anchor(c, by_key[u].anchor, by_key[u].label, own)
                                                for u in sorted(uses[it.key], key=I.natural)))
        if it.key in got["OUTSIDE"]:
            # one item used there: its card; more: the list of them on the declarations poster, row by directory
            X = I.load()
            def outside(k, n):
                if n == 1:
                    u = next(u for u in it.uses if X.items[u].chapter == k)
                    return draw.to_anchor(c, X.items[u].anchor, rm.chapter_label(k)) + " (1)"
                return draw.to_poster(decl_poster, rm.chapter_label(k), anchor=f"{I.anchor(it.key, 'o')}--{k}") + f" ({n})"
            out.append("From other directories: " + ", ".join(outside(k, n) for k, n in got["OUTSIDE"][it.key].items()))
        if used_by[it.key]:
            out.append("**Used by:** " + ", ".join(draw.to_anchor(c, by_key[u].anchor, by_key[u].label, own)
                                                   for u in sorted(used_by[it.key], key=I.natural)))
        return out

    def title(it):
        return draw.to_url(it.first.url, it.label)

    def sub(it):
        if it.key.startswith("file:"):
            parts = it.key[len("file:"):].split("/")[2:-1]     # the directories below the band
            return "/".join(parts[1:]) + "/" if len(parts) > 1 else None
        if it.pages is None:
            return None
        p0, p1 = it.pages
        return f"p. {p0}" if p0 == p1 else f"pp. {p0}–{p1}"

    for mod, keys in got["ITEMS"].items():
        y += c.heading(x0, y, f"`{mod}` · {len(keys)} {what if len(keys) != 1 else what[:-1]}", size=17)
        for r in range(0, len(keys), COLS):
            row = [by_key[k] for k in keys[r:r + COLS]]
            hs = [c.card(0, 0, cw, title(it), body(it), accent=ACCENT[it.state], sub=sub(it), size=12.5, tsize=14,
                         bullets=False, draw=False, pad=12, quote=draw.described(it.first)) for it in row]
            h = max(hs)
            for k, it in enumerate(row):
                mark = draw.anchored(c, it.anchor)
                cx = x0 + k * (cw + GAP)
                c.card(cx, y, cw, title(it), body(it), accent=ACCENT[it.state], sub=sub(it),
                       size=12.5, tsize=14, bullets=False, pad=12, h=h, dash="6 4" if it.state == "open" else None,
                       quote=draw.described(it.first))
                c.blocks[-1] = c.blocks[-1][:4] + ("node " + it.key,)
                draw.close(c, mark, cx, y, cw, h)
            y += h + GAP
        y += 18
    y += 10
    y += c.legend(x0, y, [("box", ACCENT[s], STATE_LABEL[s], "6 4" if s == "open" else None) for s in I.STATES],
                  title="Key")
    y += 30
    c.para(x0, y, x1 - x0,
           "**What this does not say.** Nothing was built or proved by this repository: the declarations and their "
           "uses are read from riemann-masullo's compiled library at the pin. A card says what the Lean holds for an "
           "item, not that the item is right. Item numbers and pages are the Lean docstrings'; the manuscript is not "
           "read. “Deviating from the print” counts declarations whose docstring has a `Deviation:` line. A card's title opens "
           "its first declaration at the pin; its other links open the cards, posters and ERRATA.md lines they name.",
           size=13.5, color="muted")
    return c
