"""M5: the printed claims the Lean refutes.

A statement false as printed is kept in riemann-masullo as `Printed.<name>`, with a theorem `Printed.<name>_false`
that proves its negation (ERRATA.md, "How this file is kept"). This poster draws every such refutation: where it
is, what it rests on, and the ERRATA.md entries that name it in code, with their Checked values.

ERRATA.md's own rule is the check: an entry is checked *Lean* when its refutation "is a proof checked by Lean that
rests on no statement still unproved". The terms say, for each refutation, whether anything open is below it.
"""
import collections
import re

import chapter as CH
import draw
import items as I
import lib
import rm

ID = "M5"
SLUG = "refuted"

# refutation -> (the entries that name it in code, their Checked values, "clean" when nothing open is below it,
# else the open declarations below it)
REFUTED = {'RiemannMasullo.Printed.absolutePWCondensation_traceNorm_tendsto_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.absolutePWCondensation_trace_tendsto_false': ([],
                                                                       [],
                                                                       ['private '
                                                                        'RiemannMasullo.spectralStripConvolution_traceCauchy_compact_block_series']),
 'RiemannMasullo.Printed.adeleFiniteOrbit_transporter_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.adeleNormOneOrbitMap_isQuotientMap_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.adeleNormOneOrbitUnion_locallyCompactSpace_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.adeleSchwartz_eq_sum_compactSubgroup_rectangles_false': (['F11'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.adelicAverage_at_zero_le_fractionalIdeal_false': (['F208'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.adelicTheta_riemannRoch_false': (['F13'], ['integrator'], 'clean'),
 'RiemannMasullo.Printed.archFlatProjectiveTensorEmbedding_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.archNuclearityDenominator_nonzero_closed_false': (['F133'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.archNuclearityJet_apply_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.archNuclearityJet_basis_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.archNuclearityJet_span_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.archNuclearityStrongDual_not_nuclear_false': (['F139'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.archNuclearity_existsUnique_localFlatRepresentative_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.archNuclearity_gammaContour_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.archNuclearity_polar_codimension_two_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.archNuclearity_trace_false': (['F138'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.archimedeanWeightedSchwartz_tensor_false': (['F54'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.asymptoticCauchy_leftHalfPlane_false': (['F14'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.compactIntervalPeriodization_kernel_support_false': (['F15'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.compactPeriodization_surjective_false': (['F15'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.completedHeckeL_logDeriv_reflection_false': (['F35'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.completedHeckeL_residues_false': (['F209'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.completedInductiveTensor_bornological_false': (['F227'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.completedInductiveTensor_directLimits_isEmbedding_false': (['F226'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.complexLogFourier_finitePart_false': (['F41'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.cond_adelicTheta_pointwiseConvergence_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.cond_homogeneousTheta_pointwiseConvergence_false': (['F160', 'F161'],
                                                                             ['reviewed', 'reviewed'],
                                                                             'clean'),
 'RiemannMasullo.Printed.criticalTraceFormula_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.criticalTraceTestCodimension_false': (['F248'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.dSequenceKernelSmoothening_mul_continuous_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.dedekindZeta_perron_contour_in_zeroFreeRegion_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.diagonalIndentationLift_regular_iff_false': (['F173', 'F216'], ['Lean', 'Lean'], 'clean'),
 'RiemannMasullo.Printed.diracPolynomials_coefficientSeminorms_false': (['F46'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.distribution_coordinatePlane_coefficientCount_false': (['F47'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.distribution_coordinatePlane_coefficientOrder_false': (['F48'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.distribution_coordinatePlane_decomposition_eq_sum_false': (['F49'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.epsilonBasisLift_of_dense_image_false': (['F190'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.epsilonBasisLift_schauder_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.euclideanBallCube_isDPrimeSequence_false': (['F171'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.exists_disjoint_dSequence_translates_false': (['F221'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.exists_heights_reciprocalPartialHeckeEulerProduct_boundedBelow_false': (['F21'],
                                                                                                 ['Lean'],
                                                                                                 'clean'),
 'RiemannMasullo.Printed.exists_sLocalNormOneCharacter_false': (['F31'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.exists_schwartz_zeroExtension_of_backwardSemiExponentialDecay_false': (['F224'],
                                                                                                ['Lean'],
                                                                                                'clean'),
 'RiemannMasullo.Printed.finiteEigendistribution_unitShell_false': (['F45'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.finiteHeckeL_quadratic_of_real_zero_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.finiteHeckeL_sq_entire_of_not_quadratic_false': (['F24'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.finiteLog_isSchwartzBruhat_false': (['F40'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.finitePlaceDifference_uniformizerIndependent_and_range_false': (['F213'],
                                                                                         ['reviewed'],
                                                                                         'clean'),
 'RiemannMasullo.Printed.finiteStandardGaussian_zeta_of_ramified_positive_false': (['F73'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.finiteWeilPrincipalValue_positiveDensity_false': (['F42'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.forwardSemiExponentialDecay_of_single_rate_false': (['F224'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.globalConverse_normTwist_bergmanMiddle_residues_surjective_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.globalConverse_normTwist_printedGenerator_divides_false': (['F80'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.globalConverse_polarCoordinates_surjective_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.globalConverse_polarValues_eq_eigendistributions_false': (['F77'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.globalIdelicZFunction_functionalEquation_false': (['F13'], ['integrator'], 'clean'),
 'RiemannMasullo.Printed.globalLineSpectralKernel_weighted_not_memLp_false': (['F262'],
                                                                              ['reviewed'],
                                                                              ['private '
                                                                               'RiemannMasullo.spectralStripConvolution_traceCauchy_compact_block_series']),
 'RiemannMasullo.Printed.globalPrincipalValueConverse_normTwist_ideal_subset_bergman_false': (['F82'],
                                                                                              ['reviewed'],
                                                                                              'clean'),
 'RiemannMasullo.Printed.globalPrincipalValueConverse_normTwist_ordinaryResidues_exact_false': (['F84'],
                                                                                                ['reviewed'],
                                                                                                'clean'),
 'RiemannMasullo.Printed.globalPrincipalValueConverse_normTwist_printedResidues_false': (['F83'],
                                                                                         ['reviewed'],
                                                                                         'clean'),
 'RiemannMasullo.Printed.globalThetaMellinIntegral_integrable_of_nontrivial_false': (['F210'],
                                                                                     ['reviewed'],
                                                                                     'clean'),
 'RiemannMasullo.Printed.globalThetaPolarValues_eq_eigendistributions_false': (['F65'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.globalThetaSobolevPrincipalValue_closedRange_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.globalThetaSobolevPrincipalValue_isClosedEmbedding_false': (['F162'],
                                                                                     ['reviewed'],
                                                                                     'clean'),
 'RiemannMasullo.Printed.globalThetaSobolevPrincipalValue_range_eq_jetKernels_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.globalThetaSobolev_allTests_integrable_false': (['F149'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.globalThetaSobolev_closedIntervals_finite_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.globalThetaSobolev_rawIsotypeDecomposition_false': (['F150'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.globalTheta_inversionAutomorphism_false': (['F29'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.hardySobolevJetKernelProjection_tendsto_false': (['F144'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.hardySobolevTranslation_conformal_false': (['F187'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.hardySobolevTranslation_preserves_finiteNorm_false': (['F175'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.hardySobolevTranslation_seminorm_le_false': (['F175'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.hasSlowGrowthNearPoles_completedHeckeL_logDeriv_false': (['F33'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.heckeArchimedean_integral_convergesAtTop_false': (['F38'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.heckeArchimedean_logDeriv_false': (['F37', 'F39'], ['Lean', 'Lean'], 'clean'),
 'RiemannMasullo.Printed.heckeArchimedean_mellinLogDeriv_centered_false': (['F37'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.heckeAsymptoticResidue_poleTerm_false': (['F32'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.heckeAsymptoticResidue_reversedSigns_false': (['F34'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.heckeExplicitFormula_poleTerm_false': (['F32'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.heckeIdealSummatory_tendsto_of_trivial_on_normOne_false': (['F25'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.heckeLogDerivPolynomial_perron_error_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.heckePrimePowerLogTail_sub_correction_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.heckePrimePowerTailOscillation_at_pole_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.heckePrimePower_mellinSample_false': (['F36'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.heckePrimePower_mellinSample_reflected_false': (['F36'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.hilbertEpsilonBasisLift_of_dense_image_false': (['F190'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.ideleClassSobolev_inversion_automorphism_false': (['F151'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.ideleNormBand_isCompact_false': (['F210'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.idelicExplicitFormula_archNormalization_false': (['F43'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.infiniteCanonicalHaar_eq_tamagawa_of_isReal_false': (['F245'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.infiniteStandardThetaAverage_schwartz_logProfile_false': (['F76'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.infinite_split_primes_reciprocalEulerProduct_normTwist_false': (['F95'],
                                                                                         ['Lean'],
                                                                                         'clean'),
 'RiemannMasullo.Printed.introTraceApprox_archimedean_bounded_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.introTraceApprox_archimedean_montel_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.introTraceApprox_conjugateWeight_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.introTraceApprox_primeSum_tendsto_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.introTraceApprox_spectral_limit_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.introTrace_characterTrace_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.introTrace_globalTrace_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.introTrace_regularized_logDeriv_analytic_false': (['F256'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.introTrace_transition_mellin_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.inv_ideleNormSectionNeighborhood_false': (['F220'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.inv_sLocalNormSectionNeighborhood_false': (['F220'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.invariantPWCondensation_traceNorm_tendsto_false': (['F241'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.invariantPWCondensation_trace_tendsto_false': ([],
                                                                        [],
                                                                        ['private '
                                                                         'RiemannMasullo.spectralStripConvolution_traceCauchy_compact_block_series']),
 'RiemannMasullo.Printed.isDDoublePrimeSequence_quotient_iff_false': (['F218'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.isDPrimeSequence_ideleLogNeighborhood_false': (['F219'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.isDPrimeSequence_infiniteIdeleLogNeighborhood_false': (['F219'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.isDPrimeSequence_sLocalIdeleLogNeighborhood_false': (['F219'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.isNuclearTVS_of_isSchwartzFrechet_false': (['F3'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.kroneckerWeyl_riemannIntegrable_forward_false': (['F20'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.latticeShiftedPowerSum_converges_false': (['F207'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.lcaTopologicalLie_dual_locallyCompact_false': (['F231'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.localEulerFactor_mellinSamples_eq_cauchyIntegral_false': (['F18'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.logPolynomialGrowth_bound_for_every_exponent_false': (['F224'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.modulatedAbsoluteCutoffOperator_injective_false': (['F238'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.modulatedCompactSupport_isotypicQuotient_equiv_false': (['F174'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.modulatedExponentialDecay_bounded_iff_countable_twists_false': (['F12'],
                                                                                         ['reviewed'],
                                                                                         'clean'),
 'RiemannMasullo.Printed.modulatedIntervalPeriodization_projectiveQuotient_continuous_false': (['F174'],
                                                                                               ['reviewed'],
                                                                                               'clean'),
 'RiemannMasullo.Printed.modulatedIntervalPeriodization_projective_sequential_false': (['F174'],
                                                                                       ['reviewed'],
                                                                                       'clean'),
 'RiemannMasullo.Printed.modulatedPoissonSummation_false': (['F232'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.modulatedPoisson_radialIntegral_eq_kernelIntegral_false': (['F232'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.modulatedQuotientLogMoment_biorthogonal_basis_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.orbitalAnnihilator_prime_products_false': (['F99', 'F103'],
                                                                    ['reviewed', 'reviewed'],
                                                                    'clean'),
 'RiemannMasullo.Printed.orbitalEulerProduct_eq_primary_false': (['F164'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.orbitalEulerSum_eq_poisson_false': (['F243'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.orbitalJet_memLp_false': (['F165'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.orbitalJet_norm_annulus_false': (['F168', 'F169'], ['Lean', 'Lean'], 'clean'),
 'RiemannMasullo.Printed.orbitalJets_basis_fullAnnihilator_false': (['F166'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.orbitalJets_not_subset_ball_false': (['F170'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.orbitalPrimeJetSpace_finite_false': (['F104'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.orbitalQuotientDual_missingPV_false': (['F167'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.orbitalTracesOnPaleyWienerLevels_false': (['F244', 'I358'],
                                                                   ['reviewed', 'reviewed'],
                                                                   ['private '
                                                                    'RiemannMasullo.spectralStripConvolution_traceCauchy_compact_block_series']),
 'RiemannMasullo.Printed.outsideLocalUnits_embed_in_ideles_false': (['F69'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.padicTamagawaFourier_translatedScaledIntegers_false': (['F217'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.positiveRealExponentialDecay_log_equiv_false': (['F176'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.positiveRealExponentialDecay_valueDecay_false': (['F52'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.primaryDivisorialCutTrace_false': (['I359'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.primaryDivisorialIndicator_localLimit_false': (['I359'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.primaryDivisorialStratum_eq_norm_preimage_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.primeOrbitalSobolevDenominator_closed_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.projectiveTensorMap_isEmbedding_false': (['F7'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.ratAdeleFundamentalDomain_disjoint_false': (['F4'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.realArchimedeanMellin_monomial_false': (['F55'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.realLogFourier_finitePart_false': (['F41'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.reciprocalHeckeEulerProductBelow_mul_normTwist_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.reciprocalHeckeEulerProductBelow_not_uniform_at_pole_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.reciprocalPartialHeckeEulerProduct_unshifted_zeros_false': (['F85'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.regularIsotypicTransform_isometries_false': (['F211'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.relativelyCompactActionAverage_properties_false': (['F212'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.relativelyCompactActionIsotypicAverage_properties_false': (['F212'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.restrictedProduct_openBox_false': (['F1'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sAdditiveTamagawaMeasure_eq_covolumeOne_false': (['F10'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sAdeleFiniteOrbit_transporter_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sAdelePolarFreeTensor_quasiCharacter_mul_false': (['F236'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sAdelePolarFree_inclusion_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sAdeleQuotient_isRatVectorSpace_false': (['F2'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sIdeleFundamentalDomain_cover_false': (['F6'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sIdeleIntervalSobolevDensity_vanishesAtInfinity_false': (['F148'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sLocalAbsolutePWSobolev_memLp_false': (['F258'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalAbsolutePW_seqDense_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalAbsolutePW_zeroMoment_codim_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalArchimedeanPoleMultiplicity_eq_sum_false': (['I313'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalCarvingCutoffProduct_descends_false': (['F205'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalCarvingLimit_eq_rawClosedSpan_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalCarvingOutsideUnits_schwartzBruhat_false': (['F204'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalCarving_cutoff_norm_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalCechBergman_reflection_false': (['F63'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalCechRadialReflection_false': (['F62'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalCech_right_commutes_false': (['F64'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalChangeOfChart_pureNormBase_false': (['F115'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sLocalCoordinate_closedEmbedding_false': (['F114'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sLocalCutoffCarving_strictSubsequence_false': (['F215'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalFunctionalEquation_extra_epsilon_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalGammaFiltration_antitone_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalGammaFiltration_dual_span_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalHomogeneousAdelicTheta_asymptotic_false': (['F87', 'F89'],
                                                                          ['reviewed', 'reviewed'],
                                                                          'clean'),
 'RiemannMasullo.Printed.sLocalIdelicMellin_transition_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalIdelicZFunction_principalValue_has_poles_false': (['I312'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalIdelicZFunction_verticalIntegrable_neg_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalInvariantPWSobolev_memLp_false': (['F258'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalInvariantPW_seqDense_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalMellin_surjective_divisorBounded_false': (['F112'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalOrbitalPhase_sub_false': (['F120'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sLocalOrbitalPrincipalParts_eigendistributions_false': (['F106'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPWOrbitalQuotients_defined_false': ([],
                                                                   [],
                                                                   ['private '
                                                                    'RiemannMasullo.sLocalMellinSchwartzBounds_meyer_infinite_span_outside_real_profiles']),
 'RiemannMasullo.Printed.sLocalPWOrbital_bases_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPWTests_twoMoments_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPWTransition_eq_units_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPW_principalValue_diagram_false': ([],
                                                                  [],
                                                                  ['private '
                                                                   'RiemannMasullo.sLocalMellinSchwartzBounds_meyer_infinite_span_outside_real_profiles']),
 'RiemannMasullo.Printed.sLocalPlaceOrbitalSupportComparison_isomorphism_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPlaceOrbitalSupportTests_inclusion_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPolarMultiplicity_greatest_smaller_false': (['F98'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPolarMultiplicity_trivial_origin_false': (['F93'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPolarPrincipalValue_tfae_exact_order_false': (['F118'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPrimaryOrbitalSupportComparison_isomorphism_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPrimaryOrbitalSupportTests_inclusion_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPrimaryPoleMultiplicity_eq_sum_orders_false': (['F119'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPrincipalPartCoeff_any_contour_false': (['F105'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPrincipalPartCoeff_eigendistribution_false': (['F106'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPrincipalPartCoeff_leading_literal_false': (['F105'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPrincipalPartCoeff_leading_unscaled_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPrincipalPartCoeff_lower_literal_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalPrincipalPartCoeff_universal_pole_bound_false': (['F107'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalPrincipalValue_tfae_exact_order_false': (['F118'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalProductCutoff_preservesSchwartzBruhat_false': (['F246'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalRestriction_surjective_false': (['F57'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sLocalRhoFactor_complex_positive_shift_false': (['F86'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalRhoFactor_iteratedDeriv_isBigO_false': (['F16'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalRhoPoleOrder_le_of_re_neg_odd_false': (['F97'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalSchwartz_invariants_projectiveLaurent_equiv_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalSmoothMass_eq_sharp_real_false': (['I392'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalSpatialCutoff_realFlatRange_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalStandardThetaTensor_factorization_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalStandardThetaTensor_inverseAverage_quotient_equiv_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalThetaEigendistributions_separate_of_interval_false': (['F67'],
                                                                                     ['reviewed'],
                                                                                     'clean'),
 'RiemannMasullo.Printed.sLocalThetaPoleBound_eigen_annihilator_false': (['F106'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalThetaPoleBound_full_eq_polarFree_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalThetaPoleBound_low_coefficients_exact_false': (['F108', 'F109', 'F110'],
                                                                              ['reviewed', 'reviewed', 'reviewed'],
                                                                              'clean'),
 'RiemannMasullo.Printed.sLocalThetaPoleBound_printed_mellin_sequence_false': (['F111', 'F112'],
                                                                               ['reviewed', 'reviewed'],
                                                                               'clean'),
 'RiemannMasullo.Printed.sLocalThetaSobolev_fourier_on_line_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalThetaSobolev_integrable_false': (['F146'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sLocalThetaSobolev_openHalfLine_finite_false': (['F145'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalThetaSobolev_rawIsotypeDecomposition_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalThetaToHomogeneousProduct_strictlyCoarser_nonclosed_false': (['F72'],
                                                                                            ['Lean'],
                                                                                            'clean'),
 'RiemannMasullo.Printed.sLocalTraceFourierCutoff_preservesSchwartzBruhat_false': (['F246'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalZLaurentCoeff_any_contour_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalZLaurentCoeff_eigendistribution_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalZLaurentCoeff_finitePlace_support_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.sLocalZLaurentCoeff_mellinResidue_false': (['F89'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalZetaPair_reflectedShift_false': (['F61'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sLocalZetaPair_translate_false': (['F60'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.sampledHardySobolevTopology_independent_false': (['F233'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.sampledHardySobolev_eval_boundary_iff_false': (['F237'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.schwartzBergman_jet_continuous_on_ordinary_schwartz_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.schwartzBergman_jet_eq_mellinInv_shifted_moment_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.schwartzBergman_normalizedJet_le_max_false': (['F102'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.singletonDecay_approximation_isotype_band_false': (['F175'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.smoothCutoffMultiplier_isClosedRange_false': (['F186'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.spectralAnnihilator_product_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralCutoffFamily_continuous_false': (['F188'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.spectralLineBandAdjoint_contains_selectedEvaluations_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineBand_jetCount_le_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineCompletion_descends_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineCompletion_quotientInjective_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineConvolution_conjugateWeight_false': (['F177', 'F239'],
                                                                          ['reviewed', 'reviewed'],
                                                                          'clean'),
 'RiemannMasullo.Printed.spectralLineConvolution_conjugateWeight_range_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineConvolution_trace_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineIsotype_bandAdjoint_contains_jets_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineJet_annulus_and_noncontainment_false': (['F154', 'F156'],
                                                                             ['reviewed', 'reviewed'],
                                                                             'clean'),
 'RiemannMasullo.Printed.spectralLineJet_annulus_false': (['F154'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralLineJet_cofinite_iff_coordinates_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineJet_lexInitialSegment_finite_false': (['F198'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralLineJet_memLp_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineJet_not_subset_ball_false': (['F156'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralLineJet_uniformBiorthogonalBound_false': (['F214'],
                                                                           ['reviewed'],
                                                                           ['private '
                                                                            'RiemannMasullo.spectralLineJet_rational_critical_zero_count']),
 'RiemannMasullo.Printed.spectralLineKernel_extraWeight_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineMarkushevichBasis_false': (['F152'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralLineMarkushevichBasis_normalized_false': (['F152'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralLineMarkushevichBasis_primal_normalized_false': (['F158'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralLineSamples_rapid_for_any_numbering_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineSelection_exists_isolatingInterval_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineTestTopology_false': (['F153'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.spectralLineTruncatedKernel_geometric_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralLineZeroEnumeration_false': (['F197'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralNuclearity_factorialNormalization_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralNuclearity_trace_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralPlancherelMeasure_eq_radialVolume_prod_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralRegular_dual_bounded_false': (['F157'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.spectralSchwartzBiorthogonal_unique_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralStripBasisLift_uniformUpperBound_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralStripConvolution_conjugateWeight_false': (['F177', 'F240'],
                                                                           ['reviewed', 'reviewed'],
                                                                           'clean'),
 'RiemannMasullo.Printed.spectralStripConvolution_conjugateWeight_range_false': (['F177'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralStripConvolution_trace_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralStripJet_annulus_and_noncontainment_false': (['F156'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralStripJet_memLp_false': (['F152'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralStripJet_not_subset_ball_singleton_false': (['F156'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralStripMarkushevichBasis_false': (['F152'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralStripMarkushevichBasis_normalized_false': (['F159'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralStripMellinJet_norm_le_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralStripMultiplicity_unbounded_false': (['F184'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.spectralStripRestrictionKernel_geometric_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.spectralStripZeroEnumeration_false': (['F197'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.strongCoprimalityFourierJet_zero_full_false': (['F142'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.strongCoprimalityPrimaryQuotient_strongDual_subquotient_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.strongCoprimality_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.strongDual_pairing_continuous_false': (['F228'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.strongDualityTopology_eq_mackeyTopology_iff_barrelled_false': (['F5'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.stronglyRecurrentOn_compact_of_closedBall_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.summable_bruhatMellin_of_discreteStrips_false': (['F44'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.tendsto_dSequenceAverage_mul_false': (['F223'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.tensorDualOperator_represents_finiteRank_false': (['F225'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.testFunction_inductiveTensor_equiv_false': (['F50'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.testFunction_no_projectiveOrInjectiveTensor_equiv_false': (['F51'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.thetaFourier_insertion_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.thetaInducedTopology_t2_false': (['F28'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.thetaIsotypeSum_strictlyFiner_false': (['F71'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.thetaIsotypicAverage_idempotent_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.torusFlow_injective_of_linearIndependent_false': (['F19'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.traceFormula_false': (['F267', 'I354', 'I372'],
                                               ['reviewed', 'reviewed', 'reviewed'],
                                               'clean'),
 'RiemannMasullo.Printed.traceNorm_mul_eq_false': (['F9'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.truncatedHardySobolevConvolution_diagonal_tendsto_false': (['F175'],
                                                                                    ['reviewed'],
                                                                                    'clean'),
 'RiemannMasullo.Printed.truncatedPerron_error_of_isBigO_false': ([], [], 'clean'),
 'RiemannMasullo.Printed.tsum_norm_hilbertDiagonal_eq_false': (['F8'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.uniformContinuous_dSequenceAverage_false': (['F222'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.unshiftedHeckeRegularization_entire_false': (['F192'], ['reviewed'], 'clean'),
 'RiemannMasullo.Printed.weaklyContDiffOn_lipschitz_false': (['F229'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.weilQuotientIntegral_measurable_false': (['F230'], ['Lean'], 'clean'),
 'RiemannMasullo.Printed.wirtinger_exponentialDecay_false': (['F53'], ['reviewed'], 'clean')}
# (Checked value of an entry, "clean" or "rests") -> entries that name a refutation
SUMMARY = {('Lean', 'clean'): 84, ('integrator', 'clean'): 1, ('reviewed', 'clean'): 96, ('reviewed', 'rests'): 4}
# the Checked "Lean" entries that name no refutation
LEAN_UNNAMED = []

W = 2400


def entries_naming(m, refs):
    """entry -> the refutations its row names in code, in any column."""
    out = {}
    for e in m.entries:
        cells = rm.split_row(m.errata_lines[e["line"] - 1])
        names = re.findall(r"`([^`]+)`", " ".join(cells))
        rs = sorted({d.key for n in names if (d := m.resolve(n)) is not None and d.key in refs})
        out[e["id"]] = rs
    return out


def build():
    m = rm.load()
    refs = {d.key: d for d in m.decls if ".Printed." in d.name and d.name.endswith("_false")}
    named = entries_naming(m, refs)
    entry = {e["id"]: e for e in m.entries}
    by_ref = collections.defaultdict(list)
    for eid in sorted(named, key=lambda s: (s[0], int(s[1:]))):
        for k in named[eid]:
            by_ref[k].append(eid)
    refuted = {}
    for k in sorted(refs):
        d = refs[k]
        below = [o.key for o in m.open_below(d.i)]
        if d.open:
            below = [d.key] + below
        refuted[k] = (by_ref.get(k, []), [entry[e]["checked"] for e in by_ref.get(k, [])], below or "clean")
    rm.require("REFUTED", REFUTED, refuted, "M5's rows")
    summary = collections.Counter()
    for eid, rs in named.items():
        if rs:
            clean = all(refuted[k][2] == "clean" for k in rs)
            summary[(entry[eid]["checked"], "clean" if clean else "rests")] += 1
    rm.require("SUMMARY", SUMMARY, dict(sorted(summary.items())), "M5's first table and its interpretation")
    lean_unnamed = sorted((eid for eid, rs in named.items() if not rs and entry[eid]["checked"] == "Lean"),
                          key=lambda s: (s[0], int(s[1:])))
    rm.require("LEAN_UNNAMED", LEAN_UNNAMED, lean_unnamed, "M5's interpretation")

    n_clean = sum(1 for v in refuted.values() if v[2] == "clean")
    n_named = sum(1 for v in refuted.values() if v[0])
    n_lean = sum(v for (chk, _), v in summary.items() if chk == "Lean")
    c = lib.Canvas(
        ID, "The printed claims the Lean refutes",
        f"riemann-masullo at {rm.SHORT} keeps {len(refs)} refutations, `Printed.<name>_false`, each a proof that a "
        f"claim of the manuscript, as the Lean states it, is false. {n_clean} rest on nothing open. {n_named} are named by "
        f"an ERRATA.md entry, and {len(refs) - n_named} by none.", W, rm.sources(m), state=rm.state(m))
    x0, x1 = c.x0, c.x1
    y = c.y
    y += draw.nav(c, ID, y)
    y += c.para(x0, y, x1 - x0,
                "**How to read it.** A refutation is a theorem of the Lean whose statement is the negation of a printed "
                "claim, kept beside it as `Printed.<name>`. That a refutation rests on nothing open is read from the "
                "terms at the pin. What the Lean proves is that the claim as written in Lean is false; whether that "
                "is the printed claim, read as the author meant it, is ERRATA.md's reading. The entries were reported "
                "and checked by AI agents, and in ERRATA.md's words, “No entry has been reviewed by a specialist.” "
                "Its rule for the Checked value “Lean” is quoted here: such an entry's refutation “is a proof checked "
                "by Lean that rests on no statement still unproved”.", size=14.5, color="muted") + 26
    y += c.heading(x0, y, "1 · The entries that name a refutation, by Checked value")
    cols = [("Checked (ERRATA.md)", 300), ("Every refutation it names rests on nothing open", 420),
            ("One rests on something open", 340)]
    rows = []
    for chk in rm.CHECKED:
        a, b = summary.get((chk, "clean"), 0), summary.get((chk, "rests"), 0)
        if a or b:
            rows.append([chk, f"{a:,}" if a else "none", f"{b:,}" if b else "none"])
    left = c.table(x0, y, cols, rows, size=13.5)
    rx = x0 + 1060 + 40
    ih = c.card(rx, y, x1 - rx, "Interpretation (this poster's own)",
                [f"Each of the {n_lean} entries checked “Lean” that names a refutation names one with nothing open "
                 f"below it, as ERRATA.md's rule asks"
                 + (f", and {len(lean_unnamed)} entries checked “Lean” name none in code." if lean_unnamed else
                    ". Every entry checked “Lean” names one.")
                 + f" {summary.get(('reviewed', 'clean'), 0)} entries checked “reviewed” name a refutation with "
                   f"nothing open below it too: ERRATA.md compares each proof with the entry's reason before it marks "
                   f"an entry “Lean”, so these are not disagreements."],
                accent="amber", size=13.5, tsize=14, bullets=False)
    if summary.get(("Lean", "rests")):
        raise ValueError("an entry checked Lean names a refutation that rests on something open: re-read M5's "
                         "interpretation")
    y += max(left, ih) + 40
    y += c.heading(x0, y, f"2 · Every refutation: {len(refs)}, by directory and file")
    cols = [("Refutation", 700), ("File and line", 440), ("Its item", 230), ("Entries that name it, with Checked", 330),
            ("What is below it", 588)]
    X = I.load()
    entry_line = {e["id"]: e["line"] for e in m.entries}
    groups = collections.defaultdict(list)
    for k, d in refs.items():
        groups[d.chapter].append(d)
    for n, ch in enumerate(sorted(groups, key=rm.chapter_order)):
        ds = sorted(groups[ch], key=lambda d: (d.module, d.line))
        trs = [{"group": f"{draw.to_poster(CH.poster_id(ch), rm.chapter_label(ch))} · {ch} · {len(ds)}",
                "accent": "grey"}]
        for d in ds:
            ents, chks, below = refuted[d.key]
            card = draw.item_line(c, d)
            trs.append({"cells": [f"`{d.show}`", f"`{d.where}`", card[0][len("Item: "):] if card else "none",
                                  ", ".join(f"{draw.to_url(m.errata_url(entry_line[e]), e)} ({ck})"
                                            for e, ck in zip(ents, chks)) or "none",
                                  "nothing open" if below == "clean" else
                                  "rests on " + ", ".join(f"`{rm.display_name(b.removeprefix('private '))}`"
                                                          for b in below)],
                        "accent": "amber" if below != "clean" else None})
        mark = draw.anchored(c, f"refuted-{ch}")
        th = c.table(x0, y, cols, trs, size=12, hsize=12.5, pad=6, header=n == 0)
        draw.close(c, mark, x0, y, x1 - x0, th, pad=4)
        y += th
        y += 8
    y += 20
    c.para(x0, y, x1 - x0,
           "**What this does not say.** A refutation shows that a statement, as the Lean writes it, is false. It does "
           "not say that the manuscript's argument fails where it uses the claim, nor that the reason an entry gives "
           "is the one the proof uses. Entries are matched to refutations by the names their rows give in code.",
           size=13.5, color="muted")
    return c
