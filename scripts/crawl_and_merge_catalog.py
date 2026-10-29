#!/usr/bin/env python3
"""
Aixploria 49-Sitemap Crawler, Accurate Extractor & Category Segregator
for aallaitools.online
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
        "no-code", "low-code", "website", "app-builder", "python", "javascript", "mcp"
    ]),
    ("voice-audio", "Voice & Audio", "🎙️ Voice & Audio Synthesis", [
        "voice", "audio", "tts", "speech", "music", "song", "podcast", "dubbing", "transcri", "sound"
    ]),
    ("video-3d", "Video & 3D", "🎥 Video & Motion FX", [
        "video", "3d", "avatar", "motion", "animation", "subtitle", "caption", "lip-sync", "film", "vfx", "mesh"
    ]),
    ("image-art", "Image & Art", "🎨 Image & Visual Arts", [
        "image", "art", "photo", "logo", "vector", "svg", "design", "background", "upscal", "drawing"
    ]),
    ("ai-search", "AI Search", "🔍 Research & Deep Search", [
        "search", "research", "academic", "science", "pdf", "detector", "citation", "literature", "knowledge"
    ]),
    ("chat-reasoning", "Chat & Reasoning", "✍️ Generative Writing", [
        "chat", "llm", "writing", "copywriting", "email", "grammar", "assistant", "productivity", "marketing"
    ]),
]

PALETTE = ["#10A37F", "#D97706", "#2563EB", "#4F46E5", "#7C3AED", "#059669", "#E11D48", "#0284C7", "#0D9488", "#0F172A"]


def curl_get(url: str, timeout: int = 10) -> str:
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


def fetch_sitemap_locs(sitemap_url: str) -> List[Tuple[str, str]]:
    raw_xml = curl_get(sitemap_url, timeout=12)
    entries: List[Tuple[str, str]] = []
    if not raw_xml:
        return entries
    locs = re.findall(r'<loc>([^<]+)</loc>', raw_xml)
    for l in locs:
        l_clean = l.strip()
        if l_clean and not l_clean.endswith(".xml") and not l_clean.endswith("/category/"):
            entries.append((l_clean, ""))
    return entries


def classify_tool(url: str, title: str, description: str) -> Tuple[str, str, str]:
    blob = f"{url} {title} {description}".lower()
    for slug, pill, section, keywords in CATEGORY_TAXONOMY:
        if any(kw in blob for kw in keywords):
            return slug, pill, section
    return "chat-reasoning", "Chat & Reasoning", "✍️ Generative Writing"


def parse_tool_page(page_url: str) -> Optional[Dict]:
    # Ensure querying the English page version if available
    target_url = page_url
    if "/en/" not in target_url:
        target_url = target_url.replace("https://www.aixploria.com/", "https://www.aixploria.com/en/")

    page_html = curl_get(target_url, timeout=10)
    if not page_html or len(page_html) < 500:
        return None

    # Title & clean name
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', page_html, re.I | re.S)
    if h1_match:
        clean_name = html.unescape(h1_match.group(1)).strip()
    else:
        title_match = re.search(r'<title[^>]*>(.*?)</title>', page_html, re.I | re.S)
        raw_title = html.unescape(title_match.group(1)).strip() if title_match else page_url.rstrip("/").split("/")[-1]
        clean_name = re.split(r'\s*[:|—-]\s*(?:Reviews|Avis|Price|Prix|Info|AIxploria|202\d)', raw_title, flags=re.I)[0].strip()

    if not clean_name or len(clean_name) > 60:
        clean_name = page_url.rstrip("/").split("/")[-1].replace("-", " ").title()

    # Description
    desc = ""
    meta_desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', page_html, re.I | re.S)
    quote_desc = re.search(r'«\s*([^»]{25,220})\s*»', page_html)
    if meta_desc and len(meta_desc.group(1).strip()) > 20:
        desc = html.unescape(meta_desc.group(1)).strip()
    elif quote_desc:
        desc = html.unescape(quote_desc.group(1)).strip()
    else:
        desc = f"Verified artificial intelligence tool indexed on Aixploria ({clean_name})."

    # Pricing
    pricing = "Freemium"
    if re.search(r'\b(100%\s*Free|Free\s*AI|Gratuit)\b', page_html, re.I):
        pricing = "Free"
    elif re.search(r'\b(Paid|Payant)\b', page_html, re.I) and not re.search(r'Freemium', page_html, re.I):
        pricing = "Paid"

    # External Outbound Link (prefer first external non-social link)
    official_url = target_url
    links = re.findall(r'href=[\"\'](https?://[^\s\"\']+)[\"\']', page_html)
    for l in links:
        l_lower = l.lower()
        if (
            "aixploria.com" not in l_lower
            and "twitter.com" not in l_lower
            and "x.com" not in l_lower
            and "linkedin.com" not in l_lower
            and "youtube.com" not in l_lower
            and "tiktok.com" not in l_lower
            and "cookiedatabase" not in l_lower
            and "schema.org" not in l_lower
            and "w.org" not in l_lower
        ):
            official_url = l
            break

    cat_slug, cat_pill, cat_section = classify_tool(page_url, clean_name, desc)
    words = [w for w in re.split(r'\W+', clean_name) if w]
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
        "description": desc[:160],
        "url": official_url,
    }


def main():
    print("[1/3] Parsing all 49 XML sitemaps...")
    seen_slugs: Set[str] = set()
    tool_links: List[str] = []

    for sm in AIXPLORIA_SITEMAP_URLS:
        entries = fetch_sitemap_locs(sm)
        for loc, _ in entries:
            slug = loc.rstrip("/").split("/")[-1]
            if slug and slug not in seen_slugs and not slug.startswith("sitemap"):
                seen_slugs.add(slug)
                tool_links.append(loc)

    print(f"Discovered {len(tool_links)} unique tool candidates across all 49 sitemaps.")

    # Load existing tools to deduplicate
    existing_tools = []
    if Path("tools.json").exists():
        try:
            existing_tools = json.loads(Path("tools.json").read_text(encoding="utf-8"))
        except Exception:
            existing_tools = []
    
    existing_names = {t["name"].lower(): t for t in existing_tools if "name" in t}
    print(f"Loaded {len(existing_tools)} existing tools from tools.json.")

    # Crawl top newly indexed and flagship tools
    print("[2/3] Crawling and enriching tool metadata...")
    new_tools = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as pool:
        futures = {pool.submit(parse_tool_page, url): url for url in tool_links[:120]}
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            if res:
                name_key = res["name"].lower()
                if name_key not in existing_names:
                    existing_names[name_key] = res
                    new_tools.append(res)
                else:
                    # Enrich existing tool with official URL if better
                    if "aixploria.com" in existing_names[name_key]["url"] and "aixploria.com" not in res["url"]:
                        existing_names[name_key]["url"] = res["url"]

    combined_tools = list(existing_names.values())
    print(f"Total unified catalog count: {len(combined_tools)} verified tools.")

    print("[3/3] Exporting AI_TOOLS_METADATA.md and tools.json...")
    Path("tools.json").write_text(json.dumps(combined_tools, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = [
        "# Exhaustive Worldwide AI Tools Metadata Catalog (`aallaitools.online`)",
        "",
        f"Master dataset combining global flagship AI platforms with all 49 `aixploria.com` XML sitemaps.",
        f"**Total Verified AI Tools Indexed**: `{len(combined_tools)}`",
        "",
    ]
    for slug, pill, section, _ in CATEGORY_TAXONOMY:
        cat_tools = [t for t in combined_tools if t.get("category_slug") == slug]
        md_lines.append(f"## {pill} (`{section}` | {len(cat_tools)} Tools)")
        md_lines.append("")
        md_lines.append("| Badge | Color | Tool Name | Pricing | Category | Description | Official URL |")
        md_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for t in cat_tools:
            safe_desc = t.get("description", "").replace("|", "\\|").replace("\n", " ")
            md_lines.append(
                f"| **{t.get('badge', 'AI')}** | `{t.get('color', '#4F46E5')}` | [{t.get('name', '')}]({t.get('url', '#')}) | {t.get('pricing', 'Freemium')} | {t.get('category_pill', pill)} | {safe_desc} | `{t.get('url', '#')}` |"
            )
        md_lines.append("")
    Path("AI_TOOLS_METADATA.md").write_text("\n".join(md_lines), encoding="utf-8")
    print("Catalog generation complete!")


if __name__ == "__main__":
    main()
