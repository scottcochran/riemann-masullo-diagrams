"""Find a stable link for each entry of the manuscript's bibliography, and write diagrams/src/papers.toml.

    uv run python tools/link-papers.py            # every entry without a `hand` entry in the file
    uv run python tools/link-papers.py Ahl Bou    # only these keys
    uv run python tools/link-papers.py --cache F  # keep what is found in F, and resume from it

The proof-posters:linking-papers method, for 319 entries at once. For each entry, as the transcription prints it
(diagrams/src/paper.py), it reads the first author's surname, the title and the year, then, in this order:

1. **Crossref** (`via = "crossref"`): the best match for the entry, kept only when its title agrees with the
   entry's (score 0.85 or more, or the record's title begins with the entry's), an author's surname is the entry's first author's, and its year is the entry's
   within one. The DOI is then fetched again from its own record and checked the same way.
2. **zbMATH Open** (`via = "zbmath"`): its records for the surname and year (or the surname and the title's words,
   when the entry prints no year), the best title kept on the same terms. The record's DOI if it has one, else an
   arXiv, numdam or EuDML link it holds, else the record itself.
3. **Crossref, on the whole entry** (`via = "crossref"`): for an entry whose authors and title the parse
   misreads, Crossref's match for the whole entry, kept only when the record's title stands in the entry word for
   word, one of its authors is named there, and its year is one the entry prints, within one.
4. **None** (`via = "none"`): neither service has the work on those terms. The entry is drawn without a link.

An entry the file marks `via = "hand"` is kept as it is. Only the citation (title, surname, year) is sent, with a
generic User-Agent. Standard library only. The file it writes is the posters' data, checked by B1 against the
bibliography both ways; this tool is not run by the build.
"""
import difflib
import json
import pathlib
import re
import sys
import time
import tomllib
import unicodedata
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "diagrams" / "src"))
import paper  # noqa: E402

OUT = ROOT / "diagrams" / "src" / "papers.toml"
UA = "proof-posters-lookup/0.1"
MIN = 0.85
HEADER = '''# The works the manuscript's bibliography lists, one entry per bibliography entry: the url a reader is sent to from
# the entry on B1. This is the posters' own data, not riemann-masullo's: the transcription prints authors, title,
# venue and year, and no link. Written by tools/link-papers.py on {date} (the proof-posters:linking-papers method):
# `via = "crossref"`, Crossref's match on the entry's title, first author and year, checked against the DOI's own
# record; `via = "zbmath"`, zbMATH Open's record for the author and year with the same title, linking its DOI, an
# arXiv, numdam or EuDML copy, or the record itself; `via = "hand"`, settled by hand, with a note; `via = "none"`,
# found by neither on those terms, drawn without a link. A DOI is given as a doi.org url. An entry's id is its key;
# the second entry printed under one key is `<key> (2)`. B1 fails if an id here is not an entry of the
# bibliography, or an entry has no id here (diagrams/src/d_b1_bibliography.py).
'''


def get(url, tries=2):
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)
        except Exception:
            if n == tries - 1:
                raise
            time.sleep(3 * (n + 1))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def score(a, b):
    """How closely a record's title b matches an entry's title a, 0 to 1. A record whose title begins with the
    entry's whole title, as a book's with its subtitle, scores 1."""
    na, nb = norm(a), norm(b)
    if na and nb[:len(na)] == na:
        return 1.0
    return round(difflib.SequenceMatcher(None, " ".join(na), " ".join(nb)).ratio(), 2)


def ident(r):
    return r.key if r.n == 1 else f"{r.key} ({r.n})"


