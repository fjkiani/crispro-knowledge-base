# Zeta Research Vault — Custodian Report

**Custodian:** Zeta Research Vault (LEAD DATA ARCHITECT mandate)
**Generated:** 2026-07-21 01:02 UTC
**Framework audited:** CrisPRO Resistance Framework (v2+v3, production-readiness report 2025-07-14)
**Scope:** Ingest → gap-map → extract → KG → hybrid index → 5 workers. NO summarization; full custodianship.

---

## 1. Executive Summary

I became custodian of three external research archives, characterized **514.8 GB** of real
biological/clinical data through **live authenticated API calls**, mapped every archive to the
existing KB's honest gaps, extracted contents into a **separate Knowledge Graph (797 entities,
798 edges)**, and hybrid-indexed them into a **new, isolated Qdrant collection `zeta_vault`**
(dense nemotron 2048-dim + BM25 sparse). The existing `crispro_kb_v3` (1418 pts) was **not touched**.

**Honest bottom line:** Zeta provides genuine train/validate/test paths for the framework's
hardcoded/simulated values — but **none closes in-sandbox today**. Full BriTROC WGS processing
is infeasible here (throughput + disk + 24h wall), Synapse is token-blocked, and only the 4.0 GB
SAS clinical warehouse is immediately actionable. **The framework remains NOT cleared for
patient-facing use**, and MFAP4's unreproducible metric is flagged — not falsely closed.

---

## 2. The Three Vaults (live-verified)

| Vault | Accession | Access | Content | Size | In-sandbox? |
|---|---|---|---|---|---|
| **EGA BriTROC-1** | EGAD00001011049 | ✅ AUTH OK (slow) | 679 WGS BAMs (HGSOC) | 510.8 GB | ❌ full DL infeasible |
| **Synapse MSK SPECTRUM** | syn25569736 | ⚠️ TOKEN INVALID (401) | 7 multi-modal datasets | metadata only | ❌ needs valid token |
| **SAS Project Data Sphere** | [SAS-PDS] | ✅ AUTH OK | 92 CDISC ADaM trials | 4.0 GB | ✅ actionable now |

- **EGA:** 679 unique BAMs = 679 unique MD5s across 2 specimen namespaces (JBLAB 292 + IM 387).
  1 BAM downloaded + **MD5-verified** (EGAF00008095569). **No clinical map in the dataset** —
  PFI/platinum labels live in the BriTROC-1 publication supplement (external).
- **Synapse:** Key WGS files identified (cna.tsv/syn39607857, cohort.maf/syn39607858,
  segments.seg/syn39607860) — the upstream source for the stripped MSK-Spectrum escape features.
  Downloads blocked pending a valid token.
- **SAS:** CDISC ADaM oncology warehouse — 14 cancer types, serial labs (adlb), AEs (adae),
  dosing (adex), serial markers (ador/adef). This is the "PRO-ACT telemetry / clinical logs."

---

## 3. Knowledge Graph (separate, custodian-built)

**797 entities · 798 edges** written to `kg/` (per-type JSON + master files):

| Entity type | Count | | Edge relation | Count |
|---|---|---|---|---|
| Biospecimen | 679 | | specimen_of | 679 |
| Trial (SAS) | 92 | | drawn_from | 105 |
| Dataset (Synapse) | 7 | | addresses_gap | 11 |
| KBGap | 7 | | part_of | 3 |
| DataResource | 5 | | | |
| DataVault | 3 | | | |
| FileArtifact | 3 | | | |
| PatientCohort | 1 | | | |

Every entity carries `source_receipts` + `verbatim_evidence` + access-state provenance.
The **`addresses_gap` bridge edges** connect each Zeta dataset to the existing-KB gap it can
train/validate/test — this is the core custodian intelligence.

---

## 4. Hybrid Index (`zeta_vault` — new, isolated)

Per the LEAD DATA ARCHITECT dual-tower mandate:

- **DENSE:** `nvidia/llama-nemotron-embed-vl-1b-v2:free` (2048-dim, Cosine)
- **SPARSE:** Qdrant/bm25 (IDF) — exact-match port for EGAF IDs, sample IDs, LOINC-style keys
- **Fusion:** RRF

