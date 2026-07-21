# Zeta KG — SAS/CAS Clinical Warehouse Extraction Checkpoint

**Session 3 · 2026-07-21 · Zeta Custodian**

This is the user-visible sanity-check gate before rebuilding the vector store (Qdrant) and graph
database (Neo4j). It reports what was extracted from the Project Data Sphere (PDS) SAS/CAS
clinical-trials warehouse and minted into the Zeta knowledge graph.

---

## 1. What this fixes

The prior "completion" left **97 hollow trial shell-nodes** (`trial:sas:*`) whose
`attributes.adam_tables=[]` and whose evidence literally read `"table list unavailable"`. The
warehouse had been *inventoried* but its **contents were never extracted**. This session extracts
the actual patient-level clinical data and mints it into the graph.

Two extraction bugs found and fixed before this run:
- **1000-row truncation** — `conn.fetch(..., to=n)` silently capped every table at 1000 rows.
  Switched to `CASTable[...].to_frame()` which pulls all rows (e.g. one AE table went 1,000 → 8,114 rows).
- **Narrow column harmonization** — sponsor-specific column names (e.g. Pfizer's `PID_A`,
  `PREFTEXT`, `AEGRADE`) were missed, so some trials extracted 0 patients. Widened the
  harmonization dictionaries from an empirical column-vocabulary survey across all caslibs.

Extraction was **parallelized across 5 worker machines** (slice = caslib index mod 5), writing
resumable per-caslib checkpoints to shared storage.

---

## 2. Graph growth

| | Before | After | Δ |
|---|---:|---:|---:|
| Entities | 870 | **20,210** | +19,340 |
| Edges | 977 | **91,635** | +90,658 |

**New entity types**
| Type | Count |
|---|---:|
| TrialPatient | 16,865 |
| AdverseEventTerm (shared) | 2,439 |
| TreatmentArm | 36 |

**New edge types**
| Relation | Count |
|---|---:|
| enrolled_in (patient → trial) | 16,865 |
| assigned_arm (patient → arm) | 14,770 |
| arm_of (arm → trial) | 36 |
| experienced_ae (patient → AE term, grade+causality on edge) | 58,987 |

Existing v3 / EGA / MSK Zeta nodes were **not modified**. The 97 trial shells were **enriched in
place** (idempotent), not duplicated.

---

## 3. Coverage — honest ceiling

| | Count | Note |
|---|---:|---|
| Trial caslibs inventoried | 94 | 15 cancer types |
| **Extracted with patient-level data** | **23** | 11 cancer types |
| No loadable tables | 69 | **annotated, not fabricated** |

The 69 non-extracted caslibs return HDFS blob / image / data-file path errors on CAS load — they
genuinely contain no loadable SAS tables. They remain as trial shell-nodes with
`extraction_status = "no_loadable_tables"` and an explanatory note. **Their contents were not
invented.**

Extracted cancer types: Colorectal (6), Breast (5), Small-cell lung (4), + Prostate, Liver,
Head & neck, Melanoma, Lymphoma, Multiple, Pancreatic, Non-small-cell lung (1 each).

---

## 4. Clinical content extracted

| Metric | Value |
|---|---:|
| Patients | 17,264 (16,865 minted as nodes; 399 bare-ID skipped) |
| Adverse-event records | 118,859 |
| AE-term nodes (shared, deduped) | 2,439 |
| Trials with ≥2 treatment arms | 12 |
| Trials with survival status | 2 |

**Adverse-event severity pyramid** (canonical CTCAE grade, on `experienced_ae` edges):

| Grade | Events |
|---|---:|
| 1 (mild) | 32,901 |
| 2 (moderate) | 14,461 |
| 3 (severe) | 9,503 |
| 4 (life-threatening) | 1,813 |
| 5 (fatal) | 289 |

A plausible descending severity distribution — a strong signal the extraction is real.

---

## 5. Modeling decisions (tiered, defensible)

1. **AE-term nodes are tiered.** Of 14,635 distinct AE-term strings, ~10,300 are free-text
   investigator verbatim (misspelled one-offs like `"RIGTH LEG EDEMA"`, `"WHEEZE."`). Nodes were
   minted only for terms appearing in **≥2 trials OR with ≥10 total events** → **2,439 meaningful
   shared terms**. The 12,196 excluded singletons (16,968 events) are **still fully counted** in
   per-trial rollups; they simply don't each get a graph node.