def fields(r):
    """An entry -> (first author's surname, title, year), read from the text as printed."""
    text = re.sub(r"\$[^$]*\$", " ", r.text)
    year = None
    ys = re.findall(r"\b(1[6-9]\d\d|20[0-2]\d)\b", text)
    if ys:
        year = int(ys[-1])
    it = re.search(r"\*([^*]{4,})\*", text)
    plain = " ".join(text.replace("*", "").split())
    # the authors end at the first ". " after a surname: two letters or more, one lower-case, not "Jr" or "eds"
    authors, rest = plain, ""
    for m in re.finditer(r"([^\s.]+)\. ", plain):
        w = m.group(1)
        if len(w) >= 2 and sum(c.islower() for c in w) >= 1 and w.lower() not in ("jr", "eds", "ed", "et", "al"):
            authors, rest = plain[:m.start(1) + len(w)], plain[m.end():]
            break
    if it:
        title = it.group(1).strip(" .")
    else:
        title = re.split(r"\. (?=[A-Z])", rest, maxsplit=1)[0].strip(" .")
    first = re.split(r",| and |;", authors)[0].strip()
    first = re.sub(r"\b(eds?|ed)\b\.?", "", first).strip()
    surname = first.split()[-1] if first.split() else ""
    return surname, title, year


def crossref_year(it):
    for k in ("published-print", "published-online", "issued", "created"):
        parts = (it.get(k) or {}).get("date-parts") or [[None]]
        if parts[0] and parts[0][0]:
            return parts[0][0]
    return None


def agrees(surname, title, year, t, names, y):
    s = score(title, t)
    a_ok = any(w in {x for n in names for x in norm(n)} for w in norm(surname)) if surname else False
    y_ok = year is None or (y is not None and abs(int(year) - int(y)) <= 1)
    return s, (s >= MIN and a_ok and y_ok)


def crossref(surname, title, year):
    q = {"query.bibliographic": title, "rows": "5"}
    if surname:
        q["query.author"] = surname
    items = get("https://api.crossref.org/works?" + urllib.parse.urlencode(q))["message"]["items"]
    best = None
    for it in items:
        t = (it.get("title") or [""])[0]
        names = [a.get("family", "") for a in it.get("author", []) + it.get("editor", [])]
        s, ok = agrees(surname, title, year, t, names, crossref_year(it))
        if ok and (best is None or s > best[0]):
            best = (s, it["DOI"], t)
    if not best:
        return None
    # the DOI against its own record
    rec = get("https://api.crossref.org/works/" + urllib.parse.quote(best[1]))["message"]
    t = (rec.get("title") or [""])[0]
    names = [a.get("family", "") for a in rec.get("author", []) + rec.get("editor", [])]
    s, ok = agrees(surname, title, year, t, names, crossref_year(rec))
    return (doi_url(best[1]), s, t) if ok else None


def crossref_whole(r):
    """Crossref's match for the whole entry, kept only when the record's title, before any colon, stands in the
    entry word for word, one of its authors' surnames is in the entry, and its year is one the entry prints, within
    one (or the entry prints none). For entries whose authors and title the parse in `fields` misreads."""
    text = " ".join(re.sub(r"\$[^$]*\$", " ", r.text).replace("*", "").split())
    words = norm(text)
    years = [int(y) for y in re.findall(r"\b(1[6-9]\d\d|20[0-2]\d)\b", text)]
    items = get("https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": text, "rows": "5"}))["message"]["items"]
    def fits(it):
        t = (it.get("title") or [""])[0]
        tw = norm(t.split(":")[0])
        if len(tw) < 2 or not any(words[k:k + len(tw)] == tw for k in range(len(words))):
            return False
        names = {w for a in it.get("author", []) + it.get("editor", []) for w in norm(a.get("family", ""))}
        y = crossref_year(it)
        return bool(names & set(words)) and not (years and (y is None or min(abs(y - x) for x in years) > 1))

    for it in items:
        if fits(it):
            # the DOI against its own record, on the same terms
            rec = get("https://api.crossref.org/works/" + urllib.parse.quote(it["DOI"]))["message"]
            if fits(rec):
                return doi_url(it['DOI']), 1.0, (rec.get("title") or [""])[0]
    return None


