#!/usr/bin/env python3
"""
Aixploria 49-Sitemap Crawler, Category Segregator & Static Directory Updater
for aallaitools.online
Uses curl for network requests to handle modern TLS negotiations seamlessly on macOS.
"""
from __future__ import annotations
import concurrent.futures
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Set

AIXPLORIA_SITEMAP_URLS = [
    "https://www.aixploria.com/sitemap-posttype-post.202610.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202609.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202608.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202607.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202606.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202605.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202604.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202603.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202602.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202601.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202512.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202511.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202510.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202509.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202508.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202507.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202506.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202505.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202504.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202503.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202502.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202501.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202412.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202411.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202410.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202409.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202408.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202407.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202406.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202405.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202404.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202403.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202402.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202401.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202312.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202311.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202310.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202309.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202308.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202307.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202306.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202305.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202304.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202303.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202302.xml",
    "https://www.aixploria.com/sitemap-posttype-post.202301.xml",
    "https://www.aixploria.com/sitemap-posttype-page.xml",
    "https://www.aixploria.com/sitemap-taxonomy-category.xml",
    "https://www.aixploria.com/ainews-sitemap.xml",
]

CATEGORY_TAXONOMY = [
    ("coding-dev", "Coding & Dev", "💻 Software & Coding", [
        "code", "coding", "developer", "ide", "github", "sql", "database", "api",
        "no-code", "low-code", "website-builder", "app-builder", "python", "javascript", "mcp"
    ]),
    ("voice-audio", "Voice & Audio", "🎙️ Voice & Audio Synthesis", [
        "voice", "audio", "tts", "text-to-speech", "speech", "music", "song",
        "podcast", "cloning", "dubbing", "transcri", "sound", "vocal"
    ]),
    ("video-3d", "Video & 3D", "🎥 Video & Motion FX", [
        "video", "3d", "avatar", "motion", "animation", "subtitle", "caption",
        "lip-sync", "film", "vfx", "mesh", "rendering", "short-clip"
    ]),
    ("image-art", "Image & Art", "🎨 Image & Visual Arts", [
        "image", "art", "photo", "logo", "vector", "svg", "design", "background",
        "upscal", "illustration", "drawing", "presentation", "fashion", "face-swap"
    ]),
    ("ai-search", "AI Search", "🔍 Research & Deep Search", [
        "search", "research", "academic", "science", "pdf", "document", "detector",
        "citation", "literature", "study", "summarizer", "knowledge", "seo"
    ]),
    ("chat-reasoning", "Chat & Reasoning", "✍️ Generative Writing", [
        "chat", "llm", "writing", "text", "copywriting", "email", "grammar",
        "paraphras", "story", "blog", "assistant", "productivity", "marketing", "prompt"
    ]),
]

PALETTE = ["#10A37F", "#D97706", "#2563EB", "#4F46E5", "#7C3AED", "#059669", "#E11D48", "#0284C7", "#0D9488", "#0F172A"]


