"""C13: Chapter 13, `Ch13_ZerosHecke`, item by item. The layout and the checks are chapter.py's; the literals
below are what this poster expects the sources to say at MASULLO_COMMIT, and the build fails on any difference."""
import chapter

ID = "C13"
SLUG = "ch13-zeroshecke"
CHAPTER = "Ch13_ZerosHecke"

ITEMS = {'DirichletZeroDisplacement.lean': ['helpers:RiemannMasullo.Ch13_ZerosHecke.DirichletZeroDisplacement'],
 'Sec3.lean': ['eq:13.3.1.1', 'eq:13.3.1.2'],
 'Sec3_Printed.lean': ['theorem:13.3.1.1']}
EXPECTED = [('eq:13.3.1.1', 'eq:13.3.1.2'), ('eq:13.3.1.2', 'theorem:13.3.1.1')]
OUTSIDE = {'helpers:RiemannMasullo.Ch13_ZerosHecke.DirichletZeroDisplacement': {'ForMathlib': 2},
 'eq:13.3.1.1': {'Ch06_LocalGlobal': 1},
 'eq:13.3.1.2': {'Ch03_IdelicZeta': 2,
                 'Ch04_PeriodicSchauderBases': 1,
                 'Ch09_HardySobolev': 1,
                 'Ch10_TraceSpectral': 4,
                 'AppA_AlgebraicNT': 2,
                 'AppD_SchwartzBruhat': 5,
                 'ForMathlib': 1},
 'theorem:13.3.1.1': {'Ch02_AdelicTheta': 2,
                      'Ch03_IdelicZeta': 7,
                      'Ch05_ThetaZSpaces': 1,
                      'Ch06_LocalGlobal': 2,
                      'Ch09_HardySobolev': 3,
                      'Ch10_TraceSpectral': 10,
                      'Ch12_TraceGeometric': 1,
                      'AppA_AlgebraicNT': 9,
                      'AppB_AnalyticNT': 5,
                      'AppC_LCTVS': 1,
                      'AppD_SchwartzBruhat': 9,
                      'ForMathlib': 2}}
STATES = {'open': [], 'rests': ['theorem:13.3.1.1']}
DEVIATIONS = {'eq:13.3.1.2': (1, 8), 'theorem:13.3.1.1': (3, 42)}
ERRATA = {'eq:13.3.1.1': {'reviewed': ['F247', 'I371']},
 'eq:13.3.1.2': {'reviewed': ['I370', 'I402', 'R23']},
 'theorem:13.3.1.1': {'reviewed': ['F247', 'F248', 'I370', 'I371', 'I372']}}


def build():
    return chapter.build(ID, CHAPTER, ITEMS=ITEMS, EXPECTED=EXPECTED, OUTSIDE=OUTSIDE, STATES=STATES,
                         DEVIATIONS=DEVIATIONS, ERRATA=ERRATA)
