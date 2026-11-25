"""The manuscript as riemann-masullo transcribes it: its bibliography, and where its text cites each entry.

Read under rule 9 (PLAN.md): the manuscript is read through riemann-masullo's transcription at MASULLO_COMMIT, once
`transcription/README.md` names the PDF it was made from by PAPER_SHA256, and is not quoted. What is read:

- **the bibliography**, `transcription/chapters/bibliography.md`: each entry, `[KEY] text`, with the PDF page it is
  printed on. An entry runs from its key to the next key, a blank line, or a page's running head or number. Its
  text is the work's authors, title, venue and year, as transcribed: bibliographic data, drawn as such.
- **the citations**, every other file of `transcription/chapters/`: a bracket group outside mathematics (`$…$`,
  `$$…$$`) and not a Markdown link, whose first part, before a comma or semicolon, is a key of the bibliography.
  Each part of the group that is a key is a citation of it; the rest is the locator (`Thm.14.4.5(b)`, `Tag 000B`).
  The page is the `## PDF page N` marker above it; printed page numbers equal PDF page numbers
  (`transcription/README.md`).

A citation is the paper's, not the Lean's (rule 10). That the paper uses the cited work where it cites it is not
checked. The transcription was checked against the PDF by scripts and AI reviewers, not by a person (its README).
Standard library only.
"""
import collections
import re

import rm

README = "transcription/README.md"
CHAPTERS = "transcription/chapters"
BIBLIOGRAPHY = f"{CHAPTERS}/bibliography.md"
# The files of the transcription, in the paper's order; each is the text of one Lean directory, or of none.
FILES = (["front-matter.md"] + [f"chapter-{n:02d}.md" for n in range(1, 15)]
         + [f"appendix-{c}.md" for c in "abcde"])
PAGE = re.compile(r"^## PDF page (\d+)\s*$")
HEAD = re.compile(r"^(\*\*\d+\*\*( · \*\*[^*]+\*\*)?|\d+|\*\*Bibliography\*\*)\s*$")
ENTRY = re.compile(r"^\[([^\]\s]+)\]\s+(.*)$")
GROUP = re.compile(r"\[([^\[\]\n]{1,200})\](?!\()")
MATH = re.compile(r"\$\$.*?\$\$|\$[^$\n]*\$", re.S)


class Ref:
    __slots__ = ("key", "n", "page", "line", "text")

    def __init__(self, key, n, page, line, text):
        self.key, self.n, self.page, self.line, self.text = key, n, page, line, text

    @property
    def anchor(self):
        """`ref-Ahl`; the second entry printed under a key is `ref-JL-2`."""
        return f"ref-{re.sub(r'[^A-Za-z0-9-]', '_', self.key)}" + (f"-{self.n}" if self.n > 1 else "")

    @property
    def plain(self):
        """The entry without its Markdown emphasis."""
        return " ".join(self.text.replace("*", "").split())


class Cite:
    __slots__ = ("key", "file", "page", "line", "locator")

    def __init__(self, key, file, page, line, locator):
        self.key, self.file, self.page, self.line, self.locator = key, file, page, line, locator


def chapter_of_file(name, chapters):
    """`chapter-04.md` -> `Ch04_PeriodicSchauderBases`, `appendix-b.md` -> `AppB_AnalyticNT`, front matter -> None."""
    m = re.match(r"chapter-(\d+)\.md$", name)
    if m:
        hit = [c for c in chapters if re.match(rf"Ch{int(m.group(1)):02d}_", c)]
    else:
        m = re.match(r"appendix-([a-e])\.md$", name)
        hit = [c for c in chapters if m and c.startswith(f"App{m.group(1).upper()}_")]
    if len(hit) > 1:
        raise ValueError(f"{CHAPTERS}/{name}: more than one Lean directory for it, {hit}")
    return hit[0] if hit else None


def file_label(name):
    """`chapter-04.md` -> `Chapter 4`, `appendix-b.md` -> `Appendix B`, `front-matter.md` -> `Front matter`."""
    m = re.match(r"chapter-(\d+)\.md$", name)
    if m:
        return f"Chapter {int(m.group(1))}"
    m = re.match(r"appendix-([a-e])\.md$", name)
    return f"Appendix {m.group(1).upper()}" if m else "Front matter"


