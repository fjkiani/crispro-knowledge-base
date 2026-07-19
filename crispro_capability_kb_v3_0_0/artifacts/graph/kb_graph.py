"""
CrisPRO Knowledge Graph — clean traversal client for external agents.

Every method returns plain JSON-serializable Python (list[dict] / dict) with
provenance fields, so an agent can query relationships and context by *name*
instead of writing Cypher or guessing at the schema.

Usage:
    from kb_graph import KBGraph
    kg = KBGraph()  # reads NEO4J_* from env or /workspace/.env
    kg.capabilities_for_product("interception")
    kg.relationships_of("capability:CAP_04")
    kg.prohibited_claims()
    kg.path_between("capability:CAP_02", "gov:path_a_locked")

Product layers: interception | insilico_trials | tumor_board |
                biology_intelligence | portfolio | platform
"""
import os, json
from neo4j import GraphDatabase

try:
    from dotenv import load_dotenv
    load_dotenv(os.environ.get("KB_ENV", "/workspace/.env"))
except Exception:
    pass


class KBGraph:
    def __init__(self, uri=None, user=None, password=None):
        self.driver = GraphDatabase.driver(
            uri or os.environ["NEO4J_URI"],
            auth=(user or os.environ["NEO4J_USER"], password or os.environ["NEO4J_PASSWORD"]),
        )

    def close(self):
        self.driver.close()

    def _run(self, cypher, **params):
        with self.driver.session() as s:
            return [r.data() for r in s.run(cypher, **params)]

    # --- EP1 ---
    def capabilities_for_product(self, product):
        return self._run(
            "MATCH (c:Capability {product_layer:$p}) "
            "RETURN c.id AS id, c.cap_code AS capability, c.name AS name, "
            "c.what_it_does AS what_it_does, c.evidence_tier AS evidence_tier, "
            "c.cannot_do AS cannot_do, c.source AS source ORDER BY c.cap_code",
            p=product)

    # --- EP2 ---
    def entity(self, entity_id):
        """Full anchored record for ANY node (Entity, Capability, Guardrail, ...).
        Label-agnostic: matches by id and returns the richest available fields,
        including capability (cap_code/what_it_does/cannot_do/evidence_tier) and
        guardrail (category/full_json) content when present."""
        r = self._run(
            "MATCH (n {id:$id}) RETURN n.id AS id, labels(n) AS labels, n.type AS type, "
            "n.name AS name, n.product_layer AS product_layer, "
            "n.governance_status AS governance_status, n.source_file AS source_file, "
            "n.line AS line, n.verbatim AS verbatim, n.attributes_json AS attributes, "
            "n.cap_code AS cap_code, n.what_it_does AS what_it_does, "
            "n.cannot_do AS cannot_do, n.evidence_tier AS evidence_tier, "
            "n.source AS source, n.category AS category, n.full_json AS full_json", id=entity_id)
        if not r:
            return None
        out = {k: v for k, v in r[0].items() if v is not None}
        if "full_json" in out:
            try:
                out["full_json"] = json.loads(out["full_json"])
            except Exception:
                pass
        return out

    # --- EP3 ---
    def neighbors(self, entity_id, depth=1, limit=50):
        depth = 2 if depth >= 2 else 1
        return self._run(
            f"MATCH (n:Entity {{id:$id}})-[*1..{depth}]-(m:Entity) "
            "RETURN DISTINCT m.id AS neighbor_id, m.type AS type, m.name AS name, "
            "m.product_layer AS product_layer LIMIT $lim", id=entity_id, lim=limit)

    # --- EP4 ---
    def relationships_of(self, entity_id):
        return self._run(
            "MATCH (n:Entity {id:$id})-[r]-(m:Entity) "
            "RETURN type(r) AS predicate, CASE WHEN startNode(r)=n THEN 'out' ELSE 'in' END AS direction, "
            "m.id AS other_id, m.name AS other_name, r.evidence AS evidence, "
            "r.source_file AS source_file, r.line AS line", id=entity_id)

    # --- EP5 ---
    def path_between(self, a, b, max_hops=6):
        return self._run(
            f"MATCH (a:Entity {{id:$a}}),(b:Entity {{id:$b}}), p=shortestPath((a)-[*..{max_hops}]-(b)) "
            "RETURN [n IN nodes(p) | n.id] AS node_path, [r IN relationships(p) | type(r)] AS rel_path, "
            "length(p) AS hops", a=a, b=b)

    # --- EP6 ---
    def evidence_for(self, entity_id):
        return self._run(
            "MATCH (n:Entity {id:$id})-[r:OWNS|GOVERNED_BY|MECHANISM_EDGE|VALIDATED_ON|DERIVED_FROM]-(e:Entity) "
            "RETURN e.id AS evidence_id, e.type AS type, e.name AS name, r.evidence AS edge_evidence, "
            "e.verbatim AS verbatim, e.source_file AS source_file", id=entity_id)

    # --- EP7 ---
    def governance_flags(self, entity_id):
        r = self._run(
            "MATCH (n:Entity {id:$id}) "
            "OPTIONAL MATCH (n)-[:GOVERNED_BY]->(g:Entity) "
            "OPTIONAL MATCH (gr:Guardrail)-[:CORRESPONDS_TO|CONSTRAINS]->(n) "
            "RETURN n.id AS id, n.governance_status AS status, "
            "collect(DISTINCT g.name) AS governed_by, collect(DISTINCT gr.name) AS guardrails", id=entity_id)
        return r[0] if r else None

    # --- EP8 ---
    def prohibited_claims(self):
        r = self._run(
            "MATCH (g:Guardrail {id:'guardrail:prohibited_claims'}) "
            "OPTIONAL MATCH (g)-[:CONSTRAINS]->(c:Entity) "
            "RETURN g.full_json AS prohibited_claims_json, "
            "collect({claim_id:c.id, name:c.name, status:c.governance_status}) AS constrained_claims")
        if not r:
            return None
        out = r[0]
        try:
            out["prohibited_claims"] = json.loads(out.pop("prohibited_claims_json"))
        except Exception:
            pass
        return out

    # --- EP9 ---
    def mandatory_disclosures(self):
        return self._run(
            "MATCH (g:Guardrail) WHERE g.category IN "
            "['mandatory_disclosures','quarantined_items','permanently_closed','active_conflicts'] "
            "RETURN g.id AS id, g.name AS name, g.governance_status AS status, g.full_json AS detail")

    # --- EP10 ---
    def what_implements(self, entity_id):
        return self._run(
            "MATCH (a:Entity {id:$id})-[r:IMPLEMENTS|SERVES]-(b:Entity) "
            "RETURN a.id AS from, type(r) AS predicate, b.id AS to, "
            "r.source_file AS source_file, r.line AS line, r.evidence AS evidence", id=entity_id)

    # --- EP11 ---
    def entities_by_layer(self, product):
        return self._run(
            "MATCH (n:Entity {product_layer:$p}) "
            "RETURN n.type AS type, count(*) AS n, collect(n.id)[0..25] AS sample_ids ORDER BY n DESC",
            p=product)

    # --- EP13 (added Step 4) ---
    def capability_provenance(self, cap_id):
        """Everything anchoring a capability: its validated_on programs, governing
        guardrails, and mentioned briefs — with the exact evidence string on each
        edge. This is the agent's one-call 'what backs CAP_xx and what bounds it?'."""
        return self._run(
            "MATCH (c:Capability {id:$id})-[r]-(m) "
            "RETURN type(r) AS predicate, "
            "CASE WHEN startNode(r)=c THEN 'out' ELSE 'in' END AS direction, "
            "m.id AS other_id, labels(m) AS other_labels, m.name AS other_name, "
            "r.evidence AS evidence, r.source_file AS source_file ORDER BY predicate", id=cap_id)

    # --- EP12 ---
    def trial_moa(self, nct):
        eid = nct if nct.startswith("trial:") else f"trial:{nct}"
        return self._run(
            "MATCH (t:Trial {id:$id}) "
            "OPTIONAL MATCH (t)-[r:GOVERNED_BY|DERIVED_FROM]->(g:Entity) "
            "RETURN t.id AS trial, t.verbatim AS moa_evidence, t.cross_refs AS axes, "
            "collect(DISTINCT g.name) AS governance", id=eid)


if __name__ == "__main__":
    kg = KBGraph()
    print("interception capabilities:", json.dumps(kg.capabilities_for_product("interception"), indent=2)[:800])
    print("\nprohibited claims:", json.dumps(kg.prohibited_claims(), indent=2)[:600])
    kg.close()
