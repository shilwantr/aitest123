#!/usr/bin/env python3
"""
Master Page & Sitemap Generator for All AI Tools (https://www.allaitools.online/)
- Generates dedicated static SEO pages for every AI tool in /<slug>/index.html and /<slug>.html
- Generates homepage index.html with card navigation to /<slug>/ and direct Open Tool button
- Generates 404.html
- Generates robots.txt explicitly allowing all bots & AI agents
- Generates canonical sitemap.xml with all tool URLs
- Generates vercel.json with clean routing and caching headers
"""

import os
import json
import html
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse, quote_plus
from datetime import datetime

BASE_URL = "https://www.allaitools.online"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

print(f"Starting master generation for {BASE_URL} ({TODAY})...")

# 1. Load tools
with open("tools.json", "r", encoding="utf-8") as f:
    raw_tools = json.load(f)

print(f"Loaded {len(raw_tools)} raw tools from tools.json")

def clean_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text).strip('-')
    return text

def get_base_slug(t):
    src = t.get('source_url', '')
    if '/tool/' in src:
        slug = src.split('/tool/')[-1].strip('/').split('?')[0].lower()
        slug = clean_slug(slug)
        if slug:
            return slug
    name = t.get('name', '')
    if name.lower().startswith('chatgpt'):
        return 'chatgpt'
    slug = clean_slug(name)
    return slug or 'ai-tool'

# Deduplicate
by_slug = {}
for t in raw_tools:
    slug = get_base_slug(t)
    if slug not in by_slug:
        by_slug[slug] = t
    else:
        existing = by_slug[slug]
        # Merge best fields
        if len(t.get('name', '')) < len(existing.get('name', '')) and ':' in existing.get('name', ''):
            existing['name'] = t['name']
        if 'aitoolsdirectory.com' in existing.get('url', '') and 'aitoolsdirectory.com' not in t.get('url', ''):
            existing['url'] = t['url']
        if t.get('image_url') and not existing.get('image_url'):
            existing['image_url'] = t['image_url']
        if len(t.get('description', '')) > len(existing.get('description', '')):
            existing['description'] = t['description']

deduped = list(by_slug.values())

# Assign final unique slug and path
seen_slugs = set()
tools = []
for t in deduped:
    s = get_base_slug(t)
    final_slug = s
    counter = 1
    while final_slug in seen_slugs:
        counter += 1
        final_slug = f"{s}-{counter}"
    seen_slugs.add(final_slug)
    t['slug'] = final_slug
    t['path'] = f"/{final_slug}/"
    tools.append(t)

print(f"Processed {len(tools)} deduplicated tools with unique slugs.")

# Save updated tools.json
with open("tools.json", "w", encoding="utf-8") as f:
    json.dump(tools, f, indent=2, ensure_ascii=False)
print("Updated tools.json with clean slugs and paths.")

total_tools = len(tools)
cat_counts = {}
for t in tools:
    c = t.get("category_slug", "chat-reasoning")
    cat_counts[c] = cat_counts.get(c, 0) + 1

def get_domain(url):
    try:
        netloc = urlparse(url).netloc
        return netloc.replace('www.', '') if netloc else 'official website'
    except Exception:
        return 'official website'

# 2. Build Homepage Cards HTML
cards_html = []
for t in tools:
    subcat = t.get('subcategory') or t.get('category_section') or t.get('category_pill') or 'AI Tool'
    desc = t.get('description', '')
    name = t.get('name', 'AI Platform')
    pricing = t.get('pricing', 'Freemium')
    pill = t.get('category_pill', 'AI Tools')
    cat_slug = t.get('category_slug', 'chat-reasoning')
    color = t.get('color', '#4F46E5')
    badge = t.get('badge', name[:2].upper())
    url = t.get('url', '#')
    img_url = t.get('image_url', '')
    slug = t.get('slug', 'tool')
    path = t.get('path', f"/{slug}/")

    price_class = "price-freemium"
    if pricing.lower() == "free":
        price_class = "price-free"
    elif pricing.lower() == "paid":
        price_class = "price-paid"

    img_tag = ""
    if img_url:
        img_tag = f'<img src="{html.escape(img_url)}" alt="{html.escape(name)} preview" class="tool-preview-thumb" loading="lazy" onerror="this.style.display=\'none\'" />'

    card = f'''        <article class="tool-card" data-category="{html.escape(cat_slug)}" data-pricing="{html.escape(pricing.lower())}" data-name="{html.escape(name.lower())}" data-desc="{html.escape(desc.lower())}" data-tool-path="{html.escape(path)}" onclick="if(!event.target.closest('a') && !event.target.closest('button')) window.location.href='{html.escape(path)}'">
          <div class="card-top">
            <div class="tool-brand">
              <div class="tool-avatar" style="background: {color};">{html.escape(badge)}</div>
              <div>
                <span class="tool-subcat">{html.escape(subcat)}</span>
                <h3 class="tool-name"><a href="{html.escape(path)}" class="tool-card-title-link">{html.escape(name)}</a></h3>
              </div>
            </div>
            <div class="badge-row">
              <span class="price-badge {price_class}">{html.escape(pricing)}</span>
              <button class="bookmark-btn" title="Bookmark tool" data-tool="{html.escape(name)}" aria-label="Bookmark {html.escape(name)}" onclick="event.stopPropagation()">&#9734;</button>
            </div>
          </div>
          {img_tag}
          <p class="tool-desc">{html.escape(desc)}</p>
          <div class="card-bottom">
            <span class="cat-pill">{html.escape(pill)}</span>
            <div class="card-actions">
              <a href="{html.escape(path)}" class="details-link">Details &rarr;</a>
              <a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer nofollow" class="tool-link" onclick="event.stopPropagation()">Open Tool &rarr;</a>
            </div>
          </div>
        </article>'''
    cards_html.append(card)

cards_block = "\n".join(cards_html)

# Build Homepage Schema Items (Top 250)
schema_items = []
for idx, t in enumerate(tools[:250], start=1):
    schema_items.append({
        "@type": "ListItem",
        "position": idx,
        "name": t.get("name", "AI Tool"),
        "url": f"{BASE_URL}{t.get('path', '/')}"
    })

schema_json = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "@id": f"{BASE_URL}/#website",
            "url": f"{BASE_URL}/",
            "name": "All AI Tools Directory & Best AI Tools List (2026)",
            "description": f"The definitive, fast, and comprehensive directory of {total_tools}+ worldwide artificial intelligence tools, models, and agents. Find all AI tools list for writing, coding, images, voice, video, and search."
        },
        {
            "@type": "ItemList",
            "@id": f"{BASE_URL}/#featured",
            "name": f"All AI Tools List & Complete Global AI Directory ({total_tools}+ Tools)",
            "numberOfItems": total_tools,
            "itemListElement": schema_items
        }
    ]
}, indent=2)

