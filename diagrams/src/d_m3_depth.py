"""M3: the paper by depth.

Every item of the manuscript that a declaration's docstring names in its `Paper:` line, as a mark: in the row of
its chapter, and in the column of its depth below the targets, the fewest direct uses from one of the seven
theorems of comparator.json down to a declaration of the item. An item with no declaration below a target is in
the last column. A mark's fill is the item's state in the Lean; its ring, if any, says that ERRATA.md has an
entry on the item, and how far that entry has been checked.

Items are keyed as riemann-masullo's scripts/progress/build.py keys them (`paper_item`): the kind word and the
number, so that `Theorem 7.3.1.6(2)` and `Theorem 7.3.1.6(3)` are one item, and `(7.3.1.6)` another.
"""
import collections

import lib
import rm
from items import NUMBER, item_key, keys_named

ID = "M3"
SLUG = "depth"

# What the build expects the sources to say at MASULLO_COMMIT.
N_ITEMS = 1251
# depth below the targets -> items; None: no declaration of the item is below a target
EXPECTED_DEPTHS = {1: 1,
 2: 2,
 3: 14,
 4: 34,
 5: 14,
 6: 7,
 7: 7,
 8: 16,
 9: 19,
 10: 7,
 11: 2,
 12: 4,
 13: 11,
 14: 12,
 15: 6,
 19: 1,
 20: 10,
 21: 7,
 22: 5,
 23: 7,
 24: 2,
 None: 1063}
# state -> items
COUNTS = {'open': 7, 'rests': 37, 'proved': 1207}
# chapter of the item's number -> (items, of them below a target)
CHAPTERS = {'1': (9, 1),
 '2': (58, 11),
 '3': (88, 29),
 '4': (90, 0),
 '5': (76, 0),
 '6': (27, 1),
 '7': (83, 0),
 '8': (11, 0),
 '9': (47, 0),
 '10': (81, 0),
 '11': (49, 0),
 '12': (44, 1),
 '13': (3, 0),
 '14': (2, 0),
 'A': (121, 44),
 'B': (116, 0),
 'C': (191, 46),
 'D': (144, 55),
 'E': (10, 0),
 'none': (1, 0)}
# Checked value -> (entries placed on an item, items they are on); and the entries placed on no item
ERRATA = {'Lean': (82, 101), 'reviewed': (613, 407), 'integrator': (1, 5), 'reported': (0, 0)}
UNPLACED = 53

W = 2000
STATES = [("open", "red", "open: a declaration of the item uses sorryAx"),
          ("rests", "amber", "proved, but rests on an open declaration"),
          ("proved", "teal", "proved, with nothing open below")]
RINGS = {"Lean": ("ink", 2.4, None), "reviewed": ("muted", 1.3, None), "integrator": ("muted", 1.3, "2 2"),
         "reported": ("muted", 1.3, "2 2")}


def chapter_key(key):
    """The chapter of the item's number: `lemma:A.2.3.4` -> `A`; an item with no number -> `none`."""
    if key.startswith("item:") and not NUMBER.search(key):
        return "none"
    return key.split(":", 1)[1].split(".")[0]


def chapter_sort(head):
    return (2, head) if head == "none" else (1, head) if head.isalpha() else (0, int(head))


def chapter_name(head):
    return "No number" if head == "none" else f"Chapter {head}" if head.isdigit() else f"Appendix {head}"


