# CrisPRO Knowledge Graph — Build & Traversal Report

**Instance:** `neo4j+s://82886682.databases.neo4j.io` (AuraDB Free, instance 82886682)
**Graph size:** **617 nodes / 655 relationships**
**Integrity:** PASS — 0 duplicate ids, 0 null ids, 0 dangling relationships.
**Source KBs:** `crispro_capability_kb_v3_0_0` (594 receipt-anchored entities + 583 edges) + `crispro_kg_v2` (capability registry, governance guardrails, program dossiers).

This graph is the **relationship layer** of the CrisPRO knowledge base. It exists so that an
external agent can traverse CrisPRO's real capability set **by name** — asking "what backs
CAP_04?", "what governs Target-Lock?", "what is prohibited?" — and get back clean JSON with a
provenance receipt on every node and edge, instead of guessing Cypher or re-reading the repo.

---

## 1. What an agent gets

Two artifacts make the graph queryable without any Cypher knowledge:

- **`kb_graph.py`** — `KBGraph` Python client. 13 named endpoints, each returns plain
  JSON-serializable `list[dict]`/`dict` with provenance fields (`evidence`, `source_file`, `line`).
- **`neo4j_endpoints.cypher`** — the same 13 endpoints as parameterized Cypher (`$param`) for
  agents that speak Cypher directly.
- **`endpoint_examples.json`** — a live call + real output for every endpoint (copy-paste ready).
- **`load_graph.cypher`** — portable, APOC-free loader that recreates the entire graph on any
  Neo4j 5.x instance (so consumers are not locked to this Aura instance).

### Named endpoints (all tested against the live graph)

| # | Endpoint | Answers |
|---|----------|---------|
| EP1 | `capabilities_for_product(product)` | "What can CrisPRO do for this product surface?" |
| EP2 | `entity(entity_id)` | Full anchored record for **any** node (label-agnostic) |
| EP3 | `neighbors(entity_id, depth)` | Context 1–2 hops around an anchor |
| EP4 | `relationships_of(entity_id)` | Every edge in/out, with evidence |
| EP5 | `path_between(a, b)` | Shortest provenance path between two anchors |
| EP6 | `evidence_for(entity_id)` | Receipts/records backing an entity |
| EP7 | `governance_flags(entity_id)` | Governance / quarantine / claim bounds |
| EP8 | `prohibited_claims()` | The hard "must-not-claim" list (claim red-team) |
| EP9 | `mandatory_disclosures()` | RUO + disclosure obligations, quarantines, closures |
| EP10 | `what_implements(entity_id)` | Code/route provenance (file + line) for a capability/endpoint |
| EP11 | `entities_by_layer(product)` | All typed anchors in a product layer |
| EP12 | `trial_moa(nct)` | Decoded 8D mechanism + review provenance for a trial |
| EP13 | `capability_provenance(cap_id)` | One-call "what backs CAP_xx **and** what bounds it" |

---

## 2. Node inventory (617 nodes)

Every node carries `id` (unique) and `product_layer`. v3 entities additionally carry
`verbatim` (load-bearing evidence text), `source_file`, `cross_refs`. Capability/Guardrail
nodes carry structured registry content (`cap_code`, `what_it_does`, `cannot_do`,
`evidence_tier`, `category`, `full_json`).

| Label | Count |
|-------|-------|
| `Entity` | 617 |
| `EndpointRef` | 165 |
| `Trial` | 150 |
| `SlEvidenceRecord` | 48 |
| `CodeModule` | 46 |
| `SlEngineComponent` | 37 |
| `Drug` | 17 |
| `OutcomeMetric` | 16 |
| `ArbiterModel` | 12 |
| `Biomarker` | 12 |
| `Capability` | 12 |
| `Guardrail` | 11 |
| `GovernanceItem` | 10 |
| `Claim` | 9 |
| `PathwayAxis` | 8 |
| `ArbiterLayer` | 7 |
| `EvidenceCitation` | 7 |
| `TrialArm` | 7 |
| `CoScientistRole` | 6 |
| `DemoSample` | 6 |
| `PatientCohort` | 6 |
| `ArbiterTemplate` | 5 |
| `UserStory` | 5 |
| `BriefProgramDeep` | 4 |
| `SlTier` | 4 |
| `Gene` | 3 |
| `Variant` | 2 |
| `CalibrationProof` | 1 |
| `RegulatoryPosture` | 1 |

*(Nodes are multi-labeled: e.g. `capability:CAP_04` is both `:Entity` and `:Capability`.)*

### Product-layer distribution (Entity nodes)
- platform 211 · insilico_trials 167 · biology_intelligence 160 · tumor_board 42 · portfolio 32 · interception 5

---

## 3. Relationship inventory (655 relationships)

| Predicate | Count |
|-----------|-------|
| `GOVERNED_BY` | 302 |
| `IMPLEMENTS` | 209 |
| `SERVES` | 33 |
| `OWNS` | 21 |
| `MECHANISM_EDGE` | 17 |
| `MEASURED_IN` | 16 |
| `VALIDATED_ON` | 13 |
| `RESISTANCE_EDGE` | 11 |
| `CONSTRAINS` | 9 |
| `CORRESPONDS_TO` | 7 |
| `EVALUATED_IN` | 6 |
| `MENTIONS` | 6 |
| `DERIVED_FROM` | 3 |
| `SUPERSEDED_BY` | 1 |
| `CONTRADICTS` | 1 |

### Edges added during graph build (Step 4 capability/evidence linking)

The v3 edge set (`v3_edges.json`, 583 edges) wires the code/governance/mechanism layers but
left the **capability registry nodes largely disconnected** (9 of 12 capabilities were orphaned).
Because the whole point is agent traversal *from capabilities*, we added evidence-bearing edges
**only where a real target node exists and the capability's own registry field justifies it**:

