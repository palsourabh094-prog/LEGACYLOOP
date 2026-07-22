# CLAUDE.md — LegacyLoop

> The Memory Layer for Industrial India.
> AI that captures 30 years of tribal engineering knowledge — before your best people retire.

This document is the single source of truth for the LegacyLoop website. Any AI or engineer working on this codebase must read this file first and treat it as the north star for tone, visual language, information architecture, and technical decisions.

---

## 1. PROJECT AT A GLANCE

| Field | Value |
|---|---|
| Product | LegacyLoop |
| Category | Industrial Knowledge Intelligence Platform |
| Positioning | "Institutional Memory as a Service" for asset-heavy industry |
| Deliverable | A single-page marketing site that looks and feels like a $5,000 boutique-agency build |
| Audience | Hackathon judges (senior industry CXOs), Plant Heads, Chief Digital Officers |
| Tone | Grounded, senior, industrial, precise — never startup-cheerful |
| Reference feel | Linear × Stripe × Palantir × Vercel × a technical whitepaper |

---

## 2. THE STORY (Non-negotiable narrative spine)

Every section of the site must serve this three-beat arc:

**Beat 1 — The Cliff.** 25% of India's veteran industrial engineers retire within a decade. Their knowledge is undocumented. When they leave, it is gone.

**Beat 2 — The Cost.** 35% of engineering hours are lost to search. 18–22% of unplanned downtime traces back to knowledge gaps. Every hour of unplanned downtime in a heavy plant costs ₹50 lakh or more.

**Beat 3 — The Loop.** LegacyLoop captures institutional knowledge continuously — from PDFs, P&IDs, maintenance logs, SOPs, incident reports, and the veterans themselves — and puts it in the pocket of every field technician. The knowledge no longer leaves when the engineer does. It loops back.

The name is the product: knowledge *loops* from legacy engineers into the system, then back out to the next generation.

---

## 3. WHO IT IS FOR

Primary personas — write for these people, not for a generic reader:

- **The Plant Head** — 50s, ex-mechanical engineer, respects competence, hates fluff. Wants zero downtime and a smooth audit.
- **The Chief Digital Officer** — 40s, ex-consulting, cares about scalable ROI and integration risk.
- **The Field Technician** — 20s–30s, uses WhatsApp more than email, needs answers in the field at 3 AM.
- **The Hackathon Judge** — a composite of the above. Has seen 40 pitches today. Wants to feel *this team gets it*.

---

## 4. INFORMATION ARCHITECTURE

The site is a single long-scroll page with a fixed slim top nav. Sections, in order:

1. **Nav** — Wordmark left. Anchors: Problem · Platform · Architecture · Impact · Team. CTA right: `Request a Pilot`.
2. **Hero** — The retirement cliff. Bold editorial headline. One sentence sub. Two CTAs (primary: Request a Pilot; ghost: Watch the 90-second demo).
3. **The Cliff** — Data-driven section. Three large stat cards with sourced numbers. Small footnote with sources (DGFASLI, NASSCOM-EY, BIS Research, McKinsey).
4. **Why Existing Tools Fail** — Four-column comparison: SharePoint / Google / Generic RAG / **LegacyLoop**. Ticks and crosses. Ends with a single sharp line: *"Filing cabinets don't reason. LegacyLoop does."*
5. **The Platform** — The four-pillar architecture, presented as an interactive diagram (Ingestion → Knowledge Graph + Vector Store → Reasoning Agent → Field Interface). Each pillar expandable with one paragraph of copy.
6. **See It Work** — A simulated chat / query demo. Pre-scripted "hero questions" the user can click:
   - *"Pump P-204 is vibrating at 6 mm/s. What do I check?"*
   - *"Why does compressor C-11 keep failing every 4 months?"*
   - *"Give me an OISD-compliant audit trail for the last confined-space entry."*
   Response appears typewriter-style with citations rendered as small chips linking to (mock) source pages.
7. **Architecture** — A dark technical diagram showing the full stack, with node labels: Document Ingestion · Layout Parser · Entity Extractor · Knowledge Graph (Neo4j-style) · Vector Store (Chroma) · Reasoning Agent (LLM) · Citation Layer · Voice/WhatsApp/Web Clients · On-Prem Deployment · Audit Log.
8. **The Loop in Practice** — Three vertical timeline cards: *Capture* → *Reason* → *Deliver*. Each with a 2-line story from the field.
9. **Impact & Scale** — Metrics: MTTD reduction, downtime saved (₹), compliance evidence generated, engineer hours reclaimed. Small industry logos (Steel, Oil & Gas, Power, Pharma, Cement) as monochrome badges — not fake customer logos.
10. **Business Viability** — TAM math laid out cleanly: 850+ large industrial facilities in India × ₹50 L / plant / year = ₹425 Cr India-only TAM. Cite the number, do not hide it.
11. **Trust** — Security posture: air-gapped, on-prem, audit-logged, role-based access, Factory Act / OISD / PESO aware.
12. **Team + Ask** — Short. "We are a team of X at ET AI Hackathon 2026. We want to build this for real. Give us the shot."
13. **Footer** — Wordmark, one line of copy, contact anchor, © 2026 LegacyLoop.

---

## 5. VISUAL SYSTEM

The visual system is the difference between "an AI site" and "a $5,000 site." Follow it precisely.

### 5.1 Palette
Not neon. Not gradient purple. **Industrial editorial.**

