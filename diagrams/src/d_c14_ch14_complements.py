"""C14: Chapter 14, `Ch14_Complements`, item by item. The layout and the checks are chapter.py's; the literals
below are what this poster expects the sources to say at MASULLO_COMMIT, and the build fails on any difference."""
import chapter

ID = "C14"
SLUG = "ch14-complements"
CHAPTER = "Ch14_Complements"

ITEMS = {'Sec2.lean': ['text:14.2', 'eq:14.2.0.1']}
EXPECTED = [('eq:14.2.0.1', 'text:14.2')]
OUTSIDE = {'text:14.2': {'ForMathlib': 3}}
STATES = {'open': [], 'rests': []}
DEVIATIONS = {'text:14.2': (5, 40), 'eq:14.2.0.1': (2, 18)}
ERRATA = {'text:14.2': {'reviewed': ['I432']}}


def build():
    return chapter.build(ID, CHAPTER, ITEMS=ITEMS, EXPECTED=EXPECTED, OUTSIDE=OUTSIDE, STATES=STATES,
                         DEVIATIONS=DEVIATIONS, ERRATA=ERRATA)