**Per-batch confirmation (mandated output):**
- **Total vectors:** 797 (679 genomic + 92 clinical + 26 dataset/gap/vault)
- **Avg silhouette:** 0.658 (by entity type, cosine — strong structure)
- **PatientID → keyword ports:** **679/679 (100%)** exact-addressable; verified
  EGAF00008095569→JBLAB-4261, cna.tsv→syn39607857
- **Metadata fingerprint** on every chunk: primary_key / source_vault / biological_state /
  genomic_signature / temporal_marker
- **VAULT_INVENTORY.json:** 797 entries, 679 with real Source_File_MD5, STALE-flagging armed
- **Chunking:** genomic by functional units (specimens/files never split); clinical at caslib
  granularity (byte-level overlapping-window chunking deferred until SAS bytes downloaded)

`temporal_marker` is honestly **null** — no clinical map exists to derive day-from-diagnosis yet.

---

## 5. The 5 Workers (executed)

| Worker | Result |
|---|---|
| **W1 Prophet** | 25-gene universe mapped; 11 genes have a Zeta train/validate route; MBD4 heuristic flagged; MFAP4 = NOT addressable |
| **W2 Kill Chain** | 2/6 signals WIRED; **4 bugs flagged**: ctDNA-not-wired (P0-006), KELIM Signal-6 dead code (P0-009), CCNE1 CNA gap (SLOP-004), MAPK_BYPASS priority |
| **W3 Disk** | 514.8 GB characterized; only 4.0 GB (SAS) in-sandbox-actionable; 510.8 GB blocked |
| **W4 Train-ledger** | 9 hardcoded/simulated/stripped values ledgered; 1 READY_ON_TOKEN, 1 NOT-addressable, 0 closable in-sandbox now |
| **W5 Refinement** | Sequenced P0→P3 plan; **NOT cleared for patient-facing**; RUO contamination check PASS |

Each worker emits the mandated per-batch output (total vectors / silhouette / PatientID verification).

---

## 6. Gap → Zeta Mapping (honest roles)

| Gap | Zeta dataset | Role | Closes? |
|---|---|---|---|
| GAP-SIG7-BRITROC | EGA BriTROC-1 | TRAIN+VALIDATE | PARTIAL (HPC+labels) |
| GAP-MSK-ESCAPE-N39 | Synapse cna/maf/seg | VALIDATE+RESTORE | **READY_ON_TOKEN** |
| GAP-KELIM-SIM | SAS serial markers | TRAIN | PARTIAL |
| GAP-SAE-LEAKAGE | SAS labs/AE | TEST | PARTIAL |
| GAP-23GENE-PROXY | EGA+Synapse | VALIDATE | PARTIAL |
| GAP-CTDNA-NOTWIRED | Synapse plasma? | TEST | UNKNOWN (token) |
| GAP-MFAP4-UNREPRODUCIBLE | — | — | **NO (out of scope)** |

---

## 7. Fetch Feasibility (honest)

- **Full 511 GB in-sandbox: INFEASIBLE** — 1.1 MB/s (non-Europe) = 1.8–5.3 days vs 24h wall;
  512 GB disk has no headroom for BAI/variant intermediates.
- **htsget range-slice: UNAVAILABLE** — EGA archive returns **HTTP 500** for range requests on
  this dataset (tested both `chr17` and `17`; auth succeeds). Server-side limitation, not client.
- **Delivered:** `resumable_fetch.py` (checkpointed, MD5-verifying, HPC/Europe-ready) +
  `htsget_slice.py` (panel design) + `download_checkpoint.json` (all 679 tracked).

---

## 8. Integrity Audit — PASS

| Check | Status |
|---|---|
| RUO contamination | PASS (0 genuine unguarded clinical claims) |
| Tier preservation | PASS (MFAP4 not falsely closed; logit PENDING_REAL_DATA preserved) |
| No fabrication | PASS (temporal_marker honestly null; 1 real BAM; 500-error file deleted) |
| Collection separation | PASS (v3=1418 untouched; zeta_vault=797 separate) |

---

## 9. Recommended Next Actions

