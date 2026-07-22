"""One-shot index build: generate corpus, ingest, extract graph, embed.

Run once before the UI: `python scripts/build_index.py`. Idempotent — it
regenerates the sample corpus, rewrites chunks.jsonl and graph.json, and
rebuilds the ChromaDB dense index from scratch.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from app.graph import build_graph, write_graph          # noqa: E402
from app.ingest import ingest_dir, write_chunks          # noqa: E402
from app.retrieve import build_dense_index               # noqa: E402
from corpus_gen import build_corpus                       # noqa: E402

RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
GRAPH = ROOT / "data" / "graph.json"
CHUNKS = PROC / "chunks.jsonl"


def main() -> None:
    """Generate the corpus, then build the chunk, graph, and dense indexes."""
    print("[1/4] Generating sample industrial corpus...")
    files = build_corpus(str(RAW))
    print("      ", ", ".join(files))

    print("[2/4] Ingesting and chunking...")
    chunks = ingest_dir(str(RAW))
    write_chunks(chunks, str(CHUNKS))
    print(f"       {len(chunks)} chunks -> {CHUNKS.relative_to(ROOT)}")

    print("[3/4] Extracting entities and building the knowledge graph...")
    graph = build_graph(chunks)
    write_graph(graph, str(GRAPH))
    print(f"       {graph['stats']['nodes']} nodes, "
          f"{graph['stats']['edges']} edges -> {GRAPH.relative_to(ROOT)}")

    print("[4/4] Embedding chunks into ChromaDB (all-MiniLM-L6-v2)...")
    n = build_dense_index(chunks, str(PROC / "chroma"))
    print(f"       {n} vectors indexed.")

    print(f"\nDone. docs: {len(files)} · chunks: {len(chunks)} · "
          f"entities: {graph['stats']['nodes']}")
    print("Next: streamlit run app/main.py")


if __name__ == "__main__":
    main()
