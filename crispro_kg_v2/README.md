# CrisPRO Knowledge Graph v2

**Version**: v2.0  
**Build Date**: 2026-07-03  
**Formula**: PATH A LOCKED 2026-04-28 — 
**Spot-Checks**: 15/15 PASS  

---

## What This Is

CrisPRO KG v2 is a deep, machine-readable knowledge graph of the CrisPRO mechanism-alignment platform. It was built by a 5-worker parallel audit of ~1.2 MB of source material (40+ files), producing 184.4 KB of structured, verified content.

**v1 used ~107 KB of source material. v2 audited ~1.2 MB — a 10× expansion.**

---

## File Structure

```
crispro_kg_v2/
├── crispro_knowledge_graph_v2.json          # Master JSON (184.4 KB) — all 10 sections
├── crispro_kg_system_prompt_snippet_v2.md   # Token-optimized agent anchor (5.5 KB)
├── README.md                                # This file
│
├── kg_modules/                              # Modular files (175.1 KB total)
│   ├── platform_identity_governance.json   # Platform identity + governance guardrails
│   ├── capability_registry.json            # 10 capabilities + 5 algorithm deep-dives
│   ├── mechanistic_deep.json               # Full mechanistic explanations (40.9 KB)
│   ├── matching_rules_v2.json              # 25 if-then matching rules
│   ├── quantitative_anchors.json           # All exact verified values
│   ├── module_catalog.json                 # 15 executable CrisPRO modules
│   ├── program_ceacam5.json                # CEACAM5 program (5 trials, full 8D vectors)
│   ├── program_atr_ddr.json                # ATR/DDR program (5 trials)
│   ├── program_io_core.json                # IO Core program (7 trials)
│   ├── program_io_appendix.json            # IO Appendix (15 trials)
│   ├── program_break_crc_001.json          # BreAK CRC-001 (STC-1010, fit=0.7375)
│   ├── program_historical_benchmarks.json  # TRIBE2 + 5 benchmarks
│   └── program_brief_sl.json               # BRIEF SL program (BRIEF-1 through BRIEF-4)
│
└── worker_outputs/                          # Raw per-worker JSON (161.2 KB total)
    ├── w1_ceacam5_atrddr.json              # W1: CEACAM5 + ATR/DDR (35.6 KB)
    ├── w2_io_core_appendix.json            # W2: IO Core + IO Appendix (32.2 KB)
    ├── w3_break_crc_biomarker.json         # W3: BreAK CRC-001 + Biomarker Biology (36.5 KB)
    ├── w4_brief_sl_ip.json                 # W4: BRIEF SL + IP/Patent (22.6 KB)
    └── w5_platform_governance.json         # W5: Platform + Governance + Rules (34.3 KB)
```

---

## Master JSON Structure (10 Sections)

| Section | Contents |
|---|---|
| `meta` | Version, build method, source files audited, formula status |
| `platform_identity` | What CrisPRO is/does/never does, 8D framework, two-layer architecture |
| `capability_registry` | 10 capabilities (CAP-01 through CAP-10) + 5 algorithm deep-dives |
| `program_index` | 7 programs with full 8D vectors, trial decodes, rationale |
| `mechanistic_deep` | Full mechanistic explanations: PATH A engine, STC-1010, IO failure archetypes, EscapeMap |
| `module_catalog` | 15 executable CrisPRO modules for BreAK CRC-001 |
| `matching_rules_v2` | 25 if-then rules (HIGH/MODERATE/CONDITIONAL confidence) |
| `offering_catalog` | 5 offerings with pitch templates and evidence anchors |
| `governance_guardrails` | Formula governance, quarantined items, active conflicts, mandatory disclosures |
| `quantitative_anchors` | 12 tables of exact verified values (CO.26, TRIBE2, BRIEF, EscapeMap, etc.) |

---

## Key Governance Rules

| Item | Status |
|---|---|
| PATH A formula | LOCKED 2026-04-28 |
| PATH B formula | PROHIBITED |
| LATIFY delta | QUARANTINED (cite responder 0.8936 vs non-responder 0.6295 only) |
| GBM ZEB1 | PERMANENTLY CLOSED |
| BRIEF-2 (PTEN-null→ITGAV) | COMPUTATIONAL HYPOTHESIS — DepMap NULL — mandatory disclosure |
| DL-07 (DDR 0.983) | QUARANTINED |
| SC-001 (CT26 BRAF V600E) | ACTIVE CONFLICT |

---

## Critical Quantitative Anchors

- **BreAK CRC-001 fit**: 0.7375 (MODERATE-HIGH)
- **CO.26 pTMB ≥28 OS HR**: 0.34 (90% CI 0.18–0.63, p=0.022)
- **CO.26 liver-met PFS HR**: 1.39 (HARMFUL) vs no-LM HR: 0.54 (Pint=0.02)
- **TRIBE2 mPFS**: 9.8 months (95% CI 9.0–10.5), ORR 50%, mOS 22.5 months
- **BRIEF-1**: delta=−0.7184, FDR=0.001203, CRISPR_VALIDATED
- **BRIEF-4**: delta=−0.7326, FDR=8×10⁻⁶, CRISPR_VALIDATED
- **OV ZEB1 continuous Cox**: HR=1.4803 (95% CI [1.1188, 1.9586], p=0.006042)
- **OV ZEB1 arm interaction**: p=0.246 → PROGNOSTIC NOT ARM-SPECIFIC

---

## Spot-Check Results (15/15 PASS)

PATH A formula · PATH B prohibited · BreAK fit 0.7375 · TRIBE2 mPFS 9.8 · CO.26 pTMB HR 0.34 · CO.26 liver-met HR 1.39 · BRIEF-1 delta −0.7184 · BRIEF-4 delta −0.7326 · OV ZEB1 HR 1.4803 · Arm interaction PROGNOSTIC_NOT_ARM_SPECIFIC · LATIFY QUARANTINED · GBM PERMANENTLY_CLOSED · BRIEF-2 COMPUTATIONAL_HYPOTHESIS · 25 rules · 7 programs
