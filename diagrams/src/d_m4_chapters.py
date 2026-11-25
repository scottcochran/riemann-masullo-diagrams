"""M4: the formalisation by chapter, and which chapters use which.

One row per module directory of riemann-masullo's library: its modules, items, declarations, their state, the
items that deviate from the print, the printed claims kept, and the errata entries on its items; then the matrix of
direct uses between items, by directory. Each row links to that directory's chapter poster (C1 to C14, CA to CE,
L1), which draws it item by item.
"""
import collections

import draw
import items as I
import lib
import rm

ID = "M4"
SLUG = "chapters"

# directory -> (modules, items, declarations, open items, items resting on an open declaration, items deviating
# from the print, declarations keeping a printed claim, errata entries on its items)
TOTALS = {'Ch01_Introduction': (2, 9, 507, 0, 2, 6, 18, 18),
 'Ch02_AdelicTheta': (6, 58, 619, 0, 0, 21, 8, 20),
 'Ch03_IdelicZeta': (6, 86, 990, 0, 0, 44, 13, 7),
 'Ch04_PeriodicSchauderBases': (11, 90, 696, 0, 0, 42, 43, 17),
 'Ch05_ThetaZSpaces': (16, 79, 1842, 1, 1, 41, 85, 88),
 'Ch06_LocalGlobal': (6, 27, 540, 0, 1, 13, 42, 40),
 'Ch07_SchauderBasesZeta': (14, 84, 1983, 2, 9, 51, 223, 125),
 'Ch08_PeriodicOrbits': (3, 11, 205, 0, 0, 5, 39, 5),
 'Ch09_HardySobolev': (6, 47, 437, 0, 0, 36, 18, 22),
 'Ch10_TraceSpectral': (18, 83, 1515, 5, 13, 50, 140, 88),
 'Ch11_ShellStructure': (14, 52, 993, 0, 3, 36, 65, 73),
 'Ch12_TraceGeometric': (10, 47, 558, 2, 5, 25, 56, 56),
 'Ch13_ZerosHecke': (3, 4, 61, 0, 1, 2, 4, 7),
 'Ch14_Complements': (1, 2, 58, 0, 0, 2, 0, 1),
 'AppA_AlgebraicNT': (10, 121, 747, 0, 0, 45, 30, 27),
 'AppB_AnalyticNT': (14, 119, 1304, 0, 0, 65, 98, 64),
 'AppC_LCTVS': (16, 190, 1197, 0, 0, 71, 22, 34),
 'AppD_SchwartzBruhat': (11, 144, 1634, 0, 0, 69, 19, 22),
 'AppE_TopologicalStacks': (2, 11, 47, 0, 0, 9, 0, 0),
 'ForMathlib': (199, 199, 1121, 1, 0, 1, 0, 0)}
