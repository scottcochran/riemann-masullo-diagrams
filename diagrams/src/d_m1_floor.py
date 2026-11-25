"""M1: what the seven target theorems rest on.

For each theorem comparator.json names, the open declarations its terms reach (its floor); the one open
declaration under all seven, with its Gap: line and the errata row it stands for; every declaration between it
and the targets, as cards with the edges between them; and the rest of the targets' closure, by chapter.

Every value below is compared with what the sources say, both ways, and the build fails on a difference.
"""
import collections
import re

import draw
import lib
import rm

ID = "M1"
SLUG = "floor"

# What the build expects the sources to say at MASULLO_COMMIT. A change in any of these fails the build; set it
# to what the sources now say, traced to deps.json or ERRATA.md, and re-read the text it stands behind.
# the reader's totals: declarations in deps.json, of them open, with a Gap: line, with a Classical input: line, vendored
TOTALS = {"decls": 21342, "open": 16, "open_gap": 10, "open_classical": 6, "vendored": 4275}
TARGETS = ["riemannHypothesis", "riemannZeta_eq_zero_re", "LFunction_ne_zero_of_half_lt_re", "LFunction_eq_zero_re",
           "LFunction_eq_zero_re_of_isPrimitive", "dedekindZeta_zeros_re", "heckeLFunction_zeros_re"]
# target -> the open declarations below it
FLOOR = {'LFunction_eq_zero_re': ['RiemannMasullo.traceFormula_exteriorZeros'],
 'LFunction_eq_zero_re_of_isPrimitive': ['RiemannMasullo.traceFormula_exteriorZeros'],
 'LFunction_ne_zero_of_half_lt_re': ['RiemannMasullo.traceFormula_exteriorZeros'],
 'dedekindZeta_zeros_re': ['RiemannMasullo.traceFormula_exteriorZeros'],
 'heckeLFunction_zeros_re': ['RiemannMasullo.traceFormula_exteriorZeros'],
 'riemannHypothesis': ['RiemannMasullo.traceFormula_exteriorZeros'],
 'riemannZeta_eq_zero_re': ['RiemannMasullo.traceFormula_exteriorZeros']}
# target -> (declarations below it of the project, vendored declarations below it)
N_BELOW = {"riemannHypothesis": (1494, 0), "riemannZeta_eq_zero_re": (1494, 0),
           "LFunction_ne_zero_of_half_lt_re": (1497, 92), "LFunction_eq_zero_re": (1496, 92),
           "LFunction_eq_zero_re_of_isPrimitive": (1494, 92), "dedekindZeta_zeros_re": (1487, 0),
           "heckeLFunction_zeros_re": (1489, 0)}
# the ERRATA.md row each declaration of the floor stands for, by its item
ROW = {"RiemannMasullo.traceFormula_exteriorZeros": "Theorem 12.5.1.1, pp. 519–520"}
# every declaration whose terms reach the floor: the cone, up to and including the targets
CONE = ['LFunction_eq_zero_re',
 'LFunction_eq_zero_re_of_isPrimitive',
 'LFunction_ne_zero_of_half_lt_re',
 'RiemannMasullo.LFunction_eq_zero_re',
 'RiemannMasullo.LFunction_eq_zero_re_of_isPrimitive',
 'RiemannMasullo.LFunction_ne_zero_of_half_lt_re',
 'RiemannMasullo.dedekindZeta_zeros_re',
 'RiemannMasullo.heckeLFunction_zeros_re',
 'RiemannMasullo.heckeL_zero_re_eq_half',
 'RiemannMasullo.introTrace_characterTrace',
 'RiemannMasullo.introTrace_combined_limit_extension',
 'RiemannMasullo.introTrace_logDeriv_extension_of_limit',
 'RiemannMasullo.riemannHypothesis',
 'RiemannMasullo.riemannZeta_eq_zero_re',
 'RiemannMasullo.traceFormula',
 'dedekindZeta_zeros_re',
 'heckeLFunction_zeros_re',
 'private RiemannMasullo.introTrace_combined_limit_extension_analytic',
 'private RiemannMasullo.introTrace_combined_limit_extension_overlap',
 'private RiemannMasullo.introTrace_combined_overlap_of_exterior_cancellation',
 'riemannHypothesis',
 'riemannZeta_eq_zero_re']
