"""A declarations poster: one module directory of riemann-masullo's library, declaration by declaration.

The expansion of a chapter poster's cards. Each item of the directory is a block, in the chapter poster's order, with
two anchors that the card's counts open: `v-<item>`, the declarations whose docstring has a `Deviation:` line,
each with that line quoted; and `d-<item>`, every declaration of the item, with its kind, file and line, and state.

Each module `d_d*.py` records, and `build()` compares both ways:

- DECLS: item -> every declaration of it, by its key, in file and line order;
- DEVIATING: item -> the declarations of it with a `Deviation:` line;
- OUTSIDE_ITEMS: item -> directory -> the items of that directory it uses directly, for the uses the chapter card
  counts under "From other directories". Each directory is a row, `o-<item>--<directory>`, that the card's count opens.
"""
import chapter as CH
import draw
import items as I
import lib
import rm

W = 2400


def order(d):
    return (I.natural(d.module), d.line, d.name)


def outside_anchor(key, directory):
    return f"{I.anchor(key, 'o')}--{directory}"


def read(chapter):
    its, got = CH.read(chapter)
    X = I.load()
    keys = {it.key for it in its}
    decls = {it.key: [d.key for d in sorted(it.decls, key=order)] for it in its}
    deviating = {it.key: [d.key for d in sorted(it.decls, key=order) if d.deviation] for it in its if it.deviations}
    outside = {}
    for it in its:
        by_dir = {}
        for u in it.uses:
            if u not in keys:
                by_dir.setdefault(X.items[u].chapter, []).append(u)
        if by_dir:
            outside[it.key] = {k: sorted(by_dir[k], key=I.natural) for k in sorted(by_dir, key=rm.chapter_order)}
    return its, got, {"DECLS": decls, "DEVIATING": deviating, "OUTSIDE_ITEMS": outside}


def build(ident, chapter, **expected):
    m = rm.load()
    its, got, lits = read(chapter)
    for name in ("DECLS", "DEVIATING", "OUTSIDE_ITEMS"):
        rm.require(f"{ident} {name}", expected[name], lits[name], f"{ident}'s blocks for {chapter}")
    by_key = {it.key: it for it in its}
    n_decls = sum(len(v) for v in lits["DECLS"].values())
    n_dev = sum(len(v) for v in lits["DEVIATING"].values())
    card_poster = CH.poster_id(chapter)
    c = lib.Canvas(
        ident, f"{CH.chapter_title(chapter)}, declaration by declaration",
        f"riemann-masullo at {rm.SHORT}: the {CH.plural(n_decls, 'declaration')} of the "
        f"{CH.plural(len(its), 'file' if chapter == 'ForMathlib' else 'item')} on {card_poster}, each with its kind, "
        f"file, line and state; {CH.plural(n_dev, 'declaration')} with a `Deviation:` line, quoted; and the items of "
        f"other directories each item uses.",
        W, rm.sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += draw.nav(c, ident, y)
    y += c.para(x0, y, x1 - x0,
                f"**How to read it.** The expansion of {draw.to_poster(card_poster, card_poster)}'s cards, in the same "
                f"order: one block per item, its heading opening the card. First the declarations whose docstring "
                f"states how the Lean departs from the print, each with its `Deviation:` line quoted from the Lean "
                f"source (Apache-2.0), then every declaration of the item. A name opens its line at the pin. A "
                f"declaration's state is read from the terms: open when it uses `sorryAx`, resting when something "
                f"open is below it. That a declaration states what its `Deviation:` line says is the docstring's "
                f"claim, not checked here.", size=14.5, color="muted") + 26
    cols = [("Declaration", 1120), ("Kind", 150), ("File and line", 680), ("State", 338)]
    for band, keys in got["ITEMS"].items():
        y += c.heading(x0, y, f"`{band}`", size=17)
        for k in keys:
            it = by_key[k]
            ds = [m.decls[d.i] for d in sorted(it.decls, key=order)]
            pages = ""
            if it.pages:
                p0, p1 = it.pages
                pages = f" · p. {p0}" if p0 == p1 else f" · pp. {p0}–{p1}"
            dmark, dy = draw.anchored(c, I.anchor(k, "d")), y
            y += c.para(x0, y, x1 - x0, draw.to_anchor(c, it.anchor, it.label)
                        + f"{pages} · {CH.plural(len(ds), 'declaration')}"
                        + (f", {it.deviations} deviating from the print" if it.deviations else ""), size=15,
                        bold=True) + 6
            if it.deviations:
                vmark, vy = draw.anchored(c, I.anchor(k, "v")), y
                for d in ds:
                    if not d.deviation:
                        continue
                    y += c.para(x0 + 14, y, x1 - x0 - 14, f"`{d.show}` · `{d.where}`", size=13, color="amber") + 2
                    text, cut = draw.coverable(d.deviation)
                    y += draw.quote(c, x0 + 32, y, x1 - x0 - 32, text, size=13.5)
                    if cut:
                        y += c.para(x0 + 32, y, x1 - x0 - 32, "Abridged here: the rest uses a character the posters' "
                                    "fonts lack. The name opens the full text at the pin.", size=12, color="faint")
                    y += 8
                draw.close(c, vmark, x0 + 6, vy, x1 - x0 - 6, y - vy - 8, pad=5)
                y += 6
            rows = []
            for d in ds:
                state = ("open" if d.open else "rests on something open" if m.open_below(d.i) else "")
                shown = " · ".join(p for p in (state, "deviates from the print" if d.deviation else "") if p)
                rows.append({"cells": [f"`{d.show}`", d.kind, f"`{d.where}`", shown],
                             "accent": "red" if d.open else "amber" if state else None})
            y += c.table(x0, y, cols, rows, size=12, hsize=12.5, pad=6, header=True)
            if k in lits["OUTSIDE_ITEMS"]:
                X = I.load()
                orows = [{"cells": [draw.to_poster(CH.poster_id(dk), rm.chapter_label(dk)),
                                    ", ".join(draw.to_anchor(c, X.items[u].anchor, X.items[u].label) for u in us)],
                          "anchor": outside_anchor(k, dk)} for dk, us in lits["OUTSIDE_ITEMS"][k].items()]
                y += 8
                y += c.table(x0, y, [("Uses of other directories", 320), ("Items it uses there directly", 1968)],
                             orows, size=12, hsize=12.5, pad=6, zebra=False)
            draw.close(c, dmark, x0, dy, x1 - x0, y - dy, pad=9)
            y += 26
        y += 10
    c.para(x0, y, x1 - x0,
           "**What this does not say.** Nothing was built or proved here; the declarations, their lines and states are "
           "read from riemann-masullo's compiled library at the pin. A quoted `Deviation:` line is the Lean's own "
           "account of how its statement departs from the print; the manuscript is not read.", size=13.5,
           color="muted")
    return c
