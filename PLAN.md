# Development plan

Written 2026.11.25, before anything is built. It is a plan, not a record: nothing below exists unless a done note
says so. It rests on two readings. The first is `riemann-diagrams`' write-up
`derived/riemann-diagrams-masullo-map-2026.11.23.md`, made at `mccorvie/riemann-masullo` `5c81fc0` and that
project's progress map from `d37dfd7`. The second is a reading of `riemann-masullo` at `3ac04f8` (2026-11-24
15:41 −08:00), a shallow clone with nothing built: `comparator.json`, `ERRATA.md`, `README.md`,
`paper/README.md`, `lakefile.toml`, `scripts/progress/build.py` and `Deps.lean`, and the workflow list. Counts
below say which reading they come from. None was recounted.

riemann-masullo-diagrams is independent of `mccorvie/riemann-masullo` and is not maintained by that project.

## Goal

Diagrams of what, in the Lean formalisation of Alessandro Maria Masullo's *The Music of the Primes*, rests on the
steps no one knows how to repair: which declarations depend on each recorded gap, how far up each dependency
reaches, and which of the seven target theorems it reaches. Every diagram is generated from `riemann-masullo` at
a pinned commit, and its build fails when the sources no longer say what the diagram draws.

What is not the goal: a second progress map. The project's map, refreshed about every 20 minutes, already draws
per section and per declaration what is stated, open and proved, the dependencies one step at a time, and the
errata by section. The posters here draw what it does not (`riemann-diagrams` write-up, F-9):

- **a cone per open step**: everything, across sections, that rests on one gap, up to the targets;
- **the whole by depth**: every paper item on one page, by its depth below the targets;
- **a fixed drawing**: dated, checksummed and released from a tag, so that it can be cited.

## What it is drawn from

| Source | What is read | Pinned by |
|---|---|---|
| `mccorvie/riemann-masullo` | `comparator.json`, `Main.lean`, `Statements.lean`, `Challenge.lean`, `ERRATA.md`, `lean-toolchain`, `lakefile.toml`, `lake-manifest.json`, `paper/README.md` | `MASULLO_COMMIT` |
| The manuscript, 940 pp., as mirrored in `paper/` | Its hash only. Item and page numbers come from the Lean's `Paper:` lines and from `ERRATA.md`. The build never reads the PDF | `PAPER_SHA256`, `e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5` |
| The dependency data: for every constant, its kind, module, range, docstring, the project constants in its type and in its body, and whether its body uses `sorryAx` directly | One derived file, written by the project's own `scripts/progress/Deps.lean` run at `MASULLO_COMMIT`, outside the build | `DEPS_SHA256`, and a `meta.json` holding the commit, toolchain and Mathlib revision it was read at |

At `3ac04f8`:

- **The targets.** `comparator.json` names seven theorems: `riemannHypothesis`, `riemannZeta_eq_zero_re`,
  `LFunction_ne_zero_of_half_lt_re`, `LFunction_eq_zero_re`, `LFunction_eq_zero_re_of_isPrimitive`,
  `dedekindZeta_zeros_re` and `heckeLFunction_zeros_re`. The permitted axioms are `propext`, `Quot.sound` and
  `Classical.choice`.
- **The 28 rows.** `ERRATA.md`, "Where no repair is known yet", has 28 rows. In its own words, 16 "have since
  been settled in Lean" and 12 are still open, each an issue labelled `open-problem` and listed in `#7349`.
- **Which open steps have Lean names.** Per the file: for 4 of the 12 the missing step is named in Lean.
  Theorem 12.5.1.1's cancellation, `traceFormula_exteriorZeros` (#5571), is the one "on which the target
  theorems rest in Lean". For 2 more, part of the step is stated in files that nothing imports. The remaining 6
  are steps the manuscript does not state precisely enough to formalise.
