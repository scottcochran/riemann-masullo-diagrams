"""DL: ForMathlib, `ForMathlib`, declaration by declaration: the expansion of L1's cards. The layout
and the checks are declarations.py's; the literals below are what this poster expects the sources to say at
MASULLO_COMMIT, and the build fails on any difference."""
import declarations

ID = "DL"
SLUG = "formathlib"
CHAPTER = "ForMathlib"

DECLS = {'file:RiemannMasullo/ForMathlib/Algebra/Module/ZLattice/Quotient.lean': ['RiemannMasullo.exists_euclidean_torus_quotient',
                                                                          'RiemannMasullo.exists_real_torus_equiv_of_open_vector_range'],
 'file:RiemannMasullo/ForMathlib/Algebra/Module/ZLattice/Summable.lean': ['RiemannMasullo.summable_lattice_exp_neg_mul_norm',
                                                                          'private '
                                                                          'RiemannMasullo.summable_pullback_finite_kernel',
                                                                          'RiemannMasullo.summable_exp_neg_mul_norm_of_isProperMap'],
 'file:RiemannMasullo/ForMathlib/Algebra/Polynomial/HasseDeriv.lean': ['RiemannMasullo.Polynomial.mul_card_le_natDegree_of_hasseDeriv',
                                                                       'RiemannMasullo.Polynomial.coeff_pow_expChar_pow_eq_zero',
                                                                       'RiemannMasullo.Polynomial.eval_hasseDeriv_mul_pow_expChar'],
 'file:RiemannMasullo/ForMathlib/AlgebraicGeometry/CurvePoints.lean': ['RiemannMasullo.sectionsAlgebra',
                                                                       'RiemannMasullo.SpecMap_sectionsAlgebra',
                                                                       'RiemannMasullo.isDomain_tensor_of_isIntegral_pullback',
                                                                       'RiemannMasullo.card_points_affineOpen',
                                                                       'RiemannMasullo.finite_compl_of_ringKrullDim_le_one'],
 'file:RiemannMasullo/ForMathlib/AlgebraicGeometry/SmoothCurve.lean': ['RiemannMasullo.isPrincipalIdealRing_mvPolynomial_fin_one',
                                                                       'RiemannMasullo.isDomain_stalk_of_smoothOfRelativeDimension_one',
                                                                       'RiemannMasullo.irreducibleSpace_of_isDomain_stalk',
                                                                       'RiemannMasullo.isIntegral_of_smoothOfRelativeDimension_one'],
 'file:RiemannMasullo/ForMathlib/Analysis/Calculus/ContDiff/LineDeriv.lean': ['private '
                                                                              'RiemannMasullo.hasFDerivAt_coordinates_of_hasDerivAt_lines',
                                                                              'RiemannMasullo.contDiff_family_of_hasDerivAt_lines'],
 'file:RiemannMasullo/ForMathlib/Analysis/Calculus/Deriv/Weak.lean': ['private RiemannMasullo.scalar_slope_error',
                                                                      'RiemannMasullo.exists_hasDerivAt_eval_zero_of_contDiff'],
 'file:RiemannMasullo/ForMathlib/Analysis/Calculus/FDeriv/Partial.lean': ['private '
                                                                          'RiemannMasullo.isLittleO_line_increment',
                                                                          'RiemannMasullo.hasFDerivAt_of_continuous_coordinate_derivatives'],
 'file:RiemannMasullo/ForMathlib/Analysis/Calculus/FDeriv/Symmetric.lean': ['RiemannMasullo.iteratedFDeriv_apply_list_perm'],
 'file:RiemannMasullo/ForMathlib/Analysis/Calculus/IteratedDeriv/ExponentialWeight.lean': ['RiemannMasullo.norm_iteratedDeriv_exp_smul_le'],
 'file:RiemannMasullo/ForMathlib/Analysis/Calculus/IteratedDeriv/UnitCube.lean': ['private '
                                                                                  'RiemannMasullo.sum_norm_at_different_times',
                                                                                  'private '
                                                                                  'RiemannMasullo.sum_norm_cube',
                                                                                  'RiemannMasullo.listDerivative',
                                                                                  'private '
                                                                                  'RiemannMasullo.listDerivative_smooth',
                                                                                  'private '
                                                                                  'RiemannMasullo.listDerivative_cons',
                                                                                  'RiemannMasullo.listDerivative_prod',
                                                                                  'RiemannMasullo.listDerivative_comp_linear',
                                                                                  'private '
                                                                                  'RiemannMasullo.listDerivative_continuous',
                                                                                  'private '
                                                                                  'RiemannMasullo.hasDerivAt_listDerivative',
                                                                                  'private '
                                                                                  'RiemannMasullo.cube_affine_update',
                                                                                  'RiemannMasullo.sum_norm_of_cube_bounds'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/Blaschke.lean': ['private '
                                                                   'RiemannMasullo.finite_sum_le_finsum_of_nonneg',
                                                                   'private '
                                                                   'RiemannMasullo.disk_divisor_finite_log_sum_le',
                                                                   'RiemannMasullo.disk_divisor_summable_one_sub_norm',
                                                                   'RiemannMasullo.disk_zero_orders_and_summability',
                                                                   'RiemannMasullo.stripBlaschkeToDisk',
                                                                   'RiemannMasullo.stripBlaschkeFromDisk',
                                                                   'private RiemannMasullo.diskCayley_re_pos',
                                                                   'private RiemannMasullo.diskInverseCayley_mem',
                                                                   'private RiemannMasullo.stripBlaschke_phase',
                                                                   'RiemannMasullo.stripBlaschkeToDisk_mem',
                                                                   'private '
                                                                   'RiemannMasullo.stripBlaschkeFromDisk_mem',
                                                                   'RiemannMasullo.stripBlaschkeFromDisk_mem_strip',
                                                                   'private RiemannMasullo.stripBlaschke_cancel',
                                                                   'RiemannMasullo.stripBlaschkeFromDisk_toDisk',
                                                                   'RiemannMasullo.stripBlaschkeToDisk_fromDisk',
                                                                   'private '
                                                                   'RiemannMasullo.stripBlaschkeFromDisk_analytic_deriv',
                                                                   'RiemannMasullo.stripBlaschkeFromDisk_analyticAt_deriv_ne_zero',
                                                                   'RiemannMasullo.stripBlaschke_disk_zero_orders',
                                                                   'RiemannMasullo.verticalStrip_divisor_blaschke',
                                                                   'RiemannMasullo.stripBlaschkeToDisk_analytic',
                                                                   'RiemannMasullo.natCast_le_analyticOrderAt_comp',
                                                                   'private RiemannMasullo.Blaschke.rotation',
                                                                   'private RiemannMasullo.Blaschke.rotation_norm',
                                                                   'private RiemannMasullo.Blaschke.rotation_mul',
                                                                   'private RiemannMasullo.Blaschke.factor',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_den_closed',
                                                                   'private RiemannMasullo.Blaschke.den_ne',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_norm_sq_gap',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_contracts',
                                                                   'private RiemannMasullo.Blaschke.factor_close',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_analytic',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.norm_mul_sub_one',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.norm_pow_sub_one',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.norm_prod_sub_one',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.product_uniform',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.product_analytic',
                                                                   'private RiemannMasullo.Blaschke.product_bound',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_continuousOn_closed',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_boundary',
                                                                   'RiemannMasullo.Blaschke.normalizedFactor',
                                                                   'RiemannMasullo.Blaschke.normalizedFactor_apply',
                                                                   'RiemannMasullo.Blaschke.product',
                                                                   'RiemannMasullo.Blaschke.finiteProduct',
                                                                   'RiemannMasullo.Blaschke.tail',
                                                                   'RiemannMasullo.Blaschke.analyticOnNhd_product',
                                                                   'RiemannMasullo.Blaschke.analyticOnNhd_tail',
                                                                   'RiemannMasullo.Blaschke.norm_tail_le_one',
                                                                   'RiemannMasullo.Blaschke.finiteProduct_inner',
                                                                   'RiemannMasullo.Blaschke.product_subtype_mem',
                                                                   'private RiemannMasullo.Blaschke.factorUnit',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_unit_decomposition',
                                                                   'private RiemannMasullo.Blaschke.factor_unit_ne',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.factor_unit_analytic',
                                                                   'RiemannMasullo.Blaschke.product_ne_zero',
                                                                   'RiemannMasullo.Blaschke.finiteProduct_mul_tail',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.product_extract_factor',
                                                                   'private '
                                                                   'RiemannMasullo.Blaschke.product_divisible',
                                                                   'RiemannMasullo.Blaschke.analyticOrderAt_product',
                                                                   'RiemannMasullo.Blaschke.tendsto_tail',
                                                                   'RiemannMasullo.Blaschke.exists_holomorphic_disk_tails',
                                                                   'RiemannMasullo.Blaschke.norm_tail_sub_one_le',
                                                                   'RiemannMasullo.Blaschke.tendstoLocallyUniformlyOn_tail',
                                                                   'RiemannMasullo.Blaschke.exists_holomorphic_disk_tails_bound'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/BlaschkeBoundary.lean': ['private '
                                                                           'RiemannMasullo.Blaschke.normalizedFactor_eq_const_mul',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.normalizedFactor_boundary',
                                                                           'RiemannMasullo.Blaschke.finiteProduct_logDeriv_sphere',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.stripExp',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.stripExp_norm',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.stripExp_boundary',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.stripExp_re_pos',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.stripChart_boundary',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.norm_deriv_stripChart_boundary',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.disk_boundary_deriv',
                                                                           'RiemannMasullo.Blaschke.stripFiniteProduct_hasDerivAt_outward',
                                                                           'RiemannMasullo.Blaschke.stripFiniteProduct_hasDerivAt_norm_sq_gap',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.poissonKernel_cayley_boundary',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.strip_poissonKernel_eq_halfPlane',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.kernel_bound_of_separated_radii',
                                                                           'RiemannMasullo.Blaschke.strip_poissonKernel_le_exp_height',
                                                                           'RiemannMasullo.Blaschke.stripBoundaryPoissonKernel',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.stripBoundaryPoissonKernel_eq',
                                                                           'RiemannMasullo.Blaschke.stripBoundaryPoissonKernel_mass_bound',
                                                                           'private '
                                                                           'RiemannMasullo.Blaschke.integrable_poly_exp_abs',
                                                                           'RiemannMasullo.Blaschke.stripBoundaryPoissonKernel_moment_bound',
                                                                           'RiemannMasullo.Blaschke.stripBoundaryPoissonKernel_test_bound'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/BlaschkeFactorization.lean': ['RiemannMasullo.Blaschke.disk_inner_multiplier_bound',
                                                                                'private '
                                                                                'RiemannMasullo.Blaschke.exists_analytic_quotient_of_order_le',
                                                                                'private '
                                                                                'RiemannMasullo.Blaschke.exists_analytic_zero_free_quotient',
                                                                                'private '
                                                                                'RiemannMasullo.Blaschke.bound_of_blaschke_mul',
                                                                                'RiemannMasullo.Blaschke.exists_bounded_analytic_blaschke_quotient',
                                                                                'RiemannMasullo.Blaschke.zeroProduct',
                                                                                'RiemannMasullo.Blaschke.exists_canonical_disk_factorization',
                                                                                'RiemannMasullo.Blaschke.exists_bounded_finite_blaschke_quotient',
                                                                                'RiemannMasullo.Blaschke.exists_tail_test_quotient'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/CoveringMap.lean': ['RiemannMasullo.exists_complexPowerCylinder'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/ExpSumUniqueness.lean': ['private '
                                                                           'RiemannMasullo.expSum_range_closed_countable',
                                                                           'private '
                                                                           'RiemannMasullo.expSum_norm_div_le',
                                                                           'private RiemannMasullo.expSum_aux_dist',
                                                                           'private '
                                                                           'RiemannMasullo.expSum_resolvent_eq_zero',
                                                                           'private '
                                                                           'RiemannMasullo.expSum_resolvent_differentiableOn',
                                                                           'RiemannMasullo.eq_zero_of_hasSum_exp_eq_zero'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/Hadamard.lean': ['private '
                                                                   'RiemannMasullo.norm_le_rpow_on_closedStrip',
                                                                   'RiemannMasullo.isBigO_rpow_verticalStrip_interpolate',
                                                                   'RiemannMasullo.isBigO_pow_verticalStrip_of_exp'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/LandauLemma.lean': ['RiemannMasullo.landauConstant',
                                                                      'RiemannMasullo.landauConstant_pos',
                                                                      'RiemannMasullo.landauConstant_div',
                                                                      'RiemannMasullo.finite_zeros_closedBall',
                                                                      'private '
                                                                      'RiemannMasullo.landau_exists_gt_analyticOnNhd',
                                                                      'private '
                                                                      'RiemannMasullo.landau_analyticOrderNatAt_eq_zero',
                                                                      'private '
                                                                      'RiemannMasullo.landau_finsum_mem_eq_sum',
                                                                      'private RiemannMasullo.landau_dist_rescale',
                                                                      'private '
                                                                      'RiemannMasullo.landau_mem_closedBall_rescale',
                                                                      'private RiemannMasullo.landau_rescale_inv',
                                                                      'private '
                                                                      'RiemannMasullo.landau_analyticOnNhd_rescale',
                                                                      'private '
                                                                      'RiemannMasullo.landau_analyticOrderNatAt_rescale',
                                                                      'private '
                                                                      'RiemannMasullo.landau_logDeriv_rescale',
                                                                      'private '
                                                                      'RiemannMasullo.landau_sum_zeros_rescale',
                                                                      'private '
                                                                      'RiemannMasullo.landau_setOfZeros_rescale_finite',
                                                                      'private '
                                                                      'RiemannMasullo.landau_finsum_eq_sum_zeros',
                                                                      'RiemannMasullo.landau_sum_analyticOrderNatAt_le',
                                                                      'RiemannMasullo.landau_norm_logDeriv_sub_le',
                                                                      'RiemannMasullo.landauConstant_quarter_le',
                                                                      'RiemannMasullo.landau_norm_logDeriv_sub_le_of_radius',
                                                                      'private RiemannMasullo.landau_neg_re_le_aux',
                                                                      'RiemannMasullo.landau_neg_re_logDeriv_le',
                                                                      'RiemannMasullo.landau_neg_re_logDeriv_le_of_forall_re_le',
                                                                      'RiemannMasullo.landau_neg_re_logDeriv_le_of_zero',
                                                                      'private RiemannMasullo.landau_pole_logDeriv',
                                                                      'RiemannMasullo.landau_pole_norm_logDeriv_sub_le',
                                                                      'RiemannMasullo.landau_pole_neg_re_logDeriv_le'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/Liouville.lean': ['RiemannMasullo.exists_eq_const_mul_exp_of_norm_add_mul_I'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/PeriodicStrip.lean': ['private '
                                                                        'RiemannMasullo.exists_sphere_norm_pos',
                                                                        'RiemannMasullo.bddAbove_strip_of_periodic_mul',
                                                                        'RiemannMasullo.norm_bounded_on_strip_of_imaginary_period'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/PhragmenLindelof.lean': ['RiemannMasullo.norm_pow_mul_le_on_verticalStrip'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/RectangleIntegral.lean': ['RiemannMasullo.rectangleIntegral',
                                                                            'RiemannMasullo.rectangleIntegral_eq',
                                                                            'private '
                                                                            'RiemannMasullo.horizontal_mapsTo_boundary',
                                                                            'private '
                                                                            'RiemannMasullo.vertical_mapsTo_boundary',
                                                                            'private '
                                                                            'RiemannMasullo.intervalIntegrable_comp_boundary',
                                                                            'RiemannMasullo.rectangleIntegral_congr_off_countable',
                                                                            'RiemannMasullo.rectangleIntegral_add',
                                                                            'RiemannMasullo.rectangleIntegral_finsetSum',
                                                                            'RiemannMasullo.rectangleIntegral_const_mul',
                                                                            'private '
                                                                            'RiemannMasullo.integral_log_deriv',
                                                                            'private '
                                                                            'RiemannMasullo.log_neg_of_im_pos',
                                                                            'private '
                                                                            'RiemannMasullo.log_neg_of_im_neg',
                                                                            'private '
                                                                            'RiemannMasullo.hasDerivAt_horizontal',
                                                                            'private '
                                                                            'RiemannMasullo.hasDerivAt_vertical',
                                                                            'RiemannMasullo.rectangleIntegral_sub_inv',
                                                                            'private '
                                                                            'RiemannMasullo.integral_zpow_deriv',
                                                                            'RiemannMasullo.rectangleIntegral_sub_zpow_of_ne'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/StripMultiplier.lean': ['RiemannMasullo.integral_energy_le_of_diagonal',
                                                                          'RiemannMasullo.re_sq_sub_sq',
                                                                          'RiemannMasullo.re_sq_sub_sq_pos',
                                                                          'RiemannMasullo.hasDerivAt_inv_sq_sub_sq',
                                                                          'RiemannMasullo.norm_deriv_inv_sq_sub_sq_le_re'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/StripReciprocal.lean': ['private '
                                                                          'RiemannMasullo.stripReciprocal_disk_harnack',
                                                                          'private '
                                                                          'RiemannMasullo.stripReciprocal_cayley_gap',
                                                                          'private '
                                                                          'RiemannMasullo.stripReciprocal_chart_gap',
                                                                          'RiemannMasullo.stripReciprocal_log_growth',
                                                                          'RiemannMasullo.stripReciprocalCutoff',
                                                                          'RiemannMasullo.stripReciprocalCutoff_analytic',
                                                                          'private '
                                                                          'RiemannMasullo.stripReciprocal_real_cos',
                                                                          'private '
                                                                          'RiemannMasullo.stripReciprocalCutoff_norm',
                                                                          'private '
                                                                          'RiemannMasullo.stripReciprocal_cosh_lower',
                                                                          'RiemannMasullo.stripReciprocalCutoff_decay',
                                                                          'RiemannMasullo.stripReciprocalCutoff_norm_le_one',
                                                                          'RiemannMasullo.stripReciprocalCutoff_tendsto_compact',
                                                                          'private '
                                                                          'RiemannMasullo.stripReciprocal_dominate',
                                                                          'RiemannMasullo.stripReciprocal_regularized_decay',
                                                                          'RiemannMasullo.stripReciprocal_regularized_analytic',
                                                                          'RiemannMasullo.stripReciprocal_regularized_tendsto',
                                                                          'private '
                                                                          'RiemannMasullo.stripReciprocal_iteratedDeriv_estimate',
                                                                          'RiemannMasullo.stripReciprocal_regularized_iteratedDeriv_decay',
                                                                          'RiemannMasullo.stripReciprocal_exists_frequency'],
 'file:RiemannMasullo/ForMathlib/Analysis/Complex/VerticalCauchyIntegral.lean': ['private '
                                                                                 'RiemannMasullo.tendsto_symmetric_cauchy_inv',
                                                                                 'private '
                                                                                 'RiemannMasullo.tendsto_dslope_vertical',
                                                                                 'private '
                                                                                 'RiemannMasullo.tendsto_horizontal_dslope',
                                                                                 'RiemannMasullo.verticalCauchyIntegral_sub_eq',
                                                                                 'RiemannMasullo.hasDerivAt_verticalCauchyIntegral',
                                                                                 'RiemannMasullo.verticalCauchy_lpBound'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/ContDiffMapSupportedIn.lean': ['RiemannMasullo.supportedToSchwartzCLM'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzJetClosure.lean': ['private '
                                                                                  'RiemannMasullo.lineProfile_bounded_chain',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_bounded_terms',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_bounded_multijets',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_finite_jet_closure',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_jet',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_jet_apply',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_coordinate_jet',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_pullMul',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_schwartz_bounded_multijets',
                                                                                  'private '
                                                                                  'RiemannMasullo.lineProfile_schwartz_jet_closure',
                                                                                  'RiemannMasullo.schwartzMap_mem_closedSubmodule_of_vanishing_jets'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/Basic.lean': ['RiemannMasullo.schwartz_pullback_bounded',
                                                                                   'RiemannMasullo.schwartz_unit_pullbacks'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/ChangeOfVariables.lean': ['private '
                                                                                               'RiemannMasullo.continuous_of_bounded_evaluations',
                                                                                               'RiemannMasullo.seminorm_comp_changeOfVariables',
                                                                                               'RiemannMasullo.continuous_schwartz_comp_family'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/ChangeVariables.lean': ['RiemannMasullo.schwartzChangeVariable'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/Complete.lean': ['private '
                                                                                      'RiemannMasullo.schwartz_iteratedFDeriv_sub',
                                                                                      'private '
                                                                                      'RiemannMasullo.schwartz_cauchy_tail',
                                                                                      'private '
                                                                                      'RiemannMasullo.schwartz_limit_taylor',
                                                                                      'private '
                                                                                      'RiemannMasullo.schwartz_uniform_limits',
                                                                                      'RiemannMasullo.completeSpace_schwartzMap'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/Gaussian.lean': ['private '
                                                                                      'SchwartzMap.expNegCutoff',
                                                                                      'SchwartzMap.gaussian',
                                                                                      'SchwartzMap.gaussian_apply'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/Grid.lean': ['private '
                                                                                  'RiemannMasullo.norm_iteratedDeriv_le_of_zero_jets',
                                                                                  'RiemannMasullo.schwartz_grid_estimate'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/Montel.lean': ['private '
                                                                                    'RiemannMasullo.compactifiedSchwartz',
                                                                                    'private '
                                                                                    'RiemannMasullo.compactifiedSchwartz_equicontinuous',
                                                                                    'private '
                                                                                    'RiemannMasullo.isCompact_closure_compactifiedSchwartz',
                                                                                    'private '
                                                                                    'RiemannMasullo.schwartzWeightedDeriv',
                                                                                    'private '
                                                                                    'RiemannMasullo.schwartzWeightedDeriv_apply',
                                                                                    'private '
                                                                                    'RiemannMasullo.schwartzCoordinates',
                                                                                    'private '
                                                                                    'RiemannMasullo.norm_schwartzCoordinates',
                                                                                    'private '
                                                                                    'RiemannMasullo.isUniformInducing_schwartzCoordinates',
                                                                                    'RiemannMasullo.schwartzMap_real_montel',
                                                                                    'RiemannMasullo.schwartz_compactified_bounded'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/TranslationDifference.lean': ['private '
                                                                                                   'RiemannMasullo.forwardTail',
                                                                                                   'private '
                                                                                                   'RiemannMasullo.tailWeight_summable',
                                                                                                   'private '
                                                                                                   'RiemannMasullo.forwardTail_bound',
                                                                                                   'private '
                                                                                                   'RiemannMasullo.forwardTail_local_bound',
                                                                                                   'private '
                                                                                                   'RiemannMasullo.forwardTail_smooth',
                                                                                                   'private '
                                                                                                   'RiemannMasullo.forwardTail_decay',
                                                                                                   'private '
                                                                                                   'RiemannMasullo.forwardTail_schwartz_of_zero_sum',
                                                                                                   'RiemannMasullo.schwartzOrbitPrimitive',
                                                                                                   'RiemannMasullo.schwartzGeometricTranslates'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/SchwartzSpace/WeightedIntegral.lean': ['RiemannMasullo.SchwartzMap.exists_strongDual_integral_mul',
                                                                                              'RiemannMasullo.integrable_abs_log_norm_div_one_add_norm_pow'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/TestFunction.lean': ['RiemannMasullo.isEmbedding_testFunction_ofSupportedIn'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/TestFunction/CoordinatePlane.lean': ['RiemannMasullo.testFunction_vanishes_off_dsupport',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.exists_factor_of_trace_bound',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.distribution_of_compact_trace_bound',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.flat_jet_bound',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.trace_normal_cutoff_bound',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.tubeCutoff',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.trace_vanishes_of_flat_plane',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedOnCompacts',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.directional',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.directional_smooth',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_loc',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_mono',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedOnCompacts_add',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedOnCompacts_mul_fixed',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_zero',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_add',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_fixed_smul',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_finsum',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_iterated_eval',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_iterated_norm',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearAverage',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearAverage_smooth',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearAverage_integrationByParts',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearProjection',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearAverage_deriv',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.weightMul',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.weightDerivative',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearAverage_loc',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearCoordinateWeight',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearAverage_direction',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.shearAverage_boundedDerivs',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.normalMonomial',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.normalMonomial_cons',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.normalMonomial_smooth',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.normalMonomialTerms',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.normalMonomialTerms_length',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.normalMonomial_deriv',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_list',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_weighted_shearAverage',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_loc',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_mono',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_of_boundedDerivs',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedOnCompacts_sub',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_sub',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_add',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_smul_const',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_sum',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_restrict',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.scaleNormal',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.radialAverage',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.radialAverage_smooth',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.trace_interval_direction',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.radialAverage_integral_deriv',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.radialAverage_directional',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.radialAverage_loc',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_radial',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.trace_radial_eq_sub',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.smoothScalar',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.smoothScalar_contDiff',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.mulNormalMonomial',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.planeRestriction',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.bounded_action_of_boundedPlaneJet',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.vanishing_product_jet',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedDerivs_comp_linear',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.traceCutTest',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.distribution_bounded_on_sequence',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.compact_trace_estimate_of_sequences',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.splitCoordinates',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.trace_coord_direction',
                                                                                            'private '
                                                                                            'RiemannMasullo.CoordinatePlane.boundedPlaneJet_of_coordinate_bounds',
                                                                                            'RiemannMasullo.CoordinatePlane.exists_orderZero_coefficients'],
 'file:RiemannMasullo/ForMathlib/Analysis/Distribution/TestFunction/Schwartz.lean': ['RiemannMasullo.isClosedEmbedding_supportedToSchwartzCLM',
                                                                                     'RiemannMasullo.testFunction_complex_polynormable',
                                                                                     'RiemannMasullo.completeSpace_testFunction',
                                                                                     'RiemannMasullo.testFunctionToSchwartzCLM',
                                                                                     'RiemannMasullo.schwartzToTestFunctionMulCLM',
                                                                                     'RiemannMasullo.schwartzToTestFunctionMulCLM_apply'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/AbelLimit.lean': ['private '
                                                                    'RiemannMasullo.poissonRadialDerivative',
                                                                    'private '
                                                                    'RiemannMasullo.integrable_poissonRadialWeight',
                                                                    'private '
                                                                    'RiemannMasullo.integral_poissonRadialDerivative',
                                                                    'private RiemannMasullo.poissonRadial_mixture',
                                                                    'private '
                                                                    'RiemannMasullo.poisson_average_bounded',
                                                                    'private RiemannMasullo.halfPlanePoissonKernel',
                                                                    'private '
                                                                    'RiemannMasullo.halfPlanePoissonKernel_eq',
                                                                    'private '
                                                                    'RiemannMasullo.halfPlanePoissonKernel_ae_norm',
                                                                    'private RiemannMasullo.halfPlaneAbelTest',
                                                                    'private RiemannMasullo.halfPlaneAbelTest_norm',
                                                                    'private RiemannMasullo.integrable_exp_neg_abs',
                                                                    'private RiemannMasullo.halfPlaneAbelTest_mem',
                                                                    'private '
                                                                    'RiemannMasullo.fourier_halfPlaneAbelTest',
                                                                    'RiemannMasullo.fourier_L2_abel_limit',
                                                                    'RiemannMasullo.integral_cexp_mul_inv_one_add_sq'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/AddCircleMulti.lean': ['RiemannMasullo.exists_dual_apply_eq_integral_of_montel',
                                                                         'RiemannMasullo.torus_mem_closedSpan_fourier',
                                                                         'RiemannMasullo.mFourierCoeff_add_left'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/CompactGroup.lean': ['RiemannMasullo.norm_sq_toLp_two',
                                                                       'private '
                                                                       'RiemannMasullo.integral_character_pair_zero',
                                                                       'RiemannMasullo.integral_character_pair',
                                                                       'RiemannMasullo.ae_eq_zero_of_character_integral_eq_zero',
                                                                       'RiemannMasullo.sum_sq_character_integral_le',
                                                                       'RiemannMasullo.sum_sq_character_integral_prod_le',
                                                                       'private '
                                                                       'RiemannMasullo.exists_character_hilbertBasis',
                                                                       'RiemannMasullo.tsum_sq_character_integral_prod'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/FourierPhase.lean': ['RiemannMasullo.hasDerivAt_integral_fourier_phase'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/Integrable.lean': ['RiemannMasullo.fourier_L2_coeFn_of_integrable'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/Log.lean': ['private RiemannMasullo.cauchy',
                                                              'private RiemannMasullo.cauchy_sub_integrals',
                                                              'private RiemannMasullo.integrable_log_mul_schwartz',
                                                              'private RiemannMasullo.log_fourier_integrable',
                                                              'private RiemannMasullo.log_pairing_eq_cauchy',
                                                              'private RiemannMasullo.laplaceProfile',
                                                              'private RiemannMasullo.laplaceProfile_eq_abelTest',
                                                              'private RiemannMasullo.laplaceProfile_integrable',
                                                              'private RiemannMasullo.fourier_laplaceProfile',
                                                              'private RiemannMasullo.cauchy_pairing_eq_laplace',
                                                              'private '
                                                              'RiemannMasullo.cauchy_sub_pairing_eq_laplace',
                                                              'private '
                                                              'RiemannMasullo.integrable_div_abs_of_local_bound',
                                                              'private RiemannMasullo.laplace_scale_integral',
                                                              'private RiemannMasullo.laplace_integral_eq_half',
                                                              'private RiemannMasullo.unitSubtraction',
                                                              "private RiemannMasullo.integrable_comp_abs'",
                                                              'private RiemannMasullo.abs_log_cauchy',
                                                              'private RiemannMasullo.laplace_log_fourier_contact',
                                                              'private RiemannMasullo.log_exp_weight',
                                                              'private RiemannMasullo.signed_tail_slice',
                                                              'private RiemannMasullo.exp_subtraction',
                                                              'private '
                                                              'RiemannMasullo.laplace_unitSubtraction_contact',
                                                              'private RiemannMasullo.remainder_div_integrable',
                                                              'private RiemannMasullo.fourier_remainder_add',
                                                              'private RiemannMasullo.unitSubtraction_eq_remainder',
                                                              'private RiemannMasullo.integrableOn_div_abs_cutoff',
                                                              'private RiemannMasullo.annulus_integral_inv_abs',
                                                              'private RiemannMasullo.cutoff_eq_unitSubtraction',
                                                              'private RiemannMasullo.tendsto_integral_abs_cutoff',
                                                              'private RiemannMasullo.real_log_fourier_of_zero',
                                                              'private '
                                                              'RiemannMasullo.real_log_fourier_unit_subtraction',
                                                              'RiemannMasullo.real_log_fourier_cutoff'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/LpSpace.lean': ['RiemannMasullo.memLp_two_fourier_and_eLpNorm_eq'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/PaleyWiener.lean': ['private RiemannMasullo.halfLaplace',
                                                                      'private RiemannMasullo.LaplaceRates',
                                                                      'private RiemannMasullo.laplace_norm',
                                                                      'private RiemannMasullo.laplace_integrable',
                                                                      'private RiemannMasullo.halfLaplace_diff',
                                                                      'private RiemannMasullo.laplaceRates_l2',
                                                                      'private RiemannMasullo.laplaceRates_growth',
                                                                      'private '
                                                                      'RiemannMasullo.rotate_integral_of_decay',
                                                                      'private RiemannMasullo.laplace_rotate',
                                                                      'private RiemannMasullo.damp',
                                                                      'private RiemannMasullo.damp_integrable',
                                                                      'private RiemannMasullo.damp_memLp',
                                                                      'private RiemannMasullo.abelIntegral',
                                                                      'private RiemannMasullo.abelIntegral_tendsto',
                                                                      'private '
                                                                      'RiemannMasullo.ae_eq_of_schwartz_pairing',
                                                                      'private RiemannMasullo.fourier_L2_ae',
                                                                      'private RiemannMasullo.dampingRate',
                                                                      'private RiemannMasullo.dampingRate_pos',
                                                                      'private RiemannMasullo.damp_tendsto_L2',
                                                                      'private '
                                                                      'RiemannMasullo.fourier_damp_tendsto_zero',
                                                                      'private '
                                                                      'RiemannMasullo.fourier_trace_support',
                                                                      'private RiemannMasullo.intervalExtension',
                                                                      'private RiemannMasullo.kernel_bound',
                                                                      'private '
                                                                      'RiemannMasullo.intervalExtension_bound',
                                                                      'private '
                                                                      'RiemannMasullo.intervalExtension_diff',
                                                                      'private '
                                                                      'RiemannMasullo.intervalExtension_real',
                                                                      'private RiemannMasullo.memLp_dilate',
                                                                      'RiemannMasullo.paleyWiener_interval'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/PoissonSummation.lean': ['RiemannMasullo.schwartz_contDiff_periodization',
                                                                           'RiemannMasullo.summable_norm_fourier_int_of_isBigO',
                                                                           'RiemannMasullo.integral_periodization_mul_exp_int',
                                                                           'private '
                                                                           'RiemannMasullo.sum_exp_int_mul_sub_one',
                                                                           'private '
                                                                           'RiemannMasullo.fourier_indicator_eq_integral_exp',
                                                                           'RiemannMasullo.tendsto_symmetric_fourier_integrals_of_integrable_quotient',
                                                                           'private '
                                                                           'RiemannMasullo.exists_radius_avoiding_shifted_finite',
                                                                           'RiemannMasullo.periodization_bounds_of_exp_decay'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/StripLaplace.lean': ['RiemannMasullo.bilateralLaplace',
                                                                       'RiemannMasullo.aestronglyMeasurable_of_exp_abs_smul',
                                                                       'RiemannMasullo.integrable_exp_neg_mul_abs',
                                                                       'RiemannMasullo.integrable_mul_cexp_of_memLp_exp_abs',
                                                                       'RiemannMasullo.memLp_mul_exp_of_memLp_exp_abs',
                                                                       'private '
                                                                       'RiemannMasullo.hasDerivAt_bilateralLaplace_bound',
                                                                       'RiemannMasullo.hasDerivAt_bilateralLaplace',
                                                                       'RiemannMasullo.differentiableOn_bilateralLaplace',
                                                                       'private '
                                                                       'RiemannMasullo.bilateralLaplace_line_eq_fourier',
                                                                       'RiemannMasullo.integrable_norm_sq_bilateralLaplace',
                                                                       'RiemannMasullo.integral_norm_sq_bilateralLaplace',
                                                                       'RiemannMasullo.lintegral_enorm_sq_bilateralLaplace',
                                                                       'RiemannMasullo.memLp_exp_abs_smul_id_mul',
                                                                       'RiemannMasullo.deriv_bilateralLaplace',
                                                                       'RiemannMasullo.integral_norm_sq_deriv_bilateralLaplace',
                                                                       'RiemannMasullo.lintegral_enorm_sq_deriv_bilateralLaplace',
                                                                       'RiemannMasullo.lintegral_strip_enorm_sq_deriv_bilateralLaplace',
                                                                       'RiemannMasullo.lintegral_strip_enorm_sq_bilateralLaplace',
                                                                       'RiemannMasullo.lintegral_strip_enorm_sq_add_deriv_bilateralLaplace'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/ThetaLattice.lean': ['private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_integral_sum_dilates',
                                                                       'private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_sum_weights_le',
                                                                       'private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_finite_dilates',
                                                                       'private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_limit_dilates',
                                                                       'private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_poisson',
                                                                       'private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_plancherel_deriv',
                                                                       'private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_fourier_samples',
                                                                       'private '
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv_inversion',
                                                                       'RiemannMasullo.schwartz_int_lattice_energy_le_deriv'],
 'file:RiemannMasullo/ForMathlib/Analysis/Fourier/Translation.lean': ['RiemannMasullo.exists_circleCharacter_norm_sub_one_le',
                                                                      'RiemannMasullo.fourierIntegral_circleCharacter_translation_bound'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/AccretiveJets.lean': ['RiemannMasullo.sum_range_quarter_pow_sub_le',
                                                                                  'RiemannMasullo.sum_triangle_quarter_pow_le',
                                                                                  'RiemannMasullo.norm_apply_le_of_accretive',
                                                                                  'RiemannMasullo.norm_pow_apply_le_of_accretive',
                                                                                  'RiemannMasullo.norm_inner_pow_add_two_le',
                                                                                  'RiemannMasullo.norm_descFactorial_mul_inner_pow_le',
                                                                                  'RiemannMasullo.two_thirds_mul_sum_le_re_sum_inner_jet',
                                                                                  'RiemannMasullo.two_thirds_mul_sum_le_re_sum_inner_jet_add'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/ExponentialGram.lean': ['private '
                                                                                    'RiemannMasullo.gapWeight',
                                                                                    'private '
                                                                                    'RiemannMasullo.edgeResponse',
                                                                                    'private '
                                                                                    'RiemannMasullo.dist_add_between',
                                                                                    'private '
                                                                                    'RiemannMasullo.edgeResponse_zero',
                                                                                    'private '
                                                                                    'RiemannMasullo.edgeResponse_cancel',
                                                                                    'private '
                                                                                    'RiemannMasullo.edgeColumn',
                                                                                    'private '
                                                                                    'RiemannMasullo.edgeColumn_apply_self',
                                                                                    'private '
                                                                                    'RiemannMasullo.edgeColumn_mulVec',
                                                                                    'RiemannMasullo.exponentialGramDiagonal',
                                                                                    'private '
                                                                                    'RiemannMasullo.exponentialGramDiagonal_nonneg',
                                                                                    'RiemannMasullo.exponentialGram_inverse_col',
                                                                                    'RiemannMasullo.exponentialGram_inverse_diag',
                                                                                    'RiemannMasullo.norm_mul_finiteGramCoordinate_sq_of_exponential_inner',
                                                                                    'RiemannMasullo.finiteGramCoordinate_eq_of_orthogonal'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/GramMatrix.lean': ['RiemannMasullo.finiteGram_coefficient_isGreatest',
                                                                               'RiemannMasullo.finiteGramCoordinate',
                                                                               'RiemannMasullo.finiteGramCoordinate_isGreatest',
                                                                               'RiemannMasullo.finiteGram_coefficient_isLUB_iff',
                                                                               'private '
                                                                               'RiemannMasullo.finiteGram_inv_diag_smul',
                                                                               'RiemannMasullo.finiteGramCoordinate_smul',
                                                                               'RiemannMasullo.norm_mul_finiteGramCoordinate_smul',
                                                                               'RiemannMasullo.norm_mul_finiteGramCoordinate_eq_normalized_inverse_diag',
                                                                               'RiemannMasullo.norm_mul_finiteGramCoordinate_le_of_pairings'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/LaplaceSemigroup.lean': ['RiemannMasullo.integrableOn_exp_smul_orbit',
                                                                                     'RiemannMasullo.mul_norm_sq_laplace_semigroup_le_re_inner'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/PiL2.lean': ['RiemannMasullo.norm_multilinear_le_sum_euclidean_basis'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/Projection/Basic.lean': ['RiemannMasullo.exists_contraction_comp_eq_of_norm_le'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/Subspace.lean': ['RiemannMasullo.summable_iff_summable_sq_norm_of_orthogonal'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/Total.lean': ['RiemannMasullo.dense_span_pontryaginDual_toLp',
                                                                          'RiemannMasullo.mem_of_mem_tmul_dense_family',
                                                                          'RiemannMasullo.exists_submodule_finite_moment_support',
                                                                          'RiemannMasullo.dense_span_quotient_biorthogonal_of_finite_support'],
 'file:RiemannMasullo/ForMathlib/Analysis/InnerProductSpace/TriangularDiagonal.lean': ['RiemannMasullo.inner_map_self_of_triangular',
                                                                                       'RiemannMasullo.inner_left_gramSchmidtNormed_eq_zero',
                                                                                       'RiemannMasullo.gramSchmidtNormed_mem_span_Iic',
                                                                                       'RiemannMasullo.inner_gramSchmidtNormed_map_of_triangular',
                                                                                       'RiemannMasullo.sum_norm_sq_map_gramSchmidtNormed_le',
                                                                                       'RiemannMasullo.summable_norm_sq_map_gramSchmidtNormed'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/BanachSteinhaus.lean': ['RiemannMasullo.isVonNBounded_image2_apply_of_pointwise'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/Barrelled.lean': ['RiemannMasullo.exists_continuousLinearMap_iteratedDeriv_of_analytic',
                                                                          'RiemannMasullo.exists_continuousLinearMap_of_analytic_continuation',
                                                                          'RiemannMasullo.continuous_of_continuous_eval_barrelled',
                                                                          'RiemannMasullo.exists_continuousLinearMap_integral_mul'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/Bounded.lean': ['RiemannMasullo.isVonNBounded_range_comp_clm',
                                                                        'RiemannMasullo.isVonNBounded_range_clm_of_pointwise',
                                                                        'RiemannMasullo.equicontinuous_comp_of_isVonNBounded_range_dual'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/Completion.lean': ['private '
                                                                           'RiemannMasullo.exists_continuous_seminorm_completion',
                                                                           'RiemannMasullo.polynormableSpace_completion'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/ContinuousOfBounded.lean': ['RiemannMasullo.continuous_of_bornological_image'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/HahnBanach.lean': ['RiemannMasullo.exists_dual_norm_le_one_lt_of_notMem',
                                                                           'RiemannMasullo.exists_dual_norm_eq_seminorm'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/InfiniteSum.lean': ['RiemannMasullo.summable_of_summable_seminorms'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/MittagLefflerLift.lean': ['private '
                                                                                  'RiemannMasullo.surjective_coeff_of_eventually_small_aux',
                                                                                  'RiemannMasullo.surjective_coeff_of_eventually_small',
                                                                                  'RiemannMasullo.surjective_coeff_of_withSeminorms'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/Montel.lean': ['private '
                                                                       'RiemannMasullo.tendsto_of_compact_evaluations',
                                                                       'private '
                                                                       'RiemannMasullo.uniformOn_montel_of_evaluations',
                                                                       'RiemannMasullo.uniformOn_montel_of_evaluations_near',
                                                                       'private '
                                                                       'RiemannMasullo.sub_mem_of_coordinate_derivatives',
                                                                       'RiemannMasullo.exists_compact_slopes_of_velocity',
                                                                       'RiemannMasullo.seqContinuous_symm_of_bounded_comparison'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/ProjectionCompleteness.lean': ['private '
                                                                                       'RiemannMasullo.cauchy_exists_seminorm_center',
                                                                                       'private '
                                                                                       'RiemannMasullo.eventually_equal_projection_limits',
                                                                                       'private '
                                                                                       'RiemannMasullo.tendsto_of_eventually_constant_projections',
                                                                                       'RiemannMasullo.cauchy_projection_limit',
                                                                                       'RiemannMasullo.complete_of_stabilizing_projections'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/Separable.lean': ['RiemannMasullo.isLindelof_preimage_of_isProperMap',
                                                                          'RiemannMasullo.separableSpace_of_withSeminorms_of_compact_bounded'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/SeparatingDual.lean': ['RiemannMasullo.locallyConvexSpace_separatingDual',
                                                                               'RiemannMasullo.polynormableSpace_separatingDual',
                                                                               'RiemannMasullo.exists_dual_eq_zero_on_submodule_of_notMem'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/SmoothFamily.lean': ['RiemannMasullo.exists_clm_iteratedFDeriv_apply'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/StrongBidual.lean': ['RiemannMasullo.isEmbedding_strongBidual_eval',
                                                                             'RiemannMasullo.exists_compact_absConvex_superset',
                                                                             'RiemannMasullo.surjective_strongBidual_eval'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/StrongDual.lean': ['RiemannMasullo.isCompact_strongDual_polar',
                                                                           'RiemannMasullo.montelSpace_strongDual'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/StrongDualPrecompact.lean': ['private '
                                                                                     'RiemannMasullo.tendstoUniformlyOn_of_equicontinuous',
                                                                                     'RiemannMasullo.isCompact_strongDual_polar_of_precompact',
                                                                                     'RiemannMasullo.isCompact_closure_strongDual_of_pointwise_bounded',
                                                                                     'RiemannMasullo.montelSpace_strongDual_of_precompact',
                                                                                     'RiemannMasullo.isEmbedding_transpose_of_bounded_image'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/TensorProduct/Bounded.lean': ['RiemannMasullo.IsInjectiveLCLimit.completion_bounded_stage',
                                                                                      'RiemannMasullo.IsNuclearTVS.tensorComparison',
                                                                                      'RiemannMasullo.IsNuclearTVS.tensorComparison_right',
                                                                                      'private '
                                                                                      'RiemannMasullo.norm_le_seminorm_of_ball_subset',
                                                                                      'private '
                                                                                      'RiemannMasullo.tensorDualForm_commute',
                                                                                      'RiemannMasullo.injectiveTensor_isEmbedding_of_generating_evaluations',
                                                                                      'RiemannMasullo.projectiveTensorMap_isEmbedding_of_comparisons',
                                                                                      'RiemannMasullo.continuous_projectiveStage_inductiveTensor',
                                                                                      'RiemannMasullo.isEmbedding_projectiveStage_inductiveTensor',
                                                                                      'private '
                                                                                      'RiemannMasullo.IsInjectiveLCLimit.transition_to',
                                                                                      'RiemannMasullo.inductiveTensor_topology_eq_diagonal_projective',
                                                                                      'RiemannMasullo.completedInductiveTensor_bounded_projectiveStage',
                                                                                      'private '
                                                                                      'RiemannMasullo.rect_finite_net',
                                                                                      'private '
                                                                                      'RiemannMasullo.rect_controlled_approximation',
                                                                                      'private '
                                                                                      'RiemannMasullo.rect_finite_support',
                                                                                      'private '
                                                                                      'RiemannMasullo.rect_unrestricted',
                                                                                      'private '
                                                                                      'RiemannMasullo.rect_dyadic',
                                                                                      'private '
                                                                                      'RiemannMasullo.rect_compact_blocks',
                                                                                      'RiemannMasullo.completedProjectiveTensor_compact_rectangle',
                                                                                      'RiemannMasullo.completedProjectiveTensor_bounded_rectangle',
                                                                                      'RiemannMasullo.completedInductiveTensor_bounded_rectangle'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/TensorProduct/Comparison.lean': ['private '
                                                                                         'RiemannMasullo.bounded_of_inducing_image',
                                                                                         'private '
                                                                                         'RiemannMasullo.comparison_of_bounded_stages',
                                                                                         'private '
                                                                                         'RiemannMasullo.projective_tensor_as_operators',
                                                                                         'private '
                                                                                         'RiemannMasullo.strongDual_bounded_total_set',
                                                                                         'RiemannMasullo.completedTensor_comparison_bounded_of_strictLF'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/TensorProduct/StrongDual.lean': ['private '
                                                                                         'RiemannMasullo.kernel_continuous_of_zero',
                                                                                         'private '
                                                                                         'RiemannMasullo.strongCurry_continuous',
                                                                                         'private '
                                                                                         'RiemannMasullo.strongCurry_precomp',
                                                                                         'private '
                                                                                         'RiemannMasullo.strongCurry_inductiveTensor',
                                                                                         'private '
                                                                                         'RiemannMasullo.strongCurry_equiv_of_bounded_rectangles',
                                                                                         'RiemannMasullo.dualKernel_of_bounded_rectangles'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/WeakSpace.lean': ['RiemannMasullo.isVonNBounded_of_dual_bounded'],
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/WithSeminorms.lean': ['RiemannMasullo.exists_seminorm_extension',
                                                                              'RiemannMasullo.polynormableSpace_quotient'],
 'file:RiemannMasullo/ForMathlib/Analysis/MellinTransform.lean': ['RiemannMasullo.isBigO_comp_log_rpow_of_isBigO_exp',
                                                                  'RiemannMasullo.mellinConvergent_of_integrable_logWeight'],
 'file:RiemannMasullo/ForMathlib/Analysis/MellinTransform/Gaussian.lean': ['mellin_gaussian',
                                                                           'integral_comp_abs_complex',
                                                                           'Complex.integral_radial'],
 'file:RiemannMasullo/ForMathlib/Analysis/MellinTransform/Holomorphic.lean': ['RiemannMasullo.analyticOnNhd_integral_mul_cpow_of_integrable'],
 'file:RiemannMasullo/ForMathlib/Analysis/MellinTransform/Weighted.lean': ['RiemannMasullo.analyticOnNhd_integral_mul_cpow',
                                                                           'RiemannMasullo.tendstoUniformlyOn_mellinBands'],
 'file:RiemannMasullo/ForMathlib/Analysis/Meromorphic/PrincipalPart.lean': ['private '
                                                                            'RiemannMasullo.analyticAt_exists_polar_expansion',
                                                                            'RiemannMasullo.MeromorphicAt.exists_polar_expansion'],
 'file:RiemannMasullo/ForMathlib/Analysis/Meromorphic/VerticalStripZeros.lean': ['RiemannMasullo.tsum_zeroWeights_le_of_bins',
                                                                                 'private '
                                                                                 'RiemannMasullo.summable_zeroWeights_of_bins',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_disk_sum',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_local_order',
                                                                                 'RiemannMasullo.sum_divisor_le_log_of_disk_bound',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_compact',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_polynomial_strip',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_center_bound',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_disk_growth',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_log_bound',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_window_jensen',
                                                                                 'RiemannMasullo.sum_divisor_le_log_height_window',
                                                                                 'private '
                                                                                 'RiemannMasullo.zeroCount_window_at_height',
                                                                                 'RiemannMasullo.summable_divisor_div_one_add_abs_im_sq'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Field/ProperSpace.lean': ['RiemannMasullo.isProperMap_units_nnNorm_pow'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Group/InfiniteSum.lean': ['RiemannMasullo.tsum_zero_of_cosets',
                                                                           'RiemannMasullo.tsum_avoiding_finset_mem',
                                                                           'RiemannMasullo.tsum_avoiding_of_tsum_intersections'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Lp/lpSpace.lean': ['lp.separableSpace'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Module/CompactInterpolation.lean': ['RiemannMasullo.exists_basis_compact_coord_le',
                                                                                     'RiemannMasullo.exists_compact_interpolant'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Module/LocalHom.lean': ['RiemannMasullo.exists_addMonoidHom_eqOn_ball_of_local_additive'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Module/LocalSubgroup.lean': ['private '
                                                                              'RiemannMasullo.good_sup_localSubgroup',
                                                                              'RiemannMasullo.exists_subspace_ball_eq_of_localSubgroup'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Module/Seminorm/DirectSum.lean': ['RiemannMasullo.directSumSeminorm',
                                                                                   'RiemannMasullo.directSumSeminorm_apply',
                                                                                   'RiemannMasullo.directSumSeminorm_lof',
                                                                                   'RiemannMasullo.sum_le_directSumSeminorm'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Module/Seminorm/Pi.lean': ['RiemannMasullo.product_seminorm_tail'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Module/Seminorm/Quotient.lean': ['RiemannMasullo.exists_seminorm_thickening'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Module/WeakDual.lean': ['RiemannMasullo.weakDual_not_completeSpace',
                                                                         'RiemannMasullo.isCompact_weakDual_polar'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Operator/AbsolutelySumming/Composition.lean': ['private '
                                                                                                'RiemannMasullo.AbsolutelySumming.summable_basis',
                                                                                                'private '
                                                                                                'RiemannMasullo.AbsolutelySumming.summable_adjoint_basis',
                                                                                                'private '
                                                                                                'RiemannMasullo.AbsolutelySumming.tendsto_scaled',
                                                                                                'private '
                                                                                                'RiemannMasullo.AbsolutelySumming.rescale_nat_series',
                                                                                                'private '
                                                                                                'RiemannMasullo.AbsolutelySumming.rescale_series',
                                                                                                'RiemannMasullo.AbsolutelySumming.exists_series_comp_three'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Operator/AbsolutelySumming/Factorization.lean': ['RiemannMasullo.AbsolutelySumming.HasBound',
                                                                                                  'RiemannMasullo.AbsolutelySumming.HasQuadraticBound',
                                                                                                  'RiemannMasullo.AbsolutelySumming.sum_sq_le',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.Ball',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.pt',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.unitBound',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.cost',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.cone',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.cone_nonneg',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.exists_nonneg_of_mem',
                                                                                                  'private '
                                                                                                  'RiemannMasullo.AbsolutelySumming.domination',
                                                                                                  'RiemannMasullo.AbsolutelySumming.factor'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Operator/Compact/Hilbert.lean': ['private '
                                                                                  'RiemannMasullo.isCompactOperator_of_summable_sq_norm_hilbertBasis',
                                                                                  'RiemannMasullo.isCompactOperator_of_hilbert_absolutelySumming'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Operator/Compact/NormAttainment.lean': ['RiemannMasullo.exists_unit_norm_eq_opNorm_of_isCompactOperator'],
 'file:RiemannMasullo/ForMathlib/Analysis/Normed/Ring/InfiniteSum.lean': ['RiemannMasullo.hasSum_prod_fin_of_nonneg'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Complex/CircleLocalHom.lean': ['RiemannMasullo.circleExp_coord_injective',
                                                                                          'RiemannMasullo.eventually_exists_small_circleLog',
                                                                                          'RiemannMasullo.exists_linearMap_circleExp_of_localHom',
                                                                                          'RiemannMasullo.circleExp_sum',
                                                                                          'RiemannMasullo.dist_circleExp_one_le'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Complex/ExpPolynomial.lean': ['RiemannMasullo.exp_mul_polynomial_eq_zero',
                                                                                         'RiemannMasullo.expPolynomial_translate_coeff_eq_zero'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Gamma/Bounds.lean': ['RiemannMasullo.norm_Gamma_le_real_Gamma',
                                                                                'RiemannMasullo.exists_norm_inv_Gamma_le_exp_mul_abs_im',
                                                                                'RiemannMasullo.inv_Gammaℝ_add_isBigO_exp'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Gamma/Digamma.lean': ['private '
                                                                                 'RiemannMasullo.digammaKernel',
                                                                                 'private '
                                                                                 'RiemannMasullo.integrableOn_digammaKernel',
                                                                                 'private '
                                                                                 'RiemannMasullo.betaDifference_eq_quotient',
                                                                                 'private '
                                                                                 'RiemannMasullo.tendsto_gammaDifference',
                                                                                 'private '
                                                                                 'RiemannMasullo.digamma_one_sub_eq_integral',
                                                                                 'RiemannMasullo.gaussDigammaDifferenceKernel',
                                                                                 'RiemannMasullo.integral_gaussDigammaDifferenceKernel',
                                                                                 'private '
                                                                                 'RiemannMasullo.one_sub_exp_neg_le',
                                                                                 'private '
                                                                                 'RiemannMasullo.abs_real_damping_sub_le',
                                                                                 'RiemannMasullo.norm_gaussDigammaDifferenceKernel_le'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Gamma/DigammaIntegral.lean': ['private '
                                                                                         'RiemannMasullo.digammaKernel',
                                                                                         'private '
                                                                                         'RiemannMasullo.integrableOn_digammaKernel',
                                                                                         'private '
                                                                                         'RiemannMasullo.betaDifference_eq_quotient',
                                                                                         'private '
                                                                                         'RiemannMasullo.tendsto_gammaDifference',
                                                                                         'RiemannMasullo.digamma_one_sub_eq_integral',
                                                                                         'RiemannMasullo.gaussDigammaDifference',
                                                                                         'RiemannMasullo.integral_gaussDigammaDifference',
                                                                                         'private '
                                                                                         'RiemannMasullo.one_sub_exp_neg_le',
                                                                                         'private '
                                                                                         'RiemannMasullo.abs_real_damping_sub_le',
                                                                                         'private '
                                                                                         'RiemannMasullo.norm_gaussDigammaDifference_le',
                                                                                         'RiemannMasullo.integrable_mul_gaussDigammaDifference'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Gamma/VerticalStrip.lean': ['private '
                                                                                       'RiemannMasullo.norm_inv_Gamma_half',
                                                                                       'RiemannMasullo.exists_norm_inv_Gamma_le_half_exp_on_strip',
                                                                                       'RiemannMasullo.exists_norm_inv_GammaReal_add_le_on_strip'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Gamma/VerticalStripRatio.lean': ['private '
                                                                                            'RiemannMasullo.gammaLogTerm_interpolation',
                                                                                            'private '
                                                                                            'RiemannMasullo.gammaLogSeq_formula',
                                                                                            'private '
                                                                                            'RiemannMasullo.gammaLog_interpolation',
                                                                                            'RiemannMasullo.norm_Gamma_div_le_rpow_on_strip'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Gaussian/Hecke.lean': ['private '
                                                                                  'RiemannMasullo.HeckeGaussian.exists_schwartz_exp_neg',
                                                                                  'private '
                                                                                  'RiemannMasullo.HeckeGaussian.temperate_fintype_prod',
                                                                                  'RiemannMasullo.HeckeGaussian.mixedGaussian_schwartz',
                                                                                  'private '
                                                                                  'RiemannMasullo.HeckeGaussian.planeGaussianGenerating',
                                                                                  'private '
                                                                                  'RiemannMasullo.HeckeGaussian.planeMoment_from_generating',
                                                                                  'private '
                                                                                  'RiemannMasullo.HeckeGaussian.angularCoord',
                                                                                  'private '
                                                                                  'RiemannMasullo.HeckeGaussian.planeGaussianMoments',
                                                                                  'private '
                                                                                  'RiemannMasullo.HeckeGaussian.radialMellin',
                                                                                  'private '
                                                                                  'RiemannMasullo.HeckeGaussian.radialMellin_power',
                                                                                  'RiemannMasullo.HeckeGaussian.realMellin_gamma',
                                                                                  'RiemannMasullo.HeckeGaussian.complexMellin_gamma',
                                                                                  'RiemannMasullo.HeckeGaussian.realGaussianFourier',
                                                                                  'RiemannMasullo.HeckeGaussian.realTest',
                                                                                  'RiemannMasullo.HeckeGaussian.complexTestPoly',
                                                                                  'RiemannMasullo.HeckeGaussian.complexTest',
                                                                                  'RiemannMasullo.HeckeGaussian.complexGaussianFourier'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Gaussian/Schwartz.lean': ['private '
                                                                                     'RiemannMasullo.gaussian_weight_bound',
                                                                                     'RiemannMasullo.exists_gaussian_schwartz',
                                                                                     'RiemannMasullo.mellin_weightedGaussian'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Pow/Complex.lean': ['private '
                                                                               'RiemannMasullo.exp_real_mul_injective',
                                                                               'RiemannMasullo.existsUnique_complexPower',
                                                                               'RiemannMasullo.existsUnique_unitaryComplexPower',
                                                                               'RiemannMasullo.existsUnique_realUnits_quasiCharacter_parameters',
                                                                               'RiemannMasullo.existsUnique_realUnits_character_parameters',
                                                                               'RiemannMasullo.existsUnique_circleCharacter_zpow',
                                                                               'RiemannMasullo.existsUnique_complexUnits_quasiCharacter_parameters',
                                                                               'RiemannMasullo.existsUnique_complexUnits_character_parameters'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Pow/Integral.lean': ['RiemannMasullo.lintegral_ennreal_rpow_eq_lintegral_meas_lt_mul'],
 'file:RiemannMasullo/ForMathlib/Analysis/SpecialFunctions/Trigonometric/HyperbolicCardinal.lean': ['RiemannMasullo.GeometricHat.profile',
                                                                                                    'private '
                                                                                                    'RiemannMasullo.GeometricHat.scaled_hyperbolic',
                                                                                                    'private '
                                                                                                    'RiemannMasullo.GeometricHat.scaled_denominator',
                                                                                                    'RiemannMasullo.GeometricHat.hasDerivAt_profile',
                                                                                                    'RiemannMasullo.GeometricHat.profile_bounds',
                                                                                                    'RiemannMasullo.GeometricHat.weighted_deriv_bound',
                                                                                                    'RiemannMasullo.GeometricHat.cancellation_bounds',
                                                                                                    'RiemannMasullo.GeometricHat.hasDerivAt_deriv_profile',
                                                                                                    'RiemannMasullo.GeometricHat.energy_flux_derivative',
                                                                                                    'RiemannMasullo.GeometricHat.finite_gap_energy',
                                                                                                    'RiemannMasullo.GeometricHat.adjacent_profile_sum_le_one',
                                                                                                    'RiemannMasullo.GeometricHat.adjacent_profile_sq_sum_le_one'],
 'file:RiemannMasullo/ForMathlib/Geometry/Manifold/Instances/UnitsOfNormedAlgebra.lean': ['private '
                                                                                          'RiemannMasullo.contDiff_additive_character',
                                                                                          'RiemannMasullo.contMDiff_units_character'],
 'file:RiemannMasullo/ForMathlib/Geometry/Manifold/LocalDiffeomorph.lean': ['RiemannMasullo.isLocalDiffeomorph_of_chartAt'],
 'file:RiemannMasullo/ForMathlib/LinearAlgebra/TensorProduct/DirectLimit.lean': ['RiemannMasullo.exists_pairwise_tensor_stage'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Function/ContinuousMapDense.lean': ['RiemannMasullo.integrable_tsum_of_lintegral_eNorm',
                                                                                   'private '
                                                                                   'RiemannMasullo.exists_compactTest_eLpNorm_sub_le',
                                                                                   'RiemannMasullo.exists_compactTest_tsum',
                                                                                   'private '
                                                                                   'RiemannMasullo.exists_continuous_indicator_error_bound',
                                                                                   'RiemannMasullo.exists_hasCompactSupport_eLpNorm_sub_le',
                                                                                   'RiemannMasullo.exists_hasCompactSupport_eLpNorm_sub_le_two',
                                                                                   'RiemannMasullo.exists_tendsto_ae_compactSupport'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Function/L1Space/Continuous.lean': ['MeasureTheory.continuous_toL1_of_continuous_eval',
                                                                                   'MeasureTheory.linearContinuous_integral_of_continuous_eval'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Function/L2Space.lean': ['MeasureTheory.L2.integral_sq_norm',
                                                                        'MeasureTheory.L2.exists_memLp_coordinates',
                                                                        'MeasureTheory.L2.exists_outerProduct'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Function/L2Space/Integral.lean': ['RiemannMasullo.integral_L2_representative'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Function/L2Space/TensorProduct.lean': ['private '
                                                                                      'RiemannMasullo.ae_zero_of_integral_rectangles',
                                                                                      'private '
                                                                                      'RiemannMasullo.memLp_tensorProduct',
                                                                                      'private '
                                                                                      'RiemannMasullo.l2ProductMap',
                                                                                      'private '
                                                                                      'RiemannMasullo.l2ProductMap_tmul',
                                                                                      'private '
                                                                                      'RiemannMasullo.l2ProductMap_inner',
                                                                                      'RiemannMasullo.exists_l2TensorProduct_isometry'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Group/Arithmetic.lean': ['RiemannMasullo.borelSpace_units_of_continuousInv₀'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Group/Compact.lean': ['RiemannMasullo.compactSpace_of_isFiniteMeasure_haar'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Group/FundamentalDomain.lean': ['RiemannMasullo.map_restrict_fundamentalDomain_eq'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Group/Measure.lean': ['RiemannMasullo.sigmaCompactSpace_of_sigmaFinite_haar'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/Bochner/Barrelled.lean': ['RiemannMasullo.exists_integralCLM_of_pointwise_continuous'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/Bochner/Convex.lean': ['RiemannMasullo.integral_mem_compact_convex_functions'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/Bochner/Regular.lean': ['RiemannMasullo.exists_isCompact_integral_norm_sdiff_lt',
                                                                                'RiemannMasullo.ae_eq_zero_of_integral_mul_circle_eq_zero'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/Bochner/Seminorm.lean': ['RiemannMasullo.exists_integral_seminorm',
                                                                                 'RiemannMasullo.continuous_integral_seminorm'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/IntegralEqImproper.lean': ['private '
                                                                                   'RiemannMasullo.intervalIntegral_deriv_eq_sub_add_sum_jumps',
                                                                                   'RiemannMasullo.integral_deriv_eq_sub_add_sum_jumps'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/LocallyConstant.lean': ['RiemannMasullo.exists_algebraic_integral_of_locallyConstant'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/Prod.lean': ['private RiemannMasullo.norm_integral_sq_le',
                                                                     'RiemannMasullo.memLp_two_prod_left_ae',
                                                                     'RiemannMasullo.memLp_two_integral_prod_left'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/ProdPi.lean': ['MeasurableEquiv.piFinsetUnion_left',
                                                                       'MeasurableEquiv.piFinsetUnion_right',
                                                                       'MeasureTheory.Measure.prod_pi_eq',
                                                                       'MeasureTheory.integral_prod_piFinsetUnion'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/ProdRegular.lean': ['RiemannMasullo.exists_isSigmaCompact_ae_mem',
                                                                            'RiemannMasullo.measurable_indicator_prod_of_isSigmaCompact',
                                                                            'RiemannMasullo.lintegral_lintegral_mul_translate'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Integral/RieszMarkovKakutani/Real.lean': ['RiemannMasullo.exists_radon_of_le_iSup'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Measure/Count.lean': ['RiemannMasullo.count_regular_of_discreteTopology',
                                                                     'RiemannMasullo.count_isHaarMeasure_of_discreteTopology'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Measure/Haar/Basic.lean': ['RiemannMasullo.haar_regular_of_compactSpace'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Measure/Haar/Extension.lean': ['RiemannMasullo.integral_inducedMeasure_complex'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Measure/Haar/Unique.lean': ['RiemannMasullo.addHaar_regular_of_sigmaCompactSpace'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Measure/Haar/Units.lean': ['RiemannMasullo.isHaarMeasure_comap_units_withDensity',
                                                                          'RiemannMasullo.map_mul_left_map_ringEquiv',
                                                                          'RiemannMasullo.real_map_mul_left_volume',
                                                                          'RiemannMasullo.complex_map_mul_left_volume'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Measure/RegularDomination.lean': ['RiemannMasullo.regular_of_le_finite_regular',
                                                                                 'RiemannMasullo.innerRegular_withDensity_of_le_of_isSigmaCompact',
                                                                                 'RiemannMasullo.measure_eq_of_lintegral_eq_on_compactlySupported_nnreal'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/Measure/Support.lean': ['MeasureTheory.ae_diagonal_eq_of_ae_eq_comp_prod'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/VectorMeasure/Integral.lean': ['MeasureTheory.VectorMeasure.integral_withDensityᵥ_mul'],
 'file:RiemannMasullo/ForMathlib/MeasureTheory/VectorMeasure/WithDensityVec.lean': ['RiemannMasullo.integral_withDensityᵥ_mul'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/ArithmeticFunction/LFunction.lean': ['RiemannMasullo.tsum_norm_LSeries_term_mul_le',
                                                                                   'RiemannMasullo.LSeries_finset_prod_bound',
                                                                                   'RiemannMasullo.LSeriesSummable_of_eventuallyEq_finset_prod',
                                                                                   'RiemannMasullo.LSeries_term_geometric_ofPowerSeries',
                                                                                   'RiemannMasullo.hasSum_norm_LSeries_term_ofPowerSeries',
                                                                                   'RiemannMasullo.LSeriesHasSum_finset_prod'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/EulerProduct/Basic.lean': ['RiemannMasullo.hasProd_eulerFactors_of_summable'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/LSeries/Convergence.lean': ['private '
                                                                          'RiemannMasullo.norm_LSeries_term_shift',
                                                                          'RiemannMasullo.tendstoUniformlyOn_LSeries_of_eventuallyEq'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/LSeries/DirichletZeros.lean': ['private '
                                                                             'RiemannMasullo.subquadratic_zeroFree_logDeriv_constant',
                                                                             'private '
                                                                             'RiemannMasullo.subquadratic_zeroFree_shift',
                                                                             'private RiemannMasullo.kernelWeight',
                                                                             'private '
                                                                             'RiemannMasullo.kernelWeight_top',
                                                                             'private '
                                                                             'RiemannMasullo.oddKernel_weight_integrable',
                                                                             'private '
                                                                             'RiemannMasullo.abs_log_exponent',
                                                                             'private '
                                                                             'RiemannMasullo.oddHurwitz_growth',
                                                                             'private '
                                                                             'RiemannMasullo.oddDirichlet_subquadratic',
                                                                             'private '
                                                                             'RiemannMasullo.oddDirichlet_shift_impossible',
                                                                             'RiemannMasullo.dirichletFive_positiveOrder'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/LinearFormsInLogarithms.lean': ['private '
                                                                              'RiemannMasullo.baker_two_logarithms_dependent_degree_zero',
                                                                              'private '
                                                                              'RiemannMasullo.baker_two_logarithms_of_not_liouville',
                                                                              'private '
                                                                              'RiemannMasullo.baker_two_logarithms_not_liouville_of_independent',
                                                                              'private '
                                                                              'RiemannMasullo.baker_two_logarithms',
                                                                              'RiemannMasullo.polynomial_bound_inv_one_sub_of_exp_eq_one',
                                                                              'RiemannMasullo.finite_euler_values_of_residue_pow_eq'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/Basic.lean': ['RiemannMasullo.RatRingOfIntegers.exists_intCast',
                                                                        'RiemannMasullo.RatRingOfIntegers.finrank_int',
                                                                        'RiemannMasullo.RatRingOfIntegers.absNorm_span_intCast',
                                                                        'RiemannMasullo.RatRingOfIntegers.absNorm_span_natCast',
                                                                        'RiemannMasullo.RatRingOfIntegers.exists_eq_span_natCast',
                                                                        'RiemannMasullo.RatRingOfIntegers.natCast_ne_zero',
                                                                        'RiemannMasullo.RatRingOfIntegers.prime_natCast_iff'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/Completion/FinitePlace.lean': ['RiemannMasullo.norm_uniformizer_adicCompletion',
                                                                                         'RiemannMasullo.nonempty_residueFieldEquiv_adicCompletion',
                                                                                         'RiemannMasullo.card_residueField_adicCompletion',
                                                                                         'private '
                                                                                         'RiemannMasullo.finite_residueField_adicCompletion',
                                                                                         'RiemannMasullo.properSpace_adicCompletion',
                                                                                         'RiemannMasullo.locallyCompactSpace_adicCompletion',
                                                                                         'RiemannMasullo.compactSpace_adicCompletionIntegers',
                                                                                         'RiemannMasullo.finitePlace_unitDecomposition'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/DedekindZeta.lean': ['RiemannMasullo.dedekindZeta_LSeriesSummable',
                                                                               'RiemannMasullo.summable_absNorm_rpow',
                                                                               'RiemannMasullo.dedekindZeta_hasProd'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/DedekindZeta/MultipleZero.lean': ['private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_groupedEuler',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_denominator',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_finiteFactor',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_discardFinite',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_zetaRelation',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_stripOrder',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_orderRelation',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_cubicGalois',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_invertTraces',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_transitiveCharacters',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_character',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_countSupport',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_ratNorm',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_ratCount',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_ratTrace',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_resolventSplits',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_subfields',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_embeddingAction',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_fixedCount',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_frobeniusLift',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_residueNorm',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_reductionInjective',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_integralEmbeddings',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_reductionBijective',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_finiteFieldMaps',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_residueDegree',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_residueDecomposition',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_residueSum',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_normFibres',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_normSum',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_frobeniusOrbits',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_frobeniusTrace',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_frobenius',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_badNorm',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_primeCounts',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_rectangle',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gaussianNorm',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gaussianHorizontal',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gaussianVertical',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_factorialEdges',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gammaStep',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gammaRecurrence',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gammaPositiveStrip',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gammaStrip',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_reflectedOrder',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_exteriorOrder',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_poles',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_entireQuotient',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_eulerFactors',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_finiteQuotient',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_eulerBound',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_finiteRegular',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_quotientValue',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_eulerNonzero',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_quotientReflection',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_gammaRight',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_rightEdge',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_verticalEdges',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_horizontalEdges',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_clearFinitePoles',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_polynomialBound',
                                                                                            'RiemannMasullo.cubicDedekindZeta_excessOrders_infinite',
                                                                                            'private '
                                                                                            'RiemannMasullo.spectralLineJet_memLp_false_cubicZeroCount',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_splittingField_comparison',
                                                                                            'RiemannMasullo.cubicSplittingField_completedDedekindZeta_multipleZeros_infinite',
                                                                                            'private '
                                                                                            'RiemannMasullo.cubicZeroCount_unbounded_of_infinite',
                                                                                            'RiemannMasullo.cubicSplittingField_completedDedekindZeta_multipleZeros_unbounded',
                                                                                            'RiemannMasullo.exists_completedDedekindZeta_multipleZero'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/HeckeLFunction.lean': ['RiemannMasullo.hecke_localPowerSeries_eq_mk',
                                                                                 'RiemannMasullo.heckeLocalEulerFactor_eventually_prod_eq',
                                                                                 'RiemannMasullo.LSeries_heckeLocalEulerFactor_bound',
                                                                                 'RiemannMasullo.LSeriesSummable_heckeLFunction'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/InfiniteAdeleRing.lean': ['RiemannMasullo.infiniteAdeleHomeomorphMixedSpace',
                                                                                    'RiemannMasullo.infiniteAdeleHomeomorphMixedSpace_toEquiv',
                                                                                    'RiemannMasullo.infiniteAdeleHomeomorphMixedSpace_apply',
                                                                                    'RiemannMasullo.infiniteAdeleHomeomorphMixedSpace_symm_apply',
                                                                                    'RiemannMasullo.continuous_infiniteAdeleRingEquivMixedSpace',
                                                                                    'RiemannMasullo.continuous_infiniteAdeleRingEquivMixedSpace_symm'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/SplitPrimeDensity.lean': ['private '
                                                                                    'RiemannMasullo.summable_prime_norm_rpow',
                                                                                    'private '
                                                                                    'RiemannMasullo.log_dedekindZeta_sub_prime_sum',
                                                                                    'private '
                                                                                    'RiemannMasullo.tendsto_neg_log_sub_one',
                                                                                    'private '
                                                                                    'RiemannMasullo.primeIdealZetaSum_univ_isEquivalent',
                                                                                    'private '
                                                                                    'RiemannMasullo.AllSplit',
                                                                                    'private '
                                                                                    'RiemannMasullo.decomp_card',
                                                                                    'private '
                                                                                    'RiemannMasullo.fixes_of_split',
                                                                                    'private '
                                                                                    'RiemannMasullo.split_iff_in_normal_closure',
                                                                                    'private '
                                                                                    'RiemannMasullo.primeTowerEquiv',
                                                                                    'private '
                                                                                    'RiemannMasullo.finite_ramified_under',
                                                                                    'private '
                                                                                    'RiemannMasullo.galois_prime_sum_error',
                                                                                    'private '
                                                                                    'RiemannMasullo.galois_split_density',
                                                                                    'RiemannMasullo.tendsto_split_primeIdealZetaSum_div',
                                                                                    'RiemannMasullo.infinite_rational_primes_splitting_completely'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/WeilBound/Bombieri.lean': ['RiemannMasullo.WeilBound.ι_injective',
                                                                         'RiemannMasullo.WeilBound.isDomain_of_baseChange',
                                                                         'RiemannMasullo.WeilBound.finrank_unknowns',
                                                                         'RiemannMasullo.WeilBound.card_le_of_ker',
                                                                         'RiemannMasullo.WeilBound.frob_identity',
                                                                         "RiemannMasullo.WeilBound.add_pow_card_pow'",
                                                                         'RiemannMasullo.WeilBound.card_fixed_le',
                                                                         'RiemannMasullo.WeilBound.quot',
                                                                         'RiemannMasullo.WeilBound.X_sub_C_mul_quot',
                                                                         'RiemannMasullo.WeilBound.quot_monic',
                                                                         'RiemannMasullo.WeilBound.natDegree_quot',
                                                                         'RiemannMasullo.WeilBound.coeff_quot_pred',
                                                                         'RiemannMasullo.WeilBound.card_moved_le'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/WeilBound/EtaleChart.lean': ['RiemannMasullo.WeilBound.exists_dvd_algebraMap',
                                                                           'RiemannMasullo.WeilBound.exists_clear_denominators',
                                                                           'RiemannMasullo.WeilBound.exists_bezout_of_separable',
                                                                           'RiemannMasullo.WeilBound.algebraMap_injective_of_etale',
                                                                           'RiemannMasullo.WeilBound.faithfulSMul_of_etale',
                                                                           'RiemannMasullo.WeilBound.formallyUnramified_fractionRing',
                                                                           'RiemannMasullo.WeilBound.essFiniteType_fractionRing',
                                                                           'RiemannMasullo.WeilBound.finiteDimensional_fractionRing',
                                                                           'RiemannMasullo.WeilBound.isSeparable_fractionRing',
                                                                           'RiemannMasullo.WeilBound.isAlgebraic_of_etale',
                                                                           'RiemannMasullo.WeilBound.exists_primitive_integral',
                                                                           'RiemannMasullo.WeilBound.exists_denominator',
                                                                           'RiemannMasullo.WeilBound.toTensor',
                                                                           'RiemannMasullo.WeilBound.toTensor_monoBasis',
                                                                           'RiemannMasullo.WeilBound.toTensor_injective',
                                                                           'RiemannMasullo.WeilBound.isDomain_adjoinRoot_baseChange',
                                                                           'RiemannMasullo.WeilBound.card_algHom_localization_eq',
                                                                           'RiemannMasullo.WeilBound.card_algHom_finiteField_eq',
                                                                           'RiemannMasullo.WeilBound.weil_etale'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/WeilBound/Filtration.lean': ['RiemannMasullo.WeilBound.monoBasis',
                                                                           'RiemannMasullo.WeilBound.monoBasis_apply',
                                                                           'RiemannMasullo.WeilBound.idx',
                                                                           'RiemannMasullo.WeilBound.mem_idx',
                                                                           'RiemannMasullo.WeilBound.filt',
                                                                           'RiemannMasullo.WeilBound.mem_filt_iff',
                                                                           'RiemannMasullo.WeilBound.filt_mono',
                                                                           'RiemannMasullo.WeilBound.monoBasis_mem_filt',
                                                                           'RiemannMasullo.WeilBound.exists_mem_filt',
                                                                           'RiemannMasullo.WeilBound.finrank_filt',
                                                                           'RiemannMasullo.WeilBound.card_idx_le',
                                                                           'RiemannMasullo.WeilBound.le_card_idx',
                                                                           'RiemannMasullo.WeilBound.finrank_filt_le',
                                                                           'RiemannMasullo.WeilBound.le_finrank_filt',
                                                                           'RiemannMasullo.WeilBound.root_pow_natDegree',
                                                                           'RiemannMasullo.WeilBound.of_mul_root_pow_mem_filt',
                                                                           'RiemannMasullo.WeilBound.of_mem_filt',
                                                                           'RiemannMasullo.WeilBound.root_pow_mem_filt',
                                                                           'RiemannMasullo.WeilBound.one_mem_filt',
                                                                           'RiemannMasullo.WeilBound.mul_mem_filt',
                                                                           'RiemannMasullo.WeilBound.pow_mem_filt',
                                                                           'RiemannMasullo.WeilBound.finrank_map_filt_le',
                                                                           'RiemannMasullo.WeilBound.rank_quotient_le',
                                                                           'RiemannMasullo.WeilBound.card_algHom_apply_eq_zero_le'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/WeilBound/NonCancellation.lean': ['RiemannMasullo.WeilBound.eq_zero_of_sum_mul_pow_eq_zero',
                                                                                'RiemannMasullo.WeilBound.constantCoeff_comp_aeval',
                                                                                'RiemannMasullo.WeilBound.exists_algHom_powerSeries',
                                                                                'RiemannMasullo.WeilBound.not_X_pow_dvd',
                                                                                'RiemannMasullo.WeilBound.injective_of_expansion',
                                                                                'RiemannMasullo.WeilBound.baseChange',
                                                                                'RiemannMasullo.WeilBound.baseChange_monic',
                                                                                'RiemannMasullo.WeilBound.natDegree_baseChange',
                                                                                'RiemannMasullo.WeilBound.ι',
                                                                                'RiemannMasullo.WeilBound.ι_of',
                                                                                'RiemannMasullo.WeilBound.ι_root',
                                                                                'RiemannMasullo.WeilBound.ι_monoBasis',
                                                                                'RiemannMasullo.WeilBound.baseChange_hw',
                                                                                'RiemannMasullo.WeilBound.frobeniusAlgHom_pow_apply',
                                                                                'RiemannMasullo.WeilBound.nonCancellation'],
 'file:RiemannMasullo/ForMathlib/NumberTheory/WeilBound/PlaneCurve.lean': ['RiemannMasullo.WeilBound.bombieri_params',
                                                                           'RiemannMasullo.WeilBound.pointOf',
                                                                           'RiemannMasullo.WeilBound.pointOf_of',
                                                                           'RiemannMasullo.WeilBound.pointOf_root',
                                                                           'RiemannMasullo.WeilBound.exists_finset_t_fixed',
                                                                           'RiemannMasullo.WeilBound.exists_weight',
                                                                           'RiemannMasullo.WeilBound.exists_quot_bound',
                                                                           'RiemannMasullo.WeilBound.exists_expansion',
                                                                           'RiemannMasullo.WeilBound.weil_final_arith',
                                                                           'RiemannMasullo.WeilBound.weil_planeCurve_aux'],
 'file:RiemannMasullo/ForMathlib/RingTheory/DedekindDomain/Ideal/Lemmas.lean': ['RiemannMasullo.HeightOneSpectrum.eq_of_dvd_pow'],
 'file:RiemannMasullo/ForMathlib/RingTheory/Etale/IsDomainLocalization.lean': ['RiemannMasullo.isDomain_of_maximalIdeal_eq_span',
                                                                               'RiemannMasullo.isDomain_localization_of_etale'],
 'file:RiemannMasullo/ForMathlib/RingTheory/PicardGroup.lean': ['private RiemannMasullo.equivPic_mk0_eq_picMk',
                                                                'RiemannMasullo.picMapAlgebra_equivPic_mk0_of_isLocalization',
                                                                'RiemannMasullo.picMapAlgebra_surjective_of_isLocalization'],
 'file:RiemannMasullo/ForMathlib/RingTheory/Trace/Defs.lean': ['RiemannMasullo.trace_of_algebra_projection'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/ContinuousMonoidHom.lean': ['RiemannMasullo.continuousAddEquiv_factors_of_snd_eq_zero'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Group/AutomaticContinuity.lean': ['RiemannMasullo.exists_residual_continuousOn_of_measurable',
                                                                                    'RiemannMasullo.continuous_equivariant_of_residual_continuousOn',
                                                                                    'RiemannMasullo.continuous_equivariant_of_continuous_injective_comp'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Group/CharacterExtension.lean': ['RiemannMasullo.exists_complexCharacter_extension_of_isOpenEmbedding'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Group/CompactOpen.lean': ['RiemannMasullo.monoidHom_eq_one_of_compact_range_subset_ball',
                                                                            'RiemannMasullo.isOpen_singleton_one_complex',
                                                                            'RiemannMasullo.exists_finset_complexCharacter_eq_one'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Group/Divisible.lean': ['RiemannMasullo.exists_continuousAddEquiv_prod_quotient_of_open'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Group/Pointwise.lean': ['RiemannMasullo.exists_nhds_zero_closure_add_avoids_finset'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Group/Units.lean': ['RiemannMasullo.compactSpace_units_of_compactSpace',
                                                                      'RiemannMasullo.isClosed_range_unitsMap'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/GroupCompletion.lean': ['RiemannMasullo.isQuotientMap_rangeFactorization_completion_map',
                                                                          'RiemannMasullo.completion_map_surjective_of_isOpenQuotientMap'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/InfiniteSum.lean': ['RiemannMasullo.summableUniformlyOn_of_ge'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/InfiniteSum/NatInt.lean': ['private '
                                                                             'RiemannMasullo.exists_perm_finset_range',
                                                                             'RiemannMasullo.hasSum_of_summable_conditional_permutations'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/InfiniteSum/Real.lean': ['RiemannMasullo.exists_pos_tendsto_zero_summable_div'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Module/ContinuousLinearMap/Quotient.lean': ['RiemannMasullo.exists_ker_quotientAction',
                                                                                              'RiemannMasullo.exists_ker_quotientEquiv_of_rightInverse',
                                                                                              'RiemannMasullo.exists_quotient_equiv_of_kernel',
                                                                                              'RiemannMasullo.quotient_equiv_of_scaled_range',
                                                                                              'RiemannMasullo.range_smul_comp_of_surjective',
                                                                                              'RiemannMasullo.isOpenMap_rangeRestrict_of_factor',
                                                                                              'RiemannMasullo.isClosed_range_of_factor',
                                                                                              'RiemannMasullo.quotient_of_sequential_comparison',
                                                                                              'ContinuousLinearEquiv.quotientMapEquiv',
                                                                                              'Submodule.exists_exact_quotient_maps',
                                                                                              'ContinuousLinearMap.exists_quotient_range_equiv',
                                                                                              'Submodule.exists_continuous_quotient_family'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Module/OpenMapping.lean': ['RiemannMasullo.isOpenMap_of_closure_image_mem_nhds_zero',
                                                                             'RiemannMasullo.isOpenMap_of_not_isMeagre_range'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Module/StrongDualQuotient.lean': ['RiemannMasullo.completeSpace_strongDual_quotient',
                                                                                    'RiemannMasullo.range_transpose_mkQL',
                                                                                    'RiemannMasullo.isClosed_range_transpose_mkQL'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/OpenSubgroup.lean': ['RiemannMasullo.exists_compact_openSubgroup_sub_mem_nhds'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/PontryaginDual.lean': ['private '
                                                                         'RiemannMasullo.dense_span_restrictedCharacters',
                                                                         'RiemannMasullo.dense_span_pontryaginDual',
                                                                         'RiemannMasullo.exists_pontryaginDual_extension_of_compact',
                                                                         'private '
                                                                         'RiemannMasullo.exists_extension_of_compact_source',
                                                                         'RiemannMasullo.exists_pontryaginDual_extension_trivial_on_compact'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/PontryaginDual/Compact.lean': ['RiemannMasullo.exists_isCompact_pontryaginDual_polar'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/PontryaginDual/Cyclic.lean': ['RiemannMasullo.exists_cyclicProductCharacterHomeomorph'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/PontryaginDual/Pi.lean': ['RiemannMasullo.exists_finset_circleCharacter_eq_prod_zpow'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/PontryaginDual/Real.lean': ['RiemannMasullo.exists_realPontryaginDualEquiv'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/PontryaginDual/Separation.lean': ['private '
                                                                                    'RiemannMasullo.haarTranslation',
                                                                                    'private '
                                                                                    'RiemannMasullo.haarTranslation_norm',
                                                                                    'private '
                                                                                    'RiemannMasullo.haarTranslation_continuous',
                                                                                    'private '
                                                                                    'RiemannMasullo.haarTranslation_ne_one',
                                                                                    'private '
                                                                                    'RiemannMasullo.aestronglyMeasurableOn_of_finite_measure',
                                                                                    'private '
                                                                                    'RiemannMasullo.integrable_weighted_orbit',
                                                                                    'private '
                                                                                    'RiemannMasullo.averageOrbit',
                                                                                    'private '
                                                                                    'RiemannMasullo.averageOrbit_apply',
                                                                                    'private '
                                                                                    'RiemannMasullo.averageOrbit_translate',
                                                                                    'private '
                                                                                    'RiemannMasullo.averageOrbit_commutes',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_averageOrbit_close',
                                                                                    'private '
                                                                                    'RiemannMasullo.averageOrbit_dense',
                                                                                    'private '
                                                                                    'RiemannMasullo.norm_averageOrbit_le',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_compact_test_of_gelfand',
                                                                                    'private '
                                                                                    'RiemannMasullo.unitary_apply_star',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_commutative_algebra_with_averages',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_compact_test_of_averageOrbit',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_character_of_rep_ne_one',
                                                                                    'RiemannMasullo.exists_pontryaginDual_apply_ne_one',
                                                                                    'RiemannMasullo.exists_compact_pontryaginDual_test',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_measure_of_positive_functional',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_spectral_measure',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_continuous_dual_of_spectrum',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_dual_measure_of_operators',
                                                                                    'private '
                                                                                    'RiemannMasullo.exists_dual_measure_of_unitary',
                                                                                    'RiemannMasullo.exists_haar_autocorrelation_measure'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/RestrictedProduct/TopologicalSpace.lean': ['RiemannMasullo.continuous_restrictedProduct_of_uniform',
                                                                                             'RiemannMasullo.isOpen_restrictedProduct_forall_mem',
                                                                                             'RiemannMasullo.restrictedProductUnitsEquiv',
                                                                                             'RiemannMasullo.isCompact_closure_restrictedProduct_iff',
                                                                                             'RiemannMasullo.restrictedProductCongr',
                                                                                             'RiemannMasullo.restrictedProductSplitFinset',
                                                                                             'RiemannMasullo.hasProd_restrictedProduct_mulSingle'],
 'file:RiemannMasullo/ForMathlib/Topology/Algebra/Valued/LocallyConstant.lean': ['RiemannMasullo.exists_finsupp_valuation_dilation_sub'],
 'file:RiemannMasullo/ForMathlib/Topology/Compactness/LocallyCompact.lean': ['RiemannMasullo.locallyCompactSpace_sigma'],
 'file:RiemannMasullo/ForMathlib/Topology/Compactness/Paracompact.lean': ['RiemannMasullo.exists_seq_finite_preimage_of_not_subset_compact'],
 'file:RiemannMasullo/ForMathlib/Topology/ContinuousMap/CompactlySupported.lean': ['RiemannMasullo.denseRange_toContinuousMap_of_real_smul'],
 'file:RiemannMasullo/ForMathlib/Topology/ContinuousMap/LocallyConvex.lean': ['RiemannMasullo.polynormableSpace_continuousMap'],
 'file:RiemannMasullo/ForMathlib/Topology/ContinuousMap/Sigma.lean': ['RiemannMasullo.continuous_continuousMap_sigma_of_components',
                                                                      'RiemannMasullo.exists_compactSupport_sigma_linearEquiv'],
 'file:RiemannMasullo/ForMathlib/Topology/Covering/AddCircle.lean': ['RiemannMasullo.exists_addCircle_addMonoidHom_lift',
                                                                     'RiemannMasullo.exists_addCircle_coe_linearMap_eq',
                                                                     'RiemannMasullo.exists_addCircle_coe_mul_eq'],
 'file:RiemannMasullo/ForMathlib/Topology/LocallyConstant/CompactSupport.lean': ['RiemannMasullo.exists_countable_span_of_locallyConstant_compactSupport'],
 'file:RiemannMasullo/ForMathlib/Topology/Maps/Strict/Module.lean': ['private '
                                                                     'RiemannMasullo.isStrictMap_comp_ker_subtype_of',
                                                                     'RiemannMasullo.isStrictMap_comp_ker_subtype_iff'],
 'file:RiemannMasullo/ForMathlib/Topology/MetricSpace/CompactQuotient.lean': ['RiemannMasullo.exists_isCompact_image_eq_of_isOpenQuotientMap'],
 'file:RiemannMasullo/ForMathlib/Topology/UniformSpace/CompactConvergence.lean': ['RiemannMasullo.isUniformAddGroup_continuousMap',
                                                                                  'RiemannMasullo.isComplete_continuousMap_of_isComplete_eval']}
DEVIATING = {'file:RiemannMasullo/ForMathlib/Topology/Algebra/RestrictedProduct/TopologicalSpace.lean': ['RiemannMasullo.isCompact_closure_restrictedProduct_iff',
                                                                                             'RiemannMasullo.restrictedProductCongr',
                                                                                             'RiemannMasullo.restrictedProductSplitFinset']}
OUTSIDE_ITEMS = {'file:RiemannMasullo/ForMathlib/Analysis/Distribution/TestFunction/Schwartz.lean': {'AppC_LCTVS': ['definition:C.1.3.1',
                                                                                                    'text:C.1.5'],
                                                                                     'AppD_SchwartzBruhat': ['remark:C.1.3.3']},
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/TensorProduct/Bounded.lean': {'AppC_LCTVS': ['corollary:C.2.3.12',
                                                                                                     'definition:C.1.3.1',
                                                                                                     'definition:C.1.4.2',
                                                                                                     'definition:C.2.4.1',
                                                                                                     'eq:C.2.3.1',
                                                                                                     'eq:C.2.3.2',
                                                                                                     'eq:C.2.3.4',
                                                                                                     'eq:C.2.3.5',
                                                                                                     'eq:C.2.3.7',
                                                                                                     'eq:C.2.3.9',
                                                                                                     'eq:C.2.3.14',
                                                                                                     'eq:C.2.3.15',
                                                                                                     'eq:C.2.3.22',
                                                                                                     'eq:C.2.3.25',
                                                                                                     'lemma:C.2.3.5',
                                                                                                     'proposition:C.1.5.3',
                                                                                                     'proposition:C.2.3.7',
                                                                                                     'proposition:C.2.3.9',
                                                                                                     'remark:C.2.3.2',
                                                                                                     'text:C.1.5',
                                                                                                     'text:C.2.3',
                                                                                                     'text:C.2.3.2',
                                                                                                     'text:C.2.3.4'],
                                                                                      'AppD_SchwartzBruhat': ['remark:C.1.3.3']},
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/TensorProduct/Comparison.lean': {'AppC_LCTVS': ['definition:C.1.3.1',
                                                                                                        'definition:C.2.4.1',
                                                                                                        'eq:C.2.3.4',
                                                                                                        'eq:C.2.3.7',
                                                                                                        'eq:C.2.3.14',
                                                                                                        'eq:C.2.3.22',
                                                                                                        'eq:C.3.1.1',
                                                                                                        'example:C.1.4.6',
                                                                                                        'lemma:C.2.1.2',
                                                                                                        'proposition:C.1.5.3',
                                                                                                        'proposition:C.2.5.1',
                                                                                                        'remark:C.2.1.8',
                                                                                                        'remark:C.3.1.1',
                                                                                                        'text:C.1.5',
                                                                                                        'text:C.2.3',
                                                                                                        'text:C.2.3.2',
                                                                                                        'text:C.2.3.4']},
 'file:RiemannMasullo/ForMathlib/Analysis/LocallyConvex/TensorProduct/StrongDual.lean': {'AppC_LCTVS': ['definition:C.2.4.1',
                                                                                                        'eq:C.2.3.14',
                                                                                                        'eq:C.2.3.22',
                                                                                                        'eq:C.2.3.23',
                                                                                                        'eq:C.3.1.1',
                                                                                                        'remark:C.3.1.1',
                                                                                                        'text:C.2.3']},
 'file:RiemannMasullo/ForMathlib/NumberTheory/NumberField/DedekindZeta/MultipleZero.lean': {'Ch01_Introduction': ['text:1.4.5',
                                                                                                                  'text:1.4.7'],
                                                                                            'Ch03_IdelicZeta': ['definition:3.2.1.2',
                                                                                                                'definition:3.2.1.4',
                                                                                                                'eq:3.2.1.3',
                                                                                                                'eq:3.2.1.10',
                                                                                                                'lemma:3.2.1.1',
                                                                                                                'proposition:3.2.1.3',
                                                                                                                'text:3.2.1'],
                                                                                            'Ch06_LocalGlobal': ['terminology:6.3.1.1'],
                                                                                            'AppA_AlgebraicNT': ['eq:A.1.3.6'],
                                                                                            'AppB_AnalyticNT': ['eq:B.4.2.3',
                                                                                                                'lemma:B.1.1.2']}}


def build():
    return declarations.build(ID, CHAPTER, DECLS=DECLS, DEVIATING=DEVIATING,
                              OUTSIDE_ITEMS=OUTSIDE_ITEMS)
