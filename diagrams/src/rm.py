"""The pins, and the reader every poster draws from.

Everything a poster shows is read here at build time from riemann-masullo at MASULLO_COMMIT, or from
diagrams/src/deps.json, the dependency data derived from it outside the build (tools/deps/README.md) and pinned by
DEPS_SHA256. Nothing the sources say is typed in. `load()` checks the pins before anything is read and raises
ValueError, naming the pin, when a checkout or a file is not what it pins.

What is read, and from where:

- **comparator.json**: the seven target theorems and the permitted axioms. Each target must be a theorem of
  `Main.lean` (in deps.json, module `Main`), and `Main` must declare nothing else.
- **paper/README.md**: the manuscript's SHA-256, which must equal PAPER_SHA256. The PDF itself is never read.
- **ERRATA.md**: the 28 rows of "Where no repair is known yet" (item, entries, what is missing, and whether and
  how the row says it was settled), the file's own count of settled and open rows, the tables of "Steps since
  proved" (what is proved, by name), and every entry of the entry tables with its Checked value.
- **deps.json**: every user-written declaration of `RiemannMasullo`, `Statements` and `Main`, with its kind,
  module, line, whether it is open (its term names `sorryAx`), its `Paper:` reference, its `Gap:` and `Classical
  input:` text, and its statement and proof dependencies.

A closure here is what the elaborated terms reach, at the pin. It is a fact about the Lean, not about the paper.
Standard library only.
"""
import collections
import hashlib
import json
import os
import pathlib
import re
import subprocess

import lib

MASULLO_COMMIT = "72a10ffc48c00276d45acb98b24a10816b253c54"
PAPER_SHA256 = "e039d3f6cf0a4b14f03c7edb85097752dd65c0a2fe543c76fe992be234f97bf5"
DEPS_SHA256 = "de4b825b53cb5d30bc2579e9b27946e8deeb1d1a28942b0e3140f9585b6c4138"

REPO = "mccorvie/riemann-masullo"
URL = f"https://github.com/{REPO}"
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DEPS = HERE / "deps.json"
META = ROOT / "tools" / "deps" / "meta.json"
CHECKOUT = pathlib.Path(os.environ.get("RIEMANN_MASULLO") or ROOT.parent / "riemann-masullo").resolve()
# The files the posters read from the checkout. CI's sparse checkout holds exactly these.
READS = ["comparator.json", "Main.lean", "ERRATA.md", "paper/README.md", "lean-toolchain"]
SHORT = MASULLO_COMMIT[:7]
LIB = "RiemannMasullo"
CHECKED = ("Lean", "reviewed", "integrator", "reported")      # ERRATA.md's Checked values, most checked first
SETTLED_KINDS = ("by another route", "from another step of this list", "from a published theorem")
WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                     "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def blob(path, line=None):
    return f"{URL}/blob/{MASULLO_COMMIT}/{path}" + (f"#L{line}" if line else "")


def number(word):
    """'twenty-eight' -> 28, 'Sixteen' -> 16."""
    w = word.lower()
    if w in WORDS:
        return WORDS[w]
    tens, _, unit = w.partition("-")
    if tens == "twenty" and unit in WORDS:
        return 20 + WORDS[unit]
    raise ValueError(f"ERRATA.md: cannot read the number {word!r}")


def display_name(name):
    """riemann-masullo's scripts/progress/build.py: `_private.Mod.0.RiemannMasullo.Ns.foo` -> `Ns.foo`."""
    m = re.match(r"_private\..*?\.0\.(.*)$", name)
    if m:
        name = m.group(1)
    return name[len(LIB) + 1:] if name.startswith(LIB + ".") else name


def chapter_of_module(module):
    """`RiemannMasullo.Ch12_TraceGeometric.Sec5` -> `Ch12_TraceGeometric`; the root modules are their own."""
    parts = module.split(".")
    return parts[1] if parts[0] == LIB and len(parts) > 1 else parts[0]


def chapter_label(key):
    """`Ch12_TraceGeometric` -> `Chapter 12`, `AppB_AnalyticNT` -> `Appendix B`, others as they are."""
    m = re.match(r"Ch(\d+)_", key)
    if m:
        return f"Chapter {int(m.group(1))}"
    m = re.match(r"App([A-E])_", key)
    if m:
        return f"Appendix {m.group(1)}"
    return key


def chapter_order(key):
    m = re.match(r"Ch(\d+)_", key)
    if m:
        return (0, int(m.group(1)), key)
    m = re.match(r"App([A-E])_", key)
    if m:
        return (1, ord(m.group(1)), key)
    return (2, 0, key)


ITEM_NUMBER = re.compile(r"(?:[A-E]|\d+)(?:\.\d+)+")       # build.py's NUMBER