- **How a gap is recorded.** A named theorem left unproved, with a `Gap:` line in its docstring and an issue
  labelled `gap`. A statement false as printed is kept as `Printed.<name>`, with its refutation
  `Printed.<name>_false`.
- **The Checked column.** Each entry has one of *integrator*, *reviewed*, *Lean* or *reported*. "No entry has
  been reviewed by a specialist."

At `5c81fc0` and `d37dfd7` (the write-up, F-5 and F-6), and not recounted since: 17,204 declarations, 64,878
type edges and 57,799 body edges between them; 11,015 theorems of the project's own, 311 open; 1,617 paper items;
and 4,069 vendored theorems, kept apart.

## Rules the design keeps

1. **Every node is read from the files at build time.** A poster's own words are marked as its own; everything
   else is `riemann-masullo`'s, and a build fails rather than draw something stale.
2. **What is drawn is checked.** Each poster records what it expects as module-level literals: the gaps, the
   row each stands for, each cone's size and the targets it reaches. A source change is a failing check, never a
   silent redraw.
3. **The sources are pinned** (`MASULLO_COMMIT`, `PAPER_SHA256`, `DEPS_SHA256`). Moving one is deliberate: bump,
   regenerate, fix what the checks report, never loosen a check.
4. **The output is deterministic**, and CI fails on the first byte that differs.
5. **The poster build builds no Lean.** The dependency data is a derived file, written outside the build at the
   pin and pinned by its hash (the `proof-posters:extracting-lean-deps` method). A cone is what the elaborated
   terms reach. It is a fact about the Lean, not a claim about the mathematics, and every poster says so.
6. **Standard library only** for the posters, on Python 3.12+.
7. **The light page is the content's mean luminance**, as in `riemann-diagrams` (`diagrams/PAGE.md` there),
   measured again on this repository's first poster.
8. **An erratum is drawn with its Checked value and no stronger claim.** A poster that shows errata says, in a
   sentence of its own, that they were reported and checked by AI agents, and quotes "No entry has been reviewed
   by a specialist". Only an entry whose Checked value is *Lean* may be drawn as a refutation.
9. **The manuscript is not quoted.** Item numbers, page numbers, Lean names and `ERRATA.md`'s text may be
   (Apache-2.0, with the attribution in `NOTICE`); the paper's own sentences may not. The paper belongs to its
   author and is outside `riemann-masullo`'s licence (its `README.md`, "License").
10. **A cone is of the formalisation, not of the paper.** The Lean states repaired forms where the print is
    wrong, marked as deviations. So a cone shows what in the Lean rests on a gap; each poster says that the
    paper's own argument may lean on the step differently.

## What comes from riemann-diagrams

- **Copied, not imported:** `diagrams/src/lib.py` (from TOPAK, Apache-2.0, as its header says), `metrics.py`,
  and the Noto font subsets with `OFL.txt`. Taken at a named `riemann-diagrams` commit, recorded in `NOTICE`.
  A fix there does not reach here until it is copied again, on purpose.
- **The `proof-posters` plugin:** enabled through `.claude/settings.json` and configured by this repository's
  own `proof-posters.toml`. It provides `moving-pins`, `recording-expectations`, `extracting-lean-deps` and
  `cutting-releases`. `linking-papers` has nothing to do until a poster draws the bibliography.
- **The same discipline:** pins, recorded expectations, CI regenerating at the pins, releases from signed tags
  that the custodian pushes, and the house style of `riemann-diagrams`' `CLAUDE.md`.
- **Not carried over:** `bp.py`'s model, the twenty poster modules, `papers.toml` and `checks.toml`. The blueprint
  model does not fit: the data here is declarations and terms, about forty times as many declarations as the
  blueprint has statements.

## Phases

### Phase 0: the repository

