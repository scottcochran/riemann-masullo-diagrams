"""C8: Chapter 8, `Ch08_PeriodicOrbits`, item by item. The layout and the checks are chapter.py's; the literals
below are what this poster expects the sources to say at MASULLO_COMMIT, and the build fails on any difference."""
import chapter

ID = "C8"
SLUG = "ch08-periodicorbits"
CHAPTER = "Ch08_PeriodicOrbits"

ITEMS = {'Sec1.lean': ['eq:8.1.0.1', 'eq:8.1.0.2'],
 'Sec1_Printed.lean': ['theorem:8.1.0.1'],
 'Sec2.lean': ['definition:8.2.0.1',
               'definition:8.2.0.2',
               'lemma:8.2.0.3',
               'proposition:8.2.0.4',
               'proposition:8.2.0.5',
               'proposition:8.2.0.6',
               'eq:8.2.0.9',
               'eq:8.2.0.10']}
EXPECTED = [('definition:8.2.0.1', 'definition:8.2.0.2'),
 ('definition:8.2.0.1', 'eq:8.2.0.10'),
 ('definition:8.2.0.1', 'eq:8.2.0.9'),
 ('definition:8.2.0.1', 'proposition:8.2.0.6'),
 ('definition:8.2.0.2', 'proposition:8.2.0.5'),
 ('eq:8.1.0.1', 'theorem:8.1.0.1'),
 ('eq:8.1.0.2', 'eq:8.1.0.1'),
 ('eq:8.2.0.10', 'proposition:8.2.0.4'),
 ('eq:8.2.0.9', 'proposition:8.2.0.4'),
 ('proposition:8.2.0.5', 'lemma:8.2.0.3')]
OUTSIDE = {'eq:8.1.0.1': {'Ch02_AdelicTheta': 1,
                'Ch03_IdelicZeta': 1,
                'Ch05_ThetaZSpaces': 5,
                'AppA_AlgebraicNT': 1,
                'AppC_LCTVS': 3,
                'AppD_SchwartzBruhat': 1},
 'eq:8.1.0.2': {'Ch02_AdelicTheta': 1,
                'Ch05_ThetaZSpaces': 2,
                'AppA_AlgebraicNT': 1,
                'AppC_LCTVS': 4,
                'AppD_SchwartzBruhat': 1},
 'theorem:8.1.0.1': {'Ch02_AdelicTheta': 10,
                     'Ch03_IdelicZeta': 14,
                     'Ch05_ThetaZSpaces': 15,
                     'Ch07_SchauderBasesZeta': 2,
                     'AppA_AlgebraicNT': 13,
                     'AppC_LCTVS': 4,
                     'AppD_SchwartzBruhat': 16,
                     'ForMathlib': 2},
 'definition:8.2.0.1': {'AppA_AlgebraicNT': 2},
 'definition:8.2.0.2': {'AppA_AlgebraicNT': 3},
 'lemma:8.2.0.3': {'AppA_AlgebraicNT': 6, 'ForMathlib': 1},
 'proposition:8.2.0.4': {'AppA_AlgebraicNT': 9, 'ForMathlib': 1},
 'proposition:8.2.0.5': {'AppA_AlgebraicNT': 8},
 'proposition:8.2.0.6': {'AppA_AlgebraicNT': 4},
 'eq:8.2.0.9': {'AppA_AlgebraicNT': 1}}
STATES = {'open': [], 'rests': []}
DEVIATIONS = {'eq:8.1.0.1': (2, 8),
 'eq:8.1.0.2': (1, 9),
 'theorem:8.1.0.1': (4, 56),
 'lemma:8.2.0.3': (3, 70),
 'proposition:8.2.0.4': (2, 18)}
ERRATA = {'eq:8.1.0.2': {'reviewed': ['R11']},
 'lemma:8.2.0.3': {'reviewed': ['R12', 'R13', 'R14']},
 'proposition:8.2.0.4': {'reviewed': ['R1']}}

# item -> the URL of each paper its entries' ERRATA.md rows link -> the entries that link it
ERRATA_PAPERS = {}

# item -> the keys of the bibliography the manuscript cites on its pages (B1)
CITES = {'definition:8.2.0.1': ['Bou-GT', 'NB'],
 'definition:8.2.0.2': ['Bou-GT'],
 'lemma:8.2.0.3': ['Bou-GT'],
 'proposition:8.2.0.4': ['Bou-GT', 'CF'],
 'proposition:8.2.0.5': ['Bou-GT', 'CF'],
 'eq:8.2.0.9': ['Bou-GT', 'CF'],
 'eq:8.2.0.10': ['Bou-GT', 'CF']}


def build():
    return chapter.build(ID, CHAPTER, ITEMS=ITEMS, EXPECTED=EXPECTED, OUTSIDE=OUTSIDE, STATES=STATES,
                         DEVIATIONS=DEVIATIONS, ERRATA=ERRATA,
                         ERRATA_PAPERS=ERRATA_PAPERS, CITES=CITES)
