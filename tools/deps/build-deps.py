#!/usr/bin/env python3
"""Write diagrams/src/deps.json, the dependency data every poster reads, and tools/deps/meta.json beside it.

    uv run python tools/deps/build-deps.py --checkout ../riemann-masullo --data DATA_DIR

Run outside the poster build, by hand, at every move of MASULLO_COMMIT; tools/deps/README.md is the runbook (how
the checkout gets its compiled library without building it, and the timings). Standard library only.

Two steps:

1. **Read.** `lake env lean --run scripts/progress/Deps.lean` in the checkout, with every module of
   `RiemannMasullo/` and the root modules `Statements` and `Main` as arguments, in one call, so that every edge
   between them is seen. `Deps.lean` is riemann-masullo's own program: for every constant of those modules it
   prints its kind, module, range, docstring, the project constants in its type and in its body, and whether its
   body names `sorryAx`. `Challenge` is not passed: it declares the same seven root names as `Main`, so the two
   cannot be loaded into one environment, and comparator.json names the targets. The output is saved, sorted, as
   DATA_DIR/deps-raw.ndjson (about 30 MB; kept outside the repository).
2. **Fold.** The constants are folded into the declarations a person wrote, by the rule of riemann-masullo's
   `scripts/progress/build.py` (`Library._find_user_declarations`, `_owners`, `_closure`, `_dependencies`),
   ported here: a constant is user-written when a declaration keyword stands between the start of its range and
   its name in the source file; every other constant (a `_proof_n`, a matcher, a projection, an anonymous
   instance) is owned by the nearest user declaration whose name is a prefix of its own, and edges are followed
   through what is owned or owned by no one. A declaration is open when its own term or the term of a constant
   it owns names `sorryAx` (build.py's `sorry_term`; build.py prefers the build's `declaration uses sorry`
   warnings, which a build cache does not carry, and cross-checks them against this).

The derived file holds, for every user declaration in name order: its name, kind, module, line, whether it is
open, its `Paper:` reference as printed, its `Gap:`, `Classical input:` and `Deviation:` text (each read from a
line that starts with it), its docstring in full where it is
open or has either line, and its statement and proof dependencies as indices into the list. `paper` is
`[item, first page, last page]`, read by build.py's `PAPER` pattern from the docstring's start. `summary` is the
docstring's own description, the paragraph after the `Paper:` reference (summary_of). Its SHA-256 is
DEPS_SHA256 in diagrams/src/rm.py; meta.json records the commit, toolchain and Mathlib revision it was read at,
and the hashes of what it was read from.
"""
import argparse
import collections
import hashlib
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = REPO / "diagrams" / "src" / "deps.json"
META = HERE / "meta.json"
LIB = "RiemannMasullo"
ROOTS = ["Statements", "Main"]

# As in riemann-masullo's scripts/progress/build.py.
KEYWORD = re.compile(r"\b(theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque|axiom)\b")
LINE = {"gap": re.compile(r"^Gap:\s*(.*?)(?=\n\s*\n|\n[A-Z][A-Za-z ]+:|\Z)", re.S | re.M),
        "classical": re.compile(r"^Classical input:\s*(.*?)(?=\n\s*\n|\n[A-Z][A-Za-z ]+:|\Z)", re.S | re.M),
        "deviation": re.compile(r"^Deviation:\s*(.*?)(?=\n\s*\n|\n[A-Z][A-Za-z ]+:|\Z)", re.S | re.M)}
PAPER = re.compile(r"Paper:\s*(.*?),?\s*pp?\.\s*(\d+)(?:\s*[-–]\s*(\d+))?\.?\s*", re.S)


def summary_of(doc, pm):
    """The docstring's own description: the paragraph after its `Paper:` reference (or from its start), cut at a
    blank line or at a line that opens a labelled part (`Deviation:`, `Gap:`, `Reconstruction:` …); none when the
    paragraph is itself labelled."""
    rest = doc[pm.end():] if pm else doc
    rest = re.split(r"\n\s*\n|\n(?=[A-Z][A-Za-z ]+:)", rest)[0]
    if re.match(r"[A-Z][A-Za-z ]+:", rest):
        return ""
    return " ".join(rest.split())


def die(msg):
    sys.exit(f"build-deps: {msg}")


def run(cmd, cwd):
    out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if out.returncode:
        die(f"{' '.join(cmd[:5])} failed:\n{(out.stdout + out.stderr)[-2000:]}")
    return out.stdout


def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def private_stripped(name):
    """`_private.Mod.Ule.0.Ns.foo` -> `Ns.foo` (build.py)."""
    if name.startswith("_private."):
        m = re.match(r"_private\..*?\.0\.(.*)$", name)
        if m:
            return m.group(1)
    return name


def read(checkout, data):
    files = sorted(p.relative_to(checkout).as_posix() for p in (checkout / LIB).rglob("*.lean"))
    modules = [f[:-5].replace("/", ".") for f in files] + ROOTS
    raw = run(["lake", "env", "lean", "--run", "scripts/progress/Deps.lean"] + modules, checkout)
    lines = sorted(ln for ln in raw.splitlines() if ln.startswith("{"))
    if not lines:
        die("Deps.lean printed nothing")
    (data / "deps-raw.ndjson").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return modules