`README.md` with the independence line at its top. `NOTICE`: Apache-2.0 for code and CC BY 4.0 for prose and
SVGs, as in `riemann-diagrams`; what is `riemann-masullo`'s; that the manuscript is its author's; and the fonts
under OFL. Also `LICENSE`, `LICENSE-DOCS`, `CLAUDE.md`, `proof-posters.toml`, `pyproject.toml`, and a pins
module in `diagrams/src/` holding `MASULLO_COMMIT`, `PAPER_SHA256` and `DEPS_SHA256`.

**Done when** `uv run python diagrams/gen-diagrams.py` runs against a checkout of `riemann-masullo` and fails,
naming the pin, when the checkout is at another commit.

**Done** (2026.11.25, not yet committed). `MASULLO_COMMIT` = `72a10ffc48c0` (2026-11-24 19:17 −08:00), the head of
`main` when read, and not the `3ac04f8` this plan was read at. A clone at its parent `3e154ab` fails each poster with
"MASULLO_COMMIT: … is at 3e154ab16098, the pin is 72a10ff". At the pin, a sparse checkout of the five files in
`rm.READS` builds clean. `lib.py`, `metrics.py`, the fonts, `build-fonts.py` and `measure-page.py` are copied
from riemann-diagrams at `f87256e` (NOTICE). Only `BRAND`, `DATE`, `HOME_ORDER` and the light page differ there.
The pins module is `diagrams/src/rm.py`, the reader too.

### Phase 1: the reader and the derived file

- **A runbook in `tools/deps/README.md`:** check out `riemann-masullo` at `MASULLO_COMMIT`, `lake exe cache
  get`, `lake build`, then `lake env lean --run scripts/progress/Deps.lean` over every module of
  `RiemannMasullo`, plus `Main` and `Challenge`. Their weekly full build allows 300 minutes on `ubuntu-latest`;
  the time on a laptop is not known.
  - `build.py` passes only library modules to `Deps.lean`, so whether `Main` and `Challenge` can be added to
    the same run is to be checked.
  - The JSON lines are sorted and written to `diagrams/src/deps.json`, compressed if large, with `meta.json`
    beside it.
- **A reader, `diagrams/src/rm.py`**, in place of `bp.py`, reading:
  - from the derived file: declarations, edges, the direct `sorryAx` flag, the `Paper:` references and `Gap:`
    lines in docstrings, and the `Printed.` namespace;
  - from `ERRATA.md`: the 28 rows (item, entries, open or settled, and how settled) and the entries by kind and
    Checked value;
  - from `Main.lean` and `comparator.json`: the seven targets.
- **Closures:** for each declaration, the open declarations it rests on, by transitive closure over type and
  body edges. Vendored code under `RiemannMasullo/External/` is left out, as the map leaves it out.

**Done when** the reader's totals are recorded as expectations and match, once, a progress map generated from
the same commit, with any difference explained in the done note; and two runs of the runbook at the pin give the
same file.

**Done** (2026.11.25, not yet committed). Open 1 is taken as the plan assumed: `Deps.lean` run at the pin. But the
compiled library came from riemann-masullo's own CI, not a local build: the `main-state` artifact of its "Main
state" run 45538898020 at `72a10ff` (593 MB, digest checked; kept one day). `lake exe cache get` gave Mathlib. The
read takes 69 s. Its 46,003 constants fold to 21,342 declarations, 16 of them open (`DEPS_SHA256` = `de4b825b…`).
The runbook is `tools/deps/README.md`, and the tool is `tools/deps/build-deps.py`. The read was run twice and the
fold five times, and both files were byte-identical each time.

Against the progress map: its own `Library` class from `scripts/progress/build.py`, run on the same rows, gives
21,329 declarations of the library and 16 open, with no notes. The fold is a port of that class. The 13 more here
are `Statements.lean`'s and `Main.lean`'s. The published page itself was not compared: it needs the issue tracker
and is replaced about every 20 minutes. `Main` and `Challenge` cannot share one run (same seven root names), so
`Main` and `Statements` are read and `Challenge` is not.

