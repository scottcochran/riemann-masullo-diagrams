"""M2: the 28 steps with no known repair.

One row per row of ERRATA.md's "Where no repair is known yet", grouped by what the Lean shows of it:

- open, and named in Lean: each open declaration the row names, its cone (the declarations whose terms reach it)
  and the targets the cone reaches;
- open, with what the manuscript states precisely in files nothing imports: the same, and the check that no
  declaration outside those files uses it;
- open, and not stated in Lean: the row only, with the first sentence of what ERRATA.md says is missing;
- settled: how, in ERRATA.md's words, and what the declarations it names rest on, read from the terms.

Then the shortest chain from each open step that reaches a target up to the nearest target, and the open
declarations no open row names. Every value is compared with the sources, both ways.
"""
import re

import draw
import lib
import rm

ID = "M2"
SLUG = "no-repair"

# The rows, by their item as ERRATA.md prints it, -> what the poster expects of each. GAPS is recorded by hand:
# each open row -> the open declarations it names (in code), traced to the row's line, which the poster prints.
GAPS = {
    "Theorem 7.1.2.3, pp. 318, 322–323": [],
    "Theorem 7.3.3.4, pp. 360–363": [
        "private RiemannMasullo.Isolated.LogarithmicForm.circle_independent_power_separation",
        "private RiemannMasullo.Isolated.LogarithmicForm.positive_independent_power_separation",
        "private RiemannMasullo.baker_two_logarithms_not_liouville_of_independent",
        "private RiemannMasullo.sLocalPWOrbital_bases_bounded_interpolation_laurent_other_prime_shift_minima"],
    "Remark 10.2.1.5, p. 444, and Proposition 10.2.2.2, pp. 446–447": [
        "private RiemannMasullo.spectralStripJet_multiple_real_zeros_finite",
        "private RiemannMasullo.spectralStripJet_multiple_zero_bounded_height_representatives",
        "private RiemannMasullo.spectralStripJet_order_and_margin_multiplicity_bounded"],
    "Theorems 10.3.1.1(1) and 10.3.2.1(1), (10.3.1.23), (10.3.2.1), pp. 448, 452–455": [
        "RiemannMasullo.Isolated.spectralStripConvolution_finiteGram_bound",
        "private RiemannMasullo.spectralStripConvolution_traceCauchy_compact_block_series"],
    "Theorems 10.4.2.1, 10.4.2.2 and 10.4.2.8, pp. 459–464, and Theorem 10.4.3.5, pp. 471–473": [
        "RiemannMasullo.Isolated.spectralStripConvolution_hilbertSchmidt_of_le_one",
        "RiemannMasullo.Isolated.spectralStripGeometricKernel_blocks_bddAbove",
        "private RiemannMasullo.Isolated.ConvolutionFactorization.elementary_compact_convolution_factorization"],
    "(11.3.1.3)–(11.3.1.4), p. 494": [],
    "Proposition 12.2.2.2(2), p. 508, as used in Theorem 11.3.2.1, p. 495": [],
    "§12.3, p. 514": [],
    "Theorem 12.4.1.1, p. 515": [],
    "Theorem 12.4.1.1, pp. 515–517": [],
    "Theorem 12.5.1.1, (12.5.1.4), p. 520, with Definition 10.4.3.7, p. 473": [
        "RiemannMasullo.Isolated.exists_projectiveKernel_stripTestAction_spectralProjection"],
    "Theorem 12.5.1.1, pp. 519–520": ["RiemannMasullo.traceFormula_exteriorZeros"],
}
# open row -> its group: "targets" (a named step's cone reaches a target), "named" (a named step lies outside the
# files nothing imports), "isolated" (every named step, and its cone, lies in an _Isolated file), "unstated"
CLASSES = {
    "Theorem 7.1.2.3, pp. 318, 322–323": "unstated",
    "Theorem 7.3.3.4, pp. 360–363": "named",
    "Remark 10.2.1.5, p. 444, and Proposition 10.2.2.2, pp. 446–447": "named",
    "Theorems 10.3.1.1(1) and 10.3.2.1(1), (10.3.1.23), (10.3.2.1), pp. 448, 452–455": "named",
    "Theorems 10.4.2.1, 10.4.2.2 and 10.4.2.8, pp. 459–464, and Theorem 10.4.3.5, pp. 471–473": "isolated",
    "(11.3.1.3)–(11.3.1.4), p. 494": "unstated",
    "Proposition 12.2.2.2(2), p. 508, as used in Theorem 11.3.2.1, p. 495": "unstated",
    "§12.3, p. 514": "unstated",
    "Theorem 12.4.1.1, p. 515": "unstated",
    "Theorem 12.4.1.1, pp. 515–517": "unstated",
    "Theorem 12.5.1.1, (12.5.1.4), p. 520, with Definition 10.4.3.7, p. 473": "isolated",
    "Theorem 12.5.1.1, pp. 519–520": "targets",
}
# open declaration -> (its cone's size, the targets it reaches, whether the cone stays in _Isolated files)
CONES = {
    "private RiemannMasullo.Isolated.LogarithmicForm.circle_independent_power_separation": (3, 0, True),
    "private RiemannMasullo.Isolated.LogarithmicForm.positive_independent_power_separation": (1, 0, True),
    "private RiemannMasullo.baker_two_logarithms_not_liouville_of_independent": (8, 0, False),
    "private RiemannMasullo.sLocalPWOrbital_bases_bounded_interpolation_laurent_other_prime_shift_minima": (5, 0, False),
    "private RiemannMasullo.spectralStripJet_multiple_real_zeros_finite": (5, 0, False),
    "private RiemannMasullo.spectralStripJet_multiple_zero_bounded_height_representatives": (5, 0, False),
    "private RiemannMasullo.spectralStripJet_order_and_margin_multiplicity_bounded": (4, 0, False),
    "RiemannMasullo.Isolated.spectralStripConvolution_finiteGram_bound": (2, 0, True),
    "private RiemannMasullo.spectralStripConvolution_traceCauchy_compact_block_series": (92, 0, False),
    "RiemannMasullo.Isolated.spectralStripConvolution_hilbertSchmidt_of_le_one": (7, 0, True),
    "RiemannMasullo.Isolated.spectralStripGeometricKernel_blocks_bddAbove": (2, 0, True),
    "private RiemannMasullo.Isolated.ConvolutionFactorization.elementary_compact_convolution_factorization": (16, 0, True),
    "RiemannMasullo.Isolated.exists_projectiveKernel_stripTestAction_spectralProjection": (1, 0, True),
    "RiemannMasullo.traceFormula_exteriorZeros": (22, 7, False),
}
# settled row -> (how, as ERRATA.md says, {theorem "Steps since proved" names for it: the open declarations below})
SETTLED = {'Lemma 5.3.1.5, p. 242': ('from a published theorem',
                           {'RiemannMasullo.sLocalThetaPrincipalValue_isClosedEmbedding': ['private '
                                                                                           'RiemannMasullo.sLocalMellinSchwartzBounds_meyer_infinite_span_outside_real_profiles']}),
 'Proposition 11.2.0.1, p. 484, and Theorem 11.2.0.2, pp. 485–486': ('by another route',
                                                                     {'RiemannMasullo.orbitalMarkushevichBasis': [],
                                                                      'private RiemannMasullo.orbitalMarkushevichBasis_singleJet_denseSpan': [],
                                                                      'private RiemannMasullo.orbitalMarkushevichBasis_synthesis': []}),
 'Theorem 11.1.2.1(2)–(3), pp. 481–483': ('by another route',
                                          {'RiemannMasullo.sLocalCarvingLimit_eq_closedSpan': [],
                                           'RiemannMasullo.sLocalUncutCarving_lt': []}),
 'Theorem 5.2.1.1(1), p. 230': ('by another route',
                                {'RiemannMasullo.sLocalAdelicThetaSpace_strictLF': [],
                                 'RiemannMasullo.sLocalThetaToGlobal_isEmbedding': []}),
 'Theorem 5.4.1.1, (5.4.1.19)–(5.4.1.20), pp. 272–273': ('by another route',
                                                         {'RiemannMasullo.sLocalZetaPair_isEmbedding': [],
                                                          'RiemannMasullo.sLocalZetaPair_range': []}),
 'Theorem 6.3.2.1(1), (6.3.2.11)–(6.3.2.13), pp. 305–306': ('by another route',
                                                            {'RiemannMasullo.globalConverse_nontrivial': [],
                                                             'RiemannMasullo.globalConverse_normTwist': []}),
 'Theorem 6.3.2.1(1), p. 308': ('by another route',
                                {'RiemannMasullo.globalConverse_nontrivial': [],
                                 'RiemannMasullo.globalConverse_normTwist': []}),
 'Theorem 7.3.1.2(1), p. 341': ('by another route',
                                {'RiemannMasullo.sLocalOrbitalPrincipalValue_eq_poleBound': []}),
 'Theorem 7.3.1.6(2)–(3), pp. 345, 349–350': ('from another step of this list',
                                              {'RiemannMasullo.sLocalPWOrbital_biorthogonal_growth': ['private '
                                                                                                      'RiemannMasullo.sLocalMellinSchwartzBounds_meyer_infinite_span_outside_real_profiles']}),
 'Theorem 7.4.1.1(2), (7.4.1.2), pp. 366–367': ('by another route',
                                                {'RiemannMasullo.exists_spectralNuclearityBiorthogonal_vectors': [],
                                                 'RiemannMasullo.spectralNuclearity_trace': [],
                                                 'RiemannMasullo.spectralNuclearity_trace_of_jet_action': []}),
 'Theorem 7.4.2.1(2), p. 367': ('from another step of this list',
                                {'RiemannMasullo.finiteNuclearity_trace': ['private '
                                                                           'RiemannMasullo.sLocalMellinSchwartzBounds_meyer_infinite_span_outside_real_profiles']}),
 'Theorem 7.4.3.1(2)–(5), (7.4.3.11), pp. 371–372': ('by another route',
                                                     {'RiemannMasullo.archNuclearityMellin_range': [],
                                                      'RiemannMasullo.archNuclearityQuotient_jetEquiv': []}),
 'Theorem 7.5.0.1, pp. 376–378': ('by another route',
                                  {'private RiemannMasullo.strongCoprimality_exists_sub_mem': []}),
 'Theorems 10.2.1.1 and 10.2.2.1, pp. 441–443, 446': ('by another route',
                                                      {'RiemannMasullo.spectralLineMarkushevichBasis': [],
                                                       'RiemannMasullo.spectralStripJet_commonKernel': [],
                                                       'RiemannMasullo.spectralStripJet_denseInterpolants': [],
                                                       'RiemannMasullo.spectralStripMarkushevichBasis': []}),
 '§1.4.3, p. 29': ('from another step of this list',
                   {'RiemannMasullo.introTraceApprox_rat_spectral_tendsto_atBot': []}),
 '§1.4.5, pp. 29–30': ('from another step of this list',
                       {'RiemannMasullo.introTrace_combined_limit_extension': ['RiemannMasullo.traceFormula_exteriorZeros']})}
