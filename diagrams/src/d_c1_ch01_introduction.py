"""C1: Chapter 1, `Ch01_Introduction`, item by item. The layout and the checks are chapter.py's; the literals
below are what this poster expects the sources to say at MASULLO_COMMIT, and the build fails on any difference."""
import chapter

ID = "C1"
SLUG = "ch01-introduction"
CHAPTER = "Ch01_Introduction"

ITEMS = {'Sec4.lean': ['text:1.4.1', 'text:1.4.2', 'section:1.4.3', 'text:1.4.3', 'text:1.4.5', 'text:1.4.6', 'text:1.4.7'],
 'Sec4_Printed.lean': ['text:1.4', 'text:1.4.4']}
EXPECTED = [('text:1.4', 'text:1.4.5'),
 ('text:1.4', 'text:1.4.7'),
 ('text:1.4.1', 'text:1.4.5'),
 ('text:1.4.2', 'text:1.4.5'),
 ('text:1.4.2', 'text:1.4.6'),
 ('text:1.4.3', 'section:1.4.3'),
 ('text:1.4.3', 'text:1.4.1'),
 ('text:1.4.3', 'text:1.4.2'),
 ('text:1.4.4', 'text:1.4.5'),
 ('text:1.4.5', 'text:1.4.3'),
 ('text:1.4.5', 'text:1.4.4')]
OUTSIDE = {'text:1.4.1': {'Ch02_AdelicTheta': 1,
                'Ch03_IdelicZeta': 12,
                'Ch05_ThetaZSpaces': 1,
                'Ch06_LocalGlobal': 1,
                'Ch10_TraceSpectral': 2,
                'Ch12_TraceGeometric': 1,
                'AppA_AlgebraicNT': 8,
                'AppB_AnalyticNT': 6,
                'AppD_SchwartzBruhat': 5,
                'ForMathlib': 2},
 'text:1.4.2': {'Ch03_IdelicZeta': 6,
                'Ch06_LocalGlobal': 1,
                'Ch10_TraceSpectral': 1,
                'Ch12_TraceGeometric': 1,
                'AppA_AlgebraicNT': 12,
                'AppB_AnalyticNT': 4,
                'AppC_LCTVS': 1,
                'AppD_SchwartzBruhat': 14,
                'ForMathlib': 2},
 'section:1.4.3': {'Ch03_IdelicZeta': 3, 'Ch06_LocalGlobal': 1, 'AppA_AlgebraicNT': 4, 'AppB_AnalyticNT': 2},
 'text:1.4.3': {'Ch03_IdelicZeta': 15,
                'Ch06_LocalGlobal': 1,
                'Ch10_TraceSpectral': 1,
                'Ch12_TraceGeometric': 1,
                'AppA_AlgebraicNT': 10,
                'AppB_AnalyticNT': 14,
                'AppD_SchwartzBruhat': 2,
                'ForMathlib': 7},
 'text:1.4.5': {'Ch03_IdelicZeta': 13,
                'Ch06_LocalGlobal': 1,
                'Ch10_TraceSpectral': 1,
                'Ch12_TraceGeometric': 1,
                'AppA_AlgebraicNT': 5,
                'AppB_AnalyticNT': 1,
                'AppD_SchwartzBruhat': 2,
                'ForMathlib': 2},
 'text:1.4.6': {'Ch02_AdelicTheta': 1,
                'Ch03_IdelicZeta': 4,
                'Ch04_PeriodicSchauderBases': 1,
                'Ch05_ThetaZSpaces': 1,
                'Ch09_HardySobolev': 1,
                'Ch10_TraceSpectral': 2,
                'Ch12_TraceGeometric': 1,
                'AppA_AlgebraicNT': 9,
                'AppB_AnalyticNT': 3,
                'AppD_SchwartzBruhat': 10,
                'ForMathlib': 2},
 'text:1.4.7': {'Ch02_AdelicTheta': 1,
                'Ch03_IdelicZeta': 19,
                'Ch05_ThetaZSpaces': 2,
                'Ch06_LocalGlobal': 1,
                'Ch07_SchauderBasesZeta': 1,
                'AppA_AlgebraicNT': 3,
                'AppB_AnalyticNT': 3,
                'AppD_SchwartzBruhat': 1},
 'text:1.4': {'Ch03_IdelicZeta': 9,
              'Ch06_LocalGlobal': 1,
              'Ch10_TraceSpectral': 1,
              'Ch12_TraceGeometric': 1,
              'AppA_AlgebraicNT': 6,
              'AppB_AnalyticNT': 2,
              'AppD_SchwartzBruhat': 2,
              'ForMathlib': 1},
 'text:1.4.4': {'Ch03_IdelicZeta': 3, 'AppA_AlgebraicNT': 1, 'AppB_AnalyticNT': 3, 'ForMathlib': 1}}
STATES = {'open': [], 'rests': ['text:1.4.1', 'text:1.4.5']}
DEVIATIONS = {'text:1.4.1': (5, 77),
 'text:1.4.2': (4, 54),
 'text:1.4.3': (15, 240),
 'text:1.4.5': (6, 76),
 'text:1.4.7': (6, 15),
 'text:1.4.4': (1, 7)}
ERRATA = {'text:1.4.1': {'reviewed': ['F250', 'F251', 'F252', 'F253', 'F254', 'I374']},
 'text:1.4.3': {'reviewed': ['F255', 'I374', 'I378', 'R2']},
 'text:1.4.5': {'reviewed': ['F256', 'I376']},
 'text:1.4.6': {'reviewed': ['F257', 'I354', 'I377', 'I403']},
 'text:1.4': {'reviewed': ['F249', 'I353']},
 'text:1.4.4': {'reviewed': ['F253', 'I375']}}

# item -> the URL of each paper its entries' ERRATA.md rows link -> the entries that link it
ERRATA_PAPERS = {}


def build():
    return chapter.build(ID, CHAPTER, ITEMS=ITEMS, EXPECTED=EXPECTED, OUTSIDE=OUTSIDE, STATES=STATES,
                         DEVIATIONS=DEVIATIONS, ERRATA=ERRATA,
                         ERRATA_PAPERS=ERRATA_PAPERS)
