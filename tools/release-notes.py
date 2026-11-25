#!/usr/bin/env python3
"""Write the notes of a release from the tag, the pins and the manifest.

    python3 tools/release-notes.py TAG pins.json diagrams/manifest.json > notes.md

The notes carry what a reader needs to check a citation of a poster (PLAN.md, Phase 6): the tag message, which
opens with the kind of move; the pins, with a link to the riemann-masullo commit; one row per poster with its card
and arrow counts, so that what moved between releases can be read without opening the SVGs; and the workflow run
that regenerated and checked the posters at the tag. Adapted from riemann-diagrams' tool of the same name at
f87256e. Standard library only.
"""
import json
import subprocess
import sys


def main(tag, pins_path, manifest_path):
    pins = json.load(open(pins_path, encoding="utf-8"))
    message = subprocess.run(["git", "tag", "-l", "--format=%(contents)", tag], capture_output=True,
                             text=True, check=True).stdout.strip()
    if not message:
        sys.exit(f"release-notes: {tag} has no message")
    ms = pins["masullo"]
    out = [message, ""]
    out.append("## The sources")
    out.append("")
    out.append("| Pin | Value |")
    out.append("|---|---|")
    out.append(f"| riemann-masullo, everything is read from it (`MASULLO_COMMIT`) | [{ms['commit'][:10]}]({ms['url']}) |")
    out.append(f"| The manuscript, as its `paper/README.md` states its hash (`PAPER_SHA256`) | `{pins['paper_sha256']}` |")
    out.append(f"| The dependency data, `diagrams/src/deps.json` (`DEPS_SHA256`) | `{pins['deps_sha256']}` |")
    out.append(f"| riemann-masullo-diagrams | `{tag}`, [{pins['generator']['commit'][:10]}]({pins['generator']['url']}) |")
    out.append("")
    out.append(f"Regenerated with Python {pins['python']}; the generator uses the standard library only. No Lean was "
               f"built: `deps.json` was read outside the build by riemann-masullo's own `scripts/progress/Deps.lean`, "
               f"as `tools/deps/README.md` at the tag says.")
    out.append("")
    out.append("## The posters")
    out.append("")
    out.append("| Id | Poster | Declaration cards | Arrows | File |")
    out.append("|---|---|---:|---:|---|")
    for k, v in json.load(open(manifest_path, encoding="utf-8")).items():
        title = v["title"].replace("|", "\\|")
        out.append(f"| {k} | {title} | {v['cards']} | {v['arrows']} | `{v['file']}` |")
    out.append("")
    out.append("## Checking a citation")
    out.append("")
    out.append("`SHA256SUMS` covers every asset. A poster's state line, at its foot, names the same riemann-masullo "
               "commit as the table above. The posters are SVG only: every browser renders them.")
    out.append("")
    out.append(f"The posters were regenerated from the pinned sources and compared byte for byte with the tagged "
               f"commit in workflow run [{pins['run']['id']}]({pins['run']['url']}), which passed before this release "
               "was created.")
    out.append("")
    out.append("riemann-masullo-diagrams is independent of riemann-masullo and is not maintained by it. What the "
               "posters quote and draw from riemann-masullo is used under its Apache-2.0 licence; the manuscript is "
               "its author's and is neither read nor quoted (see `NOTICE`).")
    print("\n".join(out))


if __name__ == "__main__":
    main(*sys.argv[1:])
