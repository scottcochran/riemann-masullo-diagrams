"""DE: Appendix E, `AppE_TopologicalStacks`, declaration by declaration: the expansion of CE's cards. The layout
and the checks are declarations.py's; the literals below are what this poster expects the sources to say at
MASULLO_COMMIT, and the build fails on any difference."""
import declarations

ID = "DE"
SLUG = "appe-topologicalstacks"
CHAPTER = "AppE_TopologicalStacks"

DECLS = {'terminology:E.0.0.2': ['RiemannMasullo.quotientImageTopology',
                         'RiemannMasullo.isOpen_quotientImageTopology_iff',
                         'RiemannMasullo.isStrictMap_iff_quotientImageTopology'],
 'definition:E.1.1.1': ['RiemannMasullo.IsKClosed', 'RiemannMasullo.isCoarsest_compactlyGenerated'],
 'remark:E.1.1.2': ['RiemannMasullo.continuous_compactlyGenerated_to_original',
                    'RiemannMasullo.isClosed_compactlyGenerated_iff'],
 'lemma:E.1.1.3': ['RiemannMasullo.HasCompactHausdorffContinuityTest',
                   'RiemannMasullo.HasCompactHausdorffContinuityTestFamily',
                   'RiemannMasullo.HasCompactHausdorffOpennessTest',
                   'RiemannMasullo.HasCompactHausdorffQuotientPresentation',
                   'private RiemannMasullo.compactHausdorffTests_tfae_continuous_indicator_iff',
                   'RiemannMasullo.compactHausdorffTests_tfae',
                   'RiemannMasullo.exists_least_vonNeumannStages',
                   'RiemannMasullo.compactHausdorffCoproductMap',
                   'RiemannMasullo.compactHausdorffCoproductMap_preimage'],
 'lemma:E.1.1.4': ['RiemannMasullo.AllSupersetsClosed',
                   'RiemannMasullo.discreteTopology_of_two_allSupersetsClosed',
                   'RiemannMasullo.compactHausdorffContinuityTest_of_two_allSupersetsClosed',
                   'private RiemannMasullo.t2Space_closure_compl_connectedComponent_separation',
                   'private RiemannMasullo.t2Space_closure_compl_connectedComponent',
                   'private RiemannMasullo.isOpen_connectedComponent_iff_of_allSupersetsClosed',
                   'RiemannMasullo.isOpen_compl_singleton_of_unique_allSupersetsClosed',
                   'RiemannMasullo.discreteTopology_compl_singleton_of_unique_allSupersetsClosed',
                   'RiemannMasullo.isQuotientMap_connectedComponent_sum_closure_compl',
                   'RiemannMasullo.isCompact_range_into_closure_compl_connectedComponent',
                   'RiemannMasullo.t2Space_range_into_closure_compl_connectedComponent',
                   'RiemannMasullo.isClosed_range_into_closure_compl_connectedComponent',
                   'RiemannMasullo.isQuotientMap_rangeFactorization_into_closure_compl_connectedComponent',
                   'RiemannMasullo.exists_compactHausdorff_quotient_connectedComponent',
                   'RiemannMasullo.compactHausdorffContinuityTestFamily_of_unique_allSupersetsClosed'],
 'remark:E.1.1.5': ['RiemannMasullo.allSupersetsClosed_sierpinski_iff',
                    'RiemannMasullo.traitBouquetTopology',
                    'RiemannMasullo.isOpen_traitBouquetTopology_iff',
                    'RiemannMasullo.exists_homeomorph_connectedComponent_traitBouquet'],
 'remark:E.1.1.6': ['RiemannMasullo.exists_zfSet_meeting_classes'],
 'definition:E.1.1.7': ['RiemannMasullo.uCompactlyGeneratedSpace_iff_continuityTest',
                        'RiemannMasullo.compactlyGeneratedToTop_full_faithful'],
 'remark:E.1.1.8': ['RiemannMasullo.uCompactlyGeneratedSpace_iff_eq_compactlyGenerated'],
 'example:E.1.1.9': ['RiemannMasullo.cocountableTopology',
                     'RiemannMasullo.isClosed_cocountableTopology_iff',
                     'private RiemannMasullo.compactlyGenerated_cocountableTopology_eq_bot_countable',
                     'RiemannMasullo.compactlyGenerated_cocountableTopology_eq_bot',
                     'RiemannMasullo.not_uCompactlyGeneratedSpace_cocountableTopology'],
 'helpers:RiemannMasullo.AppE_TopologicalStacks.Sec1a_Printed': ['RiemannMasullo.isCoarsest_compactlyGenerated_candidateProbes',
                                                                 'private '
                                                                 'RiemannMasullo.isCoarsest_compactlyGenerated_candidateProbes_false_exists_not_closed',
                                                                 'RiemannMasullo.isCoarsest_compactlyGenerated_candidateProbes_false']}
DEVIATING = {'definition:E.1.1.1': ['RiemannMasullo.IsKClosed', 'RiemannMasullo.isCoarsest_compactlyGenerated'],
 'remark:E.1.1.2': ['RiemannMasullo.continuous_compactlyGenerated_to_original',
                    'RiemannMasullo.isClosed_compactlyGenerated_iff'],
 'lemma:E.1.1.3': ['RiemannMasullo.HasCompactHausdorffContinuityTest',
                   'RiemannMasullo.HasCompactHausdorffContinuityTestFamily',
                   'RiemannMasullo.HasCompactHausdorffOpennessTest',
                   'RiemannMasullo.HasCompactHausdorffQuotientPresentation',
                   'RiemannMasullo.compactHausdorffTests_tfae',
                   'RiemannMasullo.exists_least_vonNeumannStages'],
 'lemma:E.1.1.4': ['RiemannMasullo.compactHausdorffContinuityTest_of_two_allSupersetsClosed',
                   'RiemannMasullo.exists_compactHausdorff_quotient_connectedComponent',
                   'RiemannMasullo.compactHausdorffContinuityTestFamily_of_unique_allSupersetsClosed'],
 'remark:E.1.1.5': ['RiemannMasullo.traitBouquetTopology',
                    'RiemannMasullo.exists_homeomorph_connectedComponent_traitBouquet'],
 'remark:E.1.1.6': ['RiemannMasullo.exists_zfSet_meeting_classes'],
 'definition:E.1.1.7': ['RiemannMasullo.uCompactlyGeneratedSpace_iff_continuityTest',
                        'RiemannMasullo.compactlyGeneratedToTop_full_faithful'],
 'remark:E.1.1.8': ['RiemannMasullo.uCompactlyGeneratedSpace_iff_eq_compactlyGenerated'],
 'example:E.1.1.9': ['RiemannMasullo.compactlyGenerated_cocountableTopology_eq_bot',
                     'RiemannMasullo.not_uCompactlyGeneratedSpace_cocountableTopology']}


def build():
    return declarations.build(ID, CHAPTER, DECLS=DECLS, DEVIATING=DEVIATING)
