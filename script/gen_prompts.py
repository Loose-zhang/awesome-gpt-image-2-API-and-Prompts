#!/usr/bin/env python3
"""Regenerate prompts.json for the gallery website (index.html).

Parses the 7 English category files in cases/*.md and emits prompts.json
at the repo root. Run this whenever cases/ or images/ change:

    python3 script/gen_prompts.py

Handles both case formats found in cases/*.md:
  1) ### Case N: [Title](sourceURL) (by [@handle](handleURL))  + **Prompt:** ```...```
  2) ### Case N: PlainTitle  + **Source**: [@handle](url)  + **Prompt**: ```...```
Only cases that have BOTH a local image (verified on disk) and a prompt block
are written out.
"""
import re, json, os, sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATEGORIES = {
    "portrait":    {"en": "Portrait & Photography", "zh": "人像与摄影", "emoji": "🍌"},
    "poster":      {"en": "Poster & Illustration",  "zh": "海报与插画", "emoji": "🎨"},
    "ui":          {"en": "UI & Social Media",       "zh": "UI与社媒",   "emoji": "📱"},
    "ecommerce":   {"en": "E-commerce",              "zh": "电商",       "emoji": "🛒"},
    "ad-creative": {"en": "Ad Creative",             "zh": "广告创意",   "emoji": "📣"},
    "character":   {"en": "Character Design",        "zh": "角色设计",   "emoji": "🧍"},
    "comparison":  {"en": "Comparison & Community",  "zh": "对比与社区", "emoji": "🧪"},
}

HDR    = re.compile(r'^###\s+Case\s+(\d+):\s+(.+?)\s*$', re.M)
LINKT  = re.compile(r'^\[([^\]]+)\]\(([^)]+)\)')
BYRE   = re.compile(r'\(by\s+\[([^\]]+)\]\(([^)]+)\)\)')
SRCRE  = re.compile(r'\*\*Source\*\*:\s*\[([^\]]+)\]\(([^)]+)\)')
IMG    = re.compile(r'src="[^"]*?(images/[^"]+?)"')
PROMPT = re.compile(r'\*\*Prompt:?\*\*:?\s*```[a-z]*\n(.*?)```', re.S)


def parse():
    all_cases = []
    for cat in CATEGORIES:
        path = os.path.join(REPO, "cases", f"{cat}.md")
        if not os.path.exists(path):
            print(f"  ! missing {path}", file=sys.stderr)
            continue
        txt = open(path, encoding="utf-8").read()
        matches = list(HDR.finditer(txt))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(txt)
            seg = txt[m.start():end]
            num, rawtitle = m.group(1), m.group(2).strip()
            src = author = author_url = ""
            lt = LINKT.match(rawtitle)
            title = lt.group(1).strip() if lt else rawtitle
            if lt:
                src = lt.group(2).strip()
            bm = BYRE.search(rawtitle)
            if bm:
                author, author_url = bm.group(1).lstrip("@").strip(), bm.group(2).strip()
            title = BYRE.sub("", title).strip()
            if not src:
                sm = SRCRE.search(seg)
                if sm:
                    author, author_url = sm.group(1).lstrip("@").strip(), sm.group(2).strip()
                    src = sm.group(2).strip()
            im = IMG.search(seg)
            imgpath = im.group(1) if im else None
            if imgpath and not os.path.exists(os.path.join(REPO, imgpath)):
                imgpath = None
            pm = PROMPT.search(seg)
            prompt = pm.group(1).strip() if pm else ""
            all_cases.append({
                "id": f"{cat}-{num}", "category": cat, "title": title,
                "source": src, "author": author, "authorUrl": author_url,
                "image": imgpath, "prompt": prompt,
            })
    return all_cases


def main():
    all_cases = parse()
    valid = [c for c in all_cases if c["image"] and c["prompt"]]
    out = {"categories": CATEGORIES, "cases": valid, "generated": "from cases/*.md (EN)"}
    dst = os.path.join(REPO, "prompts.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"Wrote {dst}")
    print(f"  parsed {len(all_cases)} headers -> {len(valid)} valid cases")
    print(f"  by category: {dict(Counter(c['category'] for c in valid))}")
    dropped = len(all_cases) - len(valid)
    if dropped:
        print(f"  dropped {dropped} (missing image or prompt block)")


if __name__ == "__main__":
    main()
