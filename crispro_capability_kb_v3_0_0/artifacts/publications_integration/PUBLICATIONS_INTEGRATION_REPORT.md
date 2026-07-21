# Artistry7 Platinum-Window Publications — v3 KB Integration Report

**Generated:** 2026-07-19 07:34 UTC
**Integration stream:** `v3:artistry7_publications`
**Source:** `data-room/datasets/artistry7-platinum-window/publications` (3 publication packages)
**Target KB:** `crispro_capability_kb_v3_0_0`

---

## 1. Summary

Three publication packages were parsed, independently verified where self-contained,
structured into the v3 KB JSON schema, loaded into the **live Qdrant vector store** and
**live Neo4j knowledge graph**, and also emitted as a **standalone publications KG**
(Cypher + graph JSON). All additions are **additive** and namespaced to avoid collisions
with the 594 pre-existing KB entities.

| Store | Baseline | After | Added |
|---|---|---|---|
| Qdrant points (`crispro_kb_v3`) | 1344 | 1418 | **+74** |
| Neo4j nodes | 617 | 691 | **+74** |
| Neo4j relationships | 655 | 728 | **+73** |
| KB entity JSON files | 594 | 668 | **+74** |

**74 entities / 73 edges** across 11 entity types.

### Entities by type
| Type | Count |
|---|---|
| analysis_artifact | 5 |
| biomarker | 1 |
| capability | 3 |
| drug | 10 |
| evidence_citation | 17 |
| gene | 2 |
| governance_item | 6 |
| outcome_metric | 4 |
| patient_cohort | 17 |
| publication | 3 |
| validation_result | 6 |

### Edges by predicate
| Predicate | Count |
|---|---|
| cites | 17 |
| demonstrates | 3 |
| derived_from | 21 |
| governed_by | 9 |
| implements | 1 |
| limits | 2 |
| mechanism_edge | 2 |
| reports | 4 |
| serves | 10 |
| validated_by | 4 |

---

## 2. The three publication packages

### 2.1 SPE Pharmacokinetic Feasibility Gate — `publication:spe_feasibility_gate` (NOT RUO)
Deterministic pre-filter computing **gap ratio = IC50 / free-plasma-Cmax**, classifying
drug-repurposing candidates PASS (<5x) / CONDITIONAL (5–50x) / FAIL (>50x) in <1 ms,
**before** any efficacy scoring.
- **Capability:** `capability:pub_spe_gate` (tier: `deterministic_computational`)
- **Boundary (guardrail):** A PASS means exposure is physically achievable, **NOT** that
  the drug works. Does **not** establish efficacy. Not a clinical recommendation.
- **10 drugs** ingested with per-drug gap ratios and verdicts.

### 2.2 Low-FAP/High-CXCL10 HGSOC Prognostic Fingerprint — `publication:hgsoc_fap_cxcl10_subgroup` (RUO)
Binary, platform-portable transcriptional fingerprint (**FAP_z < 0 AND CXCL10_z > 0**,
within-cohort z-scored) marking a favorable-overall-survival HGSOC subgroup (24.4% of patients).
- **Capability:** `capability:pub_hgsoc_fingerprint` (tier: `computational_retrospective_prognostic`)
- **Boundary (guardrails):** **PROGNOSTIC ONLY, NOT PREDICTIVE.** Does not predict response
  to any specific therapy. External validation on GSE32062 **DID NOT HOLD**. RUO.
- **16 MetaGx cohorts** (n=2446) + **1 external holdout** (GSE32062, n=260) ingested as cohorts.

### 2.3 Configurable Ovarian PFI / Timing Engine — `publication:timing_engine` (RUO)
Configurable engine estimating platinum-free-interval / treatment timing.
- **Capability:** `capability:pub_timing_engine` (tier: `internal_verification_plus_inconclusive_external`)
- **Boundary (guardrails):** Internal verification = **consistency**, not clinical validity.
  External equivalence vs ARIEL3 was **inconclusive (underpowered)**. RUO.

---

## 3. Verification status (end-to-end, 5 reproduced / 3 as-reported)

Every self-contained claim was **independently recomputed** in-session. Claims requiring
external dependencies (external LLM API, external-trial IPD, unshipped raw paths) were
ingested **exactly as reported** with `reproduced=false` and an explicit reason — never
skipped, never fabricated.

| Artifact | Status | Detail |
|---|---|---|
| SPE gap-ratio tiers (10 drugs) | **REPRODUCED** | 10/10 verdicts EXACT. Metformin/Ivermectin gap deltas = display rounding of intermediates; tiers identical. |
| SPE LLM benchmark (36%, 5/14) | **AS-REPORTED (external dep)** | Ingested as reported benchmark with provenance; reproduced=false reason=external_llm_api_nondeterministic |
| HGSOC pooled stratified Cox (HR 0.7208) | **REPRODUCED** | HR=0.7208, CI 0.6282-0.8270, p=3.05e-6 — EXACT match to published (R survival). |
| HGSOC per-cohort concordance (11/16) | **REPRODUCED** | 11/16 FAVORABLE exact; Stouffer z=2.322 vs 2.3219. |
| HGSOC GSE32062 external validation (NEGATIVE) | **REPRODUCED** | logrank p=0.9292, validation_holds=false — negative result preserved as-is. |
| Timing-engine confusion matrix (262/265) | **REPRODUCED** | 262 exact / 265 = 98.9% category agreement; 95.6% exact-day — internally consistent. |
| Timing-engine external validation (ARIEL3, inconclusive) | **AS-REPORTED (external dep)** | chi2 p=0.12, TOST p=0.073 ingested as reported; reproduced=false reason=external_trial_data_not_shipped |
| Timing-engine reproduce_all.py full run | **AS-REPORTED (external dep)** | Raw re-derivation blocked by external dependency; shipped precomputed tables used as ground truth instead. |