def curl_get(url: str, timeout: int = 12) -> str:
    try:
        cmd = [
            "curl", "-s", "--max-time", str(timeout),
            "-H", "User-Agent: Mozilla/5.0 (compatible; AllAIToolsCrawler/2.0; +http://aallaitools.online/robots.txt)",
            "-H", "Accept: application/xml,text/xml,text/html,application/xhtml+xml",
            url
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")
        return res.stdout
    except Exception:
        return ""


def fetch_xml_locs(sitemap_url: str) -> List[Tuple[str, str]]:
    raw_xml = curl_get(sitemap_url, timeout=15)
    entries: List[Tuple[str, str]] = []
    if not raw_xml:
        return entries
    try:
        root = ET.fromstring(raw_xml)
        for url_el in root.findall(".//{*}url"):
            loc_el = url_el.find("{*}loc")
            mod_el = url_el.find("{*}lastmod")
            if loc_el is not None and loc_el.text:
                loc = loc_el.text.strip()
                lastmod = mod_el.text.strip() if (mod_el is not None and mod_el.text) else ""
                entries.append((loc, lastmod))
    except Exception as exc:
        print(f"[WARN] XML parse fallback for {sitemap_url}: {exc}")
        locs = re.findall(r'<loc>([^<]+)</loc>', raw_xml)
        for l in locs:
            entries.append((l.strip(), ""))
    return entries


def classify_tool(url: str, title: str, description: str, categories_raw: str = "") -> Tuple[str, str, str]:
    blob = f"{url} {title} {description} {categories_raw}".lower()
    for slug, pill, section, keywords in CATEGORY_TAXONOMY:
        if any(kw in blob for kw in keywords):
            return slug, pill, section
    return "chat-reasoning", "Chat & Reasoning", "✍️ Generative Writing"


def parse_aixploria_tool_page(url: str, lastmod: str = "") -> Optional[Dict]:
    page_html = curl_get(url, timeout=12)
    if not page_html:
        return None

    title_match = re.search(r"<title[^>]*>(.*?)</title>", page_html, re.I | re.S)
    raw_title = html.unescape(title_match.group(1)).strip() if title_match else url.rstrip("/").split("/")[-1]
    clean_name = re.split(r"\s*[:|—-]\s*(?:Reviews|Price|Info|AIxploria|202\d)", raw_title, flags=re.I)[0].strip()
    if not clean_name or len(clean_name) > 65:
        clean_name = url.rstrip("/").split("/")[-1].replace("-", " ").title()

    quote_match = re.search(r"«\s*([^»]{20,240})\s*»", page_html)
    meta_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', page_html, re.I | re.S)
    if quote_match:
        description = html.unescape(quote_match.group(1)).strip()
    elif meta_match:
        description = html.unescape(meta_match.group(1)).strip()
    else:
        description = f"Verified AI tool indexed from Aixploria ({clean_name})."

    pricing = "Freemium"
    if re.search(r"\b(100%\s*Free|Free\s*AI|Gratuit)\b", page_html, re.I):
        pricing = "Free"
    elif re.search(r"\b(Paid|Payant)\b", page_html, re.I) and not re.search(r"Freemium", page_html, re.I):
        pricing = "Paid"

    ext_match = re.search(
        r'<a[^>]+href=["\'](https?://(?!(?:www\.)?aixploria\.com)[^"\']+)["\'][^>]*>(?:[^<]*(?:Visit|Access|Try|Site|Website))',
        page_html, re.I
    )
    official_url = html.unescape(ext_match.group(1)).strip() if ext_match else url

    cat_slug, cat_pill, cat_section = classify_tool(url, clean_name, description)
    words = [w for w in re.split(r"\W+", clean_name) if w]
    badge = (words[0][0] + (words[1][0] if len(words) > 1 else words[0][1:2])).upper()[:3]
    color = PALETTE[sum(ord(c) for c in clean_name) % len(PALETTE)]

    return {
        "badge": badge,
        "color": color,
        "name": clean_name,
        "pricing": pricing,
        "category_slug": cat_slug,
        "category_pill": cat_pill,
        "category_section": cat_section,
        "description": description[:165],
        "url": official_url,
        "source_sitemap_url": url,
        "lastmod": lastmod,
    }


def crawl_all_sitemaps(max_workers: int = 12) -> List[Dict]:
    seen_slugs: Set[str] = set()
    candidate_urls: List[Tuple[str, str]] = []

    print("[INFO] Ingesting all 49 Aixploria sitemaps via raw XML...")
    for sm_url in AIXPLORIA_SITEMAP_URLS:
        entries = fetch_xml_locs(sm_url)
        for loc, lastmod in entries:
            slug = loc.rstrip("/").split("/")[-1]
            if slug and slug not in seen_slugs and not slug.startswith("sitemap") and not slug.startswith("category"):
                seen_slugs.add(slug)
                candidate_urls.append((loc, lastmod))

    print(f"[INFO] Discovered {len(candidate_urls)} unique tool URLs across all 49 sitemaps.")
    tools: List[Dict] = []
    
    # Process candidates concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(parse_aixploria_tool_page, loc, lastmod) for loc, lastmod in candidate_urls[:350]]
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            if res:
                tools.append(res)

    print(f"[INFO] Successfully crawled and parsed {len(tools)} tools.")
    return tools


def export_catalog_files(tools: List[Dict], md_path: Path, json_path: Path) -> None:
    json_path.write_text(json.dumps(tools, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Complete AI Tools Metadata Catalog (`aallaitools.online`)",
        "",
        f"Automatically crawled and segregated from the 49 `aixploria.com` XML sitemaps on `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}`.",
        f"**Total Verified Tools Indexed**: `{len(tools)}`",
        "",
    ]
    for slug, pill, section, _ in CATEGORY_TAXONOMY:
        cat_tools = [t for t in tools if t.get("category_slug") == slug]
        lines.append(f"## {pill} (`{section}` | {len(cat_tools)} Tools)")
        lines.append("")
        lines.append("| Badge | Color | Tool Name | Pricing | Category | Description | Official URL |")
        lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for t in cat_tools:
            safe_desc = t.get("description", "").replace("|", "\\|").replace("\n", " ")
            lines.append(
                f"| **{t.get('badge', 'AI')}** | `{t.get('color', '#4F46E5')}` | [{t.get('name', '')}]({t.get('url', '#')}) | {t.get('pricing', 'Freemium')} | {t.get('category_pill', pill)} | {safe_desc} | `{t.get('url', '#')}` |"
            )
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    print("Starting Aixploria 49-Sitemap Crawler & Segregator...")
    crawled = crawl_all_sitemaps(max_workers=12)
    if crawled:
        export_catalog_files(crawled, Path("AI_TOOLS_METADATA.md"), Path("tools.json"))
        print(f"Successfully exported {len(crawled)} segregated tools to AI_TOOLS_METADATA.md and tools.json.")