- **`VALIDATED_ON` (13)** — capability → the program / brief / biomarker it was validated against.
  Evidence = the exact `validated_on` string from `capability_registry.json`.
- **`GOVERNED_BY` (+15, now 302 total)** — capability → the guardrail that bounds its claims
  (e.g. CAP_04 → `permanently_closed.GBM_ZEB1`; every capability → `prohibited_claims`).
- **`MEASURED_IN` (16)** — orphan `OutcomeMetric` → the program it measures (e.g.
  `outcome:co26_ptmb_ge28_os` → `program_asset_io_core`), so quantitative anchors are reachable.
- **`EVALUATED_IN` (6)** — biomarker → program.

Every added edge stores `wired_by` (`step4_capability_linking` / `step4_evidence_linking`),
`evidence`, and `source_file='crispro_kg_v2/capability_registry.json'` so it is auditable and
distinguishable from source-derived v3 edges. **No edge was created without a real target node
and a justifying registry field.**

---

## 4. Orphan nodes (117) — deliberate, documented

117 nodes have no edges. These are **not** a load bug; they fall into two honest buckets:

| Label | Count |
|-------|-------|
| `SlEngineComponent` | 37 |
| `SlEvidenceRecord` | 25 |
| `EvidenceCitation` | 7 |
| `Biomarker` | 6 |
| `CoScientistRole` | 6 |
| `DemoSample` | 6 |
| `PatientCohort` | 6 |
| `ArbiterTemplate` | 5 |
| `UserStory` | 5 |
| `Guardrail` | 4 |
| `Drug` | 3 |
| `Gene` | 3 |
| `SlTier` | 2 |
| `CalibrationProof` | 1 |
| `Capability` | 1 |

1. **Synthetic-lethality subgraph (SlEngineComponent 37 + SlEvidenceRecord 25 + SlTier 2 = 64):**
   The source file `edges/synthetic_lethal_edge.json` is **empty (`[]`)** — this is the documented
   upstream **defect D-P4-01 ("dropped 8 synthetic_lethal_edges")** recorded in
   `defect_register.csv`. The SL *engine* components therefore have no source edges to their
   targets. Per the project's honesty mandate, **synthetic lethality must not be presented as
   connected/validated where the source did not establish it**, so these are left orphaned rather
   than fabricated. (Note: 65 SL-*record* edges that DO exist in source — `governed_by`,
   `contradicts` to governance/tier nodes — are loaded correctly.)
2. **Leaf/reference nodes (EvidenceCitation, CoScientistRole, DemoSample, PatientCohort,
   ArbiterTemplate, UserStory, Drug, Gene, CalibrationProof, 6 Biomarker):** reference material
   the v3 edge set never wired to the main graph. Reachable by direct `entity(id)` lookup and full-
   text/vector search in Qdrant, just not by graph traversal.
3. **4 Guardrail "parent" containers** (`quarantined_items`, `active_conflicts`,
   `permanently_closed`, `mandatory_disclosures`): category umbrellas by design — their `.CHILD`
   variants (e.g. `quarantined_items.DL_07`) carry the real edges.

---

## 5. Governance / claim-bound wiring (feeds W5 claim ledger)

The graph makes the "what must not ship" logic directly traversable:

- **`guardrail:prohibited_claims` --CONSTRAINS--> 9 `Claim` nodes** (ct_01/02/03, dl_03/05/07,
  pc_02/05/06 formulas & LATIFY & DDR claims).
- **`guardrail:formula_governance` --CORRESPONDS_TO--> `gov:path_a_locked`, `gov:path_b_prohibited`.**
- **`guardrail:permanently_closed.GBM_ZEB1` --CORRESPONDS_TO--> `gov:gbm_zeb1_closed`.**
- **`guardrail:quarantined_items.*` --CORRESPONDS_TO--> LATIFY / DL-07 / PC-02 governance items.**
- **`guardrail:active_conflicts.SC_001` --CORRESPONDS_TO--> `gov:sc_001_active_conflict`.**
- Every capability **--GOVERNED_BY--> `guardrail:prohibited_claims`**, so an agent evaluating any
  capability is one hop from the hard claim bounds.

`EP8 prohibited_claims()` and `EP9 mandatory_disclosures()` expose this directly.

---

## 6. Reproduce / rehost

```bash
# Recreate the entire graph on any Neo4j 5.x instance (APOC not required):
cat load_graph.cypher | cypher-shell -u neo4j -p <password>
# then verify:  MATCH (n) RETURN count(n);  // 617    MATCH ()-->() RETURN count(*);  // 655
```

```python
from kb_graph import KBGraph      # reads NEO4J_* from env or /workspace/.env
kg = KBGraph()
kg.capabilities_for_product("interception")
kg.capability_provenance("capability:CAP_04")   # what backs & bounds Target-Lock
kg.prohibited_claims()                            # hard must-not-claim list
```

---

## 7. Acceptance checklist

- [x] Node/edge counts stable and reported (617 / 655).
- [x] No duplicate ids, no null ids, **no dangling relationships**.
- [x] All 13 endpoints tested against live Aura — return valid JSON **with provenance**.
- [x] Capabilities are reachable/traversable (was 9/12 orphaned → now 11/12 wired; the 1
      remaining, `CAP_07_escapemap_detail`, is a detail-annotation of CAP_07).
- [x] Portable `load_graph.cypher` emitted and validated (statement counts + quote-escaping).
- [x] Orphans characterized and justified against source (defect D-P4-01 + leaf nodes).
- [x] Added edges are auditable (`wired_by`, `evidence`, `source_file`) and never fabricated.
