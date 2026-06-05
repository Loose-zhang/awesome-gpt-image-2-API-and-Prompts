# Project Memory — awesome-gpt-image-2-prompts

> 项目记忆文件 / project memory for future sessions. Keep this short and current.

## What this repo is
An "Awesome"-style open-source collection of **GPT-Image-2** (OpenAI image model) prompts, API usage patterns, and example outputs. Upstream: `EvoLinkAI/awesome-gpt-image-2-API-and-Prompts`. License: **CC0 1.0** (see `LICENSE`). Maintained/curated locally by **MZ (Mingzhe Zhang)**.

## Repo structure
- `README.md` + `README_<lang>.md` — main docs in 11 languages (each ~460 KB).
- `cases/<category>.md` (+ `_<lang>` variants) — the actual prompt cases. 7 EN category files are the source of truth:
  `portrait`, `poster`, `ui`, `ecommerce`, `ad-creative`, `character`, `comparison`.
- `images/<category>_caseN/output.jpg` — one output image per case (~757 dirs).
- `data/` — `curation_report_*.json`, `ingested_tweets.json` (curation pipeline data).
- `script/`, `tmp/`, `result/` — tooling/scratch.

### Case formats inside `cases/*.md` (two coexist — handle both)
1. `### Case N: [Title](sourceURL) (by [@handle](handleURL))` then a `**Prompt:**` fenced block, image in an HTML `<img src=...>` table.
2. `### Case N: PlainTitle` then `**Source**: [@handle](url)`, `**Prompt**:` fenced block, `**Output**:` `<img src="../images/...">`.
Image `src` is normalized by stripping to `images/.../output.jpg`.

## The website (built June 2026)
Goal: a browsable bilingual prompt gallery for this repo, styled after meigen.ai's masonry gallery, with full source attribution + legal/disclaimer notices.

- **`index.html`** — single-file site (vanilla HTML/CSS/JS). Masonry (CSS columns) gallery, category filter pills, search (title/author/prompt), **中/EN** language toggle, click-to-open modal with full prompt + **copy** button + source link, infinite scroll (60/batch). Header signed "Awesome GPT Image 2 Prompts · 由 MZ 整理". Footer + yellow notice box cover attribution, CC0, takedown, and a disclaimer (内容仅供学习, 版权归原作者).
- **`prompts.json`** — generated data the site fetches. Schema: `{categories:{key:{en,zh,emoji}}, cases:[{id,category,title,source,author,authorUrl,image,prompt}]}`. **703 cases** parsed (of 706 headers; 3 dropped for missing prompt block). All 703 have image (verified on disk) + source + title.
- Regenerate `prompts.json` with the parser logic in this file's history (robust to both case formats). If `cases/*.md` change, re-run the parser.

### Deploy / run notes
- Must be served over **HTTP** (GitHub Pages, or `python3 -m http.server`). Opening `index.html` via `file://` fails because the browser blocks `fetch('prompts.json')` — the page shows a bilingual hint if so.
- For GitHub Pages: repo root already has `index.html` + `prompts.json` + `images/`, so enabling Pages on the default branch serves it directly.

## Legal / attribution stance (important)
- Every card links to the original author + source (mostly X/Twitter). Copyright stays with original creators; site claims no rights.
- Prompt text = CC0 per repo LICENSE; images shown for study/reference only, non-commercial.
- "GPT Image 2" belongs to OpenAI; layout inspiration credited to meigen.ai (design reference only, no assets copied).
- Takedown path: open an Issue on the upstream repo.

## User
Mingzhe Zhang (MZ). Prefers concise, direct answers. Bilingual (中文/EN) is fine.