2. **Patient nodes are worth minting.** 97.7% of patients carry ≥1 real attribute (arm 85.6%,
   age/race 51.9%, AEs 46.6%, survival status 19.1%) — the opposite of the hollow shells this
   session set out to fix. The 399 bare-ID patients (no attributes) were skipped.

3. **AE-term coding is mixed and preserved as-is.** Some trials (e.g. Alliance) code AEs as numeric
   MedDRA codes (`10029363`), others as text preferred terms (`Nausea`). Stored both; keyed nodes
   as `ae:meddra:<code>` or `ae:pt:<slug>`. **No cross-mapping between code and text was invented**
   (would require a licensed MedDRA dictionary).

4. **No cross-links were forced.** The extracted trials are solid tumors (breast, colorectal, lung,
   etc.); the existing genomics cohorts (BriTROC-1, MSK SPECTRUM) are ovarian HGSOC. There is **no
   indication overlap, no gene-target annotation, and arm codes are not drug names** — so **no
   `same_indication` / `measures_gene` / `targets_drug` edge is defensible**. None were added. The
   clinical subgraph attaches to the `vault:sas_pds` DataVault only.

---

## 6. Data-quality caveats (must read before use)

- **Demographics are NOT harmonized across trials.** Age is literal years in some trials (≈5,789
  patients, range 53–70 visible) but **age-group codes** in others (≈3,171 patients: values 2–5).
  Race and sex likewise mix text (`"White or Caucasian"`, `"Female"`) and codes (`1`, `M`). Values
  are stored **verbatim** — `age=4` in a coded trial means *age-group 4*, not 4 years old. Do not
  compare demographics across trials without per-trial code books.
- **Survival: status without duration.** The extraction found vital-status/event columns
  (`SURVSTAT`, `DTHFL`) but **no matching survival-time column**, so no `os_time` values were
  minted. Overall-survival *duration* analysis is not currently supported from this extraction.
- **Arm codes are mostly numeric and trial-local** (`1`,`8`,`37`) — not globally comparable
  treatment labels. Arm↔patient counts are distinct-patient counts (de-duplicated), not row counts.
- **AE events per patient capped at 50** for the per-patient edge list (to bound graph size);
  per-trial and per-term event totals are **uncapped and complete**.

---

## 7. Sample nodes (verification)

**Enriched trial (MedDRA-coded):** `trial:sas:Breast_Allianc_2002_194`
`extraction_status=extracted · n_patients=3171 · 8 arms · ae_events=3866 · coding=meddra_code · grades{3:2841,4:1025} · survival_event_col=SURVSTAT`

**Enriched trial (text-PT):** `trial:sas:Breast_Pfizer_2006_111`
`extraction_status=extracted · n_patients=240 · ae_events=2433 · coding=text_pt · grades{1:1566,2:632,3:191,4:27,5:17}`

**Shared AE-term:** `ae:pt:nausea` — Nausea · `total_events=5022 across 11 trials · grades{1:3605,2:1235,3:177,4:5}`

**Patient:** `patient:sas:Breast_Allianc_2002_194:3044_0` — arm 1, 2 AEs recorded → one
`experienced_ae → ae:meddra:10029363` edge with `max_grade=4`.

**Annotated (no data):** `trial:sas:Breast_Allianc_2006_216` —
`extraction_status=no_loadable_tables` with explanatory note; contents not fabricated.

---

## 8. Audit result

`AUDIT: PASS` — AE grades all in 1–5, 0 orphan edges, 0 invalid enrollment targets, 0 negative
survival, 0 "extracted" trials with zero patients, `assigned_arm` edges reconcile exactly with
arm-bearing patients (14,770).

---

## Next steps (pending your go-ahead)

4. Re-index Qdrant `zeta_vault` (dense + BM25) — ~19k new nodes to embed.
5. Reload Neo4j `:ZetaVault` — verify counts + cross-links.
6. Re-run all 5 analysis workers against the enriched graph.
7. Honesty audit + reports + additive PR.
