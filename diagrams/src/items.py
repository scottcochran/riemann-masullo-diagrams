"""Paper items: the declarations grouped by the item of the manuscript their docstrings cite, as riemann-masullo's
progress map groups them, and what each item rests on.

- **Keys** are build.py's `paper_item` keys: the kind word and the number (`theorem:5.2.1.1`), `eq:` for an
  equation, `text:` for a section, the text itself for an item with no number.
- **Grouping** is build.py's `group_items`: in each module, in line order, a declaration with no `Paper:` line is a
  helper and joins the next declaration of its file that has one, or the last one at the end of the file; a file
  with none is its own group of helpers. In `ForMathlib`, which the paper does not number, each file is one item.
  Vendored code and the root modules (`Main`, `Statements`) are left out.
- **Edges** are direct: item A uses item B when a declaration of A uses one of B. `reduce()` drops an edge that
  another path between the same items already implies, in name order, so that reachability is kept and the result
  is the same on every run.
- **State**: open when a declaration of the item is open; resting on something open when one rests on an open
  declaration; proved otherwise.
- **Errata**: an ERRATA.md entry is on every item whose number its "Where" column names, with the kind word before
  the number (or the kind of the number before it, after `and` or a comma). Withdrawn and moved entries are left out.
"""
import collections
import re

import rm

NUMBER = re.compile(r"(?:[A-E]|\d+)(?:\.\d+)+")            # build.py's NUMBER
BUILD_PLURAL = {"Equations": "Equation", "Definitions": "Definition", "Lemmas": "Lemma"}   # build.py's
PLURAL = dict(BUILD_PLURAL, Theorems="Theorem", Propositions="Proposition", Corollaries="Corollary",
              Remarks="Remark", Examples="Example")
STATES = ("open", "rests", "proved")


def item_key(raw):
    """build.py's paper_item key: `Lemma A.2.3.4(2)` -> `lemma:A.2.3.4`, `(5.4.1.19)` -> `eq:5.4.1.19`; an item
    with no number is keyed by its text, as there."""
    num = NUMBER.search(raw)
    if not num:
        return f"item:{raw}"
    before, number = raw[:num.start()], num.group(0)
    if before.endswith("("):
        return f"eq:{number}"
    if before.endswith("§"):
        return f"text:{number}"
    words = re.findall(r"[A-Za-z]+", before)
    word = BUILD_PLURAL.get(words[-1], words[-1]) if words else ""
    return f"{word.lower() or 'item'}:{number}"


def label(key):
    """`theorem:5.2.1.1` -> `Theorem 5.2.1.1`, `eq:5.4.1.19` -> `(5.4.1.19)`, `text:1.4.5` -> `§1.4.5`."""
    kind, _, rest = key.partition(":")
    if kind == "eq":
        return f"({rest})"
    if kind == "text":
        return f"§{rest}"
    if kind == "item":
        return rest
    if kind == "helpers":
        return "Helper lemmas"
    if kind == "file":
        return rest.split("/")[-1].removesuffix(".lean")
    return f"{kind.capitalize()} {rest}"


def keys_named(where):
    """Every item an entry's Where names: each number with the kind word before it, or the kind of the number before
    it when only `and`, a comma or a part in parentheses comes between (`Theorems 7.1.4.2(1) and 7.1.4.3(1)`)."""
    out, kind, last = [], None, 0
    for mt in NUMBER.finditer(where):
        before = where[last:mt.start()]
        if before.endswith("("):
            k = "eq"
        elif before.endswith("§"):
            k = "text"
        else:
            words = re.findall(r"[A-Za-z]+", re.sub(r"\([^)]*\)", "", before))
            if words and words[-1][0].isupper():
                k = PLURAL.get(words[-1], words[-1]).lower()
            elif kind and re.fullmatch(r"[\s,]*(?:\([^)]*\))?[\s,]*(?:and|or)?\s*", before):
                k = kind
            else:
                k = None
        if k:
            out.append(f"{k}:{mt.group(0)}")
            kind = k if k not in ("eq", "text") else kind
        last = mt.end()
    return out