class Paper:
    def __init__(self, m):
        self.m = m
        readme = m.read(README)
        found = re.findall(r"sha256\s+`([0-9a-f]{64})`", readme)
        if found != [rm.PAPER_SHA256]:
            raise ValueError(f"PAPER_SHA256: {README} at {rm.SHORT} names the PDF by {found}, the pin is "
                             f"{rm.PAPER_SHA256[:12]}: the transcription is not of the pinned manuscript")
        self.refs = self._read_bibliography()
        self.by_key = collections.defaultdict(list)
        for r in self.refs:
            self.by_key[r.key].append(r)
        self.cites, self.groups = self._read_citations()

    def _read_bibliography(self):
        refs, page, cur = [], None, None
        seen = collections.Counter()
        for i, ln in enumerate(self.m.read(BIBLIOGRAPHY).splitlines()):
            p = PAGE.match(ln)
            if p:
                page, cur = int(p.group(1)), None
                continue
            if not ln.strip() or HEAD.match(ln):
                cur = None if not ln.strip() else cur
                continue
            e = ENTRY.match(ln)
            if e:
                seen[e.group(1)] += 1
                cur = Ref(e.group(1), seen[e.group(1)], page, i + 1, e.group(2).strip())
                refs.append(cur)
            elif cur is not None:
                cur.text += " " + ln.strip()
            else:
                raise ValueError(f"{BIBLIOGRAPHY}:{i + 1}: a line that is neither an entry nor the rest of one: "
                                 f"{ln[:60]!r}")
        if not refs:
            raise ValueError(f"{BIBLIOGRAPHY}: no entries read")
        return refs

    def _read_citations(self):
        keys = set(self.by_key)
        cites, groups = [], 0
        for name in FILES:
            raw = self.m.read(f"{CHAPTERS}/{name}")
            # brackets are found with the mathematics blanked, every character kept in place, so that a bracket
            # inside a formula is not a citation; a group's own text is then read from the raw line
            blank = MATH.sub(lambda g: re.sub(r"[^\n]", " ", g.group(0)), raw).splitlines()
            page = None
            for i, (ln, rln) in enumerate(zip(blank, raw.splitlines())):
                p = PAGE.match(ln)
                if p:
                    page = int(p.group(1))
                    continue
                for g in GROUP.finditer(ln):
                    parts = [s.strip() for s in re.split(r"[;,]", rln[g.start(1):g.end(1)])]
                    if parts[0] not in keys:
                        continue
                    groups += 1
                    cited = [s for s in parts if s in keys]
                    locator = ", ".join(s for s in parts if s not in keys)
                    for k in dict.fromkeys(cited):
                        cites.append(Cite(k, name, page, i + 1, locator))
        return cites, groups

    def pages(self):
        """key -> transcription file -> the pages that cite it, in the paper's order."""
        out = {}
        for c in self.cites:
            out.setdefault(c.key, {}).setdefault(c.file, [])
            if c.page not in out[c.key][c.file]:
                out[c.key][c.file].append(c.page)
        return {k: {f: sorted(v[f]) for f in FILES if f in v} for k, v in out.items()}

    def tags(self, key):
        """The Stacks project's tags a key's citations name (`[SP, Tag 000B]`, `[SP, Tags 00Z8, 00Z9]`) -> the pages
        citing each, in the order first cited. A tag is written as the citation writes it, whether or not it has a
        tag's form."""
        out = {}
        for c in self.cites:
            if c.key != key:
                continue
            m = re.search(r"\bTags?\s+([0-9A-Za-z]{3,6}(?:,\s*[0-9A-Za-z]{3,6})*)", c.locator)
            for t in re.split(r",\s*", m.group(1)) if m else []:
                if c.page not in out.setdefault(t, []):
                    out[t].append(c.page)
        return out

    def keys_on(self, p0, p1):
        """The keys cited on pages p0 to p1, in the bibliography's order."""
        on = {c.key for c in self.cites if c.page is not None and p0 <= c.page <= p1}
        return [k for k in dict.fromkeys(r.key for r in self.refs) if k in on]


def card_of_page(items, page):
    """The card a cited page opens: of the items whose `Paper:` pages cover it, the one with the fewest pages, then
    the first in the paper's order; None when no item covers it."""
    import items as I
    cover = [it for it in items if it.pages and it.pages[0] <= page <= it.pages[1]]
    if not cover:
        return None
    return min(cover, key=lambda it: (it.pages[1] - it.pages[0], I.natural(it.key)))


_PAPER = None


def load():
    global _PAPER
    if _PAPER is None:
        _PAPER = Paper(rm.load())
    return _PAPER