def item_chapter(item):
    """The chapter a paper item is in, from its number: `Theorem 12.5.1.1` -> `12`, `Lemma A.2.3.4(2)` -> `A`."""
    m = ITEM_NUMBER.search(item)
    return m.group(0).split(".")[0] if m else None


def split_row(line):
    """A Markdown table row into cells, keeping escaped pipes (`\\|`) inside a cell."""
    cells = re.split(r"(?<!\\)\|", line.strip())
    return [c.strip().replace("\\|", "|") for c in cells[1:-1]]


def ticks(text):
    return re.findall(r"`([^`]+)`", text)


class Decl:
    __slots__ = ("i", "name", "show", "kind", "module", "line", "open", "paper", "gap", "classical", "doc",
                 "stmt", "proof", "chapter", "vendored", "path")

    def __init__(self, i, e):
        self.i, self.name, self.kind, self.module, self.line = i, e["n"], e["k"], e["m"], e["l"]
        self.show = display_name(self.name)
        self.open = bool(e.get("open"))
        self.paper = tuple(e["paper"]) if "paper" in e else None
        self.gap, self.classical, self.doc = e.get("gap"), e.get("classical"), e.get("doc")
        self.stmt, self.proof = e["stmt"], e["proof"]
        self.chapter = chapter_of_module(self.module)
        self.vendored = self.chapter == "External"
        self.path = self.module.replace(".", "/") + ".lean"

    @property
    def key(self):
        """How the posters' expectations name it: the Lean name, or `private <name>` for a private declaration,
        whose Lean name carries its module."""
        m = re.match(r"_private\..*?\.0\.(.*)$", self.name)
        return f"private {m.group(1)}" if m else self.name

    @property
    def url(self):
        return blob(self.path, self.line)

    @property
    def where(self):
        """`Ch12_TraceGeometric/Sec5.lean:98`."""
        p = self.path[len(LIB) + 1:] if self.path.startswith(LIB + "/") else self.path
        return f"{p}:{self.line}"


class Row:
    """One row of ERRATA.md's "Where no repair is known yet"."""

    def __init__(self, line, cells):
        self.line = line
        self.item, entries, self.missing, self.used = cells
        self.entries = [e.strip() for e in entries.split(",") if e.strip()]
        m = re.search(r"\*\*Since proved in Lean (" + "|".join(SETTLED_KINDS) + r")\b", self.missing)
        self.settled = m.group(1) if m else None
        b = re.search(r"\*\*(Since proved in Lean [^*]*?)(?::\s*see [^*]*)?\*\*", self.missing)
        self.settled_text = " ".join(b.group(1).split()) if b else None
        self.names = ticks(self.item + " " + self.missing)
        self.key = self.item.split(":")[0]          # the item and its pages, as the row prints them

    @property
    def state(self):
        return self.settled or "open"