def zbmath(surname, title, year):
    if not surname:
        return None
    terms = [f"au:{surname}"] + ([f"py:{year}"] if year else [f"ti:{w}" for w in norm(title)[:4]])
    url = "https://api.zbmath.org/v1/document/_search?" + urllib.parse.urlencode(
        {"search_string": " ".join(terms), "results_per_page": "100"})
    try:
        res = get(url).get("result") or []
    except Exception:
        return None
    best = None
    for r in res:
        t = (r.get("title") or {}).get("title", "")
        names = [a.get("name", "") for a in (r.get("contributors") or {}).get("authors", [])]
        s, ok = agrees(surname, title, year, t, names, r.get("year"))
        if ok and (best is None or s > best[0]):
            best = (s, r, t)
    if not best:
        return None
    s, r, t = best
    links = {(l.get("type") or "").lower(): l.get("url") for l in r.get("links") or [] if l.get("url")}
    for k in ("doi", "arxiv", "numdam", "eudml"):
        if links.get(k):
            u = links[k]
            if k == "doi" and not u.startswith("http"):
                u = doi_url(u)
            return u, s, t
    return r.get("zbmath_url"), s, t


def doi_url(doi):
    """A DOI as a doi.org url, with the characters an SVG attribute would escape (`<`, `>`, `&`, `"`) encoded."""
    return "https://doi.org/" + urllib.parse.quote(doi, safe="/:;()._-")


def toml_str(s):
    return json.dumps(s, ensure_ascii=False)


def main(argv):
    P = paper.load()
    old = tomllib.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    cache_arg = argv[argv.index("--cache") + 1] if "--cache" in argv else None
    only = set(a for a in argv if not a.startswith("--") and a != cache_arg)
    # what was found is kept as it is found, so that an interrupted run resumes; --cache FILE names the file
    cache_path = pathlib.Path(argv[argv.index("--cache") + 1]) if "--cache" in argv else None
    cache = json.loads(cache_path.read_text()) if cache_path and cache_path.exists() else {}
    out, report = {}, []
    for r in P.refs:
        i = ident(r)
        if old.get(i, {}).get("via") == "hand" or (only and r.key not in only and i in old):
            out[i] = old[i]
            continue
        surname, title, year = fields(r)
        if i in cache and not (only and r.key in only):
            out[i], line = cache[i]["entry"], cache[i]["report"]
            report.append(line)
            continue
        hit, via = None, "none"
        try:
            hit = crossref(surname, title, year)
            via = "crossref" if hit else via
            if not hit:
                hit = zbmath(surname, title, year)
                via = "zbmath" if hit else via
            if not hit:
                hit = crossref_whole(r)
                via = "crossref" if hit else via
        except Exception as e:
            report.append(f"{i}: lookup failed, {e!r}")
        e = {"via": via}
        if hit:
            e["url"] = hit[0]
            report.append(f"{i}: {via} {hit[1]:.2f} {hit[0]}\n    entry:  {title} — {surname} ({year})\n"
                          f"    record: {hit[2]}")
        else:
            e["note"] = "found by neither Crossref nor zbMATH Open on the entry's title, first author and year"
            report.append(f"{i}: none — {title} — {surname} ({year})")
        out[i] = e
        print(f"{len(out)}/{len(P.refs)} {report[-1].splitlines()[0]}", file=sys.stderr, flush=True)
        if cache_path:
            cache[i] = {"entry": e, "report": report[-1]}
            cache_path.write_text(json.dumps(cache, ensure_ascii=False))
        time.sleep(0.3)
    lines = [HEADER.format(date=time.strftime("%Y.%m.%d"))]
    for i in sorted(out, key=lambda s: (s.lower(), s)):
        e = out[i]
        lines.append(f"\n[{toml_str(i)}]")
        for k in ("url", "via", "note"):
            if k in e:
                lines.append(f"{k} = {toml_str(e[k])}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(report))
    n = {v: sum(1 for e in out.values() if e["via"] == v) for v in ("crossref", "zbmath", "hand", "none")}
    print(f"link-papers: {len(out)} entries; " + ", ".join(f"{v} {k}" for k, v in n.items()))


if __name__ == "__main__":
    main(sys.argv[1:])
