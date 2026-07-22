"""LegacyLoop — Streamlit entrypoint. The memory layer for industrial India.

Left rail: wordmark, hero-question chips, live corpus summary. Right panel: a
terminal-style query box and a cited answer with source cards and a mono
confidence readout. Demo-safe answers are served first; the live hybrid-RAG
agent handles everything else.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Make the project root importable when launched via `streamlit run app/main.py`
# (Streamlit puts app/ on sys.path, not the project root).
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from dotenv import load_dotenv

from app import agent, demo_safe, styles
from app.graph import extract_equipment_tags

RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
GRAPH = ROOT / "data" / "graph.json"

load_dotenv(ROOT / ".env")

st.set_page_config(page_title="LegacyLoop", layout="wide",
                   initial_sidebar_state="collapsed")
st.markdown(styles.BRAND_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def get_retriever():
    """Build the hybrid retriever once (None if the index is not built yet)."""
    from app.retrieve import HybridRetriever
    try:
        return HybridRetriever(str(PROC))
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def corpus_stats():
    """Return (docs, chunks, entities) counts from the processed corpus."""
    docs = len([p for p in RAW.glob("*") if p.suffix.lower() in
                (".pdf", ".csv", ".txt", ".md")]) if RAW.exists() else 0
    chunks = 0
    cf = PROC / "chunks.jsonl"
    if cf.exists():
        chunks = sum(1 for _ in cf.open())
    entities = 0
    if GRAPH.exists():
        entities = json.loads(GRAPH.read_text()).get("stats", {}).get("nodes", 0)
    return docs, chunks, entities


def preview_for(retriever, filename: str, page) -> str:
    """Find a short preview of the chunk backing a citation, if indexed."""
    if not retriever:
        return ""
    best = ""
    for c in retriever.chunks:
        if c["source_file"] != filename:
            continue
        best = best or c["text"]
        if isinstance(page, int) and page > 0 and c["page"] == page:
            return c["text"][:170]
    return best[:170]


def respond(query: str) -> dict:
    """Route a query: demo-safe first, then the live hybrid-RAG agent."""
    demo = demo_safe.lookup(query)
    if demo:
        return demo
    retriever = get_retriever()
    if retriever is None:
        return {"error": "Index not built. Run `python scripts/build_index.py`."}
    chunks = retriever.search(query, k=8)
    ctx_tags = {t for c in chunks for t in c.get("equipment_tags", [])}
    matched = len(set(extract_equipment_tags(query)) & ctx_tags)
    try:
        return agent.answer(query, chunks, matched_tags=matched)
    except RuntimeError:
        return {"error": "No ANTHROPIC_API_KEY set. The three hero questions "
                "still work in demo-safe mode; add a key in .env for open-ended "
                "queries."}


def render_result(result: dict) -> None:
    """Render an answer object: prose, cited-source cards, and readout."""
    if "error" in result:
        st.warning(result["error"])
        return
    body = styles.style_citations(result["answer_markdown"])
    # Blank lines inside the div let Streamlit parse the content as markdown
    # (bold, lists, tables) rather than raw-HTML context.
    st.markdown(f'<div class="ll-answer">\n\n{body}\n\n</div>',
                unsafe_allow_html=True)

    retriever = get_retriever()
    seen, cards = set(), []
    for cit in result.get("citations", []):
        key = (cit["file"], cit.get("page"))
        if cit["file"] in seen:
            continue
        seen.add(cit["file"])
        cards.append(styles.source_card(
            cit["file"], cit.get("page"),
            preview_for(retriever, cit["file"], cit.get("page"))))
    if cards:
        st.markdown('<div class="ll-sources-title">Sources used</div>',
                    unsafe_allow_html=True)
        cols = st.columns(len(cards))
        for col, card in zip(cols, cards):
            col.markdown(card, unsafe_allow_html=True)

    st.markdown(styles.readout(result["confidence"], result["retrieval"],
                               result["latency_ms"]), unsafe_allow_html=True)


def render_sidebar() -> None:
    """Sidebar: corpus summary, entity graph, and a reload control."""
    with st.sidebar:
        st.markdown("**Corpus**")
        docs, chunks, ents = corpus_stats()
        st.markdown(f"`docs: {docs}  chunks: {chunks}  entities: {ents}`")
        if GRAPH.exists():
            with st.expander("Entity graph"):
                st.json(json.loads(GRAPH.read_text()))
        if st.button("Reload index"):
            get_retriever.clear()
            corpus_stats.clear()
            st.rerun()


def main() -> None:
    """Compose the two-column LegacyLoop console."""
    st.markdown('<div class="ll-rule"></div>', unsafe_allow_html=True)
    render_sidebar()
    left, right = st.columns([0.3, 0.7], gap="large")

    with left:
        st.markdown('<div class="ll-wordmark">Legacy<span class="loop">Loop</span>'
                    '</div>', unsafe_allow_html=True)
        st.markdown('<div class="ll-sub">The Memory Layer for Industrial India'
                    '</div>', unsafe_allow_html=True)
        st.markdown('<div class="ll-eyebrow">Ask the veteran</div>',
                    unsafe_allow_html=True)
        for q in demo_safe.HERO_QUESTIONS:
            if st.button(q, key=f"chip::{q}"):
                st.session_state["query"] = q
        docs, chunks, ents = corpus_stats()
        st.markdown(f'<div class="ll-corpus">docs_indexed: <b>{docs}</b> · '
                    f'chunks: <b>{chunks}</b> · entities: <b>{ents}</b></div>',
                    unsafe_allow_html=True)

    with right:
        query = st.text_input("> ask the veteran",
                              value=st.session_state.get("query", ""),
                              placeholder="Pump P-204 is vibrating at 6 mm/s...")
        if query.strip():
            with st.spinner("Retrieving and reasoning over the corpus..."):
                result = respond(query)
            render_result(result)
        else:
            st.markdown('<div class="ll-sub">Click a question on the left, or '
                        'type your own. Every answer is grounded in the corpus '
                        'and cited to the source page.</div>',
                        unsafe_allow_html=True)


if __name__ == "__main__":
    main()