# directory -> directory -> how many (item, item it uses directly) pairs go from the first to the second
MATRIX = {'Ch01_Introduction': {'Ch01_Introduction': 24,
                       'Ch02_AdelicTheta': 3,
                       'Ch03_IdelicZeta': 84,
                       'Ch04_PeriodicSchauderBases': 1,
                       'Ch05_ThetaZSpaces': 4,
                       'Ch06_LocalGlobal': 7,
                       'Ch07_SchauderBasesZeta': 1,
                       'Ch09_HardySobolev': 1,
                       'Ch10_TraceSpectral': 8,
                       'Ch12_TraceGeometric': 6,
                       'AppA_AlgebraicNT': 58,
                       'AppB_AnalyticNT': 38,
                       'AppC_LCTVS': 1,
                       'AppD_SchwartzBruhat': 36,
                       'ForMathlib': 17},
 'Ch02_AdelicTheta': {'Ch02_AdelicTheta': 175,
                      'Ch03_IdelicZeta': 20,
                      'AppA_AlgebraicNT': 149,
                      'AppC_LCTVS': 89,
                      'AppD_SchwartzBruhat': 268,
                      'ForMathlib': 47},
 'Ch03_IdelicZeta': {'Ch02_AdelicTheta': 100,
                     'Ch03_IdelicZeta': 662,
                     'Ch04_PeriodicSchauderBases': 1,
                     'Ch05_ThetaZSpaces': 3,
                     'Ch06_LocalGlobal': 2,
                     'Ch09_HardySobolev': 3,
                     'AppA_AlgebraicNT': 365,
                     'AppB_AnalyticNT': 17,
                     'AppC_LCTVS': 32,
                     'AppD_SchwartzBruhat': 131,
                     'ForMathlib': 117},
 'Ch04_PeriodicSchauderBases': {'Ch02_AdelicTheta': 18,
                                'Ch03_IdelicZeta': 14,
                                'Ch04_PeriodicSchauderBases': 338,
                                'AppA_AlgebraicNT': 15,
                                'AppB_AnalyticNT': 4,
                                'AppC_LCTVS': 160,
                                'AppD_SchwartzBruhat': 557,
                                'ForMathlib': 70},
 'Ch05_ThetaZSpaces': {'Ch02_AdelicTheta': 240,
                       'Ch03_IdelicZeta': 502,
                       'Ch04_PeriodicSchauderBases': 35,
                       'Ch05_ThetaZSpaces': 353,
                       'Ch07_SchauderBasesZeta': 2,
                       'Ch11_ShellStructure': 1,
                       'AppA_AlgebraicNT': 287,
                       'AppB_AnalyticNT': 7,
                       'AppC_LCTVS': 225,
                       'AppD_SchwartzBruhat': 482,
                       'ForMathlib': 99},
 'Ch06_LocalGlobal': {'Ch02_AdelicTheta': 91,
                      'Ch03_IdelicZeta': 157,
                      'Ch04_PeriodicSchauderBases': 7,
                      'Ch05_ThetaZSpaces': 73,
                      'Ch06_LocalGlobal': 40,
                      'AppA_AlgebraicNT': 119,
                      'AppB_AnalyticNT': 16,
                      'AppC_LCTVS': 62,
                      'AppD_SchwartzBruhat': 84,
                      'ForMathlib': 25},
 'Ch07_SchauderBasesZeta': {'Ch01_Introduction': 2,
                            'Ch02_AdelicTheta': 188,
                            'Ch03_IdelicZeta': 726,
                            'Ch04_PeriodicSchauderBases': 80,
                            'Ch05_ThetaZSpaces': 292,
                            'Ch06_LocalGlobal': 46,
                            'Ch07_SchauderBasesZeta': 453,
                            'Ch09_HardySobolev': 3,
                            'Ch10_TraceSpectral': 2,
                            'Ch12_TraceGeometric': 2,
                            'AppA_AlgebraicNT': 358,
                            'AppB_AnalyticNT': 67,
                            'AppC_LCTVS': 198,
                            'AppD_SchwartzBruhat': 303,
                            'ForMathlib': 98},
 'Ch08_PeriodicOrbits': {'Ch02_AdelicTheta': 12,
                         'Ch03_IdelicZeta': 15,
                         'Ch05_ThetaZSpaces': 22,
                         'Ch07_SchauderBasesZeta': 2,
                         'Ch08_PeriodicOrbits': 15,
                         'AppA_AlgebraicNT': 48,
                         'AppC_LCTVS': 11,
                         'AppD_SchwartzBruhat': 18,
                         'ForMathlib': 4},
 'Ch09_HardySobolev': {'Ch02_AdelicTheta': 20,
                       'Ch03_IdelicZeta': 18,
                       'Ch04_PeriodicSchauderBases': 10,
                       'Ch05_ThetaZSpaces': 1,
                       'Ch09_HardySobolev': 160,
                       'Ch12_TraceGeometric': 2,
                       'AppA_AlgebraicNT': 21,
                       'AppC_LCTVS': 46,
                       'AppD_SchwartzBruhat': 311,
                       'ForMathlib': 32},
 'Ch10_TraceSpectral': {'Ch01_Introduction': 10,
                        'Ch02_AdelicTheta': 140,
                        'Ch03_IdelicZeta': 223,
                        'Ch04_PeriodicSchauderBases': 34,
                        'Ch05_ThetaZSpaces': 56,
                        'Ch06_LocalGlobal': 60,
                        'Ch09_HardySobolev': 269,
                        'Ch10_TraceSpectral': 516,
                        'Ch11_ShellStructure': 1,
                        'Ch12_TraceGeometric': 4,
                        'AppA_AlgebraicNT': 267,
                        'AppB_AnalyticNT': 4,
                        'AppC_LCTVS': 199,
                        'AppD_SchwartzBruhat': 286,
                        'ForMathlib': 41},
 'Ch11_ShellStructure': {'Ch01_Introduction': 1,
                         'Ch02_AdelicTheta': 156,
                         'Ch03_IdelicZeta': 149,
                         'Ch04_PeriodicSchauderBases': 35,
                         'Ch05_ThetaZSpaces': 89,
                         'Ch06_LocalGlobal': 35,
                         'Ch07_SchauderBasesZeta': 42,
                         'Ch09_HardySobolev': 124,
                         'Ch10_TraceSpectral': 167,
                         'Ch11_ShellStructure': 188,
                         'Ch12_TraceGeometric': 15,
                         'AppA_AlgebraicNT': 264,
                         'AppB_AnalyticNT': 12,
                         'AppC_LCTVS': 81,
                         'AppD_SchwartzBruhat': 166,
                         'ForMathlib': 18},
 'Ch12_TraceGeometric': {'Ch01_Introduction': 2,
                         'Ch02_AdelicTheta': 37,
                         'Ch03_IdelicZeta': 82,
                         'Ch04_PeriodicSchauderBases': 3,
                         'Ch05_ThetaZSpaces': 8,
                         'Ch06_LocalGlobal': 13,
                         'Ch07_SchauderBasesZeta': 5,
                         'Ch09_HardySobolev': 30,
                         'Ch10_TraceSpectral': 87,
                         'Ch11_ShellStructure': 8,
                         'Ch12_TraceGeometric': 145,
                         'AppA_AlgebraicNT': 209,
                         'AppB_AnalyticNT': 14,
                         'AppC_LCTVS': 56,
                         'AppD_SchwartzBruhat': 157,
                         'ForMathlib': 35},
 'Ch13_ZerosHecke': {'Ch02_AdelicTheta': 2,
                     'Ch03_IdelicZeta': 9,
                     'Ch04_PeriodicSchauderBases': 1,
                     'Ch05_ThetaZSpaces': 1,
                     'Ch06_LocalGlobal': 3,
                     'Ch09_HardySobolev': 4,
                     'Ch10_TraceSpectral': 14,
                     'Ch12_TraceGeometric': 1,
                     'Ch13_ZerosHecke': 3,
                     'AppA_AlgebraicNT': 11,
                     'AppB_AnalyticNT': 5,
                     'AppC_LCTVS': 1,
                     'AppD_SchwartzBruhat': 14,
                     'ForMathlib': 5},
 'Ch14_Complements': {'Ch14_Complements': 1, 'ForMathlib': 3},
 'AppA_AlgebraicNT': {'Ch02_AdelicTheta': 8,
                      'Ch03_IdelicZeta': 5,
                      'Ch06_LocalGlobal': 1,
                      'Ch10_TraceSpectral': 3,
                      'Ch13_ZerosHecke': 2,
                      'AppA_AlgebraicNT': 560,
                      'AppD_SchwartzBruhat': 38,
                      'ForMathlib': 63},
 'AppB_AnalyticNT': {'Ch02_AdelicTheta': 22,
                     'Ch03_IdelicZeta': 299,
                     'Ch06_LocalGlobal': 1,
                     'Ch07_SchauderBasesZeta': 1,
                     'Ch10_TraceSpectral': 1,
                     'AppA_AlgebraicNT': 117,
                     'AppB_AnalyticNT': 349,
                     'AppC_LCTVS': 9,
                     'AppD_SchwartzBruhat': 153,
                     'ForMathlib': 80},
 'AppC_LCTVS': {'AppC_LCTVS': 809, 'AppD_SchwartzBruhat': 9, 'ForMathlib': 95},
 'AppD_SchwartzBruhat': {'Ch02_AdelicTheta': 18,
                         'Ch03_IdelicZeta': 15,
                         'Ch04_PeriodicSchauderBases': 15,
                         'Ch09_HardySobolev': 2,
                         'AppA_AlgebraicNT': 58,
                         'AppB_AnalyticNT': 4,
                         'AppC_LCTVS': 246,
                         'AppD_SchwartzBruhat': 1298,
                         'ForMathlib': 120},
 'AppE_TopologicalStacks': {'AppE_TopologicalStacks': 8},
 'ForMathlib': {'Ch01_Introduction': 2,
                'Ch03_IdelicZeta': 7,
                'Ch06_LocalGlobal': 1,
                'AppA_AlgebraicNT': 1,
                'AppB_AnalyticNT': 2,
                'AppC_LCTVS': 49,
                'AppD_SchwartzBruhat': 2,
                'ForMathlib': 56}}