# the edges drawn, (used, user), between the floor and the cone
EXPECTED = [('RiemannMasullo.LFunction_eq_zero_re', 'LFunction_eq_zero_re'),
 ('RiemannMasullo.LFunction_eq_zero_re', 'RiemannMasullo.LFunction_ne_zero_of_half_lt_re'),
 ('RiemannMasullo.LFunction_eq_zero_re_of_isPrimitive', 'LFunction_eq_zero_re_of_isPrimitive'),
 ('RiemannMasullo.LFunction_eq_zero_re_of_isPrimitive', 'RiemannMasullo.LFunction_eq_zero_re'),
 ('RiemannMasullo.LFunction_ne_zero_of_half_lt_re', 'LFunction_ne_zero_of_half_lt_re'),
 ('RiemannMasullo.dedekindZeta_zeros_re', 'RiemannMasullo.riemannZeta_eq_zero_re'),
 ('RiemannMasullo.dedekindZeta_zeros_re', 'dedekindZeta_zeros_re'),
 ('RiemannMasullo.heckeLFunction_zeros_re', 'heckeLFunction_zeros_re'),
 ('RiemannMasullo.heckeL_zero_re_eq_half', 'RiemannMasullo.LFunction_eq_zero_re_of_isPrimitive'),
 ('RiemannMasullo.heckeL_zero_re_eq_half', 'RiemannMasullo.dedekindZeta_zeros_re'),
 ('RiemannMasullo.heckeL_zero_re_eq_half', 'RiemannMasullo.heckeLFunction_zeros_re'),
 ('RiemannMasullo.introTrace_characterTrace', 'RiemannMasullo.introTrace_logDeriv_extension_of_limit'),
 ('RiemannMasullo.riemannHypothesis', 'riemannHypothesis'),
 ('RiemannMasullo.riemannZeta_eq_zero_re', 'RiemannMasullo.riemannHypothesis'),
 ('RiemannMasullo.riemannZeta_eq_zero_re', 'riemannZeta_eq_zero_re'),
 ('RiemannMasullo.traceFormula_exteriorZeros', 'RiemannMasullo.heckeL_zero_re_eq_half'),
 ('RiemannMasullo.traceFormula_exteriorZeros', 'RiemannMasullo.introTrace_characterTrace'),
 ('RiemannMasullo.traceFormula_exteriorZeros', 'RiemannMasullo.traceFormula'),
 ('RiemannMasullo.traceFormula_exteriorZeros',
  'private RiemannMasullo.introTrace_combined_limit_extension_overlap'),
 ('RiemannMasullo.traceFormula_exteriorZeros',
  'private RiemannMasullo.introTrace_combined_overlap_of_exterior_cancellation'),
 ('private RiemannMasullo.introTrace_combined_limit_extension_analytic',
  'RiemannMasullo.introTrace_combined_limit_extension'),
 ('private RiemannMasullo.introTrace_combined_overlap_of_exterior_cancellation',
  'RiemannMasullo.introTrace_combined_limit_extension'),
 ('private RiemannMasullo.introTrace_combined_overlap_of_exterior_cancellation',
  'private RiemannMasullo.introTrace_combined_limit_extension_analytic')]
# chapter -> (declarations below some target, of them below the floor's own statement, of them resting on the floor)
BY_CHAPTER = {"AppA_AlgebraicNT": (312, 308, 0), "AppC_LCTVS": (120, 120, 0), "AppD_SchwartzBruhat": (457, 457, 0),
              "Ch01_Introduction": (8, 0, 1), "Ch02_AdelicTheta": (136, 134, 0), "Ch03_IdelicZeta": (210, 157, 0),
              "Ch06_LocalGlobal": (2, 1, 0), "Ch09_HardySobolev": (1, 0, 0), "Ch10_TraceSpectral": (5, 2, 0),
              "Ch12_TraceGeometric": (30, 0, 0), "Ch13_ZerosHecke": (21, 0, 7), "ForMathlib": (205, 191, 0),
              "Statements": (6, 0, 0)}