The counts from the write-up are stale at this pin. 311 open theorems at `d37dfd7` are 16 open declarations
here (`grep` finds 16 `sorry`), 10 with a `Gap:` line and 6 classical inputs. 17,204 declarations are 21,342.

### Phase 2: M1, what the targets rest on

For each of the seven targets, the open declarations in its closure, grouped by chapter and section, each with
its `Gap:` line, its issue and the errata row it stands for where `ERRATA.md` names one. It is the counterpart of
`riemann-diagrams`' R1 band 5, and the floor under the targets. If the targets share most of their closure, one
poster draws the union and marks which target reaches what.

**Done when** M1 builds clean at the pin, its `EXPECTED` lists every open declaration below each target, and a
missing or extra one fails the build.

**Done** (2026.11.25, not yet committed): `d_m1_floor.py`, `M1-floor-2026.11.25.svg`. Every target rests on one
open declaration, `traceFormula_exteriorZeros` (`FLOOR`), so one poster draws the union. Its cone is 22
declarations with 23 edges (`CONE`, `EXPECTED`), and the targets' closure is 1,513 project and 92 vendored
declarations (`N_BELOW`, `BY_CHAPTER`). A name taken from a row and an edge added, each in memory, fail the build
(`GAPS`, `CONE`).

### Phase 3: CI

`.github/workflows/posters.yml`: sparse checkout of `riemann-masullo` at `MASULLO_COMMIT` (the files in the
table above), regenerate with Python 3.12, fail on a `WARNING`, an `ERROR` or a differing byte. Tested both ways,
as `riemann-diagrams`' Phase 2 was: a pin moved without regenerating fails, a regenerated pin passes.