# the open declarations no open row names -> the ERRATA.md lines that name them in code
UNNAMED = {'private RiemannMasullo.sLocalMellinSchwartzBounds_meyer_infinite_span_outside_real_profiles': [164, 165, 179],
 'private RiemannMasullo.spectralLineJet_rational_critical_zero_count': []}
# the shortest chain from each open step that reaches a target, up to the nearest target
CHAINS = {'RiemannMasullo.traceFormula_exteriorZeros': ['RiemannMasullo.traceFormula_exteriorZeros',
                                               'RiemannMasullo.heckeL_zero_re_eq_half',
                                               'RiemannMasullo.LFunction_eq_zero_re_of_isPrimitive',
                                               'LFunction_eq_zero_re_of_isPrimitive']}

W = 2000
GROUPS = [("targets", "Open, named in Lean, and the targets rest on it", "red"),
          ("named", "Open, named in Lean; no target rests on it", "amber"),
          ("isolated", "Open; what the manuscript states precisely is in files nothing imports", "violet"),
          ("unstated", "Open, and not stated in Lean", "grey"),
          ("settled", "Settled in Lean, as ERRATA.md says", "teal")]


def first_sentence(text):
    """The first sentence of a cell; if it has TeX, which the posters do not typeset, the first sentence that has
    none, marked as abridged."""
    parts = re.split(r"(?<=[.])\s+(?=[A-Z(])", text.strip())
    if "$" not in parts[0]:
        return parts[0]
    plain = next((p for p in parts if "$" not in p and "**" not in p), None)
    return f"… {plain}" if plain else parts[0][:parts[0].index("$")].rstrip(" ,;:") + " …"


