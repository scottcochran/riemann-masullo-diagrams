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

### Phase 2: M1, what the targets rest on

For each of the seven targets, the open declarations in its closure, grouped by chapter and section, each with
its `Gap:` line, its issue and the errata row it stands for where `ERRATA.md` names one. It is the counterpart of
`riemann-diagrams`' R1 band 5, and the floor under the targets. If the targets share most of their closure, one
poster draws the union and marks which target reaches what.

**Done when** M1 builds clean at the pin, its `EXPECTED` lists every open declaration below each target, and a
missing or extra one fails the build.

### Phase 3: CI

`.github/workflows/posters.yml`: sparse checkout of `riemann-masullo` at `MASULLO_COMMIT` (the files in the
table above), regenerate with Python 3.12, fail on a `WARNING`, an `ERROR` or a differing byte. Tested both ways,
as `riemann-diagrams`' Phase 2 was: a pin moved without regenerating fails, a regenerated pin passes.

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

### Phase 5: M3, the paper by depth

`riemann-diagrams`' F6 wheel for the 1,617 paper items (at `d37dfd7`): an item's depth is its distance below the
targets through the Lean. The marks are an item's state (proved, resting on something open, open) and its errata
with their Checked values. At this scale an item is a mark, not a card. Whether the wheel holds 1,617 legibly,
or a chapter per sector with items as ticks, is decided once Phase 1 gives the numbers.

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