**Done** (2026.11.25, on `build-posters`, PR #1). Tested both ways on GitHub:

- **At the pin, it passes.** Run 45546522507, at `40ab580`, the first push with the workflow: every step passed,
  and the committed SVGs were byte-identical to the regenerated ones.
- **A moved pin, not regenerated, fails.** Run 45546651229, at `5883253`, which moves `MASULLO_COMMIT` to
  `3e154ab` and changes nothing else. It failed in "Regenerate the posters": each of M1, M2 and M3 printed
  `ERROR … deps.json was read at 72a10ffc48c0 (meta.json: 72a10ffc48c0), MASULLO_COMMIT is 3e154ab`.
- **The revert passes.** Run 45546722676, at `519d2fc`, which reverts that commit.

The test moved the pin, so the first check to stop it is the derived file's commit, not a poster's
expectations. The test commit and its revert were taken out of the branch afterwards, since together they change
nothing. `5883253` and `519d2fc` are no longer in its history, but the runs still show them. Locally, the outputs are also byte-identical on Python 3.12 and 3.14, and `determinism.py` passes.

### Phase 4: M2, the steps with no known repair

One band per row of the 28.

- **Open and named in Lean:** the gap's cone. Its size by chapter, the targets it reaches, and the shortest chain
  to the nearest target drawn as short cards.
- **Open, with part stated in a file nothing imports:** drawn with an empty cone, and a sentence of the
  poster's own saying why it is empty.
- **Open and not stated:** its row only, with `ERRATA.md`'s reason.
- **Settled:** how, in the file's four headings ("by another route", "from another step of this list", "from a
  published theorem", "shown to be as strong as a target").

The mapping from row to Lean names is recorded by hand as `GAPS` and traced to `ERRATA.md` lines; a row whose
names change fails the build. This is the step the write-up found missing (F-11). At `3ac04f8` the file names
the gaps for most open rows itself.

**Done when** M2 builds at the pin with every row in a band, each `GAPS` entry traced to a line of `ERRATA.md`,
and each cone's size and targets recorded.

**Done** (2026.11.25, not yet committed): `d_m2_no_repair.py`, `M2-no-repair-2026.11.25.svg`. The poster has one
table row per ERRATA row, in five groups: 1 the targets rest on, 3 named, 2 isolated, 6 not stated, 16 settled.
It prints each row's line in ERRATA.md. The groups are checked against ERRATA.md's own sorting sentence. For
each settled row, the theorems "Steps since proved" names are checked for what they rest on (`SETTLED`). The
11 rows settled by another route rest on nothing open. The 4 settled from another step rest on that step's open
declaration only, or on the classical input under it. Lemma 5.3.1.5 rests on Meyer's theorem only. Two open
declarations are named by no open row, both classical inputs (`UNNAMED`). The shortest chain from the floor to a
target has 4 declarations (`CHAINS`).

### Phase 5: M3, the paper by depth

`riemann-diagrams`' F6 wheel for the 1,617 paper items (at `d37dfd7`): an item's depth is its distance below the
targets through the Lean. The marks are an item's state (proved, resting on something open, open) and its errata
with their Checked values. At this scale an item is a mark, not a card. Whether the wheel holds 1,617 legibly,
or a chapter per sector with items as ticks, is decided once Phase 1 gives the numbers.

**Done** (2026.11.25, not yet committed): `d_m3_depth.py`, `M3-depth-2026.11.25.svg`. It is a grid, not a wheel:
chapters as rows, depth as columns (1 to 24, then "not below a target"), each item a dot. The numbers settled it:
188 of the 1,251 items (keyed as `build.py` keys them) are below a target, and 1,063 are not, since the floor has
no proof term. Fill is the item's state (7 open, 37 resting on an open declaration, 1,207 proved). The ring is the
most-checked erratum on the item: 696 entries are placed by the item numbers their "Where" names, and 53 name no
item a `Paper:` line names.

### Phase 6: releases

As in `riemann-diagrams`' Phase 5: an annotated, signed `vMAJOR.MINOR.PATCH` tag on `main`, pushed by the
custodian and never moved; a workflow that builds from the tag and publishes the SVGs, `pins.json` and
`SHA256SUMS`; a published release never edited; a wrong one gets a successor.

| Part | When it changes |
|---|---|
| MAJOR | What a poster is checked against changes: the rules above, or where the dependency data comes from |
| MINOR | A pin moves, or a poster is added or removed |
| PATCH | Layout, wording or library; every `EXPECTED` and `GAPS` unchanged |

The first release, `v0.1.0`, is M1 and M2 at one `MASULLO_COMMIT`, once CI holds them.

**Done** (2026.11.25): `.github/workflows/release.yml` and `tools/release-notes.py`, adapted from
riemann-diagrams' at `f87256e`. On a pushed tag, the workflow does four things:

1. It checks that the tag is the custodian's, `vMAJOR.MINOR.PATCH`, annotated, with a message, and on `main`.
2. It runs `posters.yml` on the tag.
3. It writes `pins.json`: the tag, `MASULLO_COMMIT`, `PAPER_SHA256`, `DEPS_SHA256`, the generator's commit, the
   Python version and the run.
4. It sums the SVGs and `pins.json` into `SHA256SUMS`, and creates the release with notes that open with the tag
   message.

There is no Pages site; the plan names none, and one needs a repository setting.

**`v0.1.0`**, the first release, MINOR: M1, M2 and M3 at `MASULLO_COMMIT` = `72a10ffc48c0`. M3 went out with the
first two, since it was built and CI held it.

- **The tag** is annotated and signed by the custodian, on `3ea625a` on `main`.
- **The run** is 45548560871. Its `tag`, `check / regenerate` and `release` jobs passed.
- **The release** has five assets: the three SVGs, `pins.json` and `SHA256SUMS`.
- **The checksums match the tree at the tag.** `verify-release.py v0.1.0` found the 3 SVGs in `SHA256SUMS`
  matching it, and `pins.json` naming the tag. No site was checked, since there is none.

**A Pages site, added after `v0.1.0`** (2026.11.25). The repository was made public, at the custodian's choice,
so that Pages can serve it. Pages is set to deploy from GitHub Actions, and the `github-pages` environment allows
`main` and tags matching `v*`. `.github/workflows/pages.yml` is adapted from riemann-diagrams'. It publishes one
release at a time to https://scottcochran.github.io/riemann-masullo-diagrams/: the release's SVGs, its
`pins.json`, and `diagrams/README.md` at the tag as the index. It first checks the files against the release's
`SHA256SUMS`, and after deploying it checks that the site's `pins.json` names the tag. `release.yml` calls it on
each new tag, and it can be run by hand for an existing one.

**First deployment.** `v0.1.0`, run by hand from `main` at `0a29ba9` (run 45549954393). Both the build and the
deploy job passed, and the deploy job's last step found `v0.1.0` in the site's `pins.json`. `verify-release.py
v0.1.0`, which now checks the site, passes: the 3 SVGs match the tree at the tag, and both the release's
`pins.json` and the site name `v0.1.0`. Each poster is served as `image/svg+xml`. M1 as served has the same SHA-256
as the file at the tag.

### Phase 7: the whole formalisation, item by item

Added 2026.11.25 at the custodian's request: draw as much of the formalisation as can be drawn and checked,
duplicating riemann-masullo's own progress map where that is the way to show it. This widens the goal above,
which set the progress map aside. The difference that stays is the pin: the progress map is redrawn about every 20
minutes; these posters are fixed at `MASULLO_COMMIT` and checked.

- **Chapter posters, one per module directory.** C1–C14 for the chapters, CA–CE for the appendices, and L1 for
  `ForMathlib`. Each module is a band and each paper item a card.
  - Items are grouped as the progress map groups them (`build.py`'s `group_items`): a helper joins the next item in
    its file. In `ForMathlib` each file is one item.
  - A card gives the item's pages, declarations, state, deviations from the print, printed claims, errata entries
    by Checked value, and the items of the chapter it uses and is used by.
  - Edges that another path already implies are dropped, and uses of other directories are counted.
  - The edges are given as text on the cards, not drawn: about 2 to 244 per chapter. Arrows would need routing, and
    text keeps every edge on the poster and checked.
- **M4**, the chapter map: every directory's totals, and the matrix of uses between directories. It links to each
  chapter poster.
- **M5**, the refutations: every `Printed.<name>_false`, what it rests on, and the entries that name it. It checks
  ERRATA.md's rule for the Checked value "Lean" against the terms.
- **The derived file** gains each declaration's `Deviation:` text, folded again at the same pin from the same raw
  export, so `DEPS_SHA256` moves while the declarations and edges stay.

**Done** (2026.11.25, PR #6, merged as `706e768`). The new posters are 22: M4, M5 and 20 chapter posters. There
are 1,463 items, 1,251 of them paper items, 199 `ForMathlib` files and 13 groups of helpers. M1 to M3 are
byte-identical after the re-fold. The derived file's `DEPS_SHA256` is now `92cbf6d7…`, and 1,383 declarations
carry a `Deviation:` line.

- **M5.** 305 of the 312 refutations rest on nothing open. The other 7 rest on the gap under Theorem 10.3.2.1(1),
  or on two of the classical inputs. Each of the 84 entries checked "Lean" names a refutation with nothing open
  below it. 96 entries checked "reviewed" also name one, which ERRATA.md's rule does not make a disagreement.
- **Checks.** A chapter poster fails when an item leaves its directory or an edge appears, each tried in memory on
  C5. `check-expectations.py` finds 147 literal expectations in 25 modules. `determinism.py` passes on 26 files.

**`v0.2.0`**, MINOR: the 22 posters added, and `DEPS_SHA256` moved. M1 to M3 are byte-identical to `v0.1.0`'s.

- **The tag** is annotated and signed by the custodian, on `706e768`.
- **The run** is 45552331752. All five jobs passed: tag, `check / regenerate`, release, and Pages' build and deploy.
  This is the first release that published the site.
- **The release** has 27 assets: the 25 SVGs, `pins.json` and `SHA256SUMS`.
- **The checksums match the tree at the tag.** `verify-release.py v0.2.0` found the 25 SVGs matching it, and
  `pins.json` and the site naming `v0.2.0`. Each SVG as the site serves it is byte-identical to the tag's.

### Links between the posters

Added 2026.11.25 at the custodian's request: every card, item, entry and poster links to where it is drawn in full
or to its source, as `diagrams/README.md`, "Links", lists. Every chapter card is an anchor. The generator runs twice
when anchors move, as riemann-diagrams' does, and the build fails on a link that does not resolve and on markup left
unrendered (the second caught 19 links set inside bold on M3).

**Done** (2026.11.25, on `links`, not yet merged). There are 12,219 links in the 25 posters: 3,547 within a poster,
5,574 to another poster's cards or to the poster itself, and 3,098 to riemann-masullo at the pin. Each of M3's 1,251
dots opens its item's card. The posters are byte-identical over two hash seeds after the second run. No expectation
changed.

### The declarations posters

Added 2026.11.25 at the custodian's request, so that a chapter card's counts open what they count. There is one
poster per directory: D1–D14, DA–DE, and DL for `ForMathlib`. Each item is a block in the chapter poster's order,
opened by the card: its count of declarations opens the item's table, and its count of deviations the quoted
`Deviation:` lines. A table gives every declaration with its kind, file, line and state. Each block's heading
opens the card.

- **Fonts.** The `Deviation:` lines needed six characters the subsets lacked (`ᵥᵢᵃᶻᴺ𝔭`). The subsets were rebuilt
  from the pinned Noto sources, each checked against its SHA-256, and no existing character's width changed.
  One more, `ᐟ` in `⁻³ᐟ²`, is in none of the four faces. That one quotation is cut before its sentence and marked
  as abridged, and its name opens the full text.
- **Size.** The 20 posters come to 31 MB. D7 is 62,346 px tall, one row for each of its 1,983 declarations. Every
  regeneration adds that much to the history, which a pin move makes worth weighing.

**Done** (2026.11.25, on `links`, not yet merged). The posters list 17,054 declarations and 1,383 `Deviation:`
lines (`DECLS`, `DEVIATING`). In memory on D8, a declaration leaving its item and a `Deviation:` line going each fail
the build. `check-expectations.py` finds 187 literal expectations in 45 modules. All 46 output files are
byte-identical over two hash seeds, and on Python 3.12 and 3.14.

### Showing a link's target

Added 2026.11.25 at the custodian's request. Every anchored group, 3,577 in all, now has a frame behind it: the
1,463 chapter cards, the 1,463 declaration blocks, the 634 deviation lists and the 17 directories of M5. The frame
is hidden until the address's `#fragment` names the group (CSS `:target`), then shows in amber and pulses three
times (`lib.py`'s `.rd-target`, `draw.close`). It was tried in headless Chrome on C5 at `#i-theorem-5.2.4.1` and on
D8 at `#v-eq-8.1.0.2`: the page scrolls to the target, and its frame shows. Those captures leave the part of the
page above the target unpainted. That comes from the capture, not the frame: the posters from before the frame
show the same, and a capture without a fragment is whole.

Then, at the custodian's report that the links to other chapters framed nothing, every link was given a target. A
chapter card's "From other directories" opens the used item's card when it uses one, and otherwise a row of a new
list on the declarations poster: "Uses of other directories", one anchored row per directory, naming the items
used, each opening its card. These lists are recorded as `OUTSIDE_ITEMS`, 13,136 uses. "Named on M2" opens M2's row
for the open declaration, or its card there, and "M1" opens M1's card of the floor. A link to a whole poster opens
its title block, `top`, which is framed too. The generator now fails on a link to a poster without a target.

There are 29,217 links with a target, and each target id exists (29,157 was counted here first, before
M4's 60 links to the chapter posters were given their target). A copy of D1 whose style frames the row
`#o-text-1.4.6--Ch03_IdelicZeta` by its id was rendered whole: the row shows its frame. A headless capture opened at
that address paints nothing, as before.

**`v0.3.0`**, MINOR: the 20 declarations posters added. The 25 posters of `v0.2.0` keep every expected list and gain
their links and frames. No pin moved.

- **The tag** is annotated and signed by the custodian, on `57a866a`.
- **The run** is 45563275862. All five jobs passed: tag, `check / regenerate`, release, and Pages' build and deploy.
- **The release** has 47 assets: the 45 SVGs, `pins.json` and `SHA256SUMS`.
- **The checksums match the tree at the tag.** `verify-release.py v0.3.0` found the 45 SVGs matching it, and
  `pins.json` and the site naming `v0.3.0`. Each SVG as the site serves it is byte-identical to the tag's. On the
  site, C8's link to `#d-eq-8.1.0.1` resolves on D8.
- **Counted at the tag** by the plugin's `check-links.py`: 29,217 links to an id (3,547 within a poster, 25,670 to
  another), 21,528 to riemann-masullo at the pin, 3,625 framed groups and 3,296 framed rows.

## Risks

- **The source moves fast.** At `5c81fc0` (2026.11.23) `ERRATA.md` marked none of its 28 rows settled; at
  `3ac04f8` (2026.11.24), 362 commits later, it marks 16. A poster is out of date within days, and each pin move re-records
  `GAPS` and every cone. That cost is the design; the date on each poster and the pin in its footer say which
  state it shows.
- **The derived file costs a build.** Hours, and a Mathlib cache, at every pin move. That cost argues for few
  deliberate moves, not for a source that cannot be pinned (Open, 1).
- **A drawing of errata looks like findings.** Rule 8 is the guard. A colour scale on errata counts reads as a
  verdict on the paper even when every entry is *reported*; M3 draws Checked values, not counts.
- **A cone of the Lean is read as a cone of the paper.** Rule 10, on the poster and not only here.
- **Scale.** About forty times as many declarations as `riemann-diagrams`' blueprint has statements, and about
  sixty times its 2,004 edges. No poster draws a declaration per card except along one chain.
- **The name.** "riemann-masullo-diagrams" can be taken for part of `riemann-masullo`. The README's first line
  says it is not, and no poster uses that project's name in a way that implies it endorses the poster
  (Apache-2.0, §6).

## Open

Decisions the plan raises and does not take. Each is the custodian's.

1. **Where the dependency data comes from.** Running `Deps.lean` at the pin (Phase 1), or keeping a copy of the
   data object of a progress map generated at a known commit, with its page hash, as the write-up did for
   `d37dfd7`. The second avoids a build, but the page is replaced about every 20 minutes and its generator is
   another moving part. The plan assumes the first.
2. **How often to move the pin.** Weekly, at a milestone (a row settled, a target proved), or by hand. A
   scheduled job that reports how far `riemann-masullo`'s head is past the pin, without failing, is an option.
3. **Vendored code.** Left out of every closure (the plan), or drawn apart. Leaving it out means no third-party
   notices to carry. Drawing it means carrying the `NOTICE` files of `AlgebraicNumberTheoryLean` and of the
   Fermat's Last Theorem project, and the MIT copyright lines of `Grh`, `ZetaLab` and `thatnealpatel-grh`.
4. **A map set.** Whether, as in `riemann-diagrams`, a second set quotes nothing but names and numbers, beside a
   reader set that quotes `ERRATA.md`.
5. **Whether to tell the `riemann-masullo` maintainer.** Apache-2.0 does not require it. It would settle
   whether these posters belong upstream as a view of that project's own data, which keeps one source of numbers.