# 3. Generate index.html
index_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>All AI Tools Directory (2026) | Complete All AI Tools List &amp; {total_tools}+ Top Software</title>
  <meta name="description" content="Explore the ultimate all AI tools list and global AI directory. Discover, search, and benchmark {total_tools}+ worldwide AI software, models, and autonomous agents across Chat, Coding, Image, Voice, Video, and Search." />
  <meta name="keywords" content="all ai tools, all ai tools list, ai tools directory, best ai tools 2026, free ai tools list, top ai tools, ai software list, complete ai directory, generative ai tools, artificial intelligence tools directory, aixploria alternative, aitoolsdirectory" />
  <meta name="author" content="All AI Tools" />
  <link rel="canonical" href="{BASE_URL}/" />

  <!-- OpenGraph -->
  <meta property="og:title" content="All AI Tools Directory &amp; All AI Tools List | {total_tools}+ Worldwide Platforms" />
  <meta property="og:description" content="Discover the complete all AI tools list with {total_tools}+ artificial intelligence software, models, and apps across 6 core categories. Filter by Free, Freemium, and Paid." />
  <meta property="og:url" content="{BASE_URL}/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="All AI Tools" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="All AI Tools Directory | Exhaustive All AI Tools List ({total_tools}+ Tools)" />
  <meta name="twitter:description" content="Browse the ultimate all AI tools directory and complete AI software list with lightning-fast instant search." />

  <!-- Favicon SVG -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2222%22 fill=%22%234F46E5%22/><text y=%2268%22 x=%2250%22 font-family=%22system-ui,sans-serif%22 font-weight=%22800%22 font-size=%2254%22 fill=%22white%22 text-anchor=%22middle%22>AI</text></svg>" />

  <!-- Structured Data JSON-LD -->
  <script type="application/ld+json">
{schema_json}
  </script>

  <style>
    :root {{
      --bg: #090d16;
      --bg-card: #0f1626;
      --bg-card-hover: #151f36;
      --bg-elevated: #1a253f;
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(99, 102, 241, 0.4);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --accent: #6366f1;
      --accent-glow: rgba(99, 102, 241, 0.25);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-pill: 9999px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text-main); line-height: 1.5; }}
    body {{ min-height: 100vh; overflow-x: hidden; }}
    a {{ text-decoration: none; color: inherit; }}

    /* Ambient Background Mesh */
    .ambient-glow {{
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 1000px;
      height: 520px;
      background: radial-gradient(circle 500px at 50% 120px, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.08), transparent 70%);
      pointer-events: none;
      z-index: 0;
    }}

    .container {{ max-width: 1280px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }}

    /* Header / Navbar */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(9, 13, 22, 0.82);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      height: 72px;
      display: flex;
      align-items: center;
    }}
    .nav-inner {{ display: flex; align-items: center; justify-content: space-between; width: 100%; }}
    .brand {{ display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 1.18rem; letter-spacing: -0.02em; color: #fff; }}
    .brand-icon {{
      width: 38px;
      height: 38px;
      border-radius: 11px;
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      color: #fff;
      font-size: 1.1rem;
      box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
    }}
    .live-badge {{
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: var(--radius-pill);
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .nav-links {{ display: flex; align-items: center; gap: 26px; font-size: 0.92rem; font-weight: 500; color: var(--text-muted); }}
    .nav-links a:hover {{ color: #ffffff; }}
    .nav-actions {{ display: flex; align-items: center; gap: 12px; }}
    .btn-saved {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: #fbbf24;
      padding: 8px 14px;
      border-radius: 10px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .btn-saved:hover {{ background: rgba(255, 255, 255, 0.12); border-color: rgba(255, 255, 255, 0.2); }}
    .btn-submit {{
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: #fff !important;
      padding: 9px 18px;
      border-radius: 10px;
      font-weight: 600;
      font-size: 0.88rem;
      box-shadow: 0 2px 12px rgba(99, 102, 241, 0.35);
      transition: transform 0.15s ease, opacity 0.15s ease;
    }}
    .btn-submit:hover {{ transform: translateY(-1px); opacity: 0.95; }}

    /* Hero Section */
    .hero {{ text-align: center; padding: 72px 0 46px; position: relative; }}
    .hero-eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #a5b4fc;
      font-size: 0.82rem;
      font-weight: 600;
      padding: 6px 18px;
      border-radius: var(--radius-pill);
      margin-bottom: 24px;
      letter-spacing: 0.02em;
    }}
    .hero h1 {{
      font-size: clamp(2.3rem, 5.2vw, 3.8rem);
      font-weight: 900;
      letter-spacing: -0.04em;
      line-height: 1.12;
      margin-bottom: 18px;
      color: #ffffff;
    }}
    .hero h1 .gradient-text {{
      background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .hero-sub {{
      max-width: 780px;
      margin: 0 auto 34px;
      color: var(--text-muted);
      font-size: 1.12rem;
      line-height: 1.6;
    }}

    /* Global Search Bar */
    .search-box-wrap {{
      max-width: 720px;
      margin: 0 auto 24px;
      position: relative;
      display: flex;
      align-items: center;
    }}
    .search-icon {{
      position: absolute;
      left: 20px;
      font-size: 1.25rem;
      color: var(--text-sub);
      pointer-events: none;
    }}
    .search-box {{
      width: 100%;
      padding: 18px 48px 18px 56px;
      background: rgba(15, 22, 38, 0.95);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: var(--radius-md);
      color: #ffffff;
      font-size: 1.05rem;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(99, 102, 241, 0.15);
      transition: all 0.2s ease;
      outline: none;
    }}
    .search-box:focus {{
      border-color: #6366f1;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5), 0 0 0 3px rgba(99, 102, 241, 0.35);
      background: #111a30;
    }}
    .search-box::placeholder {{ color: #64748b; }}
    .search-hint {{
      position: absolute;
      right: 18px;
      font-size: 0.76rem;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      color: var(--text-sub);
      padding: 4px 8px;
      border-radius: 6px;
      font-family: ui-monospace, monospace;
      pointer-events: none;
    }}
    .clear-search {{
      position: absolute;
      right: 56px;
      background: none;
      border: none;
      color: var(--text-sub);
      font-size: 1.2rem;
      cursor: pointer;
      display: none;
      padding: 4px;
    }}
    .clear-search:hover {{ color: #ffffff; }}

    /* Pricing Filter Row */
    .filter-pricing-row {{
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}
    .price-chip {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .price-chip:hover {{ color: #fff; background: rgba(255, 255, 255, 0.08); }}
    .price-chip.active {{
      background: rgba(99, 102, 241, 0.18);
      border-color: rgba(99, 102, 241, 0.5);
      color: #c7d2fe;
    }}

    /* Category Filter Pills */
    .filter-pills-row {{
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 34px;
    }}
    .filter-pill {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 10px 18px;
      border-radius: var(--radius-pill);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}
    .filter-pill:hover {{
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-1px);
    }}
    .filter-pill.active {{
      background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
      border-color: transparent;
      color: #ffffff;
      box-shadow: 0 4px 16px rgba(79, 70, 229, 0.35);
    }}
    .pill-count {{
      background: rgba(0, 0, 0, 0.35);
      padding: 2px 7px;
      border-radius: 10px;
      font-size: 0.74rem;
      font-weight: 700;
    }}

    /* Trust / Speed Stats Bar */
    .trust-bar {{
      display: flex;
      justify-content: center;
      gap: 36px;
      color: var(--text-sub);
      font-size: 0.86rem;
      flex-wrap: wrap;
      border-top: 1px solid var(--border);
      padding-top: 24px;
      max-width: 900px;
      margin: 0 auto;
    }}
    .trust-bar strong {{ color: #cbd5e1; }}

    /* Section Styling */
    .section {{ padding: 60px 0 80px; }}
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 36px;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .section-title {{ font-size: 1.85rem; font-weight: 800; letter-spacing: -0.02em; color: #fff; }}
    .section-sub {{ color: var(--text-muted); font-size: 0.96rem; margin-top: 4px; }}
    .results-badge {{
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #a5b4fc;
      padding: 6px 14px;
      border-radius: var(--radius-pill);
      font-size: 0.82rem;
      font-weight: 700;
    }}

    /* Tools Grid */
    .tools-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 22px;
    }}

    /* Tool Card */
    .tool-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 22px;
      display: flex;
      flex-direction: column;
      position: relative;
      cursor: pointer;
      transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .tool-card:hover {{
      transform: translateY(-3px);
      border-color: rgba(99, 102, 241, 0.4);
      background: var(--bg-card-hover);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45), 0 0 20px rgba(99, 102, 241, 0.15);
    }}
    .card-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 14px;
      gap: 12px;
    }}
    .tool-brand {{ display: flex; align-items: center; gap: 14px; }}
    .tool-avatar {{
      width: 44px;
      height: 44px;
      border-radius: 12px;
      color: #ffffff;
      font-weight: 800;
      font-size: 1.05rem;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
      flex-shrink: 0;
    }}
    .tool-preview-thumb {{
      width: 100%;
      height: 140px;
      object-fit: cover;
      border-radius: var(--radius-sm);
      margin-bottom: 14px;
      border: 1px solid var(--border);
      background: rgba(0,0,0,0.2);
    }}
    .badge-row {{ display: flex; align-items: center; gap: 8px; }}
    .price-badge {{
      font-size: 0.74rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: var(--radius-pill);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .price-freemium {{ background: rgba(99, 102, 241, 0.15); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.3); }}
    .price-free {{ background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .price-paid {{ background: rgba(244, 63, 94, 0.15); color: #fda4af; border: 1px solid rgba(244, 63, 94, 0.3); }}
    .bookmark-btn {{
      background: none;
      border: none;
      color: var(--text-sub);
      font-size: 1.25rem;
      cursor: pointer;
      line-height: 1;
      padding: 2px 4px;
      border-radius: 6px;
      transition: color 0.15s;
    }}
    .bookmark-btn:hover, .bookmark-btn.saved {{ color: #fbbf24; }}
    .tool-subcat {{
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #818cf8;
      margin-bottom: 6px;
      display: inline-block;
    }}
    .tool-name {{ font-size: 1.16rem; font-weight: 700; margin-bottom: 8px; color: #ffffff; letter-spacing: -0.01em; }}
    .tool-card-title-link {{ color: inherit; text-decoration: none; }}
    .tool-card-title-link:hover {{ color: #818cf8; }}
    .tool-desc {{
      font-size: 0.9rem;
      color: var(--text-muted);
      line-height: 1.55;
      margin-bottom: 22px;
      flex-grow: 1;
    }}
    .card-bottom {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
    }}
    .card-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .details-link {{
      font-size: 0.82rem;
      color: var(--text-sub);
      font-weight: 600;
      transition: color 0.15s;
    }}
    .details-link:hover {{ color: #fff; }}
    .cat-pill {{
      font-size: 0.76rem;
      font-weight: 600;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.04);
      padding: 4px 10px;
      border-radius: 8px;
    }}
    .tool-link {{
      font-size: 0.86rem;
      font-weight: 600;
      color: #818cf8;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: color 0.15s;
    }}
    .tool-link:hover {{ color: #c084fc; text-decoration: underline; }}

    /* Empty state */
    .empty-state {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      background: var(--bg-card);
      border: 1px dashed var(--border);
      border-radius: var(--radius-lg);
      display: none;
    }}
    .empty-state h3 {{ font-size: 1.3rem; color: #fff; margin-bottom: 8px; }}
    .empty-state p {{ color: var(--text-muted); margin-bottom: 20px; }}

    /* Domain Showcase Cards */
    .cat-showcase-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
      margin-top: 16px;
    }}
    .cat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 26px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .cat-card:hover {{
      border-color: rgba(99, 102, 241, 0.4);
      transform: translateY(-2px);
      background: var(--bg-card-hover);
    }}
    .cat-card h3 {{ font-size: 1.18rem; font-weight: 700; color: #fff; margin-bottom: 8px; }}
    .cat-card p {{ font-size: 0.9rem; color: var(--text-muted); line-height: 1.5; }}
    .cat-card-meta {{
      margin-top: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
      font-weight: 600;
      color: #818cf8;
    }}

    /* FAQ Section */
    .faq-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
      max-width: 900px;
      margin: 0 auto;
    }}
    .faq-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      overflow: hidden;
    }}
    .faq-q {{
      padding: 20px 24px;
      font-weight: 700;
      font-size: 1.05rem;
      color: #ffffff;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      user-select: none;
    }}
    .faq-q:hover {{ background: rgba(255, 255, 255, 0.02); }}
    .faq-icon {{ font-size: 1.3rem; transition: transform 0.2s ease; color: #818cf8; }}
    .faq-card.open .faq-icon {{ transform: rotate(45deg); }}
    .faq-a {{
      padding: 0 24px 22px;
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.6;
      display: none;
    }}
    .faq-card.open .faq-a {{ display: block; }}

    /* Footer */
    .footer {{
      border-top: 1px solid var(--border);
      padding: 60px 0 40px;
      background: rgba(9, 13, 22, 0.95);
      color: var(--text-sub);
      font-size: 0.9rem;
    }}
    .footer-inner {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 24px;
      margin-bottom: 30px;
    }}
    .footer-links {{ display: flex; gap: 20px; flex-wrap: wrap; }}
    .footer-links a:hover {{ color: #ffffff; }}
  </style>
</head>
<body>
  <div class="ambient-glow"></div>

  <!-- Navbar -->
  <nav class="navbar">
    <div class="container nav-inner">
      <a href="/" class="brand">
        <span class="brand-icon">AI</span>
        <span>All AI Tools</span>
        <span class="live-badge">{total_tools}+ Tools</span>
      </a>

      <div class="nav-links">
        <a href="#featured">Directory</a>
        <a href="#categories">Categories</a>
        <a href="#faq">FAQ</a>
      </div>

      <div class="nav-actions">
        <button class="btn-saved" id="showSavedBtn" title="View Saved Tools">
          <span>&#9734;</span>
          <span>Saved</span>
          <span id="savedCountBadge" style="display:none; background:rgba(0,0,0,0.4); padding:1px 6px; border-radius:10px; font-size:0.75rem;">0</span>
        </button>
        <a href="https://github.com/shilwantr/aitest123" target="_blank" rel="noopener" class="btn-submit">+ Submit AI Tool</a>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <header class="hero">
    <div class="container">
      <div class="hero-eyebrow">&#9889; Global Verified AI Tools Directory 2026</div>
      <h1>Complete <span class="gradient-text">All AI Tools</span> Directory &amp; List</h1>
      <p class="hero-sub">Explore, search, and benchmark {total_tools}+ verified artificial intelligence software, models, and autonomous agents across 6 core industry categories.</p>

      <!-- Search Box with Query Param Support -->
      <div class="search-box-wrap">
        <span class="search-icon">&#128269;</span>
        <input type="text" id="searchInput" class="search-box" placeholder="Search by name, category, pricing, or keyword... (Press '/' to focus)" autofocus autocomplete="off" />
        <button id="clearSearch" class="clear-search" aria-label="Clear Search">&times;</button>
        <span class="search-hint">/</span>
      </div>

      <!-- Pricing Filter Chips -->
      <div class="filter-pricing-row">
        <button class="price-chip active" data-pricing="all">All Pricing</button>
        <button class="price-chip" data-pricing="free">Free ({cat_counts.get('free', 0) if 'free' in cat_counts else sum(1 for t in tools if t.get('pricing','').lower()=='free')})</button>
        <button class="price-chip" data-pricing="freemium">Freemium ({sum(1 for t in tools if t.get('pricing','').lower()=='freemium')})</button>
        <button class="price-chip" data-pricing="paid">Paid ({sum(1 for t in tools if t.get('pricing','').lower()=='paid')})</button>
      </div>

      <!-- Category Filter Pills -->
      <div class="filter-pills-row">
        <button class="filter-pill active" data-filter="all">
          <span>All AI Tools</span>
          <span class="pill-count">{total_tools}</span>
        </button>
        <button class="filter-pill" data-filter="chat-reasoning">
          <span>Chat &amp; Reasoning</span>
          <span class="pill-count">{cat_counts.get('chat-reasoning', 0)}</span>
        </button>
        <button class="filter-pill" data-filter="coding-dev">
          <span>Coding &amp; Dev</span>
          <span class="pill-count">{cat_counts.get('coding-dev', 0)}</span>
        </button>
        <button class="filter-pill" data-filter="image-art">
          <span>Image &amp; Art</span>
          <span class="pill-count">{cat_counts.get('image-art', 0)}</span>
        </button>
        <button class="filter-pill" data-filter="video-3d">
          <span>Video &amp; 3D</span>
          <span class="pill-count">{cat_counts.get('video-3d', 0)}</span>
        </button>
        <button class="filter-pill" data-filter="voice-audio">
          <span>Voice &amp; Audio</span>
          <span class="pill-count">{cat_counts.get('voice-audio', 0)}</span>
        </button>
        <button class="filter-pill" data-filter="ai-search">
          <span>AI Search</span>
          <span class="pill-count">{cat_counts.get('ai-search', 0)}</span>
        </button>
      </div>

      <!-- Trust Bar -->
      <div class="trust-bar">
        <span>&#10003; <strong>{total_tools}+</strong> Verified Tools</span>
        <span>&#128269; <strong>Click Card</strong> for Tool Page &amp; SEO queries</span>
        <span>&#127760; <strong>Direct Link</strong> opens official website</span>
        <span>&#9889; <strong>Instant Search</strong> &amp; URL Filter Sharing</span>
      </div>
    </div>
  </header>

  <!-- Featured Tools Directory Grid -->
  <section class="section" id="featured">
    <div class="container">
      <div class="section-header">
        <div>
          <h2 class="section-title">All AI Tools Catalog</h2>
          <p class="section-sub">Click any tool card to view dedicated page with features, search parameters and alternatives, or click "Open Tool" to visit directly.</p>
        </div>
        <div class="results-badge" id="resultsCounter">Showing {total_tools} Verified AI Tools</div>
      </div>

      <div class="tools-grid" id="toolsGrid">
{cards_block}
        <div class="empty-state" id="emptyState">
          <h3>No AI tools found</h3>
          <p>We couldn't find anything matching your filters or search keywords.</p>
          <button class="btn-submit" id="resetFiltersBtn">Reset All Filters</button>
        </div>
      </div>
    </div>
  </section>

  <!-- Domain Showcase Categories Section -->
  <section class="section" id="categories" style="border-top: 1px solid var(--border);">
    <div class="container">
      <div class="section-header">
        <div>
          <h2 class="section-title">Explore AI Domains</h2>
          <p class="section-sub">Browse software tailored to your workflow and industry use case.</p>
        </div>
      </div>

      <div class="cat-showcase-grid">
        <div class="cat-card" data-jump="chat-reasoning">
          <div>
            <h3>Chat, Logic &amp; Reasoning</h3>
            <p>Frontier LLMs, autonomous agents, reasoning engines, and custom GPT models engineered for conversational intelligence and complex synthesis.</p>
          </div>
          <div class="cat-card-meta">
            <span>{cat_counts.get('chat-reasoning', 0)} Tools</span>
            <span>Explore Domain &rarr;</span>
          </div>
        </div>

        <div class="cat-card" data-jump="coding-dev">
          <div>
            <h3>Code Generation &amp; Engineering</h3>
            <p>Autonomous AI software engineers, full-stack app builders, terminal assistants, automated test generators, and refactoring agents.</p>
          </div>
          <div class="cat-card-meta">
            <span>{cat_counts.get('coding-dev', 0)} Tools</span>
            <span>Explore Domain &rarr;</span>
          </div>
        </div>

        <div class="cat-card" data-jump="image-art">
          <div>
            <h3>Image Generation &amp; Design</h3>
            <p>Diffusion synthesis, prompt-to-image renderers, brand asset generators, UI mockups, and AI-assisted graphic workstations.</p>
          </div>
          <div class="cat-card-meta">
            <span>{cat_counts.get('image-art', 0)} Tools</span>
            <span>Explore Domain &rarr;</span>
          </div>
        </div>

        <div class="cat-card" data-jump="video-3d">
          <div>
            <h3>Video Creation &amp; 3D Worlds</h3>
            <p>Generative cinematic video, text-to-3D mesh creators, virtual avatar presenters, automated clip repurposers, and VFX engines.</p>
          </div>
          <div class="cat-card-meta">
            <span>{cat_counts.get('video-3d', 0)} Tools</span>
            <span>Explore Domain &rarr;</span>
          </div>
        </div>

        <div class="cat-card" data-jump="voice-audio">
          <div>
            <h3>Voice, Speech &amp; Music</h3>
            <p>Zero-shot voice cloning, real-time multilingual text-to-speech, synthetic music studios, voice isolation, and audio agents.</p>
          </div>
          <div class="cat-card-meta">
            <span>{cat_counts.get('voice-audio', 0)} Tools</span>
            <span>Explore Domain &rarr;</span>
          </div>
        </div>

        <div class="cat-card" data-jump="ai-search">
          <div>
            <h3>AI Search &amp; Research</h3>
            <p>Perplexity-style conversational search engines, deep literature review assistants, fact-checking agents, and academic graph analyzers.</p>
          </div>
          <div class="cat-card-meta">
            <span>{cat_counts.get('ai-search', 0)} Tools</span>
            <span>Explore Domain &rarr;</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Section with Schema Markup -->
  <section class="section" id="faq" style="border-top: 1px solid var(--border);">
    <div class="container">
      <div class="section-header" style="text-align: center; justify-content: center;">
        <div>
          <h2 class="section-title">Frequently Asked Questions</h2>
          <p class="section-sub">Everything you need to know about the All AI Tools directory and software index.</p>
        </div>
      </div>

      <div class="faq-grid">
        <div class="faq-card">
          <div class="faq-q">
            <span>What is All AI Tools (allaitools.online)?</span>
            <span class="faq-icon">+</span>
          </div>
          <div class="faq-a">
            All AI Tools is an exhaustive, curated global directory of {total_tools}+ artificial intelligence software platforms, reasoning models, custom GPTs, and autonomous agents across 6 core industry verticals: Chat &amp; Reasoning, Coding &amp; Dev, Image &amp; Art, Video &amp; 3D, Voice &amp; Audio, and AI Search.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-q">
            <span>How does the tool page and card click work?</span>
            <span class="faq-icon">+</span>
          </div>
          <div class="faq-a">
            Clicking on any tool card opens its dedicated URL (/toolname) featuring full specs, search queries, parameters, and alternatives. Clicking the "Open Tool" button redirects directly to the tool's official website in a new window.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-q">
            <span>Are the AI tools listed on this site free to use?</span>
            <span class="faq-icon">+</span>
          </div>
          <div class="faq-a">
            Yes! We categorize every tool with clear pricing badges: Free, Freemium, and Paid. You can filter the entire directory to see 100% free AI tools or freemium tools with generous free tiers.
          </div>
        </div>

        <div class="faq-card">
          <div class="faq-q">
            <span>How frequently is the All AI Tools directory updated?</span>
            <span class="faq-icon">+</span>
          </div>
          <div class="faq-a">
            The directory is regularly refreshed with automated crawls, new tool releases, and direct submissions to ensure link uptime, verified status, and fresh software listings.
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-inner">
        <div class="brand">
          <span class="brand-icon">AI</span>
          <span>All AI Tools</span>
        </div>
        <div class="footer-links">
          <a href="#featured">Directory</a>
          <a href="/?category=chat-reasoning">Chat &amp; Reasoning</a>
          <a href="/?category=coding-dev">Coding &amp; Dev</a>
          <a href="/?category=image-art">Image &amp; Art</a>
          <a href="/?category=video-3d">Video &amp; 3D</a>
          <a href="/?category=voice-audio">Voice &amp; Audio</a>
          <a href="/?category=ai-search">AI Search</a>
          <a href="/sitemap.xml">Sitemap</a>
          <a href="/robots.txt">Robots.txt</a>
        </div>
      </div>
      <p>&copy; 2026 All AI Tools (allaitools.online). All rights reserved. Open Tool links navigate directly to third-party tools.</p>
    </div>
  </footer>

  <!-- Search & Filter JavaScript with URL Parameter Sync -->
  <script>
    (function () {{
      var searchInput = document.getElementById('searchInput');
      var clearBtn = document.getElementById('clearSearch');
      var filterPills = document.querySelectorAll('.filter-pill');
      var priceChips = document.querySelectorAll('.price-chip');
      var cards = document.querySelectorAll('.tool-card');
      var emptyState = document.getElementById('emptyState');
      var resultsCounter = document.getElementById('resultsCounter');
      var resetBtn = document.getElementById('resetFiltersBtn');
      var showSavedBtn = document.getElementById('showSavedBtn');
      var savedCountBadge = document.getElementById('savedCountBadge');

      var currentCat = 'all';
      var currentPricing = 'all';
      var filterOnlySaved = false;

      var savedTools = [];
      try {{
        savedTools = JSON.parse(localStorage.getItem('saved_ai_tools') || '[]');
      }} catch (e) {{}}

      function updateSavedUI() {{
        document.querySelectorAll('.bookmark-btn').forEach(function (btn) {{
          var toolName = btn.getAttribute('data-tool').toLowerCase();
          if (savedTools.indexOf(toolName) !== -1) {{
            btn.classList.add('saved');
            btn.innerHTML = '&#9733;';
          }} else {{
            btn.classList.remove('saved');
            btn.innerHTML = '&#9734;';
          }}
        }});
        if (savedTools.length > 0) {{
          savedCountBadge.style.display = 'inline-block';
          savedCountBadge.textContent = savedTools.length;
        }} else {{
          savedCountBadge.style.display = 'none';
        }}
      }}

      function updateUrlParams() {{
        var params = new URLSearchParams();
        var q = searchInput.value.trim();
        if (q) params.set('q', q);
        if (currentCat && currentCat !== 'all') params.set('category', currentCat);
        if (currentPricing && currentPricing !== 'all') params.set('pricing', currentPricing);
        var qString = params.toString();
        var newUrl = window.location.pathname + (qString ? '?' + qString : '');
        window.history.replaceState({{}}, '', newUrl);
      }}

      function filterTools() {{
        var q = searchInput.value.trim().toLowerCase();
        if (q.length > 0) {{
          clearBtn.style.display = 'block';
        }} else {{
          clearBtn.style.display = 'none';
        }}

        var visible = 0;
        cards.forEach(function (card) {{
          var cardCat = card.getAttribute('data-category');
          var cardPrice = card.getAttribute('data-pricing');
          var cardName = card.getAttribute('data-name');
          var cardDesc = card.getAttribute('data-desc');

          var matchesCat = (currentCat === 'all' || cardCat === currentCat);
          var matchesPrice = (currentPricing === 'all' || cardPrice === currentPricing);
          var matchesQuery = (!q || cardName.indexOf(q) !== -1 || cardDesc.indexOf(q) !== -1);
          var matchesSaved = (!filterOnlySaved || savedTools.indexOf(cardName) !== -1);

          if (matchesCat && matchesPrice && matchesQuery && matchesSaved) {{
            card.style.display = '';
            visible++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        if (visible === 0) {{
          emptyState.style.display = 'block';
          resultsCounter.textContent = '0 AI Tools Found';
        }} else {{
          emptyState.style.display = 'none';
          resultsCounter.textContent = 'Showing ' + visible + ' Verified AI Tool' + (visible === 1 ? '' : 's');
        }}

        updateUrlParams();
      }}

      // Keyboard shortcut '/'
      window.addEventListener('keydown', function (e) {{
        if (e.key === '/' && document.activeElement !== searchInput) {{
          e.preventDefault();
          searchInput.focus();
        }}
        if (e.key === 'Escape' && document.activeElement === searchInput) {{
          searchInput.value = '';
          filterTools();
          searchInput.blur();
        }}
      }});

      searchInput.addEventListener('input', filterTools);
      clearBtn.addEventListener('click', function () {{
        searchInput.value = '';
        filterTools();
        searchInput.focus();
      }});

      // Category Pill Click
      filterPills.forEach(function (pill) {{
        pill.addEventListener('click', function () {{
          filterPills.forEach(function (p) {{ p.classList.remove('active'); }});
          pill.classList.add('active');
          currentCat = pill.getAttribute('data-filter');
          filterTools();
        }});
      }});

      // Pricing Chip Click
      priceChips.forEach(function (chip) {{
        chip.addEventListener('click', function () {{
          priceChips.forEach(function (c) {{ c.classList.remove('active'); }});
          chip.classList.add('active');
          currentPricing = chip.getAttribute('data-pricing');
          filterTools();
        }});
      }});

      // Domain Showcase jump
      document.querySelectorAll('.cat-card').forEach(function (card) {{
        card.addEventListener('click', function () {{
          var jumpCat = card.getAttribute('data-jump');
          var targetPill = document.querySelector('.filter-pill[data-filter="' + jumpCat + '"]');
          if (targetPill) {{
            targetPill.click();
            document.getElementById('featured').scrollIntoView({{ behavior: 'smooth' }});
          }}
        }});
      }});

      // Reset
      resetBtn.addEventListener('click', function () {{
        searchInput.value = '';
        currentCat = 'all';
        currentPricing = 'all';
        filterOnlySaved = false;
        showSavedBtn.style.background = '';
        filterPills.forEach(function (p) {{
          p.classList.toggle('active', p.getAttribute('data-filter') === 'all');
        }});
        priceChips.forEach(function (c) {{
          c.classList.toggle('active', c.getAttribute('data-pricing') === 'all');
        }});
        filterTools();
      }});

      // Bookmarking
      document.querySelectorAll('.bookmark-btn').forEach(function (btn) {{
        btn.addEventListener('click', function (e) {{
          e.preventDefault();
          e.stopPropagation();
          var toolName = btn.getAttribute('data-tool').toLowerCase();
          var idx = savedTools.indexOf(toolName);
          if (idx === -1) {{
            savedTools.push(toolName);
          }} else {{
            savedTools.splice(idx, 1);
          }}
          try {{
            localStorage.setItem('saved_ai_tools', JSON.stringify(savedTools));
          }} catch (err) {{}}
          updateSavedUI();
          if (filterOnlySaved) filterTools();
        }});
      }});

      // Saved Filter Toggle
      showSavedBtn.addEventListener('click', function () {{
        filterOnlySaved = !filterOnlySaved;
        if (filterOnlySaved) {{
          showSavedBtn.style.background = 'rgba(251, 191, 36, 0.2)';
          showSavedBtn.style.borderColor = 'rgba(251, 191, 36, 0.5)';
        }} else {{
          showSavedBtn.style.background = '';
          showSavedBtn.style.borderColor = '';
        }}
        filterTools();
        document.getElementById('featured').scrollIntoView({{ behavior: 'smooth' }});
      }});

      // FAQ accordion
      document.querySelectorAll('.faq-q').forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          btn.parentElement.classList.toggle('open');
        }});
      }});

      // Read initial URL query parameters
      var urlParams = new URLSearchParams(window.location.search);
      var qParam = urlParams.get('q');
      var catParam = urlParams.get('category') || urlParams.get('cat');
      var pricingParam = urlParams.get('pricing') || urlParams.get('price');

      if (qParam) {{
        searchInput.value = qParam;
      }}
      if (catParam) {{
        var targetPill = document.querySelector('.filter-pill[data-filter="' + catParam + '"]');
        if (targetPill) {{
          filterPills.forEach(function (p) {{ p.classList.remove('active'); }});
          targetPill.classList.add('active');
          currentCat = catParam;
        }}
      }}
      if (pricingParam) {{
        var targetChip = document.querySelector('.price-chip[data-pricing="' + pricingParam.toLowerCase() + '"]');
        if (targetChip) {{
          priceChips.forEach(function (c) {{ c.classList.remove('active'); }});
          targetChip.classList.add('active');
          currentPricing = pricingParam.toLowerCase();
        }}
      }}

      updateSavedUI();
      if (qParam || catParam || pricingParam) {{
        filterTools();
      }}
    }})();
  </script>
</body>
</html>
"""

# Write root index.html and public/index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html_content)

os.makedirs("public", exist_ok=True)
with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(index_html_content)

print(f"Generated root index.html and public/index.html with {total_tools} tools.")

# 4. Generate 404.html
page_404_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Not Found (404) | All AI Tools</title>
  <meta name="description" content="The requested AI tool or page could not be found. Search 960+ artificial intelligence tools on All AI Tools." />
  <meta name="robots" content="noindex, follow" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2222%22 fill=%22%234F46E5%22/><text y=%2268%22 x=%2250%22 font-family=%22system-ui,sans-serif%22 font-weight=%22800%22 font-size=%2254%22 fill=%22white%22 text-anchor=%22middle%22>AI</text></svg>" />
  <style>
    :root {{
      --bg: #090d16;
      --bg-card: #0f1626;
      --border: rgba(255, 255, 255, 0.08);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #6366f1;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text-main); font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; text-align: center; }}
    .box {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px; padding: 48px 32px; max-width: 600px; width: 100%; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
    .code {{ font-size: 4rem; font-weight: 900; background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }}
    h1 {{ font-size: 1.6rem; margin-bottom: 12px; }}
    p {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 24px; line-height: 1.6; }}
    .search-input {{ width: 100%; padding: 14px 20px; background: rgba(0,0,0,0.3); border: 1px solid var(--border); border-radius: 12px; color: #fff; font-size: 1rem; margin-bottom: 20px; outline: none; }}
    .search-input:focus {{ border-color: var(--accent); }}
    .btn {{ display: inline-block; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: #fff; font-weight: 700; padding: 12px 28px; border-radius: 10px; text-decoration: none; }}
    .quick-links {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-top: 24px; }}
    .quick-link {{ background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; color: #cbd5e1; text-decoration: none; border: 1px solid var(--border); }}
    .quick-link:hover {{ background: rgba(99,102,241,0.2); color: #fff; }}
  </style>
</head>
<body>
  <div class="box">
    <div class="code">404</div>
    <h1>AI Tool or Page Not Found</h1>
    <p>The page you are looking for might have been moved, renamed, or is temporarily unavailable. Search 960+ verified AI tools below:</p>
    <input type="search" id="search404" class="search-input" placeholder="Search AI tools (e.g. ChatGPT, Claude, Midjourney)..." />
    <br />
    <a href="/" class="btn">&larr; Return to All AI Tools</a>
    <div class="quick-links">
      <a href="/?category=chat-reasoning" class="quick-link">Chat &amp; Reasoning</a>
      <a href="/?category=coding-dev" class="quick-link">Coding &amp; Dev</a>
      <a href="/?category=image-art" class="quick-link">Image &amp; Art</a>
      <a href="/?category=video-3d" class="quick-link">Video &amp; 3D</a>
      <a href="/?category=voice-audio" class="quick-link">Voice &amp; Audio</a>
      <a href="/?category=ai-search" class="quick-link">AI Search</a>
    </div>
  </div>
  <script>
    var input = document.getElementById('search404');
    input.addEventListener('keydown', function(e) {{
      if (e.key === 'Enter' && input.value.trim()) {{
        window.location.href = '/?q=' + encodeURIComponent(input.value.trim());
      }}
    }});
  </script>
</body>
</html>"""

with open("404.html", "w", encoding="utf-8") as f:
    f.write(page_404_content)
with open("public/404.html", "w", encoding="utf-8") as f:
    f.write(page_404_content)
print("Generated 404.html.")

# 5. Generate robots.txt
robots_txt_content = f"""# Robots.txt for {BASE_URL}/
# Explicitly allowing all search engine web crawlers and AI agents

User-agent: *
Allow: /

# Google Search, Google Images, Googlebot News, and Gemini Crawlers
User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: Googlebot-News
Allow: /

User-agent: Google-Extended
Allow: /

# Microsoft Bing & Copilot
User-agent: Bingbot
Allow: /

User-agent: msnbot
Allow: /

# Yahoo & DuckDuckGo
User-agent: Slurp
Allow: /

User-agent: DuckDuckBot
Allow: /

# Baidu & Yandex
User-agent: Baiduspider
Allow: /

User-agent: YandexBot
Allow: /

# Apple Intelligence & Siri
User-agent: Applebot
Allow: /

User-agent: Applebot-Extended
Allow: /

# OpenAI Crawlers (GPT-4, SearchGPT, ChatGPT Browsing)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

# Anthropic Claude Crawlers
User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Claude-Web
Allow: /

# Perplexity AI Search Crawler
User-agent: PerplexityBot
Allow: /

# Common Crawl (Used by open training datasets & LLMs)
User-agent: CCBot
Allow: /

# Meta / Facebook
User-agent: FacebookBot
Allow: /

User-agent: meta-externalagent
Allow: /

# Twitter / X
User-agent: Twitterbot
Allow: /

# Canonical Sitemap
Sitemap: {BASE_URL}/sitemap.xml
"""

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_txt_content)
with open("public/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_txt_content)
print("Generated robots.txt allowing all agents with canonical sitemap URL.")

# 6. Generate sitemap.xml with all tool pages
sitemap_urls = [
    f"""  <url>
    <loc>{BASE_URL}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
]

for t in tools:
    path = t.get('path', f"/{t['slug']}/")
    sitemap_urls.append(f"""  <url>
    <loc>{BASE_URL}{path}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
{chr(10).join(sitemap_urls)}
</urlset>
"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)
with open("public/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)
print(f"Generated sitemap.xml with {len(sitemap_urls)} URLs (1 home + {len(tools)} tool pages).")

# 7. Generate vercel.json
vercel_json_content = {
    "cleanUrls": True,
    "trailingSlash": False,
    "headers": [
        {
            "source": "/(.*)",
            "headers": [
                {
                    "key": "X-Content-Type-Options",
                    "value": "nosniff"
                },
                {
                    "key": "X-Frame-Options",
                    "value": "DENY"
                },
                {
                    "key": "X-XSS-Protection",
                    "value": "1; mode=block"
                }
            ]
        },
        {
            "source": "/sitemap.xml",
            "headers": [
                {
                    "key": "Content-Type",
                    "value": "application/xml; charset=utf-8"
                },
                {
                    "key": "Cache-Control",
                    "value": "public, max-age=3600, s-maxage=3600"
                }
            ]
        },
        {
            "source": "/robots.txt",
            "headers": [
                {
                    "key": "Content-Type",
                    "value": "text/plain; charset=utf-8"
                },
                {
                    "key": "Cache-Control",
                    "value": "public, max-age=3600, s-maxage=3600"
                }
            ]
        }
    ]
}

with open("vercel.json", "w", encoding="utf-8") as f:
    json.dump(vercel_json_content, f, indent=2)
print("Generated vercel.json with cleanUrls and security/caching headers.")

# 8. Generate each tool page
def render_tool_page(tool, all_tools):
    name = tool.get('name', 'AI Platform')
    slug = tool.get('slug', 'tool')
    path = tool.get('path', f"/{slug}/")
    desc = tool.get('description', '')
    pricing = tool.get('pricing', 'Freemium')
    pill = tool.get('category_pill', 'AI Tools')
    cat_slug = tool.get('category_slug', 'chat-reasoning')
    subcat = tool.get('subcategory') or tool.get('category_section') or pill
    color = tool.get('color', '#4F46E5')
    badge = tool.get('badge', name[:2].upper())
    url = tool.get('url', '#')
    img_url = tool.get('image_url', '')
    domain = get_domain(url)

    price_class = "price-freemium"
    if pricing.lower() == "free":
        price_class = "price-free"
    elif pricing.lower() == "paid":
        price_class = "price-paid"

    # Related tools
    related = [t for t in all_tools if t.get('category_slug') == cat_slug and t.get('slug') != slug][:5]
    related_names = ", ".join([r.get('name', '') for r in related[:3]]) if related else "top AI tools"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{BASE_URL}/#website",
                "url": f"{BASE_URL}/",
                "name": "All AI Tools",
                "description": f"Comprehensive directory of {total_tools}+ artificial intelligence tools and models."
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{BASE_URL}{path}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": f"{BASE_URL}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": pill,
                        "item": f"{BASE_URL}/?category={cat_slug}"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": name,
                        "item": f"{BASE_URL}{path}"
                    }
                ]
            },
            {
                "@type": "SoftwareApplication",
                "@id": f"{BASE_URL}{path}#software",
                "name": name,
                "description": desc,
                "url": url,
                "applicationCategory": pill,
                "operatingSystem": "All, Web, Cloud",
                "offers": {
                    "@type": "Offer",
                    "price": "0" if pricing.lower() in ["free", "freemium"] else "19.00",
                    "priceCurrency": "USD",
                    "category": pricing
                }
            },
            {
                "@type": "FAQPage",
                "@id": f"{BASE_URL}{path}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"What is {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{name} is a leading AI software in the {pill} ({subcat}) category. {desc}"
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"How much does {name} cost?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"{name} operates under a {pricing} model. Visit the official website ({domain}) for current pricing tiers and free trial details."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"How do I open and use {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"You can open and visit {name} directly via its official portal at {url}."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"What are the best alternatives to {name}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Popular alternatives to {name} in the {pill} category include {related_names}."
                        }
                    }
                ]
            }
        ]
    }
    schema_json_str = json.dumps(schema_data, indent=2)

    related_cards_html = []
    for r in related:
        r_name = r.get('name', 'AI Tool')
        r_slug = r.get('slug', '')
        r_path = r.get('path', f"/{r_slug}/")
        r_subcat = r.get('subcategory') or pill
        r_desc = r.get('description', '')
        r_pricing = r.get('pricing', 'Freemium')
        r_badge = r.get('badge', r_name[:2].upper())
        r_color = r.get('color', '#4F46E5')
        r_url = r.get('url', '#')
        r_price_class = "price-freemium"
        if r_pricing.lower() == "free":
            r_price_class = "price-free"
        elif r_pricing.lower() == "paid":
            r_price_class = "price-paid"

        related_cards_html.append(f"""
          <div class="related-card" onclick="if(!event.target.closest('a') && !event.target.closest('button')) window.location.href='{r_path}'">
            <div class="related-card-top">
              <div class="tool-avatar" style="background:{r_color};">{html.escape(r_badge)}</div>
              <div style="flex:1; min-width:0;">
                <span class="tool-subcat">{html.escape(r_subcat)}</span>
                <h4 class="related-title"><a href="{r_path}" class="tool-card-title-link">{html.escape(r_name)}</a></h4>
              </div>
              <span class="price-badge {r_price_class}">{html.escape(r_pricing)}</span>
            </div>
            <p class="related-desc">{html.escape(r_desc[:120])}{'...' if len(r_desc) > 120 else ''}</p>
            <div class="related-card-bottom">
              <a href="{r_path}" class="view-detail-link">View Details &rarr;</a>
              <a href="{html.escape(r_url)}" target="_blank" rel="noopener noreferrer nofollow" class="tool-link" onclick="event.stopPropagation()">Open Tool &rarr;</a>
            </div>
          </div>
        """)
    related_block = "\n".join(related_cards_html)

    preview_block = ""
    if img_url:
        preview_block = f"""
        <div class="preview-box">
          <img src="{html.escape(img_url)}" alt="{html.escape(name)} screenshot preview" class="tool-preview-full" loading="lazy" onerror="this.parentElement.style.display='none'" />
        </div>
        """

    q_name = quote_plus(name)
    q_subcat = quote_plus(subcat)

    js_tool_name = json.dumps(name.lower())

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(name)} — AI Features, Pricing &amp; Alternatives (2026) | All AI Tools</title>
  <meta name="description" content="Discover {html.escape(name)}: {html.escape(desc[:150])}. Compare pricing ({html.escape(pricing)}), category ({html.escape(pill)}), verified features, and alternatives." />
  <meta name="keywords" content="{html.escape(name)}, {html.escape(name)} review, {html.escape(name)} pricing, {html.escape(name)} alternatives, {html.escape(subcat)}, {html.escape(pill)}, all ai tools, ai directory" />
  <meta name="author" content="All AI Tools" />
  <link rel="canonical" href="{BASE_URL}{path}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />

  <!-- OpenGraph -->
  <meta property="og:title" content="{html.escape(name)} — AI Features, Pricing &amp; Alternatives" />
  <meta property="og:description" content="{html.escape(desc)}" />
  <meta property="og:url" content="{BASE_URL}{path}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="All AI Tools" />
  {f'<meta property="og:image" content="{html.escape(img_url)}" />' if img_url else ''}

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(name)} | All AI Tools Directory" />
  <meta name="twitter:description" content="{html.escape(desc[:150])}" />

  <!-- Favicon -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2222%22 fill=%22%234F46E5%22/><text y=%2268%22 x=%2250%22 font-family=%22system-ui,sans-serif%22 font-weight=%22800%22 font-size=%2254%22 fill=%22white%22 text-anchor=%22middle%22>AI</text></svg>" />

  <!-- Structured Data JSON-LD -->
  <script type="application/ld+json">
{schema_json_str}
  </script>

  <style>
    :root {{
      --bg: #090d16;
      --bg-card: #0f1626;
      --bg-card-hover: #151f36;
      --bg-elevated: #1a253f;
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(99, 102, 241, 0.4);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --accent: #6366f1;
      --accent-glow: rgba(99, 102, 241, 0.25);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --radius-pill: 9999px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text-main); line-height: 1.6; }}
    body {{ min-height: 100vh; overflow-x: hidden; }}
    a {{ text-decoration: none; color: inherit; }}

    /* Background Ambient */
    .ambient-glow {{
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 1000px;
      height: 520px;
      background: radial-gradient(circle 500px at 50% 120px, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.08), transparent 70%);
      pointer-events: none;
      z-index: 0;
    }}

    .container {{ max-width: 1240px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }}

    /* Navbar */
    .navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(9, 13, 22, 0.88);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      height: 72px;
      display: flex;
      align-items: center;
    }}
    .nav-inner {{ display: flex; align-items: center; justify-content: space-between; width: 100%; gap: 16px; }}
    .brand {{ display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 1.18rem; letter-spacing: -0.02em; color: #fff; }}
    .brand-icon {{
      width: 38px;
      height: 38px;
      border-radius: 11px;
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      color: #fff;
      font-size: 1.1rem;
      box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
    }}
    .nav-search-wrap {{
      flex: 1;
      max-width: 440px;
      position: relative;
      display: none;
    }}
    @media (min-width: 768px) {{ .nav-search-wrap {{ display: block; }} }}
    .nav-search-input {{
      width: 100%;
      padding: 9px 16px 9px 38px;
      background: rgba(15, 22, 38, 0.9);
      border: 1px solid var(--border);
      border-radius: var(--radius-pill);
      color: #fff;
      font-size: 0.88rem;
      outline: none;
      transition: all 0.2s;
    }}
    .nav-search-input:focus {{ border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }}
    .nav-search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-sub);
      font-size: 0.9rem;
      pointer-events: none;
    }}
    .nav-links {{ display: flex; align-items: center; gap: 16px; font-size: 0.9rem; }}
    .btn-back {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--text-muted);
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.04);
      transition: all 0.15s ease;
    }}
    .btn-back:hover {{ color: #fff; background: rgba(255, 255, 255, 0.09); border-color: rgba(255, 255, 255, 0.2); }}

    /* Breadcrumbs */
    .breadcrumbs {{
      padding: 24px 0 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.86rem;
      color: var(--text-sub);
      flex-wrap: wrap;
    }}
    .breadcrumbs a {{ color: var(--text-muted); transition: color 0.15s; }}
    .breadcrumbs a:hover {{ color: #fff; text-decoration: underline; }}
    .breadcrumbs .crumb-sep {{ color: var(--text-sub); }}
    .breadcrumbs .crumb-current {{ color: #cbd5e1; font-weight: 600; }}

    /* Tool Hero Card */
    .tool-hero {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 36px 32px;
      margin-bottom: 32px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }}
    .tool-hero::before {{
      content: "";
      position: absolute;
      top: -50px;
      right: -50px;
      width: 250px;
      height: 250px;
      background: radial-gradient(circle, {color}22 0%, transparent 70%);
      pointer-events: none;
    }}
    .hero-top-row {{
      display: flex;
      align-items: flex-start;
      gap: 24px;
      flex-wrap: wrap;
      margin-bottom: 24px;
    }}
    .hero-avatar {{
      width: 80px;
      height: 80px;
      border-radius: 20px;
      color: #fff;
      font-weight: 900;
      font-size: 1.9rem;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      flex-shrink: 0;
    }}
    .hero-info {{ flex: 1; min-width: 280px; }}
    .hero-subcat {{
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #818cf8;
      margin-bottom: 6px;
      display: inline-block;
    }}
    .hero-title {{
      font-size: clamp(1.8rem, 4vw, 2.6rem);
      font-weight: 900;
      letter-spacing: -0.02em;
      color: #ffffff;
      margin-bottom: 12px;
      line-height: 1.2;
    }}
    .hero-badges {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}

    /* Badges */
    .price-badge {{
      font-size: 0.76rem;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: var(--radius-pill);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .price-freemium {{ background: rgba(99, 102, 241, 0.15); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.3); }}
    .price-free {{ background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .price-paid {{ background: rgba(244, 63, 94, 0.15); color: #fda4af; border: 1px solid rgba(244, 63, 94, 0.3); }}

    .meta-pill {{
      font-size: 0.8rem;
      font-weight: 600;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
    }}
    .status-pill {{
      font-size: 0.78rem;
      font-weight: 600;
      color: #34d399;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
    }}
    .domain-pill {{
      font-size: 0.78rem;
      font-weight: 600;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      padding: 5px 12px;
      border-radius: var(--radius-pill);
    }}

    /* Action Row */
    .hero-actions {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      padding-top: 20px;
      border-top: 1px solid var(--border);
    }}
    .btn-open-tool {{
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: #ffffff !important;
      font-weight: 700;
      font-size: 1.05rem;
      padding: 14px 30px;
      border-radius: 12px;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .btn-open-tool:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 28px rgba(99, 102, 241, 0.6);
      opacity: 0.95;
    }}
    .btn-bookmark, .btn-share {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: #cbd5e1;
      font-weight: 600;
      font-size: 0.92rem;
      padding: 14px 20px;
      border-radius: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s ease;
    }}
    .btn-bookmark:hover, .btn-share:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.25);
      color: #fff;
    }}
    .btn-bookmark.saved {{ color: #fbbf24; border-color: rgba(251, 191, 36, 0.4); }}

    /* Layout Grid */
    .content-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 32px;
      margin-bottom: 64px;
    }}
    @media (min-width: 992px) {{
      .content-grid {{ grid-template-columns: 2fr 1fr; }}
    }}

    /* Card Box */
    .card-box {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 28px;
      margin-bottom: 28px;
    }}
    .card-box h2 {{
      font-size: 1.35rem;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .lead-desc {{
      font-size: 1.05rem;
      line-height: 1.7;
      color: var(--text-muted);
      margin-bottom: 20px;
    }}

    /* Preview box */
    .preview-box {{
      margin: 20px 0;
      border-radius: var(--radius-sm);
      overflow: hidden;
      border: 1px solid var(--border);
      background: rgba(0, 0, 0, 0.3);
    }}
    .tool-preview-full {{
      width: 100%;
      height: auto;
      max-height: 480px;
      object-fit: cover;
      display: block;
    }}

    /* Specs Table */
    .specs-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 14px;
    }}
    .specs-table tr {{ border-bottom: 1px solid rgba(255, 255, 255, 0.05); }}
    .specs-table tr:last-child {{ border-bottom: none; }}
    .specs-table td {{
      padding: 12px 0;
      font-size: 0.92rem;
    }}
    .specs-table td.label {{
      color: var(--text-sub);
      width: 38%;
      font-weight: 500;
    }}
    .specs-table td.val {{
      color: #e2e8f0;
      font-weight: 600;
    }}
    .specs-table td.val a {{ color: #818cf8; }}
    .specs-table td.val a:hover {{ text-decoration: underline; }}

    /* Query Parameters & Search Section */
    .queries-box {{
      background: rgba(99, 102, 241, 0.05);
      border: 1px solid rgba(99, 102, 241, 0.2);
    }}
    .query-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 14px;
    }}
    .query-pill {{
      background: rgba(15, 22, 38, 0.9);
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #c7d2fe;
      padding: 8px 14px;
      border-radius: var(--radius-pill);
      font-size: 0.84rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .query-pill:hover {{
      background: rgba(99, 102, 241, 0.2);
      border-color: rgba(99, 102, 241, 0.6);
      color: #fff;
      transform: translateY(-1px);
    }}

    /* FAQs */
    .faq-item {{
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding: 16px 0;
    }}
    .faq-item:last-child {{ border-bottom: none; padding-bottom: 0; }}
    .faq-q {{
      font-size: 1.02rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 8px;
    }}
    .faq-a {{
      font-size: 0.92rem;
      color: var(--text-muted);
      line-height: 1.6;
    }}

    /* Sidebar Sticky CTA Card */
    .sidebar-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 24px;
      margin-bottom: 24px;
      position: sticky;
      top: 96px;
    }}
    .sidebar-card h3 {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #fff;
      margin-bottom: 12px;
    }}
    .sidebar-cta-btn {{
      display: block;
      width: 100%;
      text-align: center;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: #fff !important;
      font-weight: 700;
      font-size: 0.98rem;
      padding: 12px 18px;
      border-radius: 10px;
      margin-top: 16px;
      box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
      transition: all 0.15s ease;
    }}
    .sidebar-cta-btn:hover {{ opacity: 0.95; transform: translateY(-1px); }}

    /* Related Tools Cards */
    .related-card {{
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 16px;
      margin-bottom: 14px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .related-card:hover {{
      background: var(--bg-card-hover);
      border-color: rgba(99, 102, 241, 0.3);
      transform: translateY(-2px);
    }}
    .related-card-top {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
    }}
    .related-card-top .tool-avatar {{
      width: 36px;
      height: 36px;
      font-size: 0.85rem;
      border-radius: 8px;
    }}
    .related-title {{
      font-size: 0.96rem;
      font-weight: 700;
      color: #fff;
    }}
    .tool-card-title-link:hover {{ color: #818cf8; text-decoration: underline; }}
    .related-desc {{
      font-size: 0.84rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 10px;
    }}
    .related-card-bottom {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.82rem;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.04);
    }}
    .view-detail-link {{ color: #94a3b8; }}
    .view-detail-link:hover {{ color: #fff; text-decoration: underline; }}
    .tool-link {{
      color: #818cf8;
      font-weight: 600;
    }}
    .tool-link:hover {{ color: #c084fc; text-decoration: underline; }}

    /* Category list in sidebar */
    .cat-links-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 12px;
    }}
    .cat-link-item {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.02);
      border-radius: 8px;
      font-size: 0.86rem;
      color: var(--text-muted);
      transition: all 0.15s;
    }}
    .cat-link-item:hover {{ background: rgba(99, 102, 241, 0.12); color: #c7d2fe; }}

    /* Footer */
    .footer {{
      border-top: 1px solid var(--border);
      padding: 48px 0;
      color: var(--text-sub);
      font-size: 0.88rem;
      text-align: center;
    }}
    .footer-links {{
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}
    .footer-links a:hover {{ color: #fff; }}

    /* Toast */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #1e1b4b;
      border: 1px solid #6366f1;
      color: #fff;
      padding: 12px 20px;
      border-radius: 10px;
      font-size: 0.9rem;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      display: none;
      z-index: 1000;
    }}
  </style>
</head>
<body>
  <div class="ambient-glow"></div>

  <!-- Navbar -->
  <header class="navbar">
    <div class="container nav-inner">
      <a href="/" class="brand">
        <span class="brand-icon">AI</span>
        <span>All AI Tools</span>
      </a>

      <div class="nav-search-wrap">
        <span class="nav-search-icon">&#128269;</span>
        <input type="search" class="nav-search-input" id="navSearchInput" placeholder="Search 960+ AI tools (Press Enter)..." />
      </div>

      <div class="nav-links">
        <a href="/" class="btn-back">&larr; Back to Directory</a>
      </div>
    </div>
  </header>

  <main class="container">
    <!-- Breadcrumbs -->
    <nav class="breadcrumbs" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span class="crumb-sep">/</span>
      <a href="/?category={cat_slug}">{html.escape(pill)}</a>
      <span class="crumb-sep">/</span>
      <span class="crumb-current">{html.escape(name)}</span>
    </nav>

    <!-- Tool Hero Card -->
    <section class="tool-hero">
      <div class="hero-top-row">
        <div class="hero-avatar" style="background:{color};">{html.escape(badge)}</div>
        <div class="hero-info">
          <span class="hero-subcat">{html.escape(subcat)}</span>
          <h1 class="hero-title">{html.escape(name)}</h1>
          <div class="hero-badges">
            <span class="price-badge {price_class}">{html.escape(pricing)}</span>
            <span class="meta-pill">{html.escape(pill)}</span>
            <span class="status-pill">&#10003; Verified &amp; Active</span>
            <span class="domain-pill">&#127760; {html.escape(domain)}</span>
          </div>
        </div>
      </div>

      <div class="hero-actions">
        <a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer nofollow" class="btn-open-tool">
          Open {html.escape(name)} &rarr;
        </a>
        <button class="btn-bookmark" id="heroBookmarkBtn" data-tool="{html.escape(name)}">&#9734; Bookmark</button>
        <button class="btn-share" id="shareBtn">&#128279; Share Tool</button>
      </div>
    </section>

    <!-- Main Content & Sidebar Layout -->
    <div class="content-grid">
      <!-- Left Main Column -->
      <div class="main-column">
        <!-- Overview -->
        <article class="card-box">
          <h2>About {html.escape(name)}</h2>
          <p class="lead-desc">{html.escape(desc)}</p>
          {preview_block}
        </article>

        <!-- Specifications -->
        <section class="card-box">
          <h2>Key Platform Details</h2>
          <table class="specs-table">
            <tbody>
              <tr>
                <td class="label">Tool Name</td>
                <td class="val">{html.escape(name)}</td>
              </tr>
              <tr>
                <td class="label">Primary Category</td>
                <td class="val"><a href="/?category={cat_slug}">{html.escape(pill)}</a></td>
              </tr>
              <tr>
                <td class="label">Domain &amp; Specialty</td>
                <td class="val"><a href="/?q={q_subcat}">{html.escape(subcat)}</a></td>
              </tr>
              <tr>
                <td class="label">Pricing Model</td>
                <td class="val"><a href="/?pricing={html.escape(pricing.lower())}">{html.escape(pricing)}</a></td>
              </tr>
              <tr>
                <td class="label">Official Website</td>
                <td class="val"><a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer nofollow">{html.escape(domain)} &rarr;</a></td>
              </tr>
              <tr>
                <td class="label">Listing Status</td>
                <td class="val"><span style="color:#34d399;">Active, Indexed &amp; Verified</span></td>
              </tr>
            </tbody>
          </table>
        </section>

        <!-- Search Queries & URL Parameters Hub -->
        <section class="card-box queries-box">
          <h2>Explore Search Queries &amp; Parameters</h2>
          <p style="color:var(--text-muted); font-size:0.92rem;">Quick search queries and targeted filter parameters to discover matching AI software:</p>
          <div class="query-pills">
            <a href="/?q={q_name}+alternatives" class="query-pill">&#128269; {html.escape(name)} alternatives</a>
            <a href="/?q={q_name}+pricing" class="query-pill">&#128269; {html.escape(name)} pricing &amp; free tiers</a>
            <a href="/?category={cat_slug}" class="query-pill">&#128269; Best {html.escape(pill)} AI tools</a>
            <a href="/?category={cat_slug}&pricing={html.escape(pricing.lower())}" class="query-pill">&#128269; {html.escape(pricing)} {html.escape(pill)}</a>
            <a href="/?q={q_subcat}" class="query-pill">&#128269; Top {html.escape(subcat)}</a>
          </div>
        </section>

        <!-- FAQs with Schema Markup -->
        <section class="card-box">
          <h2>Frequently Asked Questions</h2>
          <div class="faq-item">
            <div class="faq-q">What is {html.escape(name)}?</div>
            <div class="faq-a">{html.escape(name)} is an artificial intelligence application categorized under {html.escape(pill)} ({html.escape(subcat)}). {html.escape(desc)}</div>
          </div>
          <div class="faq-item">
            <div class="faq-q">Is {html.escape(name)} free to use?</div>
            <div class="faq-a">{html.escape(name)} offers a {html.escape(pricing)} model. For full pricing plans and trial access, visit the official site at <a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer nofollow" style="color:#818cf8;">{html.escape(domain)}</a>.</div>
          </div>
          <div class="faq-item">
            <div class="faq-q">How do I access and open {html.escape(name)}?</div>
            <div class="faq-a">Click the "Open {html.escape(name)}" button or follow the direct link to <a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer nofollow" style="color:#818cf8;">{html.escape(url)}</a> to access the platform.</div>
          </div>
          <div class="faq-item">
            <div class="faq-q">What are the best alternatives to {html.escape(name)}?</div>
            <div class="faq-a">Top verified alternatives in the {html.escape(pill)} domain include {html.escape(related_names)}. You can discover more by filtering our global directory.</div>
          </div>
        </section>
      </div>

      <!-- Right Sidebar Column -->
      <aside class="sidebar-column">
        <!-- Quick Action Sidebar -->
        <div class="sidebar-card">
          <h3>Quick Access</h3>
          <p style="font-size:0.88rem; color:var(--text-muted);">Launch the official {html.escape(name)} portal in a new tab:</p>
          <a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer nofollow" class="sidebar-cta-btn">
            Open Tool ({html.escape(domain)}) &rarr;
          </a>
        </div>

        <!-- Related Tools -->
        <div class="card-box">
          <h2>Similar {html.escape(pill)} Tools</h2>
          <div class="related-list">
            {related_block}
          </div>
          <a href="/?category={cat_slug}" class="view-detail-link" style="display:inline-block; margin-top:10px; font-weight:600; color:#818cf8;">
            Browse all {html.escape(pill)} tools &rarr;
          </a>
        </div>

        <!-- Categories Sidebar -->
        <div class="card-box">
          <h2>Explore Categories</h2>
          <div class="cat-links-list">
            <a href="/?category=video-3d" class="cat-link-item"><span>Video &amp; 3D</span> <span>&rarr;</span></a>
            <a href="/?category=coding-dev" class="cat-link-item"><span>Coding &amp; Dev</span> <span>&rarr;</span></a>
            <a href="/?category=image-art" class="cat-link-item"><span>Image &amp; Art</span> <span>&rarr;</span></a>
            <a href="/?category=chat-reasoning" class="cat-link-item"><span>Chat &amp; Reasoning</span> <span>&rarr;</span></a>
            <a href="/?category=voice-audio" class="cat-link-item"><span>Voice &amp; Audio</span> <span>&rarr;</span></a>
            <a href="/?category=ai-search" class="cat-link-item"><span>AI Search</span> <span>&rarr;</span></a>
          </div>
        </div>
      </aside>
    </div>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-links">
        <a href="/">Directory</a>
        <a href="/?category=chat-reasoning">Chat &amp; Reasoning</a>
        <a href="/?category=coding-dev">Coding &amp; Dev</a>
        <a href="/?category=image-art">Image &amp; Art</a>
        <a href="/?category=video-3d">Video &amp; 3D</a>
        <a href="/?category=voice-audio">Voice &amp; Audio</a>
        <a href="/?category=ai-search">AI Search</a>
        <a href="/sitemap.xml">Sitemap</a>
        <a href="/robots.txt">Robots.txt</a>
      </div>
      <p>&copy; 2026 All AI Tools (allaitools.online). All rights reserved. Direct links open official platforms.</p>
    </div>
  </footer>

  <div class="toast" id="toast">Link copied to clipboard!</div>

  <script>
    (function() {{
      var toolName = {js_tool_name};
      var navSearch = document.getElementById('navSearchInput');
      if (navSearch) {{
        navSearch.addEventListener('keydown', function(e) {{
          if (e.key === 'Enter' && navSearch.value.trim()) {{
            window.location.href = '/?q=' + encodeURIComponent(navSearch.value.trim());
          }}
        }});
      }}

      // Bookmarking sync
      var bookmarkBtn = document.getElementById('heroBookmarkBtn');
      var saved = [];
      try {{
        saved = JSON.parse(localStorage.getItem('saved_ai_tools') || '[]');
      }} catch (e) {{}}

      function updateBookmarkUI() {{
        if (saved.indexOf(toolName) !== -1) {{
          bookmarkBtn.classList.add('saved');
          bookmarkBtn.innerHTML = '&#9733; Saved';
        }} else {{
          bookmarkBtn.classList.remove('saved');
          bookmarkBtn.innerHTML = '&#9734; Bookmark';
        }}
      }}
      updateBookmarkUI();

      bookmarkBtn.addEventListener('click', function() {{
        var idx = saved.indexOf(toolName);
        if (idx === -1) {{
          saved.push(toolName);
        }} else {{
          saved.splice(idx, 1);
        }}
        try {{
          localStorage.setItem('saved_ai_tools', JSON.stringify(saved));
        }} catch (e) {{}}
        updateBookmarkUI();
      }});

      // Share button
      var shareBtn = document.getElementById('shareBtn');
      var toast = document.getElementById('toast');
      shareBtn.addEventListener('click', function() {{
        if (navigator.clipboard) {{
          navigator.clipboard.writeText(window.location.href).then(function() {{
            showToast('Link copied to clipboard!');
          }});
        }} else {{
          showToast('URL: ' + window.location.href);
        }}
      }});

      function showToast(msg) {{
        toast.textContent = msg;
        toast.style.display = 'block';
        setTimeout(function() {{
          toast.style.display = 'none';
        }}, 3000);
      }}
    }})();
  </script>
</body>
</html>"""
    return page_html

print(f"Generating static HTML pages for {len(tools)} tools...")
generated_count = 0
for idx, tool in enumerate(tools):
    slug = tool['slug']
    html_page = render_tool_page(tool, tools)

    # 1. public/<slug>/index.html
    dir_path = os.path.join("public", slug)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_page)

    # 2. public/<slug>.html (to prevent any trailing slash redirect issues!)
    with open(os.path.join("public", f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html_page)

    generated_count += 1
    if generated_count % 200 == 0 or generated_count == len(tools):
        print(f"  Generated {generated_count}/{len(tools)} tool pages...")

print(f"Successfully generated all {generated_count} tool pages in public/<slug>/index.html and public/<slug>.html!")
