# LegacyLoop — The Memory Layer for Industrial India

A single-file marketing site for **LegacyLoop**, an AI industrial knowledge platform built for the ET AI Hackathon 2026. LegacyLoop captures decades of tribal engineering knowledge — from PDFs, P&IDs, maintenance logs, SOPs, and incident reports — and puts it in the pocket of every field technician through a reasoning agent that gives cited answers.

## What's here

```
.
├── index.html   # the entire site — inline CSS + JS, zero build step
└── README.md
```

That's it. `index.html` is fully self-contained (only external dependency is Google Fonts over CDN). Double-click it to open locally, or deploy it anywhere that serves static files.

## Run locally

Just open the file:

```bash
open index.html
```

Or serve it over HTTP (recommended, matches production):

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Deploy

Because the site is a single static `index.html` at the repo root, every major host works with zero configuration.

### Vercel

```bash
npx vercel --prod
```

### Netlify

```bash
npx netlify deploy --prod --dir .
```

Or drag the folder onto https://app.netlify.com/drop.

### GitHub Pages

Push this folder to a repo, then in **Settings → Pages** set the source to your default branch, root (`/`). The site publishes at `https://<user>.github.io/<repo>/`.

### Cloudflare Pages

Create a project, connect the repo, leave the build command empty and the output directory as `/`.

## Tech

Vanilla HTML + CSS + JavaScript. No framework, no bundler, no build step. Responsive from 360px to 1920px, respects `prefers-reduced-motion`, and uses IntersectionObserver + requestAnimationFrame for scroll reveals and the animated Loop line.
