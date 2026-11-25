"""CE: Appendix E, `AppE_TopologicalStacks`, item by item. The layout and the checks are chapter.py's; the literals
below are what this poster expects the sources to say at MASULLO_COMMIT, and the build fails on any difference."""
import chapter

ID = "CE"
SLUG = "appe-topologicalstacks"
CHAPTER = "AppE_TopologicalStacks"

ITEMS = {'Sec1a.lean': ['terminology:E.0.0.2',
                'definition:E.1.1.1',
                'remark:E.1.1.2',
                'lemma:E.1.1.3',
                'lemma:E.1.1.4',
                'remark:E.1.1.5',
                'remark:E.1.1.6',
                'definition:E.1.1.7',
                'remark:E.1.1.8',
                'example:E.1.1.9'],
 'Sec1a_Printed.lean': ['helpers:RiemannMasullo.AppE_TopologicalStacks.Sec1a_Printed']}
EXPECTED = [('definition:E.1.1.1', 'remark:E.1.1.2'),
 ('lemma:E.1.1.3', 'definition:E.1.1.7'),
 ('lemma:E.1.1.3', 'lemma:E.1.1.4'),
 ('lemma:E.1.1.3', 'remark:E.1.1.6'),
 ('lemma:E.1.1.4', 'remark:E.1.1.5'),
 ('remark:E.1.1.2', 'definition:E.1.1.1'),
 ('remark:E.1.1.2', 'helpers:RiemannMasullo.AppE_TopologicalStacks.Sec1a_Printed')]
OUTSIDE = {}
STATES = {'open': [], 'rests': []}
DEVIATIONS = {'definition:E.1.1.1': (2, 2),
 'remark:E.1.1.2': (2, 2),
 'lemma:E.1.1.3': (6, 9),
 'lemma:E.1.1.4': (3, 15),
 'remark:E.1.1.5': (2, 4),
 'remark:E.1.1.6': (1, 1),
 'definition:E.1.1.7': (2, 2),
 'remark:E.1.1.8': (1, 1),
 'example:E.1.1.9': (2, 5)}
ERRATA = {}

# item -> the URL of each paper its entries' ERRATA.md rows link -> the entries that link it
ERRATA_PAPERS = {}


def build():
    return chapter.build(ID, CHAPTER, ITEMS=ITEMS, EXPECTED=EXPECTED, OUTSIDE=OUTSIDE, STATES=STATES,
                         DEVIATIONS=DEVIATIONS, ERRATA=ERRATA,
                         ERRATA_PAPERS=ERRATA_PAPERS)
