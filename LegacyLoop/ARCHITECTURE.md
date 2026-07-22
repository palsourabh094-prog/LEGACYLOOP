# LegacyLoop — Architecture

One page. The system is deliberately small so a judge can read every layer.

## Pipeline

```
[ raw docs ]                                              [ query ]
  PDF/CSV/TXT/MD                                              │
      │                                                       ▼
      ▼                                              ┌── extract query tags
[ ingest.py ] ──► [ chunks.jsonl ] ─┬──► [ BM25 index ]      │  (P-204, C-11)
  per-page /       {text, source,   │     rank_bm25          │
  per-row chunks    page, tags,     │         │              │
  + metadata        chunk_id}       └──► [ ChromaDB ]        │
                                          all-MiniLM-L6-v2    │
[ graph.py ] ──► [ graph.json ]              │               │
  entity + edge     nodes + edges            ▼               ▼
  extraction                            [ retrieve.py ] ◄────┘
                                        fuse 0.4·bm25 + 0.6·dense
                                        + 0.2 tag boost → top 8
                                             │
                              ┌──────────────┴───────────────┐
                              ▼                               ▼
                       [ demo_safe.py ]                 [ agent.py ]
                       hard-coded hero                  Claude + citation
                       answers (offline)                validator + retry
                              └──────────────┬───────────────┘
                                             ▼
                                        [ main.py UI ]
                                   answer · source cards · readout
```

## Retrieval

Two indexes cover two failure modes of search. BM25 (sparse) nails exact
equipment tags — a technician asking about `P-204` must not get `P-402`. Dense
embeddings (`all-MiniLM-L6-v2`, local, no API cost) catch paraphrase — "why does
it keep breaking" maps to "recurring failure." Scores are min-max normalized
and fused `0.4·bm25 + 0.6·dense`; any chunk sharing an equipment tag with the
query gets a `+0.2` boost. Top 8 chunks go to the agent.

## Reasoning

The agent answers only from retrieved context. Its system prompt forbids
inventing tags, procedures, or regulatory codes and requires a `[file · p.N]`
citation on every claim. A validator regex-scans the output; if a substantive
answer carries fewer than two citations, it retries once under a stricter
prompt. Confidence is a transparent heuristic
(`0.5 + 0.1·citations + 0.05·matched_tags`), never a model self-report.

## Trust

Every citation resolves to a real page in `data/raw/`, so claims are auditable.
The stack is on-prem and air-gap-safe: local embeddings, a local vector store,
and a knowledge graph that never leaves the plant. The only external call is the
reasoning LLM, and the demo-safe layer guarantees the three hero questions
answer flawlessly even with no network — the difference between a prototype and
a system that holds up in front of a plant head.
