"""D13: Chapter 13, `Ch13_ZerosHecke`, declaration by declaration: the expansion of C13's cards. The layout
and the checks are declarations.py's; the literals below are what this poster expects the sources to say at
MASULLO_COMMIT, and the build fails on any difference."""
import declarations

ID = "D13"
SLUG = "ch13-zeroshecke"
CHAPTER = "Ch13_ZerosHecke"

DECLS = {'helpers:RiemannMasullo.Ch13_ZerosHecke.DirichletZeroDisplacement': ['private '
                                                                      'RiemannMasullo.dirichletZero_partial_sum_bound',
                                                                      'private '
                                                                      'RiemannMasullo.dirichletZero_abel_bound',
                                                                      'private '
                                                                      'RiemannMasullo.dirichletZero_norm_sq_sub',
                                                                      'private '
                                                                      'RiemannMasullo.dirichletZero_disk_chart',
                                                                      'RiemannMasullo.dirichletLFunction_finite_zero_product',
                                                                      'RiemannMasullo.dirichletLFunction_right_zero_displacement',
                                                                      'RiemannMasullo.dirichletLFunction_right_zero_displacement_at_one',
                                                                      'private '
                                                                      'RiemannMasullo.dirichletZero_norm_lower_bound_at_two',
                                                                      'RiemannMasullo.dirichletLFunction_right_zero_displacement_at_height'],
 'eq:13.3.1.1': ['RiemannMasullo.criticalTraceMultiplicity',
                 'RiemannMasullo.criticalTraceMultiplicity_of_degree_le'],
 'eq:13.3.1.2': ['private RiemannMasullo.criticalTraceMoment_isLinearMap_integrable',
                 'RiemannMasullo.criticalTraceMoment_isLinearMap',
                 'RiemannMasullo.criticalTraceTestSubmodule',
                 'private RiemannMasullo.mem_criticalTraceTestSubmodule_iff_expMoment',
                 'private RiemannMasullo.mem_criticalTraceTestSubmodule_iff_unitaryTwist',
                 'private RiemannMasullo.mem_criticalTraceTestSubmodule_iff_decomp',
                 'private RiemannMasullo.mem_criticalTraceTestSubmodule_iff_mellin',
                 'RiemannMasullo.mem_criticalTraceTestSubmodule_iff'],
 'theorem:13.3.1.1': ['private RiemannMasullo.criticalTrace_rat_sign',
                      'private RiemannMasullo.criticalTrace_exists_nonzero_moments',
                      'RiemannMasullo.criticalTraceTestSubmodule_rat_codimension_ge_two',
                      'RiemannMasullo.criticalTraceSpectral_converges',
                      'private RiemannMasullo.criticalTraceGeometric_converges_localData',
                      'RiemannMasullo.criticalTraceGeometric_converges_summable',
                      'RiemannMasullo.criticalTraceGeometric_converges_functional',
                      'RiemannMasullo.criticalTraceGeometric_converges',
                      'private RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests_vol',
                      'private RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests_cpow',
                      'private RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests_hasSum_congr',
                      'private RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests_mul_div',
                      'private RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests_val',
                      'private RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests_scale',
                      'RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests',
                      'RiemannMasullo.Printed.criticalTraceTestCodimension',
                      'RiemannMasullo.Printed.criticalTraceTestCodimension_false',
                      'RiemannMasullo.Printed.criticalTraceFormula',
                      'private RiemannMasullo.criticalTraceFormula_false_complex_bound_integrable',
                      'private RiemannMasullo.criticalTraceFormula_false_kernel_bound',
                      'private RiemannMasullo.criticalTraceFormula_false_complex_bound',
                      'private RiemannMasullo.criticalTraceFormula_false_complex_tendsto',
                      'private RiemannMasullo.criticalTraceFormula_false_smoothed_shells',
                      'private RiemannMasullo.criticalTraceFormula_false_radial',
                      'private RiemannMasullo.criticalTraceFormula_false_radial_difference',
                      'private RiemannMasullo.criticalTraceFormula_false_shell_measure',
                      'private RiemannMasullo.norm_adicCompletion_eq_zpow_small',
                      'private RiemannMasullo.criticalTraceFormula_false_exists_shell',
                      'private RiemannMasullo.criticalTraceFormula_false_radial_shells',
                      'private RiemannMasullo.criticalTraceFormula_false_finite_pv',
                      'private RiemannMasullo.criticalTraceFormula_false_odd_shell',
                      'private RiemannMasullo.criticalTraceFormula_false_odd_weight',
                      'private RiemannMasullo.criticalTraceFormula_false_prime_powers',
                      'private RiemannMasullo.criticalTraceFormula_false_norm_prime',
                      'private RiemannMasullo.criticalTraceFormula_false_fiber_weight',
                      'private RiemannMasullo.criticalTraceFormula_false_group_norms',
                      'RiemannMasullo.criticalTraceFormula_gaussian_prime_power_regroup',
                      'RiemannMasullo.criticalTraceFormula_gaussian_shell_comparison',
                      'private RiemannMasullo.criticalTraceFormula_false_polar',
                      'private RiemannMasullo.criticalTraceFormula_false_limit',
                      'private RiemannMasullo.criticalTraceFormula_false_gaussian_degree',
                      'RiemannMasullo.Printed.criticalTraceFormula_false']}
DEVIATING = {'eq:13.3.1.2': ['RiemannMasullo.criticalTraceTestSubmodule'],
 'theorem:13.3.1.1': ['RiemannMasullo.criticalTraceTestSubmodule_rat_codimension_ge_two',
                      'RiemannMasullo.criticalTraceSpectral_converges',
                      'RiemannMasullo.hasSum_fullDivisor_on_criticalTraceTests']}


def build():
    return declarations.build(ID, CHAPTER, DECLS=DECLS, DEVIATING=DEVIATING)
