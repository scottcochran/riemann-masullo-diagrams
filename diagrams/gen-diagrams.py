#!/usr/bin/env python3
"""Generate the riemann-masullo-diagrams posters (SVG, adaptive light/dark).

Each poster is a module diagrams/src/d_<id>_<slug>.py exposing ID, SLUG and build() -> Canvas. It reads
riemann-masullo at MASULLO_COMMIT and diagrams/src/deps.json through rm.load(), which first checks every pin
(diagrams/src/rm.py), and fails if the sources disagree with what the poster expects to draw. Output:
diagrams/<ID>-<slug>-<DATE>.svg, and diagrams/manifest.json, the registry of each poster's cards and arrows. Run
with no arguments for all, or with ids (M1 M2). Any line starting WARNING or ERROR is a failure, and the exit
status is 1. Standard library only. Use Python 3.12 or later: sum() over floats changed in 3.12, and with it the
coordinates.

    uv run python diagrams/gen-diagrams.py

The checkout of riemann-masullo is ../riemann-masullo, or the directory in RIEMANN_MASULLO.

Adapted from riemann-diagrams' generator at f87256e: no map set (PLAN.md, Open, 4), and so no second run to make
links between posters follow.
"""
import importlib
import json
import pathlib
import sys
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

import lib  # noqa: E402
from lib import DATE  # noqa: E402


def main(argv):
    if sys.version_info < (3, 12):
        sys.exit("gen-diagrams: Python 3.12 or later, so that the output is reproducible")
    want = {a.upper() for a in argv if not a.startswith("--")}
    manifest_path = HERE / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    lib.load_registry(manifest)
    failed = 0
    for name in sorted(p.stem for p in (HERE / "src").glob("d_*.py")):
        if want and name.split("_")[1].upper() not in want:
            continue
        lib.TEXT_BOXES.clear()
        try:
            m = importlib.import_module(name)
            canvas = m.build()
            svg = canvas.svg()
            ET.fromstring(svg)          # well-formed XML, or the poster is not written
        except Exception as e:  # report and carry on, so one broken module cannot block the rest
            print(f"ERROR {name}: {e}")
            failed += 1
            continue
        out = HERE / f"{m.ID}-{m.SLUG}-{DATE}.svg"
        stale = [p for p in HERE.glob(f"{m.ID}-*.svg") if p != out]
        for p in stale:             # a poster renamed or redated replaces its old file
            p.unlink()
        out.write_text(svg, encoding="utf-8")
        print(out.relative_to(HERE.parent))
        manifest[m.ID] = {"file": out.name, "title": canvas.title, **canvas.stats(), "anchors": sorted(canvas.anchors),
                          "links_ext": canvas.links_ext}
        for w in canvas.warnings:
            print("  WARNING", w)
            failed += 1
    if not failed:
        manifest = {k: manifest[k] for k in sorted(manifest, key=lambda k: (k[0], int(k[1:])))}
        manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