def anchor(key):
    """The id of an item's card, valid as an SVG anchor: `theorem:5.2.1.1` -> `i-theorem-5.2.1.1`."""
    return "i-" + re.sub(r"[^\w.-]+", "_", key.replace(":", "-", 1))


def natural(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


class Item:
    __slots__ = ("key", "chapter", "module", "decls", "pages", "state", "deviations", "errata", "uses", "printed")

    @property
    def label(self):
        return label(self.key)

    @property
    def anchor(self):
        return anchor(self.key)

    @property
    def first(self):
        """The declaration a card's title links to: the first, by file and line, that cites the item."""
        cited = [d for d in self.decls if d.paper] or self.decls
        return min(cited, key=lambda d: (natural(d.module), d.line))


class Items:
    def __init__(self, m):
        self.m = m
        self.item_of = {}
        per_mod = collections.defaultdict(list)
        for d in m.decls:
            if d.vendored or d.module in ("Main", "Statements"):
                continue
            per_mod[d.module].append(d)
        for mod in sorted(per_mod):
            ds = sorted(per_mod[mod], key=lambda d: (d.line, d.name))
            if ds[0].chapter == "ForMathlib":
                for d in ds:
                    self.item_of[d.i] = f"file:{d.path}"
                continue
            following, nxt = {}, None
            for d in reversed(ds):
                nxt = item_key(d.paper[0]) if d.paper else nxt
                following[d.i] = nxt
            last = next((item_key(d.paper[0]) for d in reversed(ds) if d.paper), None)
            for d in ds:
                self.item_of[d.i] = following[d.i] or last or f"helpers:{mod}"
        members = collections.defaultdict(list)
        for i, k in self.item_of.items():
            members[k].append(m.decls[i])
        placed = collections.defaultdict(lambda: collections.defaultdict(set))
        order = {c: n for n, c in enumerate(rm.CHECKED)}
        for e in m.entries:
            if e["checked"] not in order:
                continue
            for k in sorted(set(keys_named(e["where"]))):
                placed[k][e["checked"]].add(e["id"])
        self.items = {}
        for k in sorted(members):
            ds = sorted(members[k], key=lambda d: d.name)
            it = Item()
            it.key, it.decls = k, ds
            by_mod = collections.Counter(d.module for d in ds)
            it.module = min(by_mod, key=lambda mod: (-by_mod[mod], natural(mod)))
            it.chapter = rm.chapter_of_module(it.module)
            ps = [d.paper for d in ds if d.paper]
            it.pages = (min(p[1] for p in ps), max(p[2] for p in ps)) if ps else None
            if any(d.open for d in ds):
                it.state = "open"
            elif any(m.open_below(d.i) for d in ds):
                it.state = "rests"
            else:
                it.state = "proved"
            it.deviations = sum(1 for d in ds if d.deviation)
            it.printed = sum(1 for d in ds if ".Printed." in d.name)
            it.errata = {c: sorted(placed[k][c], key=natural) for c in rm.CHECKED if placed[k][c]}
            uses = set()
            for d in ds:
                for j in m.deps[d.i]:
                    kk = self.item_of.get(j)
                    if kk is not None and kk != k:
                        uses.add(kk)
            it.uses = sorted(uses)
            self.items[k] = it

    def chapter(self, chapter):
        return [it for it in self.items.values() if it.chapter == chapter]


def reduce(edges):
    """`edges`: (user, used) pairs. Drop, in name order, each edge whose ends another path still joins, so that what
    reaches what is unchanged. Returns the kept pairs, sorted."""
    adj = collections.defaultdict(set)
    for a, b in edges:
        adj[a].add(b)

    def reaches(a, b, skip):
        seen, todo = {a}, [x for x in adj[a] if (a, x) != skip]
        while todo:
            x = todo.pop()
            if x == b:
                return True
            if x in seen:
                continue
            seen.add(x)
            todo.extend(adj[x])
        return False

    for a, b in sorted(edges):
        if reaches(a, b, (a, b)):
            adj[a].discard(b)
    return sorted((a, b) for a in adj for b in adj[a])


_ITEMS = None


def load():
    global _ITEMS
    if _ITEMS is None:
        _ITEMS = Items(rm.load())
    return _ITEMS