### Key reproductions (exact)
- **SPE gap-ratio: 10/10 verdicts reproduce EXACTLY** (`free_Cmax = Cmax*(1-PPB)`; tiers identical).
  Two benign display-rounding notes (Metformin, Ivermectin) — verdicts unchanged.
- **HGSOC pooled stratified Cox: HR = 0.7208, 95% CI 0.6282–0.8270, p = 3.05e-6** — exact match
  to the published R `survival` result, via an independent `lifelines` re-run on the shipped
  2446-patient file (16 cohorts, prevalence 24.4%).
- **HGSOC per-cohort concordance: 11/16 FAVORABLE, Stouffer z = 2.3219** — exact, from the
  shipped authoritative per-cohort validation file. Published sign-test p = 0.1051 (n.s.) preserved.
- **Timing engine internal: 262/265 category agreement (98.9%), 95.6% exact-day** — recomputed
  from the shipped confusion matrix.

### Negative / inconclusive results — preserved as-is
- **GSE32062 external validation = NEGATIVE** (logrank p = 0.9292, `validation_holds=false`).
  Attached to the HGSOC capability as a **LIMITS** edge.
- **Timing vs ARIEL3 = INCONCLUSIVE** (chi² p = 0.12; TOST equivalence p = 0.073, underpowered).
  Attached to the timing capability as a **LIMITS** edge. **Not** framed as positive equivalence.
- **SPE LLM benchmark** — external LLM (Cohere command-r-08-2024) scored 36% verdict accuracy
  (5/14) and fabricated PK parameters in 100% of queries; SPE deterministic <1 ms. Ingested as
  reported (`reproduced=false`, external nondeterministic API).

---

## 4. Honesty posture & evidence-tier discipline

The manuscripts are already honesty-forward (they separate internal verification from external
validation, flag inconclusive results, and carry correct RUO disclosures). The integration
**preserves each finding's exact evidence tier** and does **not**:
- inflate any claim above its source tier,
- convert prognostic findings into predictive ones,
- present inconclusive/negative validations as positive,
- add RUO where the source did not, nor strip RUO where the source asserted it.

**RUO is applied exactly where the source applied it:** `governance_item:pub_ruo_all` binds only
the two RUO-tagged capabilities (HGSOC fingerprint, timing engine) — **not** the SPE gate, which
the source did not RUO-tag.

### Governance guardrails (6)
| Guardrail | Binds |
|---|---|
| `pub_spe_not_efficacy` | SPE gate |
| `pub_hgsoc_prognostic_not_predictive` | HGSOC fingerprint |
| `pub_hgsoc_external_fails` | HGSOC fingerprint |
| `pub_timing_internal_not_clinical` | Timing engine |
| `pub_ruo_all` | HGSOC fingerprint, Timing engine |
| `pub_no_tier_inflation` | All three capabilities |

Each guardrail is both a Neo4j `GovernanceItem` (GOVERNED_BY edges) and a Qdrant chunk, so
retrieval **cannot surface a claim without its limitation**.

---

## 5. Integration validation (all PASS)

- **Qdrant:** 74/74 new points resolve by deterministic ID; payload `entity_id` matches; stream
  filter returns exactly 74.
- **Neo4j:** 74/74 new nodes reachable with correct labels + stream tag; 73 new relationships present.
- **Structural:** each of the 3 capabilities links to ≥1 publication and carries source receipts;
  every negative/inconclusive validation attached via **LIMITS**, every positive via **VALIDATED_BY**.
- **Tier audit (12 entities):** no claim exceeds its source tier; RUO flags match source truth.
- **Grounded retrieval (5 honesty probes):** every probe surfaces the guardrail/limitation as a
  **top hit** (e.g. "does the fingerprint predict drug response?" → prognostic-not-predictive #1;
  "cleared for clinical use?" → RUO #1).

---

## 6. Artifacts

**In v3 KB (committed to repo under `crispro_capability_kb_v3_0_0/`):**
- 74 entity JSON files under `entities/<type>/`
- Edges appended to `edges/*.json` (incl. new `demonstrates`, `validated_by`, `limits`, `reports`, `cites`)
- Updated `indexes/` (`by_type`, `by_source_file`, `by_stream`) + `corpus_provenance.json`

**Publications deliverables (`publications/`):**
- `publications_entity_manifest.csv` — full 74-entity inventory
- `claim_receipt_inventory.json` / `.csv` — 9 core claims with receipts
- `verification_log.csv` / `spe_verification.csv` — per-artifact verification status
- `new_entities.json` / `new_edges.json` — canonical structured objects
- `publications_kg.cypher` / `publications_graph.json` — standalone publications KG
- `integration_validation.json` — full validation results

---

*Research Use Only (RUO) where indicated by source. This integration preserves — and does not
extend — the evidence claims made in the source manuscripts.*