def short_list(names):
    return ", ".join(f"`{n}`" for n in names)


def build():
    m = rm.load()
    by_key = {d.key: d for d in m.decls}
    tset = {t.i for t in m.targets}
    keys = [r.key for r in m.rows]
    if len(set(keys)) != len(keys):
        raise ValueError("ERRATA.md: two rows now print the same item; M2 keys its rows by item")
    open_rows = [r for r in m.rows if not r.settled]

    def named_open(r):
        return sorted(d.key for n in r.names if (d := m.resolve(n)) is not None and d.open)

    rm.require("GAPS", GAPS, {r.key: named_open(r) for r in open_rows},
               "the open rows of ERRATA.md and the declarations each names; then their cards in M2")
    isolated_file = lambda d: d.module.endswith("_Isolated")
    cones = {}
    for k in sorted({k for v in GAPS.values() for k in v}):
        d = by_key[k]
        a = m.above(d.i)
        cones[k] = (len(a), len(a & tset), isolated_file(d) and all(isolated_file(m.decls[j]) for j in a))
    rm.require("CONES", CONES, cones, "the cone of each open step in M2, and M1 if it reaches a target")
    classes = {}
    for r in open_rows:
        ds = [by_key[k] for k in GAPS[r.key]]
        if not ds:
            classes[r.key] = "unstated"
        elif any(cones[d.key][1] for d in ds):
            classes[r.key] = "targets"
        elif all(cones[d.key][2] for d in ds):
            classes[r.key] = "isolated"
        else:
            classes[r.key] = "named"
    rm.require("CLASSES", CLASSES, classes, "the groups of M2")
    # ERRATA.md's own words for the groups: "For four of the twelve the missing step is named in Lean ... (one,
    # three and one). For two more ... The remaining six rows"
    intro = " ".join(m.errata_lines[rows_start(m):m.rows[0].line])
    said = re.search(r"For (\w+) of the (\w+) the missing step is named in Lean", intro)
    more = re.search(r"For (\w+) more \(", intro)
    rest = re.search(r"remaining (\w+) rows", intro)
    counts = re.search(r"statements that the targets do not use \((\w+), (\w+) and (\w+)\)", intro)
    if not (said and more and rest and counts):
        raise ValueError("ERRATA.md: the paragraph that sorts the open rows has changed; re-read M2's groups")
    stated = {"named": rm.number(said.group(1)), "isolated": rm.number(more.group(1)),
              "unstated": rm.number(rest.group(1))}
    got = {"named": sum(1 for v in classes.values() if v in ("targets", "named")),
           "isolated": sum(1 for v in classes.values() if v == "isolated"),
           "unstated": sum(1 for v in classes.values() if v == "unstated")}
    rm.require("ERRATA.md's sorting of the open rows", stated, got, "M2's groups against ERRATA.md lines 77–88")
    gaps_of = lambda r: [by_key[k] for k in GAPS[r.key] if by_key[k].gap and not isolated_file(by_key[k])]
    unused = [len(gaps_of(r)) for r in open_rows if classes[r.key] == "named"]
    rm.require("ERRATA.md's count of the statements the targets do not use",
               [rm.number(counts.group(k)) for k in (1, 2, 3)], unused,
               "the named rows of M2: their recorded gaps outside the _Isolated files")

    settled = {}
    for r in m.rows:
        if not r.settled:
            continue
        since = [s for s in m.since if set(s["entries"]) & set(r.entries)
                 and s["section"] != "Shown to be as strong as a target"]
        if not since:
            raise ValueError(f"ERRATA.md:{r.line}: the row says it is settled, and no row of “Steps since proved” "
                             f"shares its entries {r.entries}")
        below = {}
        for s in since:
            for n in s["names"]:
                d = m.resolve(n)
                if d is not None and d.kind == "theorem":
                    below[d.key] = [o.key for o in m.open_below(d.i)]
        settled[r.key] = (r.settled, dict(sorted(below.items())))
    rm.require("SETTLED", SETTLED, settled, "the settled rows of M2 against ERRATA.md's “Steps since proved”")
    named_anywhere = {k for v in GAPS.values() for k in v}
    unnamed = {}
    for d in m.opens:
        if d.key in named_anywhere:
            continue
        unnamed[d.key] = [i + 1 for i, ln in enumerate(m.errata_lines) if f"`{d.show}`" in ln]
    rm.require("UNNAMED", UNNAMED, unnamed, "M2's last band: the open declarations no open row names")
    chains = {}
    for k, (n, reach, _) in sorted(cones.items()):
        if reach:
            chains[k] = [d.key for d in m.chain(by_key[k].i, tset)]
    rm.require("CHAINS", CHAINS, chains, "M2's chain band")

    # -- drawing
    c = lib.Canvas(
        ID, "The steps with no known repair, and what the Lean shows of each",
        f"ERRATA.md at {rm.SHORT} lists {len(m.rows)} steps of the manuscript for which the agents that checked "
        f"them found no repair. It says {m.stated['settled']} have since been settled in Lean and "
        f"{m.stated['open']} are open. Each row here is one of them, with what the elaborated terms show.",
        W, rm.sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += draw.nav(c, ID, y)
    y += c.para(x0, y, x1 - x0,
                "**How to read it.** The first three columns are ERRATA.md's, quoted: the item and its pages, the "
                "entries of the errata the row gathers, and the first sentence of what it says is missing or how it "
                "was settled. The last is read from the Lean at the pin. A cone is every declaration whose "
                "terms reach an open step, directly or not; the targets are the seven theorems of comparator.json. "
                "The rows are the agents' assessment and their checking, not a specialist's: in ERRATA.md's words, "
                "“No entry has been reviewed by a specialist.”", size=14.5, color="muted")
    y += 30
    cols = [("Item, as ERRATA.md prints it", 420), ("Entries", 150), ("What ERRATA.md says (quoted)", 470),
            ("In the Lean, read from the terms at the pin", 848)]
    for gkey, glabel, acc in GROUPS:
        rows = [r for r in m.rows if (classes.get(r.key) == gkey if gkey != "settled" else r.settled)]
        if not rows:
            continue
        y += c.heading(x0, y, f"{glabel}: {len(rows)}", accent=acc)
        trs = []
        for r in rows:
            item = f"[[{acc}|{r.key}]] ({draw.to_url(m.errata_url(r.line), f'line {r.line}')})"
            if gkey == "settled":
                how, below = settled[r.key]
                said_txt = r.settled_text + "."
                opens = sorted({o for v in below.values() for o in v})
                lean = (f"Named as proved: {short_list(by_key[k].show for k in below)}. "
                        + ("Nothing open below any of them." if not opens else
                           "They rest on " + short_list(by_key[o].show for o in opens) + " and nothing else open."))
                trs.append({"cells": [item, ", ".join(r.entries), said_txt, lean], "anchor": f"row-{r.line}"})
                continue
            ds = [by_key[k] for k in GAPS[r.key]]
            if not ds:
                lean = "No open declaration is named: no declaration states the step."
            else:
                parts = []
                for d in ds:
                    n, reach, iso = cones[d.key]
                    kind = "gap" if d.gap else "classical input" if d.classical else "open"
                    card = draw.item_line(c, d)
                    s_ = f"`{d.show}` ({kind}{', ' + card[0][len('Item: '):] if card else ''}): cone {n}"
                    s_ += f", reaching {reach} of {len(m.targets)} targets" if reach else ", no target"
                    if iso:
                        s_ += ", all in `_Isolated` files"
                    parts.append(s_)
                lean = "; ".join(parts) + "."
            trs.append({"cells": [item, ", ".join(r.entries), first_sentence(r.missing), lean],
                        "anchor": f"row-{r.line}"})
        y += c.table(x0, y, cols, trs, size=12.5, hsize=12.5, accent=acc)
        y += 30

    # the chains
    for k, keys in sorted(chains.items()):
        y += c.heading(x0, y, f"From `{by_key[k].show}` to the nearest target: {len(keys)} declarations", accent="red")
        y += c.para(x0, y, x1 - x0, "The shortest chain of direct uses, the open step first. M1 draws its whole cone.",
                    size=13.5, color="muted") + 12
        y += draw.chain(c, x0, y, [by_key[q] for q in keys], lambda d: draw.accent_of(d, tset))
        y += 36

    # the open declarations no open row names
    y += c.heading(x0, y, f"Open declarations no open row names: {len(unnamed)}")
    y += c.para(x0, y, x1 - x0, f"The library has {len(m.opens)} open declarations. These are the ones not named in "
                "any open row above. Each is a published theorem the Lean takes as known (its docstring's "
                "`Classical input:` line, quoted), not a gap of the paper, and not checked by Lean.",
                size=13.5, color="muted") + 14
    for k, lines in unnamed.items():
        d = by_key[k]
        if not d.classical:
            raise ValueError(f"{d.show} is open, named by no open row, and not a classical input: re-read M2")
        where = (f"ERRATA.md names it on line{'s' if len(lines) > 1 else ''} {', '.join(map(str, lines))}"
                 if lines else "ERRATA.md does not name it")
        mark = draw.anchored(c, draw.m2_card(d))
        hh = c.card(x0, y, x1 - x0, f"`{d.show}`", [f"`{d.where}` · {where} · cone {len(m.above(d.i))}, "
                    f"reaching {len(m.above(d.i) & tset)} targets"] + draw.item_line(c, d), accent="grey", size=13,
                    tsize=14,
                    bullets=False, dash="6 4")
        c.blocks[-1] = c.blocks[-1][:4] + ("node " + d.name,)
        draw.close(c, mark, x0, y, x1 - x0, hh)
        y += hh + 8
        y += draw.quote(c, x0 + 16, y, x1 - x0 - 16, d.classical, size=13.5) + 16
    y += 20
    y += c.legend(x0, y, [("box", g[2], g[1]) for g in GROUPS], title="Groups", size=12.5)
    y += 30
    c.para(x0, y, x1 - x0,
           "**What this does not say.** Which open declaration a row names is read from the row's own text, and "
           "recorded by hand (GAPS) so that a change fails the build. A cone is a fact about the Lean at the pin; the "
           "paper's argument may lean on a step differently, since the Lean states repaired forms where the print "
           "is wrong. “Settled” is ERRATA.md's word: the terms show only what the named declarations rest on.",
           size=13.5, color="muted")
    return c


def rows_start(m):
    return next(i for i, ln in enumerate(m.errata_lines) if ln == "## Where no repair is known yet")
