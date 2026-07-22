"""Brand CSS and HTML fragments for the LegacyLoop Streamlit UI.

Warm off-white canvas, Signal Amber accent, Fraunces headings, Inter body,
JetBrains Mono for every number, chip, and citation. This module removes the
default Streamlit chrome and re-skins the primitives we use.
"""
from __future__ import annotations

import html
import re

CANVAS = "#F5F3EE"
INK = "#111111"
MUTED = "#4A4A4A"
AMBER = "#E4572E"
BLUEPRINT = "#1B3A57"
MONO_BG = "#0B0B0C"

BRAND_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

#MainMenu, header, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"],
.stDeployButton {{ display: none !important; }}

.stApp, [data-testid="stAppViewContainer"] {{ background: {CANVAS}; }}
.block-container {{ max-width: 1280px; padding-top: 1.4rem; }}
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; color: {INK}; }}

.ll-rule {{ height: 2px; background: {AMBER}; width: 100%; margin: 0 0 1.6rem 0;
  border-radius: 2px; }}
.ll-wordmark {{ font-family: 'JetBrains Mono', monospace; font-weight: 700;
  font-size: 1.5rem; letter-spacing: -0.02em; color: {INK}; }}
.ll-wordmark .loop {{ color: {AMBER}; }}
.ll-sub {{ font-family: 'Inter', sans-serif; color: {MUTED}; font-size: 0.9rem;
  margin: 0.2rem 0 1.4rem 0; line-height: 1.5; }}
.ll-eyebrow {{ font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  letter-spacing: 0.16em; text-transform: uppercase; color: {MUTED};
  margin-bottom: 0.5rem; }}
.ll-corpus {{ font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
  color: {BLUEPRINT}; border: 1px solid rgba(27,58,87,0.25); border-radius: 8px;
  padding: 0.7rem 0.85rem; line-height: 1.7; margin-top: 1rem; }}
.ll-corpus b {{ color: {AMBER}; }}

div.stButton > button {{
  width: 100%; text-align: left; white-space: normal; background: transparent;
  color: {INK}; border: 1px solid rgba(17,17,17,0.35); border-radius: 10px;
  padding: 0.7rem 0.85rem; font-family: 'Inter', sans-serif; font-size: 0.86rem;
  line-height: 1.35; transition: all 120ms ease; margin-bottom: 0.55rem; }}
div.stButton > button:hover {{
  background: {AMBER}; color: #fff; border-color: {AMBER};
  transform: translateY(-1px); }}
div.stButton > button:focus {{ box-shadow: none; color: #fff; }}

.stTextInput > div > div input {{
  background: {MONO_BG}; color: #EDEDED; border: 1px solid rgba(17,17,17,0.4);
  border-radius: 10px; font-family: 'JetBrains Mono', monospace;
  font-size: 0.95rem; padding: 0.85rem 1rem; caret-color: {AMBER}; }}
.stTextInput > div > div input:focus {{ border-color: {AMBER};
  box-shadow: 0 0 0 2px rgba(228,87,46,0.18); }}
.stTextInput label {{ font-family: 'JetBrains Mono', monospace;
  color: {MUTED}; font-size: 0.78rem; letter-spacing: 0.04em; }}

.ll-answer {{ font-family: 'Fraunces', Georgia, serif; font-size: 1.14rem;
  line-height: 1.62; color: {INK}; background: #FFFFFF;
  border: 1px solid rgba(17,17,17,0.1); border-left: 3px solid {AMBER};
  border-radius: 12px; padding: 1.5rem 1.7rem; }}
.ll-answer table {{ border-collapse: collapse; width: 100%; margin: 0.8rem 0;
  font-family: 'Inter', sans-serif; font-size: 0.9rem; }}
.ll-answer th, .ll-answer td {{ border: 1px solid rgba(17,17,17,0.15);
  padding: 0.45rem 0.6rem; text-align: left; }}
.ll-answer th {{ background: rgba(27,58,87,0.06); font-weight: 600; }}
.ll-answer strong {{ font-weight: 600; }}

.ll-cite {{ font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
  color: {BLUEPRINT}; background: rgba(27,58,87,0.07);
  border: 1px solid rgba(27,58,87,0.28); border-radius: 6px;
  padding: 0.05rem 0.4rem; white-space: nowrap; }}

.ll-sources-title {{ font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
  letter-spacing: 0.14em; text-transform: uppercase; color: {MUTED};
  margin: 1.4rem 0 0.6rem 0; }}
.ll-card {{ background: #FFFFFF; border: 1px solid rgba(17,17,17,0.12);
  border-radius: 10px; padding: 0.8rem 0.9rem; height: 100%; }}
.ll-card .fn {{ font-family: 'JetBrains Mono', monospace; font-size: 0.76rem;
  color: {INK}; font-weight: 500; }}
.ll-card .pg {{ font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
  color: {AMBER}; margin: 0.15rem 0 0.4rem 0; }}
.ll-card .pv {{ font-size: 0.76rem; color: {MUTED}; line-height: 1.45;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
  overflow: hidden; }}

.ll-readout {{ font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
  color: {MUTED}; background: {MONO_BG}; border-radius: 8px;
  padding: 0.6rem 0.9rem; margin-top: 1.2rem; }}
.ll-readout .k {{ color: #7FB069; }}
.ll-readout .a {{ color: {AMBER}; }}
</style>
"""

_CITE_RE = re.compile(r"\[([^\]\[]+?\s·\s(?:p\.\d+|§[^\]]+))\]")


def style_citations(markdown_text: str) -> str:
    """Wrap [file · p.N] / [file · §x] chips in styled inline spans."""
    return _CITE_RE.sub(
        lambda m: f'<span class="ll-cite">{html.escape(m.group(1))}</span>',
        markdown_text)


def source_card(filename: str, page, preview: str) -> str:
    """Return the HTML for one cited-source card."""
    loc = f"p.{page}" if isinstance(page, int) and page > 0 else "reference"
    pv = html.escape((preview or "").strip()) or "Cited source in corpus."
    return (f'<div class="ll-card"><div class="fn">{html.escape(filename)}</div>'
            f'<div class="pg">{loc}</div><div class="pv">{pv}</div></div>')


def readout(confidence: float, retrieval: str, latency_ms: int) -> str:
    """Return the mono confidence/retrieval/latency readout bar."""
    pct = int(round(confidence * 100))
    sec = latency_ms / 1000.0
    return (f'<div class="ll-readout">confidence: <span class="a">{pct}%</span> '
            f'&nbsp;·&nbsp; retrieval: <span class="k">{html.escape(retrieval)}</span> '
            f'&nbsp;·&nbsp; latency: <span class="a">{sec:.1f}s</span></div>')