def build():
    m = rm.load()
    items = collections.defaultdict(list)
    for d in m.decls:
        if d.paper and not d.vendored:
            items[item_key(d.paper[0])].append(d)
    rm.require("N_ITEMS", N_ITEMS, len(items), "M3, every row")
    dist = m.depth_from_targets()
    depth = {k: min((dist[d.i] for d in v if d.i in dist), default=None) for k, v in items.items()}
    hist = collections.Counter(depth.values())
    rm.require("EXPECTED_DEPTHS", EXPECTED_DEPTHS, {k: hist[k] for k in sorted(hist, key=lambda x: (x is None, x or 0))},
               "M3's columns")
    state = {}
    for k, v in items.items():
        if any(d.open for d in v):
            state[k] = "open"
        elif any(m.open_below(d.i) for d in v):
            state[k] = "rests"
        else:
            state[k] = "proved"
    counts = collections.Counter(state.values())
    rm.require("COUNTS", COUNTS, {s: counts[s] for s, _, _ in STATES}, "M3's fills and key")
    chap = collections.defaultdict(lambda: [0, 0])
    for k in items:
        chap[chapter_key(k)][0] += 1
        chap[chapter_key(k)][1] += depth[k] is not None
    chapters = {h: tuple(chap[h]) for h in sorted(chap, key=chapter_sort)}
    rm.require("CHAPTERS", CHAPTERS, chapters, "M3's rows")
    ring = {}
    placed = collections.defaultdict(lambda: [0, set()])
    unplaced = 0
    order = {c: n for n, c in enumerate(rm.CHECKED)}
    for e in m.entries:
        if e["checked"] not in order:                    # withdrawn or moved: the entry did not stand
            continue
        ks = sorted({k for k in keys_named(e["where"]) if k in items})
        if not ks:
            unplaced += 1
            continue
        placed[e["checked"]][0] += 1
        for k in ks:
            placed[e["checked"]][1].add(k)
            if k not in ring or order[e["checked"]] < order[ring[k]]:
                ring[k] = e["checked"]
    errata = {c: (placed[c][0], len(placed[c][1])) for c in rm.CHECKED}
    rm.require("ERRATA", ERRATA, errata, "M3's rings and the errata note")
    rm.require("UNPLACED", UNPLACED, unplaced, "M3's errata note")

    # -- drawing
    n_below = sum(1 for v in depth.values() if v is not None)
    maxd = max(v for v in depth.values() if v is not None)
    c = lib.Canvas(
        ID, "The paper by depth below the targets",
        f"The {len(items):,} items of the manuscript that the Lean's docstrings name, by chapter and by how far below "
        f"the seven target theorems their declarations are. {n_below} have a declaration below a target, at depths 1 "
        f"to {maxd}; the other {len(items) - n_below:,} are not reached from the targets at {rm.SHORT}.",
        W, rm.sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += c.para(x0, y, x1 - x0,
                "**How to read it.** One mark is one item (a theorem, lemma, definition, equation or section) that at "
                "least one declaration names in its `Paper:` line. Its column is the fewest direct uses from a target "
                "down to one of its declarations; the last column holds the items none of whose declarations is "
                "below a target. All seven targets rest on one open declaration with no proof term "
                "(`traceFormula_exteriorZeros`, M1), so what its proof would use is not below them. Depth is a fact "
                "about the Lean at the pin, not about the paper's argument.", size=14.5, color="muted")
    y += 24
    errata_n = sum(v[0] for v in errata.values())
    y += c.para(x0, y, x1 - x0,
                f"**The rings are errata.** ERRATA.md's entries were reported and checked by AI agents, as that file "
                f"says; its Checked column is drawn as it is, and nothing stronger. In its words: “No entry has been "
                f"reviewed by a specialist.” {errata_n} entries are placed on an item by the numbers their “Where” "
                f"column names ({', '.join(f'{v[0]} {k}' for k, v in errata.items() if v[0])}); "
                f"{unplaced} name no item that a `Paper:` line names, and are not drawn. Withdrawn and moved entries "
                f"are left out. A ring is the most-checked entry on the item.", size=14.5, color="muted")
    y += 28

    # grid
    label_w, col_w, last_w = 150, 46, 0
    cols = list(range(1, maxd + 1))
    last_x = x0 + label_w + col_w * len(cols) + 16
    last_w = x1 - last_x
    dot, step = 9, 12
    per_col = max(1, int((col_w - 6) // step))
    per_last = int((last_w - 12) // step)
    c.text(x0, y + 14, "Chapter", 13, "faint", bold=True)
    for k, dd in enumerate(cols):
        c.text(x0 + label_w + k * col_w + col_w / 2, y + 14, str(dd), 12.5, "faint", anchor="middle", bold=True)
    c.text(last_x + 6, y + 14, "not below a target", 13, "faint", bold=True)
    c.text(x0 + label_w, y - 6, "depth below the targets →", 12, "faint")
    y += 26
    by_cell = collections.defaultdict(list)
    for k in items:
        by_cell[(chapter_key(k), depth[k])].append(k)
    sorder = {s: n for n, (s, _, _) in enumerate(STATES)}
    for head in chapters:
        cells = {dd: sorted(by_cell.get((head, dd), []), key=lambda k: (sorder[state[k]], k)) for dd in cols + [None]}
        nrows = max([1] + [-(-len(v) // per_col) for dd, v in cells.items() if dd is not None] +
                    [-(-len(cells[None]) // per_last)])
        rh = nrows * step + 14
        c.line(x0, y, x1, y, accent="line", sw=1)
        name = chapter_name(head)
        c.text(x0, y + 18, f"**{name}**", 13.5, "ink")
        c.text(x0, y + 35, f"{chapters[head][1]} of {chapters[head][0]}", 12, "muted")
        for dd, v in cells.items():
            cx = (x0 + label_w + cols.index(dd) * col_w + 3) if dd is not None else last_x + 6
            per = per_col if dd is not None else per_last
            for n, k in enumerate(v):
                px = cx + (n % per) * step + step / 2
                py = y + 10 + (n // per) * step + step / 2
                acc = next(a for s, a, _ in STATES if s == state[k])
                c.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{dot / 2 - 0.4:.1f}" {lib.fs(acc, acc)} '
                      f'stroke-width="0.8"><title>{lib.escape(k)}</title></circle>')
                if k in ring:
                    col, sw, dash = RINGS[ring[k]]
                    da = f' stroke-dasharray="{dash}"' if dash else ""
                    c.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{dot / 2 + 1.3:.1f}" '
                          f'{lib.sonly(col)} stroke-width="{sw}"{da}/>')
        y += max(rh, 44)
    c.line(x0, y, x1, y, accent="line", sw=1)
    y += 24
    y += c.legend(x0, y, [("box", a, lab) for _, a, lab in STATES], title="Fill", size=13)
    y += 10
    items_l = []
    for chk, (col, sw, dash) in RINGS.items():
        if errata[chk][0]:
            items_l.append(("line", col, f"ring: an entry checked “{chk}” ({errata[chk][1]} items)", dash))
    y += c.legend(x0, y, items_l, title="Ring", size=13)
    y += 30
    rows = [[chapter_name(h), f"{v[0]:,}", f"{v[1]:,}" if v[1] else "none"]
            for h, v in chapters.items()]
    hist_rows = [[str(dd) if dd is not None else "not below", f"{hist[dd]:,}"]
                 for dd in sorted(hist, key=lambda x: (x is None, x or 0))]
    y0 = y
    h1 = c.table(x0, y, [("Chapter", 220), ("Items", 140), ("Below a target", 180)], rows, size=12.5)
    h2 = c.table(x0 + 600, y0, [("Depth", 160), ("Items", 140)], hist_rows, size=12.5)
    h3 = c.table(x0 + 960, y0, [("State in the Lean", 420), ("Items", 140)],
                 [[lab, f"{counts[s]:,}"] for s, _, lab in STATES], size=12.5)
    y += max(h1, h2, h3) + 30
    c.para(x0, y, x1 - x0,
           "**What this does not say.** An item's place comes from the docstrings: an item no declaration names is not "
           "drawn, and one named by many is one mark. Depth counts direct uses between declarations, so it measures "
           "the Lean's route, not the paper's. A ring says an entry exists and how far it was checked, not that the "
           "item is wrong; only an entry checked “Lean” rests on a proof checked by Lean. The manuscript is not read.",
           size=13.5, color="muted")
    return c
