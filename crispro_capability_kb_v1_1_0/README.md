# CrisPRO Capability Knowledge Base — v1.1.0

Generated: 2026-07-03T21:47:11+00:00

## Layout
- `crispro_capability_kb_v1_1_0.json` — master JSON with all 422 entities.
- `streams/` — 12 per-stream JSONs (v1: 6 depth-1 streams, v2: 5 deep-audit streams).
- `entities/<type>/<id>.json` — every entity split into its own file, grouped by type.
- `audit.json` — 6-check self-audit results.

## Audit summary
- Overall pass: **True**
- Entity total: **422**
- Files audited across all streams: **233**
- Check A (receipt existence):     pass=True  (missing=0)
- Check B (verbatim lookups):      pass=True  (failures=0)
- Check C (duplicate IDs):         pass=True  (dups=0)
- Check D (correction locks):      pass=True  ({'D1_mbd4_receipt_canonical_state': True, 'D2_mrtx1719_bug_open_status': True})
- Check E (cross-ref integrity):   pass=True  (dangling=0)
- Check F (what/how/why present):  pass=True  (missing=0)

## Streams
- **v1:architecture** — Architecture, Repos, Layers, Engines
- **v1:brenus_and_deliverables** — Brenus diligence module + Sanofi/AACR deliverables + open bugs
- **v1:evidence_and_receipts** — Evidence corpus + canonical receipts (MBD4/ATR + live API proofs)
- **v1:moat_and_governance** — Methodological moat + governance decisions + data provenance
- **v1:operations_and_access** — Operations, data access, and additional CrisPRO evidence artefacts
- **v1:synthetic_lethality** — Synthetic Lethality Engine — contracts, fuser, tiers, RS, invariants
- **v2:architecture_deep** — DEEP AUDIT — architecture: line-by-line module/file/commit/rule extraction
- **v2:brenus_and_operations_deep** — DEEP AUDIT — Brenus + ops: full parse of Sanofi directive, AACR schemas, session nav, faceted filtering, GTM bridge, access packs
- **v2:brenus_and_operations_deep_patch** — PATCH — deep_brenus grouper modules (aacr_tracker, sl_maps, access_packs)
- **v2:evidence_and_receipts_deep** — DEEP AUDIT — evidence + receipts: per-file content parsing (CSV headers/ranges, full JSON payloads, markdown heading trees)
- **v2:moat_and_governance_deep** — DEEP AUDIT — moat + governance: full-depth expansion of moat_comparison.json (every dimension, every audit correction, every caveat)
- **v2:synthetic_lethality_deep** — DEEP AUDIT — SL: chapter-by-chapter code+threshold+invariant extraction from CRISPRO_SL_PHD_ROADMAP.txt

## Type group counts (top 20)
- frontend_module_reference: 69
- endpoint_reference: 57
- code_module_reference: 20
- roadmap_chapter: 18
- csv_content: 15
- markdown_content: 14
- dbgap_access_pack: 12
- evidence_analysis: 11
- section_index: 10
- moat_dimension: 9
- code_block_index: 9
- moat_dimension_deep: 9
- cancer_context: 8
- candidate_axis: 8
- invariant: 8
- moat_document_field: 8
- evidence_modality: 7
- commit_reference: 7
- critical_paragraph_index: 6
- contract_model: 5

## Grounding rules
Every entity carries:
- `what_it_solves` / `how_it_solves` / `why_it_exists` — plain-English trio (F check).
- `source_receipts[]` — path + sha256 + mtime + bytes for each file the claim rests on.
- `verbatim_evidence[]` — where relevant, needle-lookup results with line/offset.
- `cross_refs[]` — links to other entity IDs (E check ensures they resolve).
- `attributes.raw` — for v2 entities, the raw JSON payload from the source file (no re-interpretation).

## v1 → v1.1 delta
- v1 total: 129 entities, 6 streams (shallow structural summary + verbatim lookups).
- v1.1 adds 5 deep-audit streams with per-CSV column ranges, per-JSON raw payload,
  per-chapter roadmap segments, per-dimension moat expansion, per-slide Sanofi directive,
  per-session AACR schema, per-code-block verbatim extraction with line offsets.