# what ERRATA.md's "Shown to be as strong as a target" names, -> the open declarations below each
AS_STRONG = {"traceFormula_exteriorZeros_rat_iff_dirichletGRH": [],
             "introTrace_exterior_cancellation_iff_all_zeros_in_window": [],
             "introTrace_cofinal_exterior_cancellation_iff_critical_line": []}

W = 2000


def sentences_naming(text, name):
    """The sentences of `text` that name `name` in code, and the sentence after the last of them."""
    parts = re.split(r"(?<=[.])\s+(?=[A-Z])", text)
    hits = [k for k, s in enumerate(parts) if f"`{name}`" in s]
    if not hits:
        raise ValueError(f"ERRATA.md: the row no longer names `{name}`")
    return " ".join(parts[hits[0]:hits[-1] + 2])


def build():
    m = rm.load()
    totals = {"decls": len(m.decls), "open": len(m.opens), "open_gap": sum(1 for d in m.opens if d.gap),
              "open_classical": sum(1 for d in m.opens if d.classical and not d.gap),
              "vendored": sum(1 for d in m.decls if d.vendored)}
    rm.require("TOTALS", TOTALS, totals, "tools/deps/meta.json against the previous one, and M1's how-to-read")
    rm.require("TARGETS", TARGETS, m.target_names, "comparator.json and every band of M1")
    tset = {t.i for t in m.targets}
    floor = {t.show: [d.key for d in m.open_below(t.i)] for t in m.targets}
    rm.require("FLOOR", FLOOR, floor, "deps.json's open declarations, M1's title and band 2")
    n_below = {t.show: (sum(1 for j in m.below(t.i) if not m.decls[j].vendored),
                        sum(1 for j in m.below(t.i) if m.decls[j].vendored)) for t in m.targets}
    rm.require("N_BELOW", N_BELOW, n_below, "band 1")
    floor_decls = sorted({n for v in floor.values() for n in v})
    by_key = {d.key: d for d in m.decls}
    gaps = [by_key[n] for n in floor_decls]
    rows = {}
    for g in gaps:
        found = [r for r in m.rows if g.show in r.names and not r.settled]
        rows[g.key] = found[0].key if len(found) == 1 else [r.key for r in found]
    rm.require("ROW", ROW, rows, "ERRATA.md's rows that name the floor, and band 2")
    cone = set()
    for g in gaps:
        cone |= m.above(g.i)
    rm.require("CONE", CONE, sorted(m.decls[i].key for i in cone), "band 3, every card")
    drawn = cone | {g.i for g in gaps}
    edges = sorted((m.decls[a].key, m.decls[b].key) for b in drawn for a in m.deps[b] if a in drawn)
    rm.require("EXPECTED", EXPECTED, edges, "band 3, every arrow")
    union = set().union(*(m.below(t.i) for t in m.targets))
    under_floor = set().union(*(m.below(g.i) for g in gaps))
    by_ch = collections.defaultdict(lambda: [0, 0, 0])
    for j in sorted(union):
        d = m.decls[j]
        if d.vendored:
            continue
        v = by_ch[d.chapter]
        v[0] += 1
        v[1] += j in under_floor
        v[2] += j in cone
    rm.require("BY_CHAPTER", BY_CHAPTER, {k: tuple(v) for k, v in sorted(by_ch.items())}, "band 4")
    strong = {}
    for s in m.since:
        if s["section"] == "Shown to be as strong as a target":
            for n in s["names"]:
                d = m.resolve(n)
                if d and d.kind == "theorem":
                    strong[n] = [o.key for o in m.open_below(d.i)]
    rm.require("AS_STRONG", AS_STRONG, strong, "ERRATA.md, \"Shown to be as strong as a target\", and band 2")

    n_vendored = sum(1 for j in union if m.decls[j].vendored)
    vend_from = sorted({m.decls[j].module.split(".")[2] for j in union if m.decls[j].vendored})
    g = gaps[0]
    c = lib.Canvas(
        ID, "What the seven target theorems rest on",
        f"riemann-masullo at {rm.SHORT}: each of the {len(m.targets)} theorems comparator.json names rests in Lean "
        f"on {len(gaps)} open declaration, `{g.show}`, the recorded gap for {g.paper[0]}. Everything else below "
        f"them is proved. Read from the elaborated terms, not from the paper.",
        W, rm.sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += draw.nav(c, ID, y)
    h = c.para(x0, y, x1 - x0,
               f"**How to read it.** A declaration rests on another when its type or proof term names it, directly or "
               f"through other declarations: the closure riemann-masullo's own `scripts/progress/Deps.lean` reads "
               f"from the compiled library at {rm.SHORT}. An open declaration is one whose term uses `sorryAx`: "
               f"{sum(1 for d in m.decls if d.open)} of the {len(m.decls):,} declarations of the library, "
               f"`Statements.lean` and `Main.lean` are. This is a fact about the Lean. The Lean states repaired forms "
               f"where the print is wrong, so the paper's own argument may lean on the step differently.",
               size=14.5, color="muted")
    y += h + 30

    # band 1: the targets
    y += c.heading(x0, y, "1 · The seven targets, and what each rests on")
    cols = [("Target (comparator.json, Main.lean)", 430, {"mono": False}), ("Proved in Main.lean from", 430),
            ("Declarations below it", 230), ("Vendored, counted apart", 230), ("Open declarations below it", 560)]
    trs = []
    for t in m.targets:
        via = [m.decls[j] for j in m.deps[t.i] if m.decls[j].module != "Statements"]
        trs.append([f"`{t.show}`", ", ".join(f"`{d.where}`" for d in via), f"{n_below[t.show][0]:,}",
                    f"{n_below[t.show][1]:,}" if n_below[t.show][1] else "none",
                    ", ".join(f"`{by_key[n].show}`" for n in floor[t.show])])
    y += c.table(x0, y, cols, trs, size=13.5, accent="blue")
    y += 12
    y += c.para(x0, y, x1 - x0,
                f"Together they rest on {len(union) - n_vendored:,} declarations of the project and "
                f"{n_vendored} vendored ones ({', '.join(vend_from)}, under `RiemannMasullo/External/`), which are "
                f"counted here and not drawn. The permitted axioms are {', '.join(f'`{a}`' for a in m.axioms)} "
                f"(comparator.json).", size=13.5, color="muted")
    y += 34

    # band 2: the floor
    y += c.heading(x0, y, "2 · The one open declaration below them")
    row = next(r for r in m.rows if r.key == ROW[g.key])
    left_w = 900
    body = [f"`{g.where}`, at the pin", "Paper: " + draw.pages(g.paper),
            f"Its term uses `sorryAx`. Its statement rests on {len(m.below(g.i)):,} declarations, all proved; it has "
            f"no proof."] + draw.item_line(c, g)
    hl = c.card(x0, y, left_w, f"`{g.show}`", body, accent="red", dash="6 4", size=13.5, tsize=17, bullets=False)
    c.blocks[-1] = c.blocks[-1][:4] + ("node " + g.name,)
    yy = y + hl + 16
    yy += c.para(x0, yy, left_w, "Its docstring, `Gap:` line (Lean source, quoted):", size=13, color="faint", bold=True)
    yy += draw.quote(c, x0 + 14, yy, left_w - 14, g.gap)
    yy += 14
    yy += c.para(x0, yy, left_w, f"ERRATA.md, the row it stands for "
                 f"({draw.to_url(m.errata_url(row.line), f'line {row.line}')}, entries "
                 f"{', '.join(row.entries)}), quoted:", size=13, color="faint", bold=True)
    yy += draw.quote(c, x0 + 14, yy, left_w - 14, f"{row.item}. … {sentences_naming(row.missing, g.show)}")
    yy += 10
    yy += c.para(x0, yy, left_w, "ERRATA.md's rows and entries were reported and checked by AI agents, as that file "
                 "says. In its words: “No entry has been reviewed by a specialist.”", size=13, color="muted")
    rx = x0 + left_w + 40
    rw = x1 - rx
    ry = y
    ry += c.para(rx, ry, rw, "ERRATA.md, “Shown to be as strong as a target” (quoted, each proved with nothing "
                 "open below it):", size=13, color="faint", bold=True)
    for s in m.since:
        if s["section"] != "Shown to be as strong as a target":
            continue
        ry += 6
        ry += c.para(rx, ry, rw, f"**{s['item']}.**", size=13.5)
        ry += draw.quote(c, rx + 14, ry, rw - 14, s["proved"], size=13.5)
        ry += 6
    ry += 10
    # Guarded by FLOOR (one open step under every target) and AS_STRONG (the theorems named are proved, nothing open
    # below them). That the right side is the target's statement is ERRATA.md's reading: in the Lean it is a local
    # notation, which the dependency data cannot see, and the card says so.
    ih = c.card(rx, ry, rw, "Interpretation (this poster's own)",
                [f"Read with band 1: the one step under all seven targets is, over ℚ, shown as strong as one of "
                 f"them. That the right-hand side is the target's statement is ERRATA.md's reading: in "
                 f"`{m.resolve('traceFormula_exteriorZeros_rat_iff_dirichletGRH').where}` it is a local notation, "
                 f"which the dependency data cannot see."],
                accent="amber", size=13.5, tsize=14, bullets=False)
    ry += ih
    y = max(yy, ry) + 40

    # band 3: the cone
    y += c.heading(x0, y, f"3 · Everything that rests on it: {len(cone)} declarations, up to the targets")
    y += c.para(x0, y, x1 - x0, "An arrow runs from a declaration to one whose terms use it directly. The foot of "
                "the drawing is the open step; the top row is `Main.lean`.", size=13.5, color="muted") + 14
    layer = {}

    def lay(i):
        if i not in layer:
            ins = [j for j in m.deps[i] if j in drawn]
            layer[i] = 0 if not ins else 1 + max(lay(j) for j in ins)
        return layer[i]

    for i in sorted(drawn):
        lay(i)
    layers = [[m.decls[i] for i in sorted(drawn) if layer[i] == k] for k in range(max(layer.values()) + 1)]
    pairs = [(a, b) for b in sorted(drawn) for a in m.deps[b] if a in drawn]
    y += draw.layered(c, y, layers, pairs, lambda d: draw.accent_of(d, tset),
                      extra={d.i: draw.item_line(c, d) for L in layers for d in L})
    y += 26
    y += c.legend(x0, y, [("box", "red", "open: its term uses sorryAx", "6 4"),
                          ("box", "amber", "proved, and rests on the open step"),
                          ("box", "blue", "a target, in Main.lean"),
                          ("arrow", "muted", "used by")], title="Key")
    y += 40

    # band 4: by chapter
    y += c.heading(x0, y, "4 · Where the rest lies, by chapter")
    y += c.para(x0, y, x1 - x0,
                f"Of the {len(union) - n_vendored:,} declarations below a target, "
                f"{sum(v[1] for v in by_ch.values()):,} are below the open step's statement: what it is stated with. "
                f"The step has no proof term, so nothing its proof would use is counted.", size=13.5,
                color="muted") + 12
    cols = [("Chapter (module directory)", 520), ("Below a target", 300), ("Below the open step's statement", 400),
            ("Rest on the open step", 300)]
    trs = [[f"{rm.chapter_label(k)} · `{k}`", f"{v[0]:,}", f"{v[1]:,}", f"{v[2]:,}" if v[2] else "none"]
           for k, v in sorted(by_ch.items(), key=lambda kv: rm.chapter_order(kv[0]))]
    trs.append({"cells": ["**All**", f"**{sum(v[0] for v in by_ch.values()):,}**",
                          f"**{sum(v[1] for v in by_ch.values()):,}**", f"**{sum(v[2] for v in by_ch.values()):,}**"],
                "accent": "grey"})
    y += c.table(x0, y, cols, trs, size=13.5)
    y += 34
    y += c.para(x0, y, x1 - x0,
                "**What this does not say.** Nothing here was built or proved by this repository: the closure is read "
                "from riemann-masullo's compiled library at the pin, as its CI saved it. A card says where a "
                "declaration is and what it rests on, not that the mathematics is right. `Paper:` references are the "
                "Lean docstrings'; the manuscript itself is not read or quoted.", size=13.5, color="muted")
    return c