1. **P0** — Provide a valid Synapse token → unblocks MSK escape-pair restore (READY_ON_TOKEN) + ctDNA modality check.
2. **P0** — Download + parse SAS PDS (4.0 GB, feasible now) → real serial-marker kinetics + SAE-leakage stress-test.
3. **P1** — Code-only fixes (KELIM `kelim`→`k`, CCNE1 CNA path, v3 T2/T12) in the backend repo.
4. **P1** — Run BriTROC Sig7 extraction on an EGA-adjacent/HPC node (+ obtain clinical map for labels).

**Security:** All EGA/Synapse/SAS credentials were provided in plaintext — rotate after this session.


---

## SESSION 2 ADDENDUM (2026-07-21): MSK Genomics Extraction + EGA Metadata Enrichment

**Trigger:** Valid Synapse Personal Access Token provided (authenticated as `fjkiani`, scopes view/download/modify). Directive: extract *relationships/metadata*, not the 500+ GB of raw BAMs.

### MSK SPECTRUM genomics — EXTRACTED (real data, in-sandbox)
The previously token-blocked `GAP-MSK-ESCAPE-N39` is now **ADDRESSED with real genomics**:
- Downloaded + **MD5-verified** (all 3 MATCH Synapse): `cna.tsv` (756 genes × 40 samples), `cohort.maf` (87 somatic mutations, VEP+OncoKB), `segments.seg` (49,620 CN segments). Total 3.6 MB.
- Cohort is **N=40 HGSOC patients** (the "N39" label was approximate; 39 carry somatic mutations).
- Minted **+41 sample/cohort entities + 30 GenomicFeature nodes** (aggregated functional units, not 49k raw segments):
  - **CCNE1 high-level amplification in 6/40 samples (15%)** — closes W2 Kill Chain gap TF2-SLOP-004
  - **TP53 mutated in 39/40** (near-universal, HGSOC sanity check ✓); CDK12/RB1/BRCA1 oncogenic mutations
  - BRCA1/BRCA2/RB1/NF1 copy-number loss profiles
- **+135 relationship edges** (`harbors_mutation`, `harbors_cna`, `specimen_of`).

### EGA BriTROC-1 — ENRICHED via metadata API (no BAM bytes)
- Pulled dataset + 679 samples + 679 files from `metadata.ega-archive.org`. **100% MD5 overlap (679/679)** with existing manifest.
- Newly established facts: **shallow WGS (sWGS)** on Illumina HiSeq 2500/4000; **all female HGSOC**; **265 unique subjects** (longitudinal, up to 11 samples/subject).
- **Temporal axis recovered:** 385 `diagnosis` vs 294 `relapse` samples — minted as `CohortStratum` nodes; enables the Sig7 diagnosis→relapse resistance contrast **without downloading BAMs**.

### Worker deltas (all 5 re-run)
- **W1 Prophet:** 11 genes with *real* Zeta routes; BRAF/KRAS/NRAS (the hidden logit-model genes) upgraded by observed MSK mutation evidence. **MFAP4 still correctly NOT addressable.**
- **W2 Kill Chain:** signals with data **2/6 → 3/6** (CCNE1 CNA gap closed). **ctDNA verified non-wirable** — MSK SPECTRUM is tissue-only, no ctDNA/cfDNA modality exists. KELIM Signal6 dead code (RES-OV-P0-009) unchanged (framework code bug, not data).
- **W3 Disk:** MSK 3.6 MB downloaded+parsed; EGA 510.8 GB still blocked.
- **W4 Train-ledger:** real MSK genomic frequencies logged (replace assumptions).
- **W5 Refinement:** **`cleared_for_patient_facing` = NO** (unchanged — data enrichment does not change production-eligibility).

### Stores after session 2
- KG: **797 → 870 entities, 798 → 977 edges** (Neo4j `:ZetaVault` namespace, **0 cross-links** to v3).
- Qdrant `zeta_vault`: **797 → 870 points** (dense+BM25); avg silhouette **0.594** (honest decrease from 0.658 — new HGSOC-overlapping types reduce inter-cluster separation). `crispro_kb_v3` untouched at 1418.
- PatientID keyword ports: MSK 40/40 + EGA 53/53 spot-check = **100% addressable**.

