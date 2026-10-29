#!/usr/bin/env python3
"""
Autonomous AI Tool Crawler, Category Segregator & Static HTML/Schema Sync Engine
for aallaitools.online
"""
import html
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CATEGORY_RULES = [
    ("coding-dev", "Coding & Dev", "💻 Software & Coding", [
        "code", "coding", "ide", "developer", "react", "fullstack", "full-stack",
        "git", "deploy", "postgres", "compiler", "terminal", "debugging", "programming"
    ]),
    ("voice-audio", "Voice & Audio", "🎙️ Voice & Audio Synthesis", [
        "voice", "audio", "speech", "tts", "music", "song", "podcast", "dubbing",
        "transcription", "cloning", "sound", "vocal"
    ]),
    ("video-3d", "Video & 3D", "🎥 Video & Motion FX", [
        "video", "3d", "avatar", "motion", "cinematic", "animation", "mesh",
        "clip", "film", "vfx", "rendering", "lip-sync"
    ]),
    ("image-art", "Image & Art", "🎨 Image & Visual Arts", [
        "image", "art", "photo", "vector", "svg", "design", "illustration",
        "background", "upscale", "canvas", "graphic", "mockup"
    ]),
    ("ai-search", "AI Search", "🔍 Research & Deep Search", [
        "search", "research", "citation", "academic", "paper", "literature",
        "answer engine", "peer-reviewed", "evidence", "notebook"
    ]),
    ("chat-reasoning", "Chat & Reasoning", "✍️ Generative Writing", [
        "chat", "reasoning", "llm", "writing", "copywriting", "grammar",
        "paraphrase", "assistant", "gpt", "workspace"
    ]),
]

PALETTE = ["#10A37F", "#D97706", "#2563EB", "#4F46E5", "#7C3AED", "#059669", "#E11D48", "#0284C7", "#0D9488", "#0F172A"]


def classify_tool(title: str, description: str) -> tuple[str, str, str]:
    text = f"{title} {description}".lower()
    for slug, pill, section, keywords in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return slug, pill, section
    return "chat-reasoning", "Chat & Reasoning", "✍️ Generative Writing"


def crawl_tool_metadata(url: str, fallback_name: str = "", pricing: str = "Freemium") -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; AllAIToolsBot/1.0; +http://aallaitools.online/robots.txt)"}
    )
    title, desc = fallback_name or url, ""
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw_html = resp.read(65536).decode("utf-8", errors="ignore")
            t_match = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.I | re.S)
            if t_match and not fallback_name:
                title = html.unescape(t_match.group(1)).strip().split("|")[0].split("—")[0].strip()
            d_match = re.search(
                r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
                raw_html, re.I | re.S
            )
            if d_match:
                desc = html.unescape(d_match.group(1)).strip()
    except Exception:
        pass

    slug, pill, section = classify_tool(title, desc)
    words = [w for w in re.split(r"\W+", title) if w]
    badge = (words[0][0] + (words[1][0] if len(words) > 1 else words[0][1:2])).upper()[:3]
    color = PALETTE[sum(ord(c) for c in title) % len(PALETTE)]
    return {
        "badge": badge,
        "color": color,
        "name": title,
        "pricing": pricing,
        "category_slug": slug,
        "category_pill": pill,
        "category_section": section,
        "description": desc[:160] if desc else f"Verified AI platform in the {pill} category.",
        "url": url,
    }


def render_card_html(tool: dict) -> str:
    search_blob = f"{tool['name']} {tool['description']} {tool['category_pill']} {tool['pricing']}".lower()
    return f"""      <article class="tool-card" data-category="{tool['category_slug']}" data-search="{html.escape(search_blob)}">
        <div class="card-top">
          <div class="tool-badge" style="background:{tool['color']}">{html.escape(tool['badge'])}</div>
          <span class="price-pill">{html.escape(tool['pricing'])}</span>
        </div>
        <h3 class="tool-name">{html.escape(tool['name'])}</h3>
        <p class="tool-desc">{html.escape(tool['description'])}</p>
        <div class="card-bottom">
          <span class="cat-pill">{html.escape(tool['category_pill'])}</span>
          <a href="{html.escape(tool['url'])}" class="visit-btn" target="_blank" rel="noopener noreferrer">Visit Tool &rarr;</a>
        </div>
      </article>"""


if __name__ == "__main__":
    print(f"[{datetime.now(timezone.utc).isoformat()}] Ready to crawl and sync aallaitools.online directory.")