class Model:
    def __init__(self):
        self.checkout = CHECKOUT
        self._check_pins()
        meta = json.loads(META.read_text(encoding="utf-8"))
        data = json.loads(DEPS.read_text(encoding="utf-8"))
        if data["commit"] != MASULLO_COMMIT or meta["masullo_commit"] != MASULLO_COMMIT:
            raise ValueError(f"deps.json was read at {data['commit'][:12]} (meta.json: {meta['masullo_commit'][:12]}), "
                             f"MASULLO_COMMIT is {SHORT}: rebuild it (tools/deps/README.md)")
        if meta["deps_sha256"] != DEPS_SHA256:
            raise ValueError("tools/deps/meta.json records another deps.json than DEPS_SHA256")
        self.meta = meta
        self.decls = [Decl(i, e) for i, e in enumerate(data["decls"])]
        self.by_name = {d.name: d for d in self.decls}
        self.by_show = collections.defaultdict(list)
        for d in self.decls:
            self.by_show[d.show].append(d)
        self.deps = [sorted(set(d.stmt) | set(d.proof)) for d in self.decls]
        users = collections.defaultdict(set)
        for d in self.decls:
            for j in self.deps[d.i]:
                users[j].add(d.i)
        self.users = {k: sorted(v) for k, v in users.items()}
        self._below, self._above = {}, {}
        self._read_comparator()
        self._read_errata()
        self.date = subprocess.run(["git", "log", "-1", "--format=%cs", MASULLO_COMMIT], cwd=self.checkout,
                                   capture_output=True, text=True, check=True).stdout.strip()

    # -- pins
    def _check_pins(self):
        if not (self.checkout / "comparator.json").exists():
            raise ValueError(f"no riemann-masullo checkout at {self.checkout}: set RIEMANN_MASULLO")
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.checkout, capture_output=True, text=True,
                              check=True).stdout.strip()
        if head != MASULLO_COMMIT:
            raise ValueError(f"MASULLO_COMMIT: {self.checkout} is at {head[:12]}, the pin is {SHORT}. Check out the "
                             f"pin, or move it (proof-posters:moving-pins)")
        dirty = subprocess.run(["git", "status", "--porcelain", "--", *READS], cwd=self.checkout,
                               capture_output=True, text=True, check=True).stdout.strip()
        if dirty:
            raise ValueError(f"MASULLO_COMMIT: the checkout has local changes to what the posters read:\n{dirty}")
        readme = self.read("paper/README.md")
        found = re.findall(r"sha256: `([0-9a-f]{64})`", readme)
        if found != [PAPER_SHA256]:
            raise ValueError(f"PAPER_SHA256: paper/README.md at {SHORT} gives {found}, the pin is {PAPER_SHA256[:12]}")
        got = hashlib.sha256(DEPS.read_bytes()).hexdigest()
        if got != DEPS_SHA256:
            raise ValueError(f"DEPS_SHA256: diagrams/src/deps.json has {got[:12]}, the pin is {DEPS_SHA256[:12]}")

    def read(self, path):
        return (self.checkout / path).read_text(encoding="utf-8")

    # -- comparator.json and Main.lean
    def _read_comparator(self):
        comp = json.loads(self.read("comparator.json"))
        self.target_names = list(comp["theorem_names"])
        self.axioms = list(comp["permitted_axioms"])
        main = [d for d in self.decls if d.module == comp["solution_module"]]
        names = sorted(d.name for d in main)
        if names != sorted(self.target_names):
            raise ValueError(f"comparator.json names {sorted(self.target_names)}, Main.lean declares {names}")
        self.targets = [self.by_name[n] for n in self.target_names]
        for t in self.targets:
            if t.kind != "theorem" or t.open:
                raise ValueError(f"target {t.name}: a {t.kind}{', open' if t.open else ''} in Main.lean")

    # -- ERRATA.md
    def _read_errata(self):
        text = self.read("ERRATA.md")
        lines = text.split("\n")
        self.errata_lines = lines
        heads = [(i, ln) for i, ln in enumerate(lines) if re.match(r"#+ ", ln)]   # not a wrapped "#7468, ..."

        def section(title, level="## "):
            starts = [i for i, ln in heads if ln == level + title]
            if len(starts) != 1:
                raise ValueError(f"ERRATA.md: {len(starts)} headings {level + title!r}")
            s = starts[0]
            e = next((i for i, ln in heads if i > s and len(ln) - len(ln.lstrip("#")) <= len(level) - 1), len(lines))
            return s, e

        s, e = section("Where no repair is known yet")
        self.rows = []
        header = None
        for i in range(s, e):
            ln = lines[i]
            if not ln.startswith("|"):
                continue
            cells = split_row(ln)
            if header is None:
                header = cells
                if header != ["Item", "Entries", "What is missing", "Used later on pp."]:
                    raise ValueError(f"ERRATA.md:{i + 1}: the rows' columns are now {header}")
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            self.rows.append(Row(i + 1, cells))
        intro = " ".join(lines[s:e])
        m = re.search(r"(\w+) of the ([\w-]+) rows have since been settled in Lean", intro)
        m2 = re.search(r"The (\w+) that are still open", intro)
        if not (m and m2):
            raise ValueError("ERRATA.md: the sentence counting the settled and open rows has changed")
        self.stated = {"settled": number(m.group(1)), "rows": number(m.group(2)), "open": number(m2.group(1))}
        n_settled = sum(1 for r in self.rows if r.settled)
        got = {"settled": n_settled, "rows": len(self.rows), "open": len(self.rows) - n_settled}
        if got != self.stated:
            raise ValueError(f"ERRATA.md says {self.stated} of its rows, the rows read give {got}")

        # "Steps since proved": every table, with the subsection it is under.
        s, e = section("Steps since proved, and steps shown to be as strong as a target")
        self.since = []
        sub, header = None, None
        for i in range(s, e):
            ln = lines[i]
            if ln.startswith("### "):
                sub, header = ln[4:], None
                continue
            if not ln.startswith("|"):
                header = None if not ln.strip() else header
                continue
            cells = split_row(ln)
            if header is None:
                header = cells
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            row = dict(zip(header, cells))
            ids = re.findall(r"\b[FIMR]\d+\b", row["Item"])
            self.since.append({"line": i + 1, "section": sub, "item": row["Item"], "entries": ids,
                               "proved": row["What is proved"], "names": ticks(row["What is proved"])})

        # The entry tables: every row whose first column is an entry id, with its Checked value.
        self.entries = []
        sec, header = None, None
        for i, ln in enumerate(lines):
            if ln.startswith("## "):
                sec, header = ln[3:], None
                continue
            if not ln.startswith("|"):
                header = None if not ln.strip() else header
                continue
            cells = split_row(ln)
            if header is None:
                header = cells
                continue
            if header[0] != "#" or "Checked" not in header or not re.fullmatch(r"[FIMR]\d+", cells[0]):
                continue
            row = dict(zip(header, cells))
            self.entries.append({"id": cells[0], "where": row.get("Where", ""), "checked": row["Checked"],
                                 "section": sec, "line": i + 1})

    def errata_url(self, line):
        return blob("ERRATA.md", line)

    # -- names and closures
    def resolve(self, name):
        """A name as ERRATA.md or a docstring prints it (`Isolated.foo`, `foo`) -> the one declaration, or None."""
        found = self.by_show.get(name, [])
        if len(found) == 1:
            return found[0]
        tail = [d for d in self.decls if d.show.endswith("." + name)] if not found else []
        return tail[0] if len(tail) == 1 else None

    def below(self, i):
        """Every declaration the terms of declaration i reach, i excluded."""
        if i not in self._below:
            seen, todo = set(), list(self.deps[i])
            while todo:
                x = todo.pop()
                if x not in seen:
                    seen.add(x)
                    todo.extend(self.deps[x])
            self._below[i] = frozenset(seen)
        return self._below[i]

    def above(self, i):
        """Every declaration whose terms reach declaration i, i excluded: its cone."""
        if i not in self._above:
            seen, todo = set(), list(self.users.get(i, ()))
            while todo:
                x = todo.pop()
                if x not in seen:
                    seen.add(x)
                    todo.extend(self.users.get(x, ()))
            self._above[i] = frozenset(seen)
        return self._above[i]

    def open_below(self, i):
        return sorted((self.decls[j] for j in self.below(i) if self.decls[j].open), key=lambda d: d.show)

    @property
    def opens(self):
        return sorted((d for d in self.decls if d.open), key=lambda d: d.show)

    def depth_from_targets(self):
        """The fewest steps from any target down to each declaration below one (targets at 0)."""
        dist = {t.i: 0 for t in self.targets}
        frontier = sorted(dist)
        while frontier:
            nxt = []
            for x in frontier:
                for y in self.deps[x]:
                    if y not in dist:
                        dist[y] = dist[x] + 1
                        nxt.append(y)
            frontier = sorted(set(nxt))
        return dist

    def chain(self, low, highs):
        """A shortest chain of declarations from `low` up to the nearest of `highs`, both ends included; ties
        broken by name, so the chain is the same on every run."""
        prev, frontier, seen = {}, [low], {low}
        while frontier:
            hit = sorted((x for x in frontier if x in highs), key=lambda x: self.decls[x].name)
            if hit:
                path, x = [hit[0]], hit[0]
                while x != low:
                    x = prev[x]
                    path.append(x)
                return [self.decls[x] for x in reversed(path)]
            nxt = []
            for x in sorted(frontier, key=lambda x: self.decls[x].name):
                for y in sorted(self.users.get(x, ()), key=lambda y: self.decls[y].name):
                    if y not in seen:
                        seen.add(y)
                        prev[y] = x
                        nxt.append(y)
            frontier = nxt
        return []