### Honesty audit (session 2): **PASS** (all 4 checks)
RUO contamination 0 flags · MFAP4 tier preserved · no fabrication (EGA specimen temporal null; MSK MD5s verified) · collection separation intact.

### Still honest / unchanged limitations
- ctDNA gap remains architectural (framework wiring), not closable by Zeta.
- MFAP4 out of scope (GSE63885 external GEO).
- Full 510.8 GB EGA BAM download infeasible in-sandbox; htsget still HTTP 500 server-side.
- Framework not cleared for patient-facing use.


---

## SESSION 3 ADDENDUM (2026-07-21): SAS/CAS Project Data Sphere Clinical Extraction

**Trigger:** The SAS/CAS warehouse had been *inventoried* (92 hollow `trial:sas:*` shells,
`adam_tables=[]`, evidence "table list unavailable") but **never extracted**. Directive:
extract the warehouse contents into the Zeta KG and propagate to all 3 stores. Parallelized
across **5 workers** (worker-0..4) per user instruction.

### What was extracted (real data, in-sandbox, 0 GB raw bytes)
Ran a robust CAS extractor across **94 caslibs**, checkpointing per caslib (resumable).
Two critical extractor bugs were found and fixed before the authoritative run:
- **1000-row truncation:** `conn.fetch(table, to=n)` silently caps at 1000 rows. Fixed with
  `CASTable[varlist].to_frame()` (pulls all rows). This is why corrected counts (17,264 patients /
  118,859 AE records) far exceed the earlier buggy pass.
- **Narrow harmonization dict:** widened to evidence-based CDISC/sponsor-specific column maps
  from an empirical column survey (Pfizer trials use `PID_A`/`PREFTEXT`/`AEGRADE`/`SEXC`, etc.).

**Coverage (honest ceiling):**
| Stage | Count |
|---|---|
| Caslibs inventoried | 94 |
| Caslibs with loadable tables | 33 |
| Clinical trials with patient data | 23 |
| Trial nodes annotated `no_loadable_tables` (not fabricated) | 69 |

61 caslibs returned `no_table_files` (HDFS blob/image/data-file path errors on CAS load — genuinely
no loadable SAS tables). The 69 clinical-trial nodes with no loadable tables are **annotated with an
explanatory note — their contents are NOT fabricated**. (92 `Trial` nodes = 23 extracted + 69 no-load;
5 additional non-clinical SAS-resource caslibs are typed `DataResource`.)

**Extraction aggregate:** 17,264 patients · 118,859 adverse-event records · 2,439 tiered
AE-term nodes · 36 treatment arms. Cancer types with data: Colorectal (6), Breast (5),
Lung small-cell (4), + Prostate / Liver / Head&Neck / Melanoma / Lymphoma / Multiple myeloma /
Pancreatic / Lung non-small-cell (1 each). **No ovarian trial had loadable tables.**

### The one real gene→trial link (defensible, not forced)
Two colorectal trials (`Colorec_Amgen_2005_262`, `Colorec_Amgen_2006_263`) carry **patient-level
KRAS genotype** columns. Combined **wild-type 884 / mutant 667 = ~43% mutant**, matching the known
~40% CRC KRAS prevalence (external-validity check ✓). Minted `biomarker:kras:colorectal`
(GenomicFeature, `disease_context='colorectal'`, **NOT merged** with the ovarian MSK gene nodes)
+ 2 `stratified_by_biomarker` edges. **No `same_indication`/`measures_gene`/`targets_drug` edges
were forced** between these solid-tumor trials and the ovarian HGSOC genomics cohorts.

### Tiering decisions (no fabrication)
- **AE-term nodes tiered:** of 14,635 distinct AE strings (~10,300 are free-text investigator
  verbatim noise), minted nodes ONLY for terms with **≥2 trials OR ≥10 events → 2,439 nodes**
  (165 MedDRA-code + 2,274 text-PT). Excluded 12,196 singletons (16,968 events) are **still counted
  in trial/arm rollups**, not dropped.
- **Patient nodes:** 97.7% (16,865) carry ≥1 real attribute; 399 bare-ID patients skipped.
- **AE grade rollup** (canonical, on `experienced_ae` edges): G1 32,901 · G2 14,461 · G3 9,503 ·
  G4 1,813 · G5 289 (plausible severity pyramid; 289 fatal events).
