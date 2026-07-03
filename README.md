# CrisPRO Capability Knowledge Base

Audited, receipt-anchored, deep-parsed knowledge base of the CrisPRO platform, its synthetic-lethality engine, its evidence corpus (MBD4/ATR), its moat/governance record, and the Brenus/AACR/Sanofi deliverable pipeline.

Two immutable versions are shipped together — v1.0.0 (shallow structural) and v1.1.0 (deep audit). Each version is fully self-contained: `<version>.json` is the master artifact, and `<version>/` is the same content mirrored as a folder tree so consumers can walk it without loading the master JSON.

## Contents

| Version | Master JSON | Folder mirror | Entities | Streams | Audit |
|---|---|---|---|---|---|
| **v1.0.0** | `crispro_capability_kb.json` | `crispro_capability_kb/` | 129 | 6 | 6/6 pass |
| **v1.1.0** | `crispro_capability_kb_v1_1_0.json` | `crispro_capability_kb_v1_1_0/` | 422 | 12 | 6/6 pass |

## What's in v1.1.0 that v1.0.0 didn't have

v1.1.0 adds five deep-audit streams (one per capability). Each stream re-reads the source files at a lower level of granularity than v1:

| Stream | Deeper cut |
|---|---|
| `architecture_deep` | Line-by-line regex sweep of 10 CrisPRO architecture + hardening + handoff documents. Enumerates every Python module, TypeScript file, commit SHA, HTTP endpoint, heading, code block, and "critical / discovery / gap / hardcoded / bug / blocker" paragraph as its own entity. Two OpenClaw docs (MDC_architecture.md, MDC_training.md) are explicitly typed as `conflation_guard` so downstream ingestors do not conflate them with CrisPRO. |
| `synthetic_lethality_deep` | Chapter-segments the 89 KB `CRISPRO_SL_PHD_ROADMAP.txt` (18 chapters). One entity per chapter (with subheading tree), one per fenced code block (verbatim, with line offsets), threshold + weight + `clip(...)` regex indices, invariant/sprint/gap keyword index, and full parses of `gap_exploit_api_verification.json`, `agent_conduct_audit_2026-06-06.json`, `agent_full_audit_all_commits_v2.json`, `crispro_sl_audit_findings.json`. |
| `evidence_and_receipts_deep` | Per-CSV column ranges + 5 sample rows (numeric ⇒ n/min/max/mean; categorical ⇒ top-3 + unique count) for every MBD4/ATR CSV. Full-payload parse of the canonical `evidence_matrix_final_v2.json` and every JSON in `mbd4_atr_evidence/`. Full parses of the three live-endpoint responses (`crispro_live_api_proof.json`, `sl_endpoint_mbd4_live.json`, `bundle_endpoint_mbd4_live.json`). |
| `moat_and_governance_deep` | Expands `moat_comparison.json` from a single entity into one entity per top-level key. Each of the 9 `comparison_dimensions` becomes its own entity with the raw sub-payload plus a `verbatim_evidence` record carrying the Bev2026 verbatim quote and its source page. `document_purpose`, `provenance`, `definition_of_moat`, `comparative_summary_table`, `honest_moat_assessment`, `competitor_landscape_not_assessed_this_session`, `audit_corrections_2026_06_24`, and `moat_caveats` each get their own entity. Companion 9p21 audit JSONs and any `formula_governance/` artifacts are full-parsed. |
| `brenus_and_operations_deep` | Full parse of `sanofiPitchDeckDirective.json` (one entity per top-level directive field). Root-shape summary of `aacr2026_schema_a_master.json` (~4 MB) plus per-session/cluster entities for the first 40 items of any session-shaped list (overflow explicitly declared). Session navigation, GTM bridge, and faceted-filtering markdowns as first-class entities. Every AACR-related CSV parsed with column ranges. crispro_docs (`COMPUTATIONAL_CANCER_CURE_ROADMAP.md`, `FRONTEND_AGENT_PROMPT.md`) and any SL maps / gap-lineage / dbGaP / GBM / CRC / GEO / GLASS access packs auto-parsed by extension. A durable memory-anchored entity for the BreAK CRC-001 program (STC-1010, Alzeeb 2024 DOI). |

## Audit — v1.1.0

All six self-audit checks pass:

- **A. Receipt existence** — every `source_receipts[].path` either exists on disk or begins with an explicit external prefix (`fjkiani/`, `governance/`, `Bev2026`, `user_memory`, `api/services/`, `pharmacologic_analyzer.py`, `core/`, `kb/`, `external:`, `https://`). Missing: **0**.
- **B. Verbatim lookups** — every `verbatim_evidence[]` entry that carries a `found` field must be `True`. Failures: **0**.
- **C. Duplicate IDs** — no entity ID appears in more than one stream. Duplicates: **0**.
- **D. Correction lock traps** — `receipt:mbd4_atr_evidence_matrix_v2` MUST carry `canonical_state.current_tier == "Mechanistic candidate only"` AND `canonical_state.overall_verdict.tier_change == "NO CHANGE"`. `bug:mrtx1719_wrn_mismap` MUST exist with `status == "OPEN"`. Both traps hold.
- **E. Cross-ref integrity** — every `cross_refs[]` entry must resolve to a real entity ID or be typed `external:*`. Dangling: **0**.
- **F. what/how/why present** — every entity carries non-empty `what_it_solves`, `how_it_solves`, `why_it_exists`. Missing: **0**.

The full audit report lives at `crispro_capability_kb_v1_1_0/audit.json`.

## Standard entity schema

Every entity — regardless of version or stream — carries:

```
{
  "id":              "type:name",             # unique across the KB
  "type":            "entity_type",           # e.g. moat_dimension_deep, roadmap_code_block
  "name":            "human-readable",
  "what_it_solves":  "problem scope",         # (F check)
  "how_it_solves":   "method / code path",    # (F check)
  "why_it_exists":   "gap addressed",         # (F check)
  "attributes":      { ... type-specific ... },
  "verbatim_evidence": [
    {"quote": "...", "file": "...", "line": N, "found": true|false}
  ],
  "source_receipts": [
    {"path": "/abs/path", "sha256": "...", "mtime_iso": "...", "bytes": N, "span_extracted": "..."}
  ],
  "cross_refs":      ["other_entity_id", ...],   # (E check)
  "gaps_still_open": [...]
}
```

## Grounding rules

- No summarisation of load-bearing content. Numbers, thresholds, code, formulas, and Bev2026 verbatim quotes are preserved verbatim in `attributes` or `attributes.raw`.
- No fabricated cross-references. If a link cannot resolve within the KB, either the target entity is declared, the ref is typed `external:*`, or the audit fails.
- No silent tier changes. The MBD4 canonical state is enforced by check D at every merge — any drift fails the build.
- No hidden documents. Every file in the audit is enumerated in the stream's `files_audited[]` with sha256 + mtime + bytes, so the KB is reproducible against the exact bytes it was built from.

## Regeneration

The build scripts live in the Brenus/CrisPRO tooling workspace (not in this repository). See:
- v1.0.0 build: `/mnt/shared-workspace/shared/crispro_kb/scripts/*.py`
- v1.1.0 build: `/mnt/shared-workspace/shared/crispro_kb/scripts_v2/*.py`

The merger (`merge_v2.py`) re-runs the same six audit checks on every rebuild and refuses to write the master JSON claim of `overall_pass=True` unless all six pass.
