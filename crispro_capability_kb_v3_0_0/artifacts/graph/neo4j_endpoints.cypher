// =============================================================================
// CrisPRO Knowledge Graph — Clean Traversal Endpoints for External Agents
// Instance: neo4j+s://82886682.databases.neo4j.io   Graph: 617 nodes / 605 rels
// Every query is parameterized ($param) and returns provenance-carrying JSON.
// These are the "anchored" entry points: an agent NEVER has to guess Cypher —
// it calls a named endpoint and gets clean context/relationships back.
// =============================================================================

// -----------------------------------------------------------------------------
// EP1. capabilities_for_product(product)
// "What can CrisPRO actually do for <product surface>?"  product ∈
// {interception, insilico_trials, tumor_board, biology_intelligence, portfolio}
// -----------------------------------------------------------------------------
MATCH (c:Capability {product_layer:$product})
RETURN c.id AS id, c.cap_code AS capability, c.name AS name,
       c.what_it_does AS what_it_does, c.evidence_tier AS evidence_tier,
       c.cannot_do AS cannot_do, c.source AS source
ORDER BY c.cap_code;

// -----------------------------------------------------------------------------
// EP2. entity(entity_id)  — full anchored record for ANY node (label-agnostic).
// Works for :Entity, :Capability, :Guardrail, :Trial, ... Returns the richest
// available fields incl. capability (cap_code/what_it_does/cannot_do) + guardrail
// (category/full_json) content when present.
// -----------------------------------------------------------------------------
MATCH (n {id:$entity_id})
RETURN n.id AS id, labels(n) AS labels, n.type AS type, n.name AS name,
       n.product_layer AS product_layer, n.governance_status AS governance_status,
       n.source_file AS source_file, n.line AS line, n.verbatim AS verbatim,
       n.attributes_json AS attributes, n.cap_code AS cap_code,
       n.what_it_does AS what_it_does, n.cannot_do AS cannot_do,
       n.evidence_tier AS evidence_tier, n.source AS source,
       n.category AS category, n.full_json AS full_json;

// -----------------------------------------------------------------------------
// EP3. neighbors(entity_id, depth)  — context around an anchor (1–2 hops)
// -----------------------------------------------------------------------------
MATCH (n:Entity {id:$entity_id})-[r*1..2]-(m:Entity)
RETURN DISTINCT m.id AS neighbor_id, m.type AS type, m.name AS name,
       m.product_layer AS product_layer
LIMIT 50;

// -----------------------------------------------------------------------------
// EP4. relationships_of(entity_id)  — every edge in/out with evidence
// -----------------------------------------------------------------------------
MATCH (n:Entity {id:$entity_id})-[r]-(m:Entity)
RETURN type(r) AS predicate,
       CASE WHEN startNode(r)=n THEN 'out' ELSE 'in' END AS direction,
       m.id AS other_id, m.name AS other_name,
       r.evidence AS evidence, r.source_file AS source_file, r.line AS line;

// -----------------------------------------------------------------------------
// EP5. path_between(a, b)  — shortest provenance path between two anchors
// -----------------------------------------------------------------------------
MATCH (a:Entity {id:$a}), (b:Entity {id:$b}),
      p = shortestPath((a)-[*..6]-(b))
RETURN [n IN nodes(p) | n.id] AS node_path,
       [r IN relationships(p) | type(r)] AS rel_path,
       length(p) AS hops;

// -----------------------------------------------------------------------------
// EP6. evidence_for(entity_id)  — what receipts/records back this entity
// (follows OWNS / GOVERNED_BY / MECHANISM_EDGE to evidence-bearing nodes)
// -----------------------------------------------------------------------------
MATCH (n:Entity {id:$entity_id})-[r:OWNS|GOVERNED_BY|MECHANISM_EDGE|VALIDATED_ON|DERIVED_FROM]-(e:Entity)
RETURN e.id AS evidence_id, e.type AS type, e.name AS name,
       r.evidence AS edge_evidence, e.verbatim AS verbatim, e.source_file AS source_file;

// -----------------------------------------------------------------------------
// EP7. governance_flags(entity_id)  — governance/quarantine/claim bounds on an entity
// -----------------------------------------------------------------------------
MATCH (n:Entity {id:$entity_id})
OPTIONAL MATCH (n)-[:GOVERNED_BY]->(g:Entity)
OPTIONAL MATCH (gr:Guardrail)-[:CORRESPONDS_TO|CONSTRAINS]->(n)
RETURN n.id AS id, n.governance_status AS status,
       collect(DISTINCT g.name) AS governed_by,
       collect(DISTINCT gr.name) AS guardrails;

// -----------------------------------------------------------------------------
// EP8. prohibited_claims()  — the hard "must not claim" list (for claim red-team)
// -----------------------------------------------------------------------------
MATCH (g:Guardrail {id:'guardrail:prohibited_claims'})
OPTIONAL MATCH (g)-[:CONSTRAINS]->(c:Entity)
RETURN g.full_json AS prohibited_claims_json,
       collect({claim_id:c.id, name:c.name, status:c.governance_status}) AS constrained_claims;

// -----------------------------------------------------------------------------
// EP9. mandatory_disclosures()  — RUO + disclosure obligations
// -----------------------------------------------------------------------------
MATCH (g:Guardrail) WHERE g.category IN ['mandatory_disclosures','quarantined_items','permanently_closed','active_conflicts']
RETURN g.id AS id, g.name AS name, g.governance_status AS status, g.full_json AS detail
ORDER BY g.category;

// -----------------------------------------------------------------------------
// EP10. what_implements(endpoint_or_module)  — code/route provenance for a capability
// -----------------------------------------------------------------------------
MATCH (a:Entity {id:$entity_id})-[r:IMPLEMENTS|SERVES]-(b:Entity)
RETURN a.id AS from, type(r) AS predicate, b.id AS to,
       r.source_file AS source_file, r.line AS line, r.evidence AS evidence;

// -----------------------------------------------------------------------------
// EP11. entities_by_layer(product)  — all anchors in a product layer (typed)
// -----------------------------------------------------------------------------
MATCH (n:Entity {product_layer:$product})
RETURN n.type AS type, count(*) AS n, collect(n.id)[0..25] AS sample_ids
ORDER BY n DESC;

// -----------------------------------------------------------------------------
// EP12. trial_moa(nct)  — decoded 8D mechanism vector + review provenance for a trial
// -----------------------------------------------------------------------------
MATCH (t:Trial {id:$entity_id})
OPTIONAL MATCH (t)-[r:GOVERNED_BY|DERIVED_FROM]->(g:Entity)
RETURN t.id AS trial, t.verbatim AS moa_evidence, t.cross_refs AS axes,
       collect(DISTINCT g.name) AS governance;

// -----------------------------------------------------------------------------
// EP13. capability_provenance(cap_id)  — one-call "what backs CAP_xx AND what
// bounds it": validated_on programs, governing guardrails, mentioned briefs,
// each with the exact evidence string on the edge.
// -----------------------------------------------------------------------------
MATCH (c:Capability {id:$cap_id})-[r]-(m)
RETURN type(r) AS predicate,
       CASE WHEN startNode(r)=c THEN 'out' ELSE 'in' END AS direction,
       m.id AS other_id, labels(m) AS other_labels, m.name AS other_name,
       r.evidence AS evidence, r.source_file AS source_file
ORDER BY predicate;