- **AE coding kept mixed** (2 trials MedDRA-numeric, 11 text-PT, 10 none). Stored both; **no
  cross-mapping invented** (needs licensed MedDRA dictionary).

### Data-quality caveats (must-read before use)
- **Demographics NOT harmonized:** age is literal years in some trials but age-GROUP codes in
  others (e.g. `age=4` = age-group 4, not 4 years). Race/sex mix text + codes. Stored VERBATIM —
  **do not compare across trials.**
- **Survival = status WITHOUT duration:** event/status columns found (SURVSTAT, DTHFL) but **no
  matching time column → 0 patients have `os_time`.** OS-duration analysis is NOT supported.
- **Arm codes** are mostly numeric/trial-local; assigned_arm edges (14,770) reconcile exactly with
  arm-bearing patients (0 missing arm nodes).
- **CA-125:** absent from every extracted trial (ovarian marker, wrong tumor types). 17 trials do
  have serial-lab (LB/adlb) tables — the machinery is present, the analyte is not.

### Worker deltas (all 5 re-run)
- **W1 Prophet:** SAS gene linkage = **PARTIAL_REAL**. KRAS-CRC **fulfilled** (real patient-level,
  ~43% mut). BRAF/KRAS(ovarian)/NRAS/TP53 logit-outcome fit **NOT fulfilled** (SAS has no
  survival-time, solid tumors, no gene annotation except KRAS-CRC).
- **W2 Kill Chain:** `CA125_RISING` = **NOT_FULFILLED** (corrected from an earlier aspirational
  "WIRED via SAS"). KELIM = still dead code. Added a **new graded-AE safety layer** (118,859
  records) — orthogonal to the ovarian kill-chain. CCNE1/ctDNA unchanged.
- **W3 Disk:** **0 GB** raw bytes downloaded (honored the constraint); captured relationships only.
- **W4 Train-ledger:** real AE frequency top-10 + grade ledger + KRAS-CRC rates now available.
- **W5 Refinement:** `cleared_for_patient_facing` = **NO** (unchanged); RUO check PASS; patient
  nodes de-identified (masked subject IDs, no PHI).

### Stores after Session 3
- KG: **870 → 20,211 entities, 977 → 91,637 edges** (new: TrialPatient 16,865, AdverseEventTerm
  2,439, TreatmentArm 36, +1 KRAS GenomicFeature; edges enrolled_in 16,865, assigned_arm 14,770,
  arm_of 36, experienced_ae 58,987, stratified_by_biomarker 2). Neo4j `:ZetaVault` = 20,211 / 91,637,
  **0 cross-links** to non-Zeta.
- Qdrant `zeta_vault`: **870 → 20,211 points** (dense+BM25). `crispro_kb_v3` untouched at **1418**.
  Silhouette: **0.4244 stratified / 0.2776 natural-balance** — an *honest decrease* from 0.594
  (83% of points are now near-homogeneous patient nodes; expected, not a regression).

### Honesty audit (Session 3): **PASS** (all 4 checks)
RUO contamination PASS (kb_v3=1418 untouched) · evidence-tier preservation PASS (0 entities missing
evidence/receipts; genomics 31 GenomicFeature / 719 Biospecimen preserved) · no fabrication PASS
(69 no-load trials annotated with 0 fabricated content; AE singletons pooled; 0 forced cross-links;
only 2 KRAS-CRC edges) · collection separation PASS (0 Neo4j cross-links; 691 non-Zeta nodes preserved).

### Still honest / unchanged limitations
- ctDNA gap remains architectural (MSK tissue-only; SAS has no ctDNA) — not closable by Zeta.
- MFAP4 out of scope (GSE63885 external GEO).
- Full 510.8 GB EGA BAM download infeasible in-sandbox; htsget still HTTP 500 server-side.
- **Framework NOT cleared for patient-facing use.**
- SAS survival-duration analysis not supported (status without time); demographics non-harmonized.

**Security:** SAS/Synapse/EGA/GitHub credentials were provided in plaintext — **rotate after this session.**
