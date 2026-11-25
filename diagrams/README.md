# The posters, and what each checks

Each poster is a module `src/d_<id>_<slug>.py` with `ID`, `SLUG` and `build()`. It reads everything through
`src/rm.py`'s `load()`, records what it expects the sources to say as module-level literals, and raises an error,
with both values and what to re-read, when they say otherwise. `gen-diagrams.py` writes `<ID>-<slug>-<date>.svg`
and `manifest.json`, parses every SVG as XML, and exits 1 on any `WARNING` or `ERROR`.

| Poster | Shows | Reads |
|---|---|---|
| [M1](M1-floor-2026.11.25.svg) | what the seven targets rest on: the one open declaration below them, its cone up to the targets, the rest by chapter | comparator.json, Main.lean, ERRATA.md (the row of the floor, "Shown to be as strong as a target"), deps.json |
| [M2](M2-no-repair-2026.11.25.svg) | the 28 rows of "Where no repair is known yet", by what the Lean shows of each; the chain to the nearest target; the open declarations no row names | ERRATA.md (rows, its count of them, its sorting of the open rows, "Steps since proved"), deps.json |
| [M3](M3-depth-2026.11.25.svg) | the 1,251 paper items the docstrings name, by chapter and depth below the targets, with their state and their errata's Checked values | ERRATA.md (every entry), deps.json |

## What the build checks

Before any poster, `rm.load()`:

- the checkout is at `MASULLO_COMMIT`, with no local change to the files read;
- `paper/README.md` gives `PAPER_SHA256` and no other hash;
- `deps.json` has `DEPS_SHA256`, and it and `tools/deps/meta.json` were read at `MASULLO_COMMIT`;
- `Main.lean` declares exactly the theorems comparator.json names, each closed;
- ERRATA.md's "Where no repair is known yet" has its four columns, and the rows read agree with the file's own
  sentence counting them ("Sixteen of the twenty-eight rows…", "The twelve that are still open").

Then each poster, against its literals:

| Poster | Expectation | Fails when |
|---|---|---|
| M1 | `TOTALS` | the declarations in deps.json, the open ones, their `Gap:` and `Classical input:` lines, or the vendored ones change in number |
| | `TARGETS` | comparator.json names other targets |
| | `FLOOR` | a target rests on another set of open declarations |
| | `N_BELOW` | the number of declarations, project or vendored, below a target changes |
| | `ROW` | the floor is named by another open row of ERRATA.md, or by none |
| | `CONE`, `EXPECTED` | a declaration or an edge appears in or leaves the floor's cone |
| | `BY_CHAPTER` | the closure's counts by chapter move |
| | `AS_STRONG` | "Shown to be as strong as a target" names other theorems, or one now rests on something open |
| M2 | `GAPS` | an open row names another set of open declarations (recorded by hand, each traced to the row's line) |
| | `CONES` | an open step's cone, the targets it reaches, or whether it stays in `_Isolated` files changes |
| | `CLASSES` | an open row moves between groups; also checked against ERRATA.md's own sorting ("For four of the twelve…", "For two more", "The remaining six", "(one, three and one)") |
| | `SETTLED` | a settled row's "Steps since proved" names other theorems, or what they rest on moves |
| | `UNNAMED` | another open declaration is named by no open row, or the lines naming one move; and each such must be a classical input |
| | `CHAINS` | the shortest chain from an open step to the nearest target changes |
| M3 | `N_ITEMS`, `EXPECTED_DEPTHS`, `COUNTS`, `CHAPTERS` | the items, their depths, states or chapters move |
| | `ERRATA`, `UNPLACED` | the entries placed on items, by Checked value, or those placed on none, move |

What is not checked: the counts in `README.md` and this file are written by hand, and no build compares them;
the page grey (`PAGE.md`) is measured, not enforced; and M2's grouping of a row rests on the declarations the row
names in code, so a row that names its step only in prose is "not stated" here.

## Kinds of text

Each sentence on a poster is one of four kinds: quoted (in italics, or a table column headed "quoted", from a file
the footer names), computed (a template filled at build time), framing (titles, keys, "How to read it", "What this
does not say"), or an interpretation, in an amber card headed as the poster's own and guarded by a check. M1 has
the one interpretation, guarded by `FLOOR` and `AS_STRONG`.

## Files

| File | What it is |
|---|---|
| `gen-diagrams.py` | the generator |
| `src/rm.py` | the pins and the reader |
| `src/draw.py` | the shared drawing: a declaration card, a layered graph, a chain, a quotation |
| `src/lib.py`, `src/metrics.py`, `src/fonts/` | the drawing library, widths and fonts, from riemann-diagrams (NOTICE) |
| `src/deps.json` | the derived dependency data, pinned by `DEPS_SHA256` |
| `PAGE.md` | the light page's grey, and its measurement |
| `manifest.json` | each poster's file, title, cards and arrows |
