import hashlib
import json
import os
import re
from datetime import datetime, timezone

import requests
from defusedxml import ElementTree as ET

POSTS_DIR = "_posts"
STATE_FILE = "scripts/state.json"

# Change feeds as you like
FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
]

MAX_POSTS_PER_RUN = 1  # every 10 min = 1 post

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return (text[:80] if text else "news")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"seen": []}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def fetch_rss(url):
    r = requests.get(url, timeout=25)
    r.raise_for_status()
    return r.content

def parse_rss(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link") or "").strip()
        desc  = (item.findtext("description") or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "desc": desc})
    return items

def make_id(title, link):
    return hashlib.sha256((title + "|" + link).encode("utf-8")).hexdigest()

def deepseek_rewrite(title, desc, link):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        # fallback (still posts)
        return f"{desc}\n\n**Source:** [{link}]({link})"

    # OpenAI-compatible endpoint pattern used by DeepSeek
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    system = "You are a careful news editor. Write an original short news post. No plagiarism."
    user = f"""
Write an original news post based on this.
Title: {title}
Snippet: {desc}
Source link: {link}

Rules:
- 120 to 180 words
- Neutral tone, no hype
- Do NOT copy phrases verbatim
- End with 3 bullet key points
"""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=45)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()

def write_post(title, content, source_link):
    os.makedirs(POSTS_DIR, exist_ok=True)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    filename = f"{date_str}-{slugify(title)}-{now.strftime('%H%M%S')}.md"
    path = os.path.join(POSTS_DIR, filename)

    md = f"""---
layout: post
title: "{title.replace('"','\\"')}"
date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}
source: "{source_link}"
---

{content}

**Original Source:** [{source_link}]({source_link})
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)

def main():
    state = load_state()
    seen = set(state.get("seen", []))
    created = 0

    for feed in FEEDS:
        try:
            items = parse_rss(fetch_rss(feed))
        except (requests.RequestException, ET.ParseError) as e:
            print("Feed error:", feed, e)
            continue

        for it in items:
            nid = make_id(it["title"], it["link"])
            if nid in seen:
                continue

            content = deepseek_rewrite(it["title"], it["desc"], it["link"])
            write_post(it["title"], content, it["link"])

            seen.add(nid)
            created += 1
            if created >= MAX_POSTS_PER_RUN:
                break

        if created >= MAX_POSTS_PER_RUN:
            break

    state["seen"] = list(seen)[-5000:]
    save_state(state)
    print("Created:", created)

if __name__ == "__main__":
    main()
