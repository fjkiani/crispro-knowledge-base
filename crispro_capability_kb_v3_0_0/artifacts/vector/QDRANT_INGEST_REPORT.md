# Qdrant Vectorization Report — CrisPRO KB

**Collection:** `crispro_kb_v3` (Qdrant Cloud, eu-west-2)
**Points:** 1344 | **Vector dim:** 2048 | **Distance:** cosine
**Embedding model:** `nvidia/llama-nemotron-embed-vl-1b-v2` (via OpenRouter, free tier, no fallback)
**Source scope:** `crispro_capability_kb_v3_0_0` + `crispro_kg_v2`

## Corpus composition

| Dimension | Breakdown |
|---|---|
| By kind | entity=594, edge=583, program=81, responder_analysis=59, capability=15, governance=11, platform_identity=1 |
| By source KB | v3_0_0=1177, kg_v2=167 |
| By product layer | insilico_trials=520, platform=451, biology_intelligence=222, tumor_board=71, portfolio=45, interception=35 |

## Payload metadata (per point)

Every point carries filterable metadata enabling anchored, non-slop retrieval:
`chunk_id, entity_id, entity_type, kind, name, source_kb, source_file, line, json_pointer,
product_layer, governance_status, predicate/src/dst (edges), evidence_tier, cannot_do,
axis, cross_refs, scientific_priority, mint_planner, mint_timestamp, text`.

**Indexed fields** (fast filtering): `entity_type, kind, source_kb, product_layer, governance_status, predicate, entity_id`.

## Retrieval validation (spot queries)

All spot queries returned the semantically correct entity in top-1/top-3:

- *"PATH A mechanism fit formula"* → Mechanism Fit Engine capability + `fit=0.7375` outcome_metric + `claim:ct_01_formula -[governed_by]-> gov:path_a_locked` (0.45)
- *"BRIEF-2 PTEN ITGAV computational hypothesis DepMap"* → BRIEF program + `gov:brief_2_hypothesis` governance (0.61)
- *"Evo2 Enformer AlphaFold3 target lock metastasis"* → Target-Lock capability (interception) (0.42)
- *"prohibited claims individual patient outcomes"* → `prohibited_claims` guardrail (0.34)
- *"synthetic lethality MBD4 ATR"* → MBD4/ATR evidence-record edges (0.45)

**Metadata filtering verified:** `product_layer=interception` filter returns only interception-layer chunks (no leakage).

## Note on similarity scores

Absolute cosine scores are modest (0.3–0.6) because chunks are short, dense, and jargon-heavy
(entity records, formulas, governance strings). Retrieval quality is driven by **ranking**, which
is correct across all spot checks. RAGAS (next step) quantifies context precision/recall and the
metadata-utilization delta.
