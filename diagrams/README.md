# The posters, and what each checks

Each poster is a module `src/d_<id>_<slug>.py` with `ID`, `SLUG` and `build()`. It reads everything through
[`src/rm.py`](src/rm.py)'s `load()`, records what it expects the sources to say as module-level literals, and raises an error,
with both values and what to re-read, when they say otherwise. [`gen-diagrams.py`](gen-diagrams.py) writes `<ID>-<slug>-<date>.svg`
and [`manifest.json`](manifest.json), parses every SVG as XML, and exits 1 on any `WARNING` or `ERROR`, and once, with a `NOTE`,
when a poster's anchors moved (see [Links](#links)).

| Poster | Shows | Reads |
|---|---|---|
| [M1](M1-floor-2026.11.25.svg) | what the seven targets rest on: the one open declaration below them, its cone up to the targets, the rest by chapter | comparator.json, Main.lean, ERRATA.md (the row of the floor, "Shown to be as strong as a target"), deps.json |
| [M2](M2-no-repair-2026.11.25.svg) | the 28 rows of "Where no repair is known yet", by what the Lean shows of each; the chain to the nearest target; the open declarations no row names | ERRATA.md (rows, its count of them, its sorting of the open rows, "Steps since proved"), deps.json |
| [M3](M3-depth-2026.11.25.svg) | the 1,251 paper items the docstrings name, by chapter and depth below the targets, with their state and their errata's Checked values | ERRATA.md (every entry), deps.json |
| [M4](M4-chapters-2026.11.25.svg) | the 20 module directories: their items, declarations, states, deviations, printed claims and errata, and which directories' items use which | ERRATA.md (every entry), deps.json |
| [M5](M5-refuted-2026.11.25.svg) | the 312 refutations `Printed.<name>_false`, what each rests on, the entries that name them, and their Checked values against ERRATA.md's rule for "Lean" | ERRATA.md (every entry, every column), deps.json |
| [C1](C1-ch01-introduction-2026.11.25.svg) to [C14](C14-ch14-complements-2026.11.25.svg), [CA](CA-appa-algebraicnt-2026.11.25.svg) to [CE](CE-appe-topologicalstacks-2026.11.25.svg), [L1](L1-formathlib-2026.11.25.svg) | one module directory each, item by item: a band per module, a card per item, with the items it uses and is used by | ERRATA.md (every entry), deps.json |
| [D1](D1-ch01-introduction-2026.11.25.svg) to [D14](D14-ch14-complements-2026.11.25.svg), [DA](DA-appa-algebraicnt-2026.11.25.svg) to [DE](DE-appe-topologicalstacks-2026.11.25.svg), [DL](DL-formathlib-2026.11.25.svg) | the same directories, declaration by declaration: every declaration of each item, with kind, file, line and state, and its `Deviation:` line quoted | deps.json |
| [B1](B1-bibliography-2026.11.25.svg) | the manuscript's bibliography, entry by entry, with a link to each work and the pages that cite it, each opening the card that covers it | transcription/README.md, transcription/chapters/ (the bibliography and every chapter), deps.json, src/papers.toml |

## What the build checks

Before any poster, `rm.load()`:

- the checkout is at `MASULLO_COMMIT`, with no local change to the files read;
- `paper/README.md` gives `PAPER_SHA256` and no other hash;
- `deps.json` has `DEPS_SHA256`, and it and [`tools/deps/meta.json`](../tools/deps/meta.json) were read at `MASULLO_COMMIT`;
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
| | `ERRATA_PAPERS` | a paper that an entry's row of ERRATA.md links, on a row's entries, appears, goes, moves to another address or to other entries |
| M3 | `N_ITEMS`, `EXPECTED_DEPTHS`, `COUNTS`, `CHAPTERS` | the items, their depths, states or chapters move |
| | `ERRATA`, `UNPLACED` | the entries placed on items, by Checked value, or those placed on none, move |
| M4 | `TOTALS` | a directory's modules, items, declarations, open or resting items, deviating items, printed claims or errata entries change in number |
| | `MATRIX` | the uses between two directories' items change in number |
| M5 | `REFUTED` | a refutation appears or goes, the entries that name it or their Checked values change, or what is open below it moves |
| | `SUMMARY`, `LEAN_UNNAMED` | the entries naming a refutation change by Checked value and state, or an entry checked "Lean" names none; and an entry checked "Lean" whose refutation rests on something open fails the build outright |
| | `ERRATA_PAPERS` | a paper that an entry's row of ERRATA.md links, on the entries naming a refutation, appears, goes, moves to another address or to other entries |
| C*, L1 | `ITEMS` | an item appears in, leaves or moves between the bands of the directory |
| | `EXPECTED` | an edge between two items of the directory appears or goes, after the redundant ones are dropped |
| | `OUTSIDE` | an item's direct uses of another directory's items change in number |
| | `STATES`, `DEVIATIONS`, `ERRATA` | an item's state, its count of deviating declarations, or the entries on it change |
| | `CITES` | the works the manuscript cites on an item's pages change |
| | `ERRATA_PAPERS` | a paper that an entry's row of ERRATA.md links, on the entries on an item, appears, goes, moves to another address or to other entries |
| B1 | `REFERENCES` | an entry of the bibliography appears, goes, or moves in the order printed |
| | `CITED`, `UNCITED` | a work is cited on other pages or chapters, or by no bracketed key |
| | `SP_TAGS` | the Stacks project's tags cited (`[SP, Tag 000B]`), or the pages citing one, change |
| | (papers.toml) | an entry has no id in the papers file, an id names no entry, or an entry lacks a url, a via, or the note `hand` and `none` need |
| D*, DL | `DECLS` | a declaration appears in, leaves or moves between items, or changes its place in its file |
| | `DEVIATING` | a declaration gains or loses its `Deviation:` line |
| | `OUTSIDE_ITEMS` | an item's direct uses of another directory's items change |

What is not checked: a quotation cut before a character the fonts lack is marked as abridged, and its name opens the
full text (one `Deviation:` line, which writes `⁻³ᐟ²`); the counts in [`README.md`](../README.md) and this file are written by hand, and no build compares them;
the page grey ([`PAGE.md`](PAGE.md)) is measured, not enforced; and M2's grouping of a row rests on the declarations the row
names in code, so a row that names its step only in prose is "not stated" here.

## Links

Every poster links to the others, so that a reader can follow an item from any poster to its card and to the source.

