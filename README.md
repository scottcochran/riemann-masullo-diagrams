# riemann-masullo-diagrams

**This repository is independent of [riemann-masullo](https://github.com/mccorvie/riemann-masullo) and is not
maintained by that project.**

Posters of what, in riemann-masullo's Lean formalisation of A. M. Masullo's *The Music of the Primes*, rests on
the steps no one knows how to repair: which declarations depend on each open step, how far up each reaches, and
which of the seven target theorems it reaches. Each poster is generated from riemann-masullo at a pinned commit,
`MASULLO_COMMIT` = `72a10ff` (2026-11-24), and its build fails when the sources no longer say what it draws.

The project's own progress page already draws, per section and declaration, what is stated, open and proved.
These posters draw what it does not: the cone of each open step across sections, the whole paper by depth below
the targets, and a fixed drawing that can be cited. `PLAN.md` says why, and what is planned and done.

## Posters

Open them on their own and zoom in. The latest release's posters are served at
https://scottcochran.github.io/riemann-masullo-diagrams/.

- [M1, what the seven target theorems rest on](diagrams/M1-floor-2026.11.25.svg). All seven rest in Lean on one
  open declaration, `traceFormula_exteriorZeros`, the recorded gap for Theorem 12.5.1.1. The poster draws it,
  its `Gap:` line and errata row, the 22 declarations that rest on it up to the targets, and the 1,513
  declarations below the targets by chapter.
- [M2, the steps with no known repair](diagrams/M2-no-repair-2026.11.25.svg). The 28 rows of ERRATA.md's "Where no
  repair is known yet", grouped by what the Lean shows of each:
  - 1 open row that the targets rest on;
  - 3 open rows named in Lean;
  - 2 open rows stated only in files nothing imports;
  - 6 open rows not stated in Lean;
  - 16 settled rows, each checked against what its named theorems rest on.

  It also draws the two open declarations that no row names.
- [M3, the paper by depth](diagrams/M3-depth-2026.11.25.svg). The 1,251 manuscript items that a `Paper:` line
  names, as marks by chapter and by depth below the targets, with their errata's Checked values. 188 are below a
  target; the other 1,063 are not reached from the targets at the pin.
- [M4, the formalisation by chapter](diagrams/M4-chapters-2026.11.25.svg). The 20 module directories, with their
  1,463 items and 17,054 declarations, the state of their items, their deviations from the print and their errata;
  and the matrix of which directories' items use which. Each row opens its chapter poster.
- [M5, the printed claims the Lean refutes](diagrams/M5-refuted-2026.11.25.svg). All 312 refutations
  (`Printed.<name>_false`), what each rests on, and the ERRATA.md entries that name them. Each of the 84 entries
  checked "Lean" names a refutation with nothing open below it, as ERRATA.md's rule asks.
- The chapter posters, one per module directory, item by item: the progress map's view of each section, pinned.
  Each module is a band and each paper item a card, with its declarations, state, deviations, errata, and the
  items it uses and is used by.
  - [C1](diagrams/C1-ch01-introduction-2026.11.25.svg) to [C14](diagrams/C14-ch14-complements-2026.11.25.svg),
    the chapters.
  - [CA](diagrams/CA-appa-algebraicnt-2026.11.25.svg) to [CE](diagrams/CE-appe-topologicalstacks-2026.11.25.svg),
    the appendices.
  - [L1](diagrams/L1-formathlib-2026.11.25.svg), `ForMathlib`, file by file.

  M4 links to every one of them.
- The declarations posters, D1 to D14, DA to DE and DL, one per directory: every one of the 17,054 declarations,
  item by item, with its kind, file, line and state, and the 1,383 `Deviation:` lines quoted. They expand the
  chapter cards: a card's count of declarations opens its item's table, and its count of deviations the quoted
  lines.

## What it is drawn from

| Source | What is read | Pinned by |
|---|---|---|
| riemann-masullo | `comparator.json`, `Main.lean`, `ERRATA.md`, `paper/README.md`, `lean-toolchain` | `MASULLO_COMMIT` |
| The manuscript | its hash only, as `paper/README.md` states it; never read | `PAPER_SHA256` |
| The dependency data | `diagrams/src/deps.json`: 21,342 declarations, what each uses, and their `Paper:`, `Gap:`, `Classical input:` and `Deviation:` lines, read by riemann-masullo's own `Deps.lean` from its compiled library, outside the build ([tools/deps/README.md](tools/deps/README.md)) | `DEPS_SHA256` |

The pins are in `diagrams/src/rm.py`. No Lean is built here. A dependency is what the elaborated terms reach: a
fact about the Lean, not about the paper. The errata are reported and checked by AI agents. In ERRATA.md's words,
"No entry has been reviewed by a specialist."

## Building

```sh
uv run python diagrams/gen-diagrams.py          # all posters; or: ... M1 M2
```

The generator expects riemann-masullo checked out at the pin in `../riemann-masullo`, or in the directory
`RIEMANN_MASULLO` names. Any `WARNING` or `ERROR` line is a failure. `diagrams/README.md` says what each poster
checks. `.github/workflows/posters.yml` regenerates them at the pin and fails on any byte that differs.

## Licence

Code under Apache-2.0, prose and posters under CC BY 4.0; what is quoted from riemann-masullo is under its
Apache-2.0 licence; the manuscript is its author's. See `NOTICE`.