_MODEL = None


def load():
    """The model, read once per run. Sets the library's link prefixes: every code run that is the name of a
    declaration links to its line at the pin."""
    global _MODEL
    if _MODEL is None:
        _MODEL = Model()
        lib.PINNED[:] = [f"{URL}/blob/{MASULLO_COMMIT}/"]
        lib.EXTERNAL.clear()
        for show, ds in _MODEL.by_show.items():
            if len(ds) == 1:
                lib.EXTERNAL[show] = ds[0].url
    return _MODEL


def sources(m):
    return (f"riemann-masullo ({URL}) at {SHORT} ({m.date}): comparator.json, Main.lean, ERRATA.md, "
            f"paper/README.md; diagrams/src/deps.json, read from it by its own scripts/progress/Deps.lean "
            f"(tools/deps/README.md). riemann-masullo-diagrams is independent of riemann-masullo and not maintained "
            f"by it.")


def state(m):
    return f"State drawn: riemann-masullo at {SHORT}, {m.date}"


def require(name, expected, got, reread):
    """The comparison every poster makes: fail with both values and what to re-read."""
    if expected != got:
        raise ValueError(f"{name} differs from the sources at {SHORT}. Re-read {reread}.\n  expected: {expected!r}\n"
                         f"  read:     {got!r}")
