"""D14: Chapter 14, `Ch14_Complements`, declaration by declaration: the expansion of C14's cards. The layout
and the checks are declarations.py's; the literals below are what this poster expects the sources to say at
MASULLO_COMMIT, and the build fails on any difference."""
import declarations

ID = "D14"
SLUG = "ch14-complements"
CHAPTER = "Ch14_Complements"

DECLS = {'text:14.2': ['private RiemannMasullo.meromorphicOrderAt_exp_sub_one',
               'private RiemannMasullo.meromorphicOrderAt_one_sub_exp',
               'private RiemannMasullo.meromorphicOrderAt_one_sub_exp_inv',
               'private RiemannMasullo.meromorphicOrderAt_one_sub_exp_inv_affine',
               'private RiemannMasullo.natCast_cpow_eq_exp',
               'private RiemannMasullo.meromorphicOrderAt_cpow_factor',
               'RiemannMasullo.curveZetaEulerFactor_prod_order',
               'private RiemannMasullo.finite_ringHom_of_adjoin',
               'private RiemannMasullo.finite_spec_hom_affineOpen',
               'private RiemannMasullo.finite_spec_hom',
               'RiemannMasullo.curveZeta_closedPointsOfDegree_finite',
               'RiemannMasullo.curveZetaClosedPointCount',
               'private RiemannMasullo.curveZetaStructMap',
               'private RiemannMasullo.curveZetaStructMap_spec',
               'private RiemannMasullo.curveZeta_structMap_comp_iff',
               'private RiemannMasullo.curveZeta_isClosed_of_residueFieldMap',
               'private RiemannMasullo.curveZeta_moduleFinite_residueField',
               'private RiemannMasullo.curveZeta_ringHomEquivAlgHom',
               'private RiemannMasullo.curveZeta_natCard_residueFieldMap',
               'private RiemannMasullo.curveZeta_natCard_fiberOfClosed',
               'private RiemannMasullo.curveZeta_dvd_finrank_of_fiber',
               'private RiemannMasullo.curveZeta_sigmaSubtypeEquiv',
               'private RiemannMasullo.curveZeta_fiberEquiv',
               'private RiemannMasullo.curveZeta_overEquiv',
               'RiemannMasullo.curveZeta_extensionPointCount',
               'private RiemannMasullo.curveZeta_closedPointsOfDegree_bound_of_weil_geom',
               'private RiemannMasullo.curveZeta_closedPointsOfDegree_bound_of_weil_geom_sqrt',
               'private RiemannMasullo.curveZeta_closedPointsOfDegree_bound_of_weil_aux',
               'RiemannMasullo.curveZeta_closedPointsOfDegree_bound_of_weil',
               'private RiemannMasullo.curveZeta_fromSpecResidueField_comp',
               'private RiemannMasullo.curveZeta_extensionPointCount_isOver_iff',
               'private RiemannMasullo.curveZeta_pointCount_weil_bound_of_eventually',
               'private RiemannMasullo.curveZeta_pointCount_weil_bound_exists_extension',
               'private RiemannMasullo.curveZeta_pointCount_weil_bound_of_points',
               'private RiemannMasullo.curveZeta_pointCount_weil_bound_chart',
               'private RiemannMasullo.curveZeta_pointCount_weil_bound_dim',
               'private RiemannMasullo.curveZeta_pointCount_weil_bound_outside',
               'private RiemannMasullo.curveZeta_pointCount_weil_bound_main',
               'RiemannMasullo.curveZeta_pointCount_weil_bound',
               'RiemannMasullo.curveZeta_closedPointsOfDegree_asymptotic'],
 'eq:14.2.0.1': ['RiemannMasullo.curveZetaEulerFactor',
                 'RiemannMasullo.curveZetaEulerProduct',
                 'private RiemannMasullo.closedPoint_residueField_card_pow',
                 'private RiemannMasullo.curveZetaEulerFactor_card_ringHom_finiteField_le',
                 'private RiemannMasullo.curveZetaEulerFactor_card_ringHom_mvPolynomial_le',
                 'private RiemannMasullo.curveZetaEulerFactor_card_ringHom_le_of_isIntegral',
                 'private RiemannMasullo.curveZetaEulerFactor_ringKrullDim_le_of_quasiFinite',
                 'private RiemannMasullo.curveZetaEulerFactor_ringKrullDim_le_of_isIntegral_of_injective',
                 'private '
                 'RiemannMasullo.curveZetaEulerFactor_ringKrullDim_le_one_of_isStandardSmoothOfRelativeDimension_one',
                 'private '
                 'RiemannMasullo.curveZetaEulerFactor_card_ringHom_le_of_isStandardSmoothOfRelativeDimension_one',
                 'private RiemannMasullo.curveZetaEulerFactor_specHom_affineOpen_injective',
                 'private RiemannMasullo.curveZetaEulerFactor_card_ringHom_chart',
                 'private RiemannMasullo.curveZetaEulerFactor_card_specHom_le',
                 'private RiemannMasullo.curveZetaEulerFactor_closedPointsOfDegree_le',
                 'private RiemannMasullo.curveZetaEulerFactor_summable_pow_deg',
                 'private RiemannMasullo.curveZetaEulerFactor_norm_inv_one_sub_sub_one_le',
                 'RiemannMasullo.summable_curveZetaEulerFactor_sub_one',
                 'RiemannMasullo.hasProd_curveZetaEulerProduct']}
DEVIATING = {'text:14.2': ['RiemannMasullo.curveZeta_closedPointsOfDegree_finite',
               'RiemannMasullo.curveZeta_extensionPointCount',
               'RiemannMasullo.curveZeta_closedPointsOfDegree_bound_of_weil',
               'RiemannMasullo.curveZeta_pointCount_weil_bound',
               'RiemannMasullo.curveZeta_closedPointsOfDegree_asymptotic'],
 'eq:14.2.0.1': ['RiemannMasullo.curveZetaEulerProduct', 'RiemannMasullo.hasProd_curveZetaEulerProduct']}


def build():
    return declarations.build(ID, CHAPTER, DECLS=DECLS, DEVIATING=DEVIATING)
