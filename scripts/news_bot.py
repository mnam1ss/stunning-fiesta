import os
import json
import hashlib
import re
from datetime import datetime, timezone

import requests
import xml.etree.ElementTree as ET

POSTS_DIR = "_posts"
STATE_FILE = "scripts/state.json"

# RSS feeds (add/remove as you want)
FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
]

MAX_POSTS_PER_RUN = 1  # every run: create 1 new post only (safe)
MAX_DESC_CHARS = 600   # how much snippet to send to DeepSeek


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return (text[:80] if text else "news")


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"seen": []}


def save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def fetch_rss(url: str) -> bytes:
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.content


def parse_rss(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = (item.findtext("description") or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "desc": desc})
    return items


def make_id(title: str, link: str) -> str:
    return hashlib.sha256((title + "|" + link).encode("utf-8")).hexdigest()


def deepseek_rewrite(title: str, desc: str, link: str) -> str:
    """
    Rewrites a short original summary using DeepSeek.
    If DEEPSEEK_API_KEY is missing, fallback is used.
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")

    # Fallback (if you haven't set secret yet)
    if not api_key:
        cleaned = re.sub(r"<.*?>", "", desc)  # remove html tags (basic)
        cleaned = cleaned.strip()
        if not cleaned:
            cleaned = "Short update: A new story was posted. Visit the source for full details."
        return f"{cleaned}\n\n- Key point: Source-linked update\n- Key point: Short summary mode\n- Key point: More details in source"

    # DeepSeek OpenAI-compatible endpoint (common)
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Clean HTML-ish junk from RSS descriptions
    cleaned_desc = re.sub(r"<.*?>", "", desc).strip()
    cleaned_desc = cleaned_desc[:MAX_DESC_CHARS]

    system = (
        "You are a careful news editor. Write an ORIGINAL short news post. "
        "Do not plagiarize. Keep it neutral and factual."
    )

    user = f"""
Create an original short news post using the info below.

Title: {title}
Snippet: {cleaned_desc}
Source: {link}

Rules:
- 120 to 180 words
- Neutral tone (no hype, no opinion)
- Do NOT copy exact phrases from the snippet
- End with exactly 3 bullet points labeled 'Key points:'
- No copyrighted full text, only summary
"""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=45)
    resp.raise_for_status()
    data = resp.json()

    return data["choices"][0]["message"]["content"].strip()


def write_post(title: str, content: str, source_link: str) -> str:
    """
    Writes a Jekyll post in _posts/
    Returns file path.
    """
    os.makedirs(POSTS_DIR, exist_ok=True)

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    # Avoid YAML break from quotes
    safe_title = title.replace('"', "").strip()
    if not safe_title:
        safe_title = "News Update"

    filename = f"{date_str}-{slugify(title)}-{now.strftime('%H%M%S')}.md"
    path = os.path.join(POSTS_DIR, filename)

    md = f"""---
layout: post
title: "{safe_title}"
date: {now.strftime("%Y-%m-%d %H:%M:%S %z")}
source: "{source_link}"
---

{content}

**Original Source:** [{source_link}]({source_link})
"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(md)

    return path


def main():
    state = load_state()
    seen = set(state.get("seen", []))

    created = 0

    for feed in FEEDS:
        try:
            items = parse_rss(fetch_rss(feed))
        except Exception as e:
            print("Feed error:", feed, str(e))
            continue

        for it in items:
            nid = make_id(it["title"], it["link"])
            if nid in seen:
                continue

            content = deepseek_rewrite(it["title"], it["desc"], it["link"])
            p = write_post(it["title"], content, it["link"])

            print("Created post:", p)
            seen.add(nid)
            created += 1

            if created >= MAX_POSTS_PER_RUN:
                break

        if created >= MAX_POSTS_PER_RUN:
            break

    state["seen"] = list(seen)[-5000:]  # keep last N ids
    save_state(state)

    print("Total created this run:", created)


if __name__ == "__main__":
    main()
