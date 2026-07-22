"""Hybrid retrieval: BM25 (sparse, exact tag matches) + dense (ChromaDB) + rerank.

BM25 catches exact equipment tags like P-204 that embeddings blur; dense
catches paraphrase. Scores are min-max normalized and fused 0.4/0.6, then
chunks sharing an equipment tag with the query get a +0.2 boost.
"""
from __future__ import annotations

import os

from rank_bm25 import BM25Okapi

from app.graph import extract_equipment_tags
from app.ingest import load_chunks

EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION = "legacyloop"
BM25_WEIGHT = 0.4
DENSE_WEIGHT = 0.6
TAG_BOOST = 0.2


def _tokenize(text: str) -> list:
    """Lowercase word tokenizer that keeps tag characters like the hyphen."""
    return [t for t in text.lower().replace("/", " ").split() if t]


def _minmax(scores: dict) -> dict:
    """Min-max normalize a {id: score} map into [0, 1]."""
    if not scores:
        return {}
    vals = list(scores.values())
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-9:
        return {k: 1.0 for k in scores}
    return {k: (v - lo) / (hi - lo) for k, v in scores.items()}


def _chroma_collection(persist_dir: str):
    """Open (or create) the persistent Chroma collection with local embeddings."""
    import chromadb
    from chromadb.utils import embedding_functions
    client = chromadb.PersistentClient(path=persist_dir)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return client.get_or_create_collection(
        name=COLLECTION, embedding_function=ef, metadata={"hnsw:space": "cosine"})


def build_dense_index(chunks: list, persist_dir: str) -> int:
    """Embed all chunks into a fresh Chroma collection. Returns count indexed."""
    import chromadb
    from chromadb.utils import embedding_functions
    os.makedirs(persist_dir, exist_ok=True)
    client = chromadb.PersistentClient(path=persist_dir)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    col = client.get_or_create_collection(
        name=COLLECTION, embedding_function=ef, metadata={"hnsw:space": "cosine"})
    ids = [c["chunk_id"] for c in chunks]
    docs = [c["text"] for c in chunks]
    metas = [{"source_file": c["source_file"], "page": c["page"],
              "source_type": c["source_type"]} for c in chunks]
    col.add(ids=ids, documents=docs, metadatas=metas)
    return len(ids)


class HybridRetriever:
    """Fuses BM25 and dense retrieval with a query-tag boost over the corpus."""

    def __init__(self, processed_dir: str):
        """Load chunks, build the BM25 index, and open the Chroma collection."""
        self.chunks = load_chunks(os.path.join(processed_dir, "chunks.jsonl"))
        self.by_id = {c["chunk_id"]: c for c in self.chunks}
        self.bm25 = BM25Okapi([_tokenize(c["text"]) for c in self.chunks])
        self._ids = [c["chunk_id"] for c in self.chunks]
        self.collection = _chroma_collection(os.path.join(processed_dir, "chroma"))

    def _bm25_top(self, query: str, k: int) -> dict:
        """Return the top-k BM25 scores as {chunk_id: score}."""
        scores = self.bm25.get_scores(_tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return {self._ids[i]: float(scores[i]) for i in ranked if scores[i] > 0}

    def _dense_top(self, query: str, k: int) -> dict:
        """Return the top-k dense similarities as {chunk_id: score}."""
        res = self.collection.query(query_texts=[query], n_results=k)
        ids = res.get("ids", [[]])[0]
        dists = res.get("distances", [[]])[0]
        return {cid: 1.0 - float(d) for cid, d in zip(ids, dists)}

    def search(self, query: str, k: int = 8) -> list:
        """Retrieve, fuse, tag-boost, and return the top-k chunk records."""
        bm = _minmax(self._bm25_top(query, 20))
        dn = _minmax(self._dense_top(query, 20))
        q_tags = set(extract_equipment_tags(query))
        fused = {}
        for cid in set(bm) | set(dn):
            score = BM25_WEIGHT * bm.get(cid, 0.0) + DENSE_WEIGHT * dn.get(cid, 0.0)
            if q_tags & set(self.by_id[cid].get("equipment_tags", [])):
                score += TAG_BOOST
            fused[cid] = score
        top = sorted(fused, key=lambda c: fused[c], reverse=True)[:k]
        results = []
        for cid in top:
            rec = dict(self.by_id[cid])
            rec["score"] = round(fused[cid], 4)
            results.append(rec)
        return results