W = 2400


def build():
    m = rm.load()
    X = I.load()
    chapters = sorted({it.chapter for it in X.items.values()}, key=rm.chapter_order)
    totals = {}
    for ch in chapters:
        its = X.chapter(ch)
        totals[ch] = (len({it.module for it in its}), len(its), sum(len(it.decls) for it in its),
                      sum(1 for it in its if it.state == "open"), sum(1 for it in its if it.state == "rests"),
                      sum(1 for it in its if it.deviations), sum(it.printed for it in its),
                      len({e for it in its for ids in it.errata.values() for e in ids}))
    rm.require("TOTALS", TOTALS, totals, "M4's table, and the subtitles of the chapter posters")
    matrix = {}
    for ch in chapters:
        cnt = collections.Counter(X.items[u].chapter for it in X.chapter(ch) for u in it.uses)
        if cnt:
            matrix[ch] = {k: cnt[k] for k in chapters if cnt[k]}
    rm.require("MATRIX", MATRIX, matrix, "M4's matrix")

    poster = {}
    for pid, f in lib.POSTERS.items():
        if pid[0] in "CL":
            poster_ch = next((ch for ch in chapters if f.startswith(f"{pid}-{ch.lower().replace('_', '-')}-")), None)
            if poster_ch:
                poster[poster_ch] = (pid, f)
    n_items = sum(v[1] for v in totals.values())
    c = lib.Canvas(
        ID, "The formalisation by chapter, and which chapters use which",
        f"riemann-masullo at {rm.SHORT}: {len(chapters)} module directories, {n_items:,} items, "
        f"{sum(v[2] for v in totals.values()):,} declarations, vendored code apart. Each row opens its chapter's poster, "
        f"item by item.", W, rm.sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += draw.nav(c, ID, y)
    y += c.para(x0, y, x1 - x0,
                "**How to read it.** The directories are the Lean's (`RiemannMasullo/Ch05_ThetaZSpaces/` and so on). "
                "An item is a paper item with the declarations that cite it and the helpers before them, as "
                "riemann-masullo's progress map groups them; in `ForMathlib` an item is a file. A use is what the "
                "elaborated terms reach at the pin. Errata entries were reported and checked by AI agents; in "
                "ERRATA.md's words, “No entry has been reviewed by a specialist.”", size=14.5, color="muted") + 26
    y += c.heading(x0, y, "1 · Each directory")
    cols = [("Directory", 470), ("Poster", 110), ("Modules", 120), ("Items", 110), ("Declarations", 150),
            ("Open items", 130), ("Items resting on an open one", 220), ("Items deviating from the print", 230),
            ("Printed claims kept", 180), ("Errata entries", 160)]
    rows = []
    for ch in chapters:
        v = totals[ch]
        pid, f = poster.get(ch, ("", ""))
        link = f"[[@{f}|{pid}]]" if f else "none"
        name = f"{rm.chapter_label(ch)} · `{ch}`" if rm.chapter_label(ch) != ch else f"`{ch}`"
        rows.append([f"[[@{f}|{name}]]" if f else name, link,
                     *[f"{n:,}" if n else "none" for n in v]])
    # an entry on items of two directories is counted in both rows, and once in the total
    n_entries = len({e for it in X.items.values() for ids in it.errata.values() for e in ids})
    rows.append({"cells": ["**All**", "", *[f"**{sum(v[k] for v in totals.values()):,}**" for k in range(7)],
                           f"**{n_entries:,}** distinct"], "accent": "grey"})
    y += c.table(x0, y, cols, rows, size=13)
    y += 40
    y += c.heading(x0, y, "2 · Which directories use which")
    y += c.para(x0, y, x1 - x0,
                "A cell counts the pairs (item of the row's directory, item it uses directly) whose second item is in "
                "the column's directory. The diagonal counts uses within a directory, the chapter posters' edges "
                "before the redundant ones are dropped. The columns are in the rows' order, by their short names.",
                size=13.5, color="muted") + 12

    def short(ch):
        lab = rm.chapter_label(ch)
        return lab.replace("Chapter ", "Ch ").replace("Appendix ", "App ") if lab != ch else "FML"

    lw = 250
    cw = (x1 - x0 - lw) / len(chapters)
    mcols = [("Uses →", lw)] + [(short(ch), cw) for ch in chapters]
    mrows = []
    for ch in chapters:
        r = matrix.get(ch, {})
        pid, f = poster.get(ch, ("", ""))
        mrows.append([f"[[@{f}|{rm.chapter_label(ch)}]]" if f else rm.chapter_label(ch)] + [(f"**{r[k]:,}**" if k == ch else f"{r[k]:,}") if r.get(k) else ""
                                                    for k in chapters])
    y += c.table(x0, y, mcols, mrows, size=12, hsize=12, pad=7)
    y += 34
    c.para(x0, y, x1 - x0,
           "**What this does not say.** The counts are of the Lean at the pin, read from riemann-masullo's compiled "
           "library; nothing was built or proved here. A count of errata entries says how many entries are on a "
           "directory's items, not how wrong a chapter is; each entry carries its own Checked value on the chapter "
           "poster.", size=13.5, color="muted")
    return c
