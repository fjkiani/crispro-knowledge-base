# CHANGELOG — v3.0.0

Generated: 2026-07-13T23:26:44.854292Z
Merge branch: v3-audit-upgrade

## Summary
- v3 upgrade delivers deep evidence-graph refactor of `crispro_capability_kb`
- 5 planners (P1-P5), 5 executors (X1-X5), contracts sha256-locked
- Manager-approved user directives applied: implements cap at 200, no padding, honest ceilings

## Additions
- **594 v3 entities** across 26 types
- **583 v3 edges** across 9 predicates
- Semantic/mechanical ratio: 1.79 (target ≥ 1.5)

## Entity counts by type
```
arbiter_layer                  7
arbiter_model                  12
arbiter_template               5
biomarker                      12
brief_program_deep             4
calibration_proof              1
claim                          9
co_scientist_role              6
code_module                    46
demo_sample                    6
drug                           17
endpoint_ref                   165
evidence_citation              7
gene                           3
governance_item                10
outcome_metric                 16
pathway_axis                   8
patient_cohort                 6
regulatory_posture             1
sl_engine_component            37
sl_evidence_record             48
sl_tier                        4
trial                          150
trial_arm                      7
user_story                     5
variant                        2
```

## Edge counts by predicate
```
contradicts                    1
derived_from                   3
governed_by                    287
implements                     209
mechanism_edge                 17
owns                           21
resistance_edge                11
serves                         33
superseded_by                  1
```

## Audit (10/11 passed)
- **A** entity_source_receipts_present: PASS
- **B** entity_provenance_fields_present: PASS
- **C** edge_integrity_no_dangling: PASS
- **D** no_duplicate_entity_ids: PASS
- **E** edges_have_predicate_and_evidence: PASS
- **F** retroactive_trials_have_moa_vector: PASS
- **G** no_phd_roadmap_relifts: PASS
- **H** governance_entities_participate_in_edges: PASS
- **I** axis_trials_have_governed_by: PASS
- **J** brief_ownership_coverage_90pct: FAIL (n/a failures)
- **K** semantic_edges_dominate_ratio_gte_1.5: PASS

## Defects filed
- **D-P4-01** (medium): P4 minted 8 synthetic_lethal_edge entries with src=synthetic_lethal_edge:axis:XXX. These were derived from v1.1.0 candidate_axis entities whose source...
- **D-P2-01** (low): P2 generated 2 sl_evidence_record entities with identical slugified IDs due to filename stem collisions. `positioning/02_patent_filing_briefs.md` and ...
- **D-P4-02** (low): mechanism_edge entries citing BEACON-CRC (and other trial mechanistic evidence) do not link to evidence_citation:PMID_XXXXX entities. P1 currently min...
- **D-P2-02** (medium): Only BRIEF-2 (PTEN-null → ITGAV) has dedicated sl_evidence_record substrate (21 MBD4 files). BRIEF-1 (ZEB1→ITGAV), BRIEF-3 (ZEB1-high+PD-1), and BRIEF...