- Canvas: `#F5F3EE` (warm off-white paper) OR `#0B0B0C` (deep near-black) for dark hero moments
- Ink: `#111111`
- Muted ink: `#4A4A4A`
- Rule / hairline: `#111111` at 1px, always crisp
- Accent — **Signal Amber**: `#E4572E` (used sparingly, only for the "loop" motif, primary CTA, and key data highlights)
- Accent — **Blueprint**: `#1B3A57` (used for architecture diagrams, technical chips)
- Success / positive stat: `#0F5132`

No purple gradients. No pastel. No glassmorphism. No AI-generated-looking hero image.

### 5.2 Typography
Pair one editorial serif with one precise mono. Sans is body only.

- Display: **GT Sectra**, **Tiempos Headline**, or free fallback **"Fraunces"** — used at massive sizes (clamp between 56px and 168px on hero)
- Body: **Inter** or **Söhne** — 16–18px, generous line-height 1.55
- Mono: **JetBrains Mono** or **IBM Plex Mono** — used for stats, code, chips, and callouts
- Numerals in stats: mono, tabular, oversized (clamp 72–144px)

Headlines are set tight (letter-spacing -0.02em). Body is set normal. Mono is set open.

### 5.3 Grid & Layout
- 12-column grid, 80px gutters on desktop, 24px on mobile
- Content max-width: 1280px, but hero and data sections can bleed to 1440px
- Generous vertical rhythm: sections are 160px tall minimum on desktop
- Left-aligned by default. Center alignment is banned except for the hero eyebrow.
- Section numbers in the margin (`01 / The Cliff`, `02 / The Cost`...) — like a technical report

### 5.4 Motion
- Understated. No bounce. No parallax gimmicks.
- Scroll-triggered reveals: 400ms ease-out, 8px translate-y, opacity 0→1
- The "Loop" motif — a single continuous line that draws itself across sections as the user scrolls, connecting Cliff → Cost → Loop. This is the one signature animation.
- The demo chat types at ~30ms per character
- Hover: 120ms, subtle underline slide on links, no color-flip

### 5.5 The Loop Motif (signature element)
A single 1px amber line begins at the top of the page, threads through every section as the user scrolls, and closes back on itself at the footer — visually enacting the product name. Implement with an SVG path + `stroke-dashoffset` tied to scroll progress.

### 5.6 Imagery
- No stock photos. No fake dashboards. No 3D blobs.
- Preferred: high-contrast monochrome photography of real industrial environments (turbines, pipe racks, control rooms) if available — otherwise, use technical illustration in the Blueprint color.
- P&ID / schematic-style line drawings are perfect for section dividers.
- Data visuals are hand-crafted (SVG), never charting-library-default.

### 5.7 What "Premium" Actually Means Here
Premium is restraint. Every element earns its place. If a section can lose a decoration and still land the message, remove the decoration. The page should read like a Financial Times special report, not a SaaS landing page.

---

## 6. COPY VOICE

- Sentences are short. Verbs do the work.
- No exclamation marks. No emoji. No "revolutionize," "unleash," "empower," "seamless," "cutting-edge."
- Numbers over adjectives. "18–22% of unplanned downtime" beats "significant downtime."
- Never call it "an AI platform." Call it "a memory layer."
- Never say "users." Say "field technicians," "plant heads," "operators."
- The word "Loop" is capitalized when it refers to the product motif.

Sample headlines that land the tone:
- *"In the next decade, a quarter of India's industrial memory retires."*
- *"Filing cabinets don't reason. LegacyLoop does."*
- *"The knowledge no longer leaves when the engineer does."*

---

## 7. THE INTERACTIVE DEMO (Section 6)

This is the moment the site earns its keep. Build it well.

- Three pre-written prompts as clickable chips
- A fixed "response" area below
- On click: response types out (setInterval, ~30ms) with markdown-style formatting
- Every fact in the response is followed by a small citation chip: `[MO-P204-2024.pdf · p.12]`
- Below the response: a mini "sources used" strip showing 3–5 doc thumbnails
- A subtle "confidence: 94%" mono readout at the bottom

Pre-scripted answers should feel like a real senior engineer wrote them — specific, cautious, procedural, with numbered steps.

---

## 8. TECHNICAL SCOPE OF THIS SITE

- Pure HTML + CSS + vanilla JS, single file if possible, otherwise clean multi-file
- No frameworks unless absolutely justified — Tailwind is allowed via CDN if used with restraint
- No build step required to view
- Fonts loaded from Google Fonts (Fraunces, Inter, JetBrains Mono)
- Fully responsive: 360px → 1920px
- Passes Lighthouse: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95
- Semantic HTML5, proper landmarks, alt text on every image, prefers-reduced-motion respected

---

## 9. WHAT TO AVOID (Hard rules)

- No purple/pink gradient hero
- No AI-generated 3D imagery
- No "trusted by" logo wall with fake logos
- No dark-mode toggle (pick one mood and commit — this site is warm off-white with a dark technical section)
- No animated background particles
- No cookie banner
- No chatbot bubble in the corner
- No "Get started for free" — this is enterprise. Say "Request a Pilot."

---

## 10. DEFINITION OF DONE

The site is done when a judge, on first scroll, thinks *"this team already has a company."* If any section makes them think *"this is a hackathon project,"* that section fails and must be rewritten.
