"""Reasoning agent: Claude wrapper with hard citation enforcement.

The agent answers only from retrieved context and must cite every claim as
[filename · p.N]. A validator rejects under-cited answers and retries once with
a stricter instruction. Confidence is a transparent heuristic, not a model
self-report. All facts and their pages come from the retrieval layer.
"""
from __future__ import annotations

import os
import re
import time

SYSTEM_PROMPT = (
    "You are LegacyLoop, a senior industrial reliability engineer answering a "
    "field technician. Answer only from the provided context chunks. Every "
    "factual claim MUST end with a citation in the form [filename · p.N] "
    "where filename and page come from the chunk metadata. If the context does "
    "not contain the answer, respond exactly: 'I don't have that in the current "
    "corpus — flag this to the plant knowledge officer for capture.' Never "
    "invent equipment tags, procedures, or regulatory codes. Answer in numbered "
    "steps when the query asks for a procedure. Keep responses under 250 words "
    "unless the query explicitly asks for detail."
)

PRIMARY_MODEL = os.getenv("LEGACYLOOP_MODEL", "claude-opus-4-7")
FALLBACK_MODEL = "claude-3-5-sonnet-latest"
CITATION_RE = re.compile(r"\[([^\]]+?)\s·\sp\.(\d+)\]")


def format_context(chunks: list) -> str:
    """Render retrieved chunks with their citation metadata for the prompt."""
    blocks = []
    for c in chunks:
        head = f"[{c['source_file']} · p.{c['page']}] (chunk {c['chunk_id']})"
        blocks.append(f"{head}\n{c['text']}")
    return "\n\n---\n\n".join(blocks)


def parse_citations(text: str) -> list:
    """Extract [file · p.N] citation chips from an answer."""
    seen, out = set(), []
    for file, page in CITATION_RE.findall(text):
        key = (file.strip(), int(page))
        if key not in seen:
            seen.add(key)
            out.append({"file": file.strip(), "page": int(page)})
    return out


def _confidence(num_citations: int, num_tags: int) -> float:
    """Heuristic confidence from citation count and matched equipment tags."""
    return round(min(1.0, 0.5 + 0.1 * num_citations + 0.05 * num_tags), 2)


def _client():
    """Construct an Anthropic client, or raise if no API key is configured."""
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key or key.startswith("sk-ant-your-key"):
        raise RuntimeError("ANTHROPIC_API_KEY not set — running demo-safe only.")
    import anthropic
    return anthropic.Anthropic(api_key=key)


def _call(client, model: str, user: str, strict: bool) -> str:
    """Single Claude call; strict mode reinforces the citation requirement."""
    system = SYSTEM_PROMPT
    if strict:
        system += (" Reminder: cite EVERY sentence as [filename · p.N]. "
                   "An answer with fewer than two citations is invalid.")
    resp = client.messages.create(
        model=model, max_tokens=700, system=system,
        messages=[{"role": "user", "content": user}])
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def _generate(client, user: str, strict: bool) -> str:
    """Call the primary model, falling back to Sonnet on model errors."""
    try:
        return _call(client, PRIMARY_MODEL, user, strict)
    except Exception:
        return _call(client, FALLBACK_MODEL, user, strict)


def answer(query: str, chunks: list, matched_tags: int = 0) -> dict:
    """Generate a cited, validated answer object from retrieved context."""
    start = time.perf_counter()
    client = _client()
    user = (f"Context chunks:\n\n{format_context(chunks)}\n\n"
            f"Field technician question: {query}")

    text = _generate(client, user, strict=False)
    citations = parse_citations(text)
    if len(citations) < 2 and len(text.split()) > 40:
        text = _generate(client, user, strict=True)
        citations = parse_citations(text)

    latency_ms = int((time.perf_counter() - start) * 1000)
    return {
        "answer_markdown": text.strip(),
        "citations": citations,
        "sources_used": [c["chunk_id"] for c in chunks],
        "confidence": _confidence(len(citations), matched_tags),
        "latency_ms": latency_ms,
        "retrieval": "hybrid (bm25 + dense)",
        "demo_safe": False,
    }
