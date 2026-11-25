# The dependency data: `diagrams/src/deps.json`

Every poster reads one derived file, `diagrams/src/deps.json`: for every user-written declaration of
riemann-masullo's library, `Statements.lean` and `Main.lean`, its kind, module, line, whether its term uses
`sorryAx`, its `Paper:`, `Gap:` and `Classical input:` lines, and the declarations its statement and its proof
use. It is written outside the poster build, at every move of `MASULLO_COMMIT`, by `build-deps.py` here, and
pinned by `DEPS_SHA256` in `diagrams/src/rm.py`. `meta.json` beside this file records what it was read from.

No Lean is compiled by this repository. The data is read by riemann-masullo's own `scripts/progress/Deps.lean`
(the program behind its progress page) from the compiled library, which comes from riemann-masullo's CI.

## At `72a10ff` (2026.11.25)

| | |
|---|---|
| Pin | `MASULLO_COMMIT` = `72a10ffc48c00276d45acb98b24a10816b253c54` (2026-11-24 19:17 −08:00), the head of `main` when read |
| Toolchain, Mathlib | `leanprover/lean4:v4.36.0`, Mathlib `fc4f59e577fe` (`lake-manifest.json`) |
| Compiled library | artifact `main-state` 14988454572 of riemann-masullo's "Main state" run 45538898020, built at `72a10ff` (incrementally, from the saved build of `3e154ab`). Zip 593 MB, `sha256:2e8ab5c3…`, which matched GitHub's digest; `build.tar.zst` `ad5c6d2c…`, 3.1 GB unpacked. The artifact expires after one day |
| Read | 587 modules (585 under `RiemannMasullo/`, then `Statements`, `Main`) in one call to `Deps.lean`: 46,003 constants, 29 MB, 69 s on an Apple-silicon laptop |
| Folded | 21,342 user declarations, 16 open; `deps.json` 7.2 MB, `DEPS_SHA256` = `1b9e9843…`. First folded as `de4b825b…`; folded again from the same raw export when the `Deviation:` lines were added (`92cbf6d7…`), and when the docstrings' descriptions were (14,909 of them), each time with the same declarations and edges |
| Repeated | the read twice, the fold five times: the raw export and `deps.json` byte-identical each time |
| Cross-check | riemann-masullo's own `Library` class (`build.py`) on the same rows: 21,329 declarations of the library (21,342 less the 13 of `Statements` and `Main`), 16 open, no notes |

## The runbook

1. **The checkout.** riemann-masullo at `MASULLO_COMMIT`, with no local changes to `RiemannMasullo/`,
   `Statements.lean`, `Main.lean` or `scripts/progress/` (the tool checks both).
2. **Mathlib's build.** In the checkout: `lake exe cache get`. About 5 GB into `.lake/packages/`, a few minutes.
3. **The library's build**, either of:
   - **The CI's saved build**, if the pin is a recent commit of `main`: its "Main state" run uploads `main-state`
     (the whole `.lake/build`) and keeps it one day.
     ```sh
     gh api 'repos/mccorvie/riemann-masullo/actions/artifacts?name=main-state&per_page=20' \
       --jq '.artifacts[] | [.id, .workflow_run.head_sha, .expired, .digest] | @tsv'
     gh api repos/mccorvie/riemann-masullo/actions/artifacts/<id>/zip > main-state.zip   # in an empty directory
     unzip main-state.zip                       # build.tar.zst, meta.json (its "sha" must be the pin)
     zstd -dc build.tar.zst | tar -tf - | grep -v '^build/'   # must print nothing
     zstd -dc build.tar.zst | tar -xf - -C <checkout>/.lake
     ```
     Check the zip against the artifact's `digest` first.
   - **A build**, otherwise: `lake build RiemannMasullo Main` in the checkout. Not timed here; riemann-masullo's
     CI builds it from scratch in just under an hour (its `main_state.yml`).
4. **Read and fold.**
   ```sh
   uv run python tools/deps/build-deps.py --checkout ../riemann-masullo --data <data dir> \
     --artifact "<what step 3 used, with its digests>"
   ```
   `<data dir>` is outside the repository; it receives `deps-raw.ndjson`, the sorted output of `Deps.lean`. The
   tool writes `diagrams/src/deps.json` and `tools/deps/meta.json` and prints the latter. `--fold-only` reuses the
   raw file.
5. **Pin it.** Set `DEPS_SHA256` in `diagrams/src/rm.py` to `meta.json`'s `deps_sha256`, regenerate, and record
   what each failing check now reads (proof-posters:moving-pins). Compare `decls` and `open` with the previous
   `meta.json` and explain a large swing from the upstream diff first.

## What the fold does, and where it could be wrong

- **Which constants are declarations** is riemann-masullo's rule (`build.py`, `Library._find_user_declarations`):
  a declaration keyword stands between the start of the constant's range and its name in the source. The rest
  (`_proof_n`, matchers, projections, anonymous instances) are folded into the declaration that owns them.
- **Open** means its term, or that of a constant it owns, names `sorryAx`. `build.py` prefers the build's
  `declaration uses sorry` warnings, which a saved build does not carry. At `72a10ff`, 16 declarations are open,
  and `grep` finds exactly 16 `sorry` in the library's source.
- **A `sorryAx` in a constant no declaration owns** would be lost by the fold; the tool stops if it finds one.
- **`Challenge.lean` is not read**: it declares the same seven root names as `Main.lean`, so the two cannot be
  loaded into one environment. comparator.json names the targets.
- **`RiemannMasulloClassField` is not read**: it is a separate library that `RiemannMasullo` does not import, and
  the saved build does not include it.
- **`Deviation:` lines** are kept for the 1,383 declarations whose docstring has a line starting with
  `Deviation:`. Six more docstrings use the word inside a sentence; they are not counted.
- **A docstring's description** (`summary`) is the paragraph after its `Paper:` reference, or from its start,
  cut at a blank line or at a line that opens a labelled part (`Deviation:`, `Gap:` …). A paragraph that is
  itself labelled gives none.
- **Vendored code** (`RiemannMasullo/External/`) is in the file, marked by its module. The posters count it apart
  and draw none of it (PLAN.md, Open, 3).
