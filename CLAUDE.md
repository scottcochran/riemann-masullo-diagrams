# riemann-masullo-diagrams

Generated SVG posters of what riemann-masullo's Lean formalisation of Masullo's *The Music of the Primes* rests
on, read from riemann-masullo at a pinned commit and from a dependency file derived from it. The build fails when
the sources no longer say what a poster draws. `README.md` says what each poster shows, `diagrams/README.md` what
is checked, `PLAN.md` what is planned, decided and done. This repository is independent of riemann-masullo.

## Rules every change keeps

From `PLAN.md`, "Rules the design keeps". Read them there in full before changing a poster.

1. Every node is read from the files at build time. A poster's own words are marked as its own.
2. What is drawn is checked: each poster records what it expects as module-level literals, compared both ways.
3. The sources are pinned (`MASULLO_COMMIT`, `PAPER_SHA256`, `DEPS_SHA256` in `diagrams/src/rm.py`). Moving one is
   deliberate: bump, regenerate, fix what the checks report.
4. The output is deterministic, and CI fails on the first byte that differs.
5. The poster build builds no Lean. `diagrams/src/deps.json` is derived outside it (`tools/deps/README.md`).
6. Standard library only for the posters, on Python 3.12+.
7. The light page is the content's mean luminance (`diagrams/PAGE.md`).
8. An erratum is drawn with its Checked value and no stronger claim, beside the quoted "No entry has been reviewed
   by a specialist".
9. The manuscript is not quoted, and not read.
10. A cone is of the formalisation, not of the paper, and each poster says so.

And:

- **Never loosen a check.** Fix a failure by recording what the source now says, traced to a source line.
- **Never touch a published release or tag.** A wrong release gets a successor. The custodian (scottcochran)
  signs and pushes tags. Draft the message; don't push.
- **Stage files by name**, never a directory. Keep notes out of the tree.
- Run Python with `uv run`. The generator is `uv run python diagrams/gen-diagrams.py`. Any WARNING or ERROR is a
  failure. An exit of 1 with a NOTE means anchors moved: run it again, so that the links follow.
- The source is a sibling checkout, `../riemann-masullo`, or `RIEMANN_MASULLO`. CI's sparse checkout holds
  `comparator.json`, `Main.lean`, `ERRATA.md`, `paper/README.md` and `lean-toolchain` (`rm.READS`).
- To look at a poster in both themes: `tools/look.sh OUT_DIR diagrams/M1-*.svg` (headless Chrome).

## House style

As riemann-diagrams': plain and exact. Give numbers with what they count ("16 of the 21,342 declarations"), name
pins by name and value, and say what was not checked. No praise words, no hype. Commit subjects are
`<area>: <what changed>` or `Phase <n>: <poster>, <what it shows>`. The body says what moved and what the build now
checks.

## Skills

The method is the `proof-posters` plugin from riemann-diagrams, enabled by `.claude/settings.json` and configured
by `proof-posters.toml`.

| Skill | When |
|---|---|
| `proof-posters:moving-pins` | riemann-masullo moved; `MASULLO_COMMIT`, `PAPER_SHA256` or `DEPS_SHA256` fails |
| `proof-posters:extracting-lean-deps` | `diagrams/src/deps.json` must be rebuilt (`tools/deps/README.md`) |
| `proof-posters:recording-expectations` | a poster is added or changes what it reads, draws or says |
| `proof-posters:cutting-releases` | a release is due (PLAN.md, Phase 6) |
| `proof-posters:linking-posters` | posters are linked, a link lands on nothing, or a target is not framed when opened; `check-links.py` holds `[links]` in `proof-posters.toml` |

`proof-posters:linking-papers` does not apply: there is no bibliography to link, and no `[papers]` table.
