# LegacyLoop

The memory layer for industrial India. A citation-first, hybrid-retrieval RAG
prototype that captures 30 years of tribal engineering knowledge and puts it in
the pocket of every field technician — before the veterans retire.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && python -m spacy download en_core_web_sm
cp .env.example .env          # paste your ANTHROPIC_API_KEY (optional for demo)
python scripts/build_index.py && streamlit run app/main.py
```

The three hero questions run fully offline in demo-safe mode — no API key
needed to demo. A key unlocks open-ended queries against the corpus.

## What to try

Click a chip, or paste any of these into the query box:

- `Pump P-204 is vibrating at 6 mm/s. What do I check?`
- `Why does compressor C-11 keep failing every 4 months?`
- `Give me an OISD-compliant audit trail for the last confined-space entry.`

Verify the pipeline end-to-end:

```bash
python scripts/smoke_test.py   # asserts >=2 valid citations per hero answer
```

## Architecture

Documents are ingested per page, chunked, and indexed two ways: BM25 for exact
equipment-tag matches (P-204) and dense embeddings (all-MiniLM-L6-v2 in
ChromaDB) for paraphrase. Retrieval fuses both scores (0.4/0.6) and boosts
chunks that share an equipment tag with the query. The Claude reasoning agent
answers only from retrieved context and must cite every claim as
`[file · p.N]`; a validator rejects under-cited answers. Everything runs
on-prem and air-gap-safe, and a hard-coded demo-safe layer guarantees the hero
questions never fail on stage. See `ARCHITECTURE.md` for the full diagram.

## Files

- `app/ingest.py` — PDF/CSV/TXT/MD ingestion and token-windowed chunking.
- `app/graph.py` — regex + spaCy entity extraction and the knowledge graph.
- `app/retrieve.py` — hybrid BM25 + dense retrieval with tag boosting.
- `app/agent.py` — Claude wrapper with citation enforcement and confidence.
- `app/demo_safe.py` — hard-coded flawless answers for the three hero questions.
- `app/styles.py` — LegacyLoop brand CSS and HTML fragments.
- `app/main.py` — the Streamlit console (entrypoint).
- `scripts/build_index.py` — generate corpus, ingest, embed, build graph.
- `scripts/smoke_test.py` — end-to-end hero-question citation assertions.
- `scripts/corpus_gen.py` — programmatic sample industrial corpus.

Pure HTML/CSS/JS-free Python. No LangChain. No LlamaIndex. Every layer is
readable in twenty minutes.