| From | To |
|---|---|
| Every poster | the overviews, M1 to M5, by the line under the title; M4 lists every chapter poster |
| A Lean name in code | its declaration's line in riemann-masullo at the pin |
| A chapter card's title | the item's first declaration at the pin |
| A chapter card's count of declarations, and of deviations | the item's table, and its quoted `Deviation:` lines, on the declarations poster |
| A declarations block's heading | the item's card on the chapter poster |
| A card's "Uses" and "Used by" | the cards they name, on the same poster |
| "From other directories" | the used item's card when it is one item; else that directory's row of the item's "Uses of other directories" on the declarations poster, whose items open their cards |
| An errata entry id, or a row's line | its line of ERRATA.md at the pin |
| A key in a card's "Its pages cite" | that work's row on B1 |
| A page in B1's "Where the text cites it" | the card on that chapter's poster whose `Paper:` pages cover it, the one with fewest pages where several do |
| A chapter in B1's "Where the text cites it" | that chapter's poster |
| A link in B1's Link column | the work, at the address `src/papers.toml` gives |
| A tag in B1's row of [SP] | that tag's page on the Stacks project, when it has a tag's form (four characters, digits and capital letters) |
| An arXiv number after an entry, or a card's "Papers the errata link" | the paper, at the address the entry's row of ERRATA.md gives (unversioned: arXiv opens its latest version) |
| "Printed claims kept" | that directory's part of M5 |
| An open or resting item | the row of M2 that names its open declaration (or that declaration's card on M2), and M1's card of the floor where the floor is below it |
| A declaration card on M1 or M2, a refutation on M5, a dot on M3 | the item's card on its chapter poster |
| A directory on M4, a row of M3 or M5, the line under a title | the poster's title block, `top` |

A card is an anchor (`i-<kind>-<number>`, from `items.anchor`); a declarations poster's blocks are `d-…` and their
deviations `v-…`; M5's directories are `refuted-<directory>`. Every link to a poster names a target on it, and the generator fails on one that does not. The target of a link
stands out when it is opened: each anchored group has an amber frame behind it, and each anchored table row (M2's
rows, `row-<line>`; the declarations posters' `o-<item>--<directory>`) is framed itself, hidden until the address names it (CSS `:target`), when it shows and
pulses three times. It works where a browser opens the SVG itself, as on the Pages site, from a release or from a
file; GitHub's file viewer shows an SVG as an image, without its links or this style, and a renderer without CSS
keeps the frame hidden. A link
to another poster is made only to an anchor the committed `manifest.json` lists, so a run that moves anchors
updates the manifest, prints a `NOTE` and exits 1, and a second run makes the links follow. `Canvas.check` fails the
build on a link to a poster, a card or an address that does not exist (an address must be at the pin, be a
paper an entry's row of ERRATA.md links, or be one of [`src/papers.toml`](src/papers.toml)), and the
generator fails on markup left unrendered.

## Kinds of text

Each sentence on a poster is one of four kinds: quoted (in italics, or a table column headed "quoted", from a file
the footer names; a chapter card's italic line is the first sentence of its first declaration's docstring, after the
`Paper:` reference, and is the Lean's, not the manuscript's), computed (a template filled at build time), framing (titles, keys, "How to read it", "What this
does not say"), or an interpretation, in an amber card headed as the poster's own and guarded by a check. M1 has
one interpretation, guarded by `FLOOR` and `AS_STRONG`, and M5 one, guarded by `SUMMARY` and `LEAN_UNNAMED`. B1's
entries are the bibliography's, as riemann-masullo's transcription prints them: a work's authors, title, venue
and year, drawn as bibliographic data under rule 9 ([PLAN.md](../PLAN.md)), not the manuscript's prose, which no poster quotes.

## Files

| File | What it is |
|---|---|
| [`gen-diagrams.py`](gen-diagrams.py) | the generator |
| [`src/rm.py`](src/rm.py) | the pins and the reader |
| [`src/draw.py`](src/draw.py) | the shared drawing: a declaration card, a layered graph, a chain, a quotation |
| [`src/items.py`](src/items.py) | the paper items: declarations grouped as the progress map groups them, their state, deviations, errata and uses, and the dropping of redundant edges |
| [`src/chapter.py`](src/chapter.py) | the chapter posters' layout and checks; each `src/d_c*.py` and [`src/d_l1_formathlib.py`](src/d_l1_formathlib.py) holds one directory's literals |
| [`src/paper.py`](src/paper.py) | the transcription of the manuscript: its bibliography, and where its text cites each entry |
| [`src/papers.toml`](src/papers.toml) | the link to each work of the bibliography, and how it was found, written by [`tools/link-papers.py`](../tools/link-papers.py) |
| [`src/declarations.py`](src/declarations.py) | the declarations posters' layout and checks; each `src/d_d*.py` holds one directory's literals |
| [`src/lib.py`](src/lib.py), [`src/metrics.py`](src/metrics.py), [`src/fonts/`](src/fonts/) | the drawing library, widths and fonts, from riemann-diagrams ([NOTICE](../NOTICE)) |
| [`src/deps.json`](src/deps.json) | the derived dependency data, pinned by `DEPS_SHA256` |
| [`PAGE.md`](PAGE.md) | the light page's grey, and its measurement |
| [`manifest.json`](manifest.json) | each poster's file, title, cards and arrows |
