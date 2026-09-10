# georgia-sa-portfolio

Source for [georgia-sa-portfolio.vercel.app](https://georgia-sa-portfolio.vercel.app), a technical build log:
21 things I built, each with the problem, the decisions, and in most cases a prototype you can run in the page.

**Run it:** open `index.html`. No build step, no dependencies, no bundler.
**What it proves:** the page reads two ways. A "Plain English / Technical" switch rewrites every
description in place, because the job is translating between those two audiences.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | The whole site. One self-contained file: inline CSS, inline JS, 18 interactive prototypes. |
| `api/translate.js` | Vercel serverless function. Six task-specific prompts behind one endpoint, so the "Run live with Claude" buttons call a real model. The key is an environment variable and never reaches the client. |
| `src/` | The generator. `build.py` assembles `index.html` from the extracted content model plus the design system, so copy and layout stay separable. |

## The live buttons

Most prototypes compute their answer in the browser: the distance validator runs the real Haversine
formula, the record cleaner really parses the rows you type. Six of them can also call Claude for real,
capped at one call per demo per session. If the call fails the page silently falls back to the instant
version, so a cold API never shows a visitor an error.

## Rebuilding

```bash
cd src && python3 build.py     # writes ../index.html
```

Content lives in `src/content.json` (technical copy, extracted from the previous version) and
`src/plain.json` (the plain-English layer). Design tokens are in `src/style.css`.

## Deploying

Pushes to `main` deploy to Vercel automatically. `ANTHROPIC_API_KEY` must be set as a project
environment variable for the live buttons to work; without it they fall back to the instant version.

MIT licensed. Content and case studies are mine.
