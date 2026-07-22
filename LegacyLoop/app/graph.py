"""Entity extraction and a mini knowledge graph over the chunk corpus.

Regex catches equipment tags and regulatory codes deterministically; a curated
failure-mode lexicon and (optional) spaCy add procedures and people. The graph
links equipment to the failures, procedures, and regulations it co-occurs with,
every edge carrying the evidence chunk that justifies it.
"""
from __future__ import annotations

import json
import os
import re

TAG_RE = re.compile(r"\b([A-Z]{1,3}-\d{2,4}[A-Z]?)\b")
REG_RE = re.compile(r"\b(OISD|PESO|Factory Act|DGMS|IS)[- ]?(\d{2,4})\b", re.I)
PROC_RE = re.compile(r"\b(procedure|SOP|checklist|inspection|test)\b", re.I)

# Prefixes that match the tag pattern but are not equipment (permits, orders...).
_NON_EQUIPMENT = {"WO", "PTW", "INC", "PM", "ISO", "LEL", "MO"}

FAILURE_MODES = [
    "bearing failure", "seal leak", "seal failure", "cavitation", "gasket rupture",
    "motor burnout", "overheating", "misalignment", "imbalance", "vibration",
    "lubrication failure", "corrosion", "erosion", "fatigue crack", "coupling failure",
    "impeller wear", "shaft crack", "winding fault", "insulation breakdown",
    "filter loading", "filter degradation", "valve leak", "valve failure",
    "pressure drop", "flow reduction", "surge", "fouling", "scaling", "blockage",
    "leakage", "flange leak", "packing wear", "thermal expansion", "trip",
    "high vibration", "high temperature", "loss of flush", "grease degradation",
    "inlet-filter degradation", "discharge temperature rise",
]

_spacy_nlp = None


def _load_spacy():
    """Lazily load en_core_web_sm; return None if spaCy/model is unavailable."""
    global _spacy_nlp
    if _spacy_nlp is not None:
        return _spacy_nlp
    try:
        import spacy
        _spacy_nlp = spacy.load("en_core_web_sm")
    except Exception:
        _spacy_nlp = False
    return _spacy_nlp


def extract_equipment_tags(text: str) -> list:
    """Return unique equipment tags (e.g. P-204, C-11, V-401A) found in text."""
    found = []
    for m in TAG_RE.findall(text or ""):
        prefix = m.split("-")[0]
        if prefix in _NON_EQUIPMENT:
            continue
        if m not in found:
            found.append(m)
    return found


def extract_regulations(text: str) -> list:
    """Return normalized regulatory codes (e.g. OISD-105) found in text."""
    out = []
    for name, num in REG_RE.findall(text or ""):
        code = f"{name.upper().replace(' ', '-')}-{num}"
        if code not in out:
            out.append(code)
    return out


def extract_failure_modes(text: str) -> list:
    """Return failure modes from the curated lexicon present in text."""
    low = (text or "").lower()
    return [fm for fm in FAILURE_MODES if fm in low]


def extract_procedures(text: str) -> list:
    """Return procedure-like noun phrases via spaCy, or regex fallback."""
    nlp = _load_spacy()
    if not nlp:
        return sorted({m.group(0).lower() for m in PROC_RE.finditer(text or "")})
    doc = nlp(text or "")
    procs = {c.text.strip().lower() for c in doc.noun_chunks if PROC_RE.search(c.text)}
    return sorted(procs)


def extract_people(text: str) -> list:
    """Return PERSON entities via spaCy, or a light regex fallback."""
    nlp = _load_spacy()
    if not nlp:
        return sorted(set(re.findall(r"\b[A-Z]\.\s?[A-Z][a-z]+\b", text or "")))
    doc = nlp(text or "")
    return sorted({e.text.strip() for e in doc.ents if e.label_ == "PERSON"})


def _node(nodes, nid, ntype, label, chunk_id):
    """Insert or update a graph node and record the chunk that mentioned it."""
    n = nodes.setdefault(nid, {"id": nid, "type": ntype, "label": label,
                               "mentioned_in": []})
    if chunk_id not in n["mentioned_in"]:
        n["mentioned_in"].append(chunk_id)


def build_graph(chunks: list) -> dict:
    """Build the entity graph (nodes + typed, evidence-bearing edges)."""
    nodes, edges, seen_edges = {}, [], set()

    def add_edge(src, rel, dst, evidence):
        key = (src, rel, dst)
        if key in seen_edges:
            return
        seen_edges.add(key)
        edges.append({"source_node": src, "target_node": dst,
                      "relation": rel, "evidence_chunk": evidence})

    for ch in chunks:
        cid, text = ch["chunk_id"], ch["text"]
        tags = ch.get("equipment_tags") or extract_equipment_tags(text)
        regs = extract_regulations(text)
        fails = extract_failure_modes(text)
        procs = extract_procedures(text)
        people = extract_people(text)

        for t in tags:
            _node(nodes, f"equip:{t}", "equipment", t, cid)
        for r in regs:
            _node(nodes, f"reg:{r}", "regulation", r, cid)
        for fm in fails:
            _node(nodes, f"fail:{fm}", "failure_mode", fm, cid)
        for p in procs:
            _node(nodes, f"proc:{p}", "procedure", p, cid)
        for person in people:
            _node(nodes, f"person:{person}", "person", person, cid)

        for t in tags:
            for fm in fails:
                add_edge(f"equip:{t}", "failed_with", f"fail:{fm}", cid)
            for r in regs:
                add_edge(f"equip:{t}", "governed_by", f"reg:{r}", cid)
            for p in procs:
                add_edge(f"equip:{t}", "has_procedure", f"proc:{p}", cid)
            for person in people:
                add_edge(f"person:{person}", "knows_about", f"equip:{t}", cid)

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "stats": {"nodes": len(nodes), "edges": len(edges)},
    }


def write_graph(graph: dict, path: str) -> None:
    """Persist the knowledge graph to JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(graph, f, indent=2)
