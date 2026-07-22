"""Ingestion: walk data/raw/, extract text, chunk, attach metadata.

PDFs are read per page (page numbers preserved for citation). CSV rows become
one natural-language chunk each. TXT/MD are paragraph-split then windowed into
~400-token chunks with 60-token overlap. Output: data/processed/chunks.jsonl.
"""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone

from pypdf import PdfReader

from app.graph import extract_equipment_tags

CHUNK_TOKENS = 400
OVERLAP_TOKENS = 60


def _now() -> str:
    """Return an ISO-8601 UTC timestamp for chunk provenance."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _window(words: list, size: int, overlap: int):
    """Yield overlapping windows of a word list (token ~= whitespace word)."""
    if not words:
        return
    step = max(1, size - overlap)
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if piece:
            yield " ".join(piece)
        if start + size >= len(words):
            break


def _chunk_record(text, source_file, source_type, page, idx):
    """Assemble a single chunk record with its citation metadata."""
    cid = f"{os.path.splitext(source_file)[0]}::p{page}::c{idx}"
    return {
        "chunk_id": cid,
        "text": text.strip(),
        "source_file": source_file,
        "source_type": source_type,
        "page": page,
        "equipment_tags": extract_equipment_tags(text),
        "created_at": _now(),
    }


def _ingest_pdf(path, name):
    """Extract one chunk set per PDF page, preserving 1-indexed page numbers."""
    out = []
    reader = PdfReader(path)
    for pno, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            continue
        words = text.split()
        for i, win in enumerate(_window(words, CHUNK_TOKENS, OVERLAP_TOKENS)):
            out.append(_chunk_record(win, name, "pdf", pno, i))
    return out


def _row_sentence(row: dict) -> str:
    """Turn a maintenance-log CSV row into a natural-language sentence."""
    date = row.get("date", "an unknown date")
    tag = row.get("equipment_tag", "equipment")
    sym = row.get("symptom", "")
    act = row.get("action_taken", "")
    tech = row.get("technician", "")
    dt = row.get("downtime_hrs", "")
    wo = row.get("work_order", "")
    return (f"On {date}, compressor {tag} (work order {wo}) reported: {sym}. "
            f"Action taken: {act}. Technician: {tech}. Downtime: {dt} hrs.")


def _ingest_csv(path, name):
    """Emit one chunk per CSV row; page holds the 1-indexed data row number."""
    out = []
    with open(path, newline="") as f:
        for row_no, row in enumerate(csv.DictReader(f), start=1):
            sentence = _row_sentence(row)
            rec = _chunk_record(sentence, name, "csv", row_no, 0)
            rec["row"] = row_no
            out.append(rec)
    return out


def _ingest_text(path, name, source_type):
    """Paragraph-split a TXT/MD file, then window into overlapping chunks."""
    out = []
    with open(path) as f:
        raw = f.read()
    idx = 0
    for para in [p for p in raw.split("\n\n") if p.strip()]:
        words = para.split()
        for win in _window(words, CHUNK_TOKENS, OVERLAP_TOKENS):
            out.append(_chunk_record(win, name, source_type, 1, idx))
            idx += 1
    return out


def ingest_dir(raw_dir: str) -> list:
    """Ingest every supported file in raw_dir and return all chunk records."""
    chunks = []
    for name in sorted(os.listdir(raw_dir)):
        path = os.path.join(raw_dir, name)
        ext = os.path.splitext(name)[1].lower()
        if ext == ".pdf":
            chunks.extend(_ingest_pdf(path, name))
        elif ext == ".csv":
            chunks.extend(_ingest_csv(path, name))
        elif ext in (".txt", ".md"):
            chunks.extend(_ingest_text(path, name, ext.lstrip(".")))
    return chunks


def write_chunks(chunks: list, out_path: str) -> None:
    """Persist chunk records as JSON Lines."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        for c in chunks:
            f.write(json.dumps(c) + "\n")


def load_chunks(path: str) -> list:
    """Load chunk records from a JSON Lines file."""
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]
