"""Smoke test: run the three hero questions end-to-end and assert citations.

Exits 0 only if each hero answer routes through the pipeline and contains at
least two [file · p.N] citations that resolve to real files in data/raw/.
Runs offline via demo-safe mode, so it passes with no API key.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent import parse_citations          # noqa: E402
from app.demo_safe import HERO_QUESTIONS, lookup  # noqa: E402

RAW = ROOT / "data" / "raw"


def check(question: str) -> None:
    """Assert one hero question yields >=2 citations to files that exist."""
    result = lookup(question)
    assert result is not None, f"No routed answer for: {question!r}"
    citations = parse_citations(result["answer_markdown"])
    assert len(citations) >= 2, (
        f"Expected >=2 [file · p.N] citations, got {len(citations)} "
        f"for: {question!r}")
    for cit in citations:
        assert (RAW / cit["file"]).exists(), (
            f"Citation file not found in corpus: {cit['file']}")
    print(f"  OK  {question}")
    print(f"      citations: {len(citations)} · "
          f"confidence: {int(result['confidence'] * 100)}%")


def main() -> int:
    """Run all hero questions and report pass/fail."""
    print("LegacyLoop smoke test — three hero questions\n")
    for q in HERO_QUESTIONS:
        check(q)
    print("\nAll hero questions passed with valid citations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