def fold(checkout, rows):
    files = {f[:-5].replace("/", "."): f for f in
             sorted(p.relative_to(checkout).as_posix() for p in (checkout / LIB).rglob("*.lean"))}
    files.update({r: f"{r}.lean" for r in ROOTS})
    src = {}

    def lines(module):
        if module not in src:
            src[module] = (checkout / files[module]).read_text(encoding="utf-8").split("\n")
        return src[module]

    user = {}
    for name, r in rows.items():          # build.py, Library._find_user_declarations
        if "r" not in r or "sel" not in r:
            continue
        L = lines(r["m"])
        (l0, c0, _l1, _c1), (sl, sc) = r["r"], r["sel"]
        head = L[l0 - 1][c0:sc] if sl == l0 else "\n".join([L[l0 - 1][c0:]] + L[l0:sl - 1] + [L[sl - 1][:sc]])
        head = re.sub(r"/--.*?-/", "", head, flags=re.S)
        kws = KEYWORD.findall(head)
        if not kws:
            continue
        kw = kws[-1]
        kind = "theorem" if r["k"] == "theorem" else ("def" if kw in ("theorem", "lemma") else kw)
        user[name] = dict(kind=kind, module=r["m"], line=sl)
    owner = {}
    for name, r in rows.items():          # build.py, Library._owners
        if name in user:
            continue
        if r.get("of") in user:
            owner[name] = r["of"]
            continue
        for cand in (name, private_stripped(name)):
            parts = cand.split(".")
            found = next((".".join(parts[:i]) for i in range(len(parts) - 1, 0, -1) if ".".join(parts[:i]) in user),
                         None)
            if found:
                owner[name] = found
                break
    aux_of = collections.defaultdict(list)
    for aux, own in sorted(owner.items()):
        aux_of[own].append(aux)

    def closure(me, start):               # build.py, Library._closure
        found, seen, hidden, todo = set(), set(), False, list(start)
        while todo:
            c = todo.pop()
            if c in seen or c == me:
                continue
            seen.add(c)
            if c in user:
                found.add(c)
                continue
            r = rows.get(c)
            if r is None:
                continue
            own = owner.get(c)
            if own is not None and own != me:
                found.add(own)
                continue
            if r.get("s") and own is None:
                hidden = True
            todo.extend(r.get("t", []))
            todo.extend(r.get("v", []))
        return found, hidden

    names = sorted(user)
    index = {n: i for i, n in enumerate(names)}
    out, hidden_any = [], []
    for n in names:                       # build.py, Library._dependencies
        d, r = user[n], rows[n]
        stmt_start, proof_start = list(r.get("t", [])), []
        if d["kind"] == "theorem":
            proof_start = list(r.get("v", []))
        else:
            stmt_start += r.get("v", [])
            for aux in aux_of.get(n, []):
                if rows[aux]["k"] == "constructor":
                    stmt_start += rows[aux].get("t", [])
        stmt, h1 = closure(n, stmt_start)
        proof, h2 = closure(n, proof_start)
        if h1 or h2:
            hidden_any.append(n)
        is_open = bool(r.get("s")) or any(rows[a].get("s") for a in aux_of.get(n, []))
        doc = r.get("doc", "")
        e = {"n": n, "k": d["kind"], "m": d["module"], "l": d["line"]}
        if is_open:
            e["open"] = True
        pm = PAPER.match(doc)             # build.py, paper_item: the item as printed, and its first and last page
        if pm:
            e["paper"] = [" ".join(pm.group(1).split()), int(pm.group(2)), int(pm.group(3) or pm.group(2))]
        summary = summary_of(doc, pm)
        if summary:
            e["summary"] = summary
        for key, rx in LINE.items():
            m = rx.search(doc)
            if m:
                e[key] = " ".join(m.group(1).split())
        if is_open or "gap" in e or "classical" in e:
            e["doc"] = doc
        e["stmt"] = sorted(index[x] for x in stmt)
        e["proof"] = sorted(index[x] for x in proof - stmt)
        out.append(e)
    if hidden_any:
        die(f"a sorryAx in a constant no declaration owns, below {hidden_any[:5]}: the fold would lose it")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkout", required=True, type=pathlib.Path, help="riemann-masullo at MASULLO_COMMIT")
    ap.add_argument("--data", required=True, type=pathlib.Path, help="a directory outside the repository")
    ap.add_argument("--artifact", help="what the checkout's .lake/build came from, recorded in meta.json")
    ap.add_argument("--fold-only", action="store_true", help="reuse DATA/deps-raw.ndjson")
    a = ap.parse_args()
    checkout, data = a.checkout.resolve(), a.data.resolve()
    data.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(REPO / "diagrams" / "src"))
    import rm
    head = run(["git", "rev-parse", "HEAD"], checkout).strip()
    if head != rm.MASULLO_COMMIT:
        die(f"{checkout} is at {head}, MASULLO_COMMIT is {rm.MASULLO_COMMIT}")
    if run(["git", "status", "--porcelain", "--", LIB, *(f"{r}.lean" for r in ROOTS), "scripts/progress"],
           checkout).strip():
        die(f"{checkout} has local changes to the Lean source")
    if not a.fold_only:
        read(checkout, data)
    raw = data / "deps-raw.ndjson"
    rows = {}
    for ln in raw.read_text(encoding="utf-8").splitlines():
        r = json.loads(ln)
        rows[r["n"]] = r
    decls = fold(checkout, rows)
    text = json.dumps({"commit": head, "decls": decls}, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    OUT.write_text(text.replace('},{"', '},\n{"') + "\n", encoding="utf-8")
    manifest = json.loads((checkout / "lake-manifest.json").read_text(encoding="utf-8"))
    meta = {
        "masullo_commit": head,
        "toolchain": (checkout / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "mathlib_rev": next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"),
        "deps_lean_sha256": sha256(checkout / "scripts/progress/Deps.lean"),
        "build_from": a.artifact or "",
        "raw": {"constants": len(rows), "sha256": sha256(raw)},
        "decls": len(decls),
        "open": sum(1 for d in decls if d.get("open")),
        "deps_sha256": sha256(OUT),
    }
    META.write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
