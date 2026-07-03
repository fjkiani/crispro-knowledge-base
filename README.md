# CrisPRO Capability Knowledge Base

Audited, verbatim-grounded snapshot of the CrisPRO platform: repos, engines, layers,
contracts, evidence receipts, invariants, moat dimensions, governance decisions,
deliverables, and open bugs.

## Layout

- `crispro_capability_kb.json` — master, one-JSON view of everything
- `crispro_capability_kb/streams/<stream>.json` — per-capability audits (6 streams)
- `crispro_capability_kb/entities/<type>/<id>.json` — one file per entity, grouped by type (52 typed folders)
- `crispro_capability_kb/audit.json` — self-audit results (6 checks)
- `crispro_capability_kb/README.md` — layout + summary

## Streams

- **architecture** — repos, layers, engine boundaries, Ayesha bundle waterfall
- **synthetic_lethality** — contracts, 8-axis enum, 4-tier hierarchy, 7-modality fuser, RS framework, invariants, tier promotion
- **evidence_and_receipts** — canonical MBD4/ATR-WEE1 receipt, live-endpoint proofs, A1-A9 modality analyses
- **moat_and_governance** — 9 verbatim-sourced moat dimensions vs Bev2026, PATH A formula lock, 8D remediation, Mars Protocol
- **brenus_and_deliverables** — Brenus diligence module (BreAK CRC-001 / STC-1010), Sanofi pitch, AACR tracker, MRTX1719 bug
- **operations_and_access** — dbGaP / GBM / CRC / GEO / GLASS data-access packs, SL countermeasure map, gap-lineage reports

## Grounding rules

1. Every entity carries `source_receipts` with `sha256` + `mtime_iso` + `bytes`.
2. High-stakes claims (thresholds, formulas, invariants, tier statements) carry `verbatim_evidence`; `found=false` ⇒ stale.
3. Correction locks (D-check) enforce:
   - `receipt:mbd4_atr_evidence_matrix_v2` — `current_tier="Mechanistic candidate only"`, `overall_verdict.tier_change="NO CHANGE"`
   - `bug:mrtx1719_wrn_mismap` — `status="OPEN"`
4. No entity is reconstructed from memory or from any compaction summary — everything is derived at generation time from files on disk.

See `crispro_capability_kb/audit.json` for the current audit pass status.
