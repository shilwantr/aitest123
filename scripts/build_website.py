#!/usr/bin/env python3
"""
Build complete index.html with classy, elegant UI and all 200 categorized tools.
"""

import json
import html

with open("tools.json", "r", encoding="utf-8") as f:
    tools = json.load(f)

# Build schema
schema_items = []
for idx, t in enumerate(tools[:100], start=1):
    schema_items.append({
        "@type": "ListItem",
        "position": idx,
        "name": t["name"],
        "url": t["url"]
    })

schema_json = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "@id": "http://aallaitools.online/#website",
            "url": "http://aallaitools.online/",
            "name": "aallaitools.online",
            "description": "The definitive, fast, and comprehensive directory of 200+ worldwide artificial intelligence tools, models, and agents."
        },
        {
            "@type": "ItemList",
            "@id": "http://aallaitools.online/#featured",
            "name": "Exhaustive Global AI Tools & GPTs Directory",
            "numberOfItems": len(tools),
            "itemListElement": schema_items
        }
    ]
}, indent=2)

cards_html = []
for t in tools:
    subcat = t.get('subcategory') or t.get('category_section') or t.get('category_pill') or 'AI Tool'
    desc = t.get('description', '')
    name = t.get('name', 'AI Platform')
    pricing = t.get('pricing', 'Freemium')
    pill = t.get('category_pill', 'AI Tools')
    cat_slug = t.get('category_slug', 'chat-reasoning')
    color = t.get('color', '#4F46E5')
    badge = t.get('badge', 'AI')
    url = t.get('url', '#')

    search_blob = f"{name} {subcat} {desc} {pill} {pricing}".lower()
    price_class = pricing.lower().replace(' ', '-')
    card = f"""        <article class="tool-card" data-category="{cat_slug}" data-pricing="{price_class}" data-name="{html.escape(name)}" data-search="{html.escape(search_blob)}">
          <div class="card-top">
            <div class="tool-badge" style="background:{color}">{html.escape(badge)}</div>
            <div class="top-meta">
              <span class="price-pill price-{price_class}">{html.escape(pricing)}</span>
              <button class="bookmark-btn" aria-label="Bookmark {html.escape(name)}" data-tool="{html.escape(name)}">&#9734;</button>
            </div>
          </div>
          <span class="tool-subcat">{html.escape(subcat)}</span>
          <h3 class="tool-name">{html.escape(name)}</h3>
          <p class="tool-desc">{html.escape(desc)}</p>
          <div class="card-bottom">
            <span class="cat-pill">{html.escape(pill)}</span>
            <a href="{html.escape(url)}" class="visit-btn" target="_blank" rel="noopener noreferrer">Visit Tool &rarr;</a>
          </div>
        </article>"""
    cards_html.append(card)

cards_block = "\n".join(cards_html)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>All AI Tools — Exhaustive Global Directory of 200+ AI Tools &amp; Agents | aallaitools.online</title>
  <meta name="description" content="Discover, compare, and filter 200+ verified worldwide artificial intelligence tools, reasoning models, custom GPTs, and autonomous agents across Chat, Coding, Image, Voice, Video &amp; AI Search." />
  <link rel="canonical" href="http://aallaitools.online/" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="All AI Tools — The Exhaustive Global AI Directory" />
  <meta property="og:description" content="The definitive index of 200+ verified artificial intelligence software, models, and agents." />
  <meta property="og:url" content="http://aallaitools.online/" />

  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
{schema_json}
  </script>

  <style>
    :root {{
      --bg: #090d16;
      --bg-card: #111827;
      --bg-card-hover: #172033;
      --bg-subtle: #1e293b;
      --border: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(99, 102, 241, 0.5);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --primary-glow: rgba(99, 102, 241, 0.25);
      --accent: #8b5cf6;
      --accent-pink: #ec4899;
      --accent-green: #10b981;
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --radius-pill: 9999px;
      --shadow-card: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
      --shadow-hover: 0 12px 30px -4px rgba(99, 102, 241, 0.2);
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
      background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
      color: #fff;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.95rem;
      box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
    }}
    .live-badge {{
      font-size: 0.72rem;
      font-weight: 700;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.25);
      padding: 3px 10px;
      border-radius: var(--radius-pill);
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .nav-links {{ display: flex; align-items: center; gap: 26px; font-size: 0.92rem; font-weight: 500; color: var(--text-muted); }}
    .nav-links a:hover {{ color: #fff; }}
    .nav-actions {{ display: flex; align-items: center; gap: 14px; }}
    .btn-saved {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: var(--text-main);
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
      max-width: 720px;
      margin: 0 auto 34px;
      color: var(--text-muted);
      font-size: 1.12rem;
      line-height: 1.6;
    }}

    /* Global Search Bar */
    .search-box-wrap {{
      max-width: 680px;
      margin: 0 auto 24px;
      position: relative;
    }}
    .search-box {{
      width: 100%;
      padding: 18px 52px 18px 54px;
      font-size: 1.02rem;
      background: rgba(17, 24, 39, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: var(--radius-pill);
      color: #fff;
      outline: none;
      box-shadow: 0 4px 25px rgba(0, 0, 0, 0.4);
      transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
    }}
    .search-box::placeholder {{ color: var(--text-sub); }}
    .search-box:focus {{
      background: rgba(17, 24, 39, 0.98);
      border-color: #818cf8;
      box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2), 0 8px 30px rgba(0, 0, 0, 0.6);
    }}
    .search-icon {{
      position: absolute;
      left: 20px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-sub);
      font-size: 1.15rem;
      pointer-events: none;
    }}
    .search-hint {{
      position: absolute;
      right: 18px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--text-sub);
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      padding: 3px 8px;
      border-radius: 6px;
      pointer-events: none;
    }}
    .clear-search {{
      position: absolute;
      right: 50px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-sub);
      font-size: 1.1rem;
      cursor: pointer;
      display: none;
    }}
    .clear-search:hover {{ color: #fff; }}

    /* Pricing Chips Bar */
    .filter-pricing-row {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 8px;
      margin-bottom: 18px;
    }}
    .price-chip {{
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.03);
      color: var(--text-muted);
      font-size: 0.8rem;
      font-weight: 600;
      padding: 5px 13px;
      border-radius: var(--radius-pill);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .price-chip:hover {{ background: rgba(255, 255, 255, 0.08); color: #fff; }}
    .price-chip.active {{
      background: rgba(99, 102, 241, 0.2);
      border-color: rgba(99, 102, 241, 0.5);
      color: #c7d2fe;
    }}

    /* Category Filter Pills */
    .filter-pills-row {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      margin-bottom: 28px;
    }}
    .filter-pill {{
      border: 1px solid var(--border);
      background: rgba(17, 24, 39, 0.7);
      color: var(--text-muted);
      font-size: 0.86rem;
      font-weight: 600;
      padding: 9px 18px;
      border-radius: var(--radius-pill);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s ease;
    }}
    .filter-pill:hover {{
      border-color: rgba(255, 255, 255, 0.2);
      color: #fff;
      background: rgba(255, 255, 255, 0.05);
    }}
    .filter-pill.active {{
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      color: #fff;
      border-color: transparent;
      box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
    }}
    .pill-count {{
      font-size: 0.72rem;
      background: rgba(0, 0, 0, 0.3);
      padding: 2px 7px;
      border-radius: 999px;
      opacity: 0.9;
    }}

    /* Trust Stats Bar */
    .trust-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 32px;
      font-size: 0.86rem;
      color: var(--text-sub);
      font-weight: 500;
      padding-top: 14px;
    }}
    .trust-bar strong {{ color: var(--text-main); font-weight: 700; }}

    /* Directory Main Area */
    .section {{ padding: 52px 0 64px; }}
    .section-header {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      margin-bottom: 32px;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .section-title {{ font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em; color: #fff; }}
    .section-sub {{ color: var(--text-muted); font-size: 0.96rem; margin-top: 6px; }}
    .results-badge {{
      font-size: 0.86rem;
      font-weight: 700;
      color: #a5b4fc;
      background: rgba(99, 102, 241, 0.12);
      border: 1px solid rgba(99, 102, 241, 0.25);
      padding: 7px 16px;
      border-radius: var(--radius-pill);
    }}

    /* Tool Cards Grid */
    .tools-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 22px;
    }}
    .tool-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 24px;
      display: flex;
      flex-direction: column;
      position: relative;
      box-shadow: var(--shadow-card);
      transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.18s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.18s ease;
    }}
    .tool-card:hover {{
      transform: translateY(-3px);
      background: var(--bg-card-hover);
      border-color: rgba(99, 102, 241, 0.35);
      box-shadow: var(--shadow-hover);
    }}
    .card-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }}
    .tool-badge {{
      width: 44px;
      height: 44px;
      border-radius: 12px;
      color: #fff;
      font-weight: 800;
      font-size: 0.95rem;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      letter-spacing: -0.02em;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
    }}
    .top-meta {{ display: flex; align-items: center; gap: 8px; }}
    .price-pill {{
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
    .cat-pill {{
      font-size: 0.76rem;
      font-weight: 600;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.04);
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }}
    .visit-btn {{
      font-size: 0.86rem;
      font-weight: 700;
      color: #a5b4fc;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: gap 0.15s ease, color 0.15s ease;
    }}
    .visit-btn:hover {{ color: #ffffff; gap: 8px; }}

    /* Empty state */
    .empty-state {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 64px 20px;
      background: var(--bg-card);
      border: 1px dashed var(--border);
      border-radius: var(--radius-lg);
      display: none;
    }}
    .empty-state h3 {{ font-size: 1.3rem; margin-bottom: 8px; color: #fff; }}
    .empty-state p {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 18px; }}

    /* Explore by Category Showcase */
    .cat-showcase-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 20px;
      margin-top: 12px;
    }}
    .cat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
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

    /* Architecture Value Grid */
    .arch-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 24px;
      margin-top: 28px;
    }}
    .arch-box {{
      padding: 28px;
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      background: var(--bg-card);
    }}
    .arch-box h3 {{ font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 10px; }}
    .arch-box p {{ font-size: 0.92rem; color: var(--text-muted); line-height: 1.6; }}

    /* FAQ Section */
    .faq-wrap {{ max-width: 860px; margin: 0 auto; display: flex; flex-direction: column; gap: 14px; }}
    .faq-item {{
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg-card);
      overflow: hidden;
      transition: border-color 0.15s;
    }}
    .faq-item:hover {{ border-color: rgba(255, 255, 255, 0.15); }}
    .faq-q {{
      width: 100%;
      text-align: left;
      padding: 20px 24px;
      background: none;
      border: none;
      font-size: 1.02rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
    }}
    .faq-q span {{ font-size: 1.3rem; color: var(--primary); transition: transform 0.2s; }}
    .faq-a {{
      padding: 0 24px 22px;
      font-size: 0.94rem;
      color: var(--text-muted);
      line-height: 1.6;
      display: none;
    }}
    .faq-item.open .faq-a {{ display: block; }}
    .faq-item.open .faq-q span {{ transform: rotate(45deg); }}

    /* CTA Banner */
    .cta-banner {{
      background: radial-gradient(circle at 50% 50%, #4338ca 0%, #312e81 100%);
      border: 1px solid rgba(99, 102, 241, 0.35);
      border-radius: 24px;
      padding: 64px 32px;
      text-align: center;
      margin: 64px 0 32px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }}
    .cta-banner h2 {{ font-size: 2.1rem; font-weight: 800; color: #fff; margin-bottom: 14px; }}
    .cta-banner p {{ font-size: 1.05rem; color: #e0e7ff; max-width: 620px; margin: 0 auto 28px; line-height: 1.6; }}
    .btn-white {{
      display: inline-block;
      background: #ffffff;
      color: #312e81;
      font-weight: 700;
      font-size: 0.95rem;
      padding: 14px 30px;
      border-radius: var(--radius-pill);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
      transition: transform 0.15s ease;
    }}
    .btn-white:hover {{ transform: scale(1.03); }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border);
      padding: 64px 0 36px;
      margin-top: 60px;
      font-size: 0.88rem;
      color: var(--text-muted);
      background: rgba(13, 18, 30, 0.7);
    }}
    .footer-grid {{
      display: grid;
      grid-template-columns: 1.6fr 1fr 1fr 1.2fr;
      gap: 36px;
      margin-bottom: 44px;
    }}
    .footer-col h4 {{
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #fff;
      margin-bottom: 16px;
    }}
    .footer-col ul {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}
    .footer-col ul a:hover {{ color: #fff; }}
    .footer-bottom {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 28px;
      border-top: 1px solid var(--border);
      font-size: 0.82rem;
      color: var(--text-sub);
      flex-wrap: wrap;
      gap: 14px;
    }}

    @media (max-width: 900px) {{
      .nav-links {{ display: none; }}
      .footer-grid {{ grid-template-columns: 1fr 1fr; }}
      .tools-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="ambient-glow"></div>

  <!-- Sticky Top Navbar -->
  <header class="navbar">
    <div class="container nav-inner">
      <a href="#" class="brand">
        <span class="brand-icon">AI</span>
        <span>aallaitools.online</span>
        <span class="live-badge">200+ Verified</span>
      </a>
      <nav class="nav-links" aria-label="Main Navigation">
        <a href="#featured">Directory</a>
        <a href="#categories">Categories</a>
        <a href="#faq">FAQ</a>
        <a href="/sitemap.xml">Sitemap</a>
        <a href="/robots.txt">Robots</a>
      </nav>
      <div class="nav-actions">
        <button id="show-saved-btn" class="btn-saved" title="View Bookmarked Tools">
          &#9733; Saved (<span id="saved-count">0</span>)
        </button>
        <a href="#submit" class="btn-submit">+ Submit Tool</a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="container">
      <div class="hero-eyebrow">&#9889; Complete Exhaustive Global Directory &bull; Fast &amp; Live</div>
      <h1>The World's Definitive <span class="gradient-text">AI Tools &amp; Agents</span> Index</h1>
      <p class="hero-sub">Explore, search, and benchmark 200+ verified frontier artificial intelligence platforms, reasoning models, custom GPTs, and autonomous agents.</p>

      <!-- Search Input -->
      <div class="search-box-wrap">
        <span class="search-icon">&#128269;</span>
        <input type="search" id="tool-search" class="search-box" placeholder="Search 200+ AI tools (e.g., Cursor, DeepSeek, Suno, Sora, Flux, Devin)..." aria-label="Search AI tools" autofocus />
        <button id="clear-search-btn" class="clear-search" aria-label="Clear search">&times;</button>
        <span class="search-hint">Press / to search</span>
      </div>

      <!-- Pricing Filter Chips -->
      <div class="filter-pricing-row" role="tablist" aria-label="Filter by pricing tier">
        <button class="price-chip active" data-pricing="all">All Tiers</button>
        <button class="price-chip" data-pricing="freemium">Freemium</button>
        <button class="price-chip" data-pricing="free">100% Free</button>
        <button class="price-chip" data-pricing="paid">Commercial / Paid</button>
      </div>

      <!-- Category Filter Pills -->
      <div class="filter-pills-row" role="tablist" aria-label="Filter by category">
        <button class="filter-pill active" data-filter="all">All Categories <span class="pill-count">200</span></button>
        <button class="filter-pill" data-filter="chat-reasoning">Chat &amp; Reasoning <span class="pill-count">35</span></button>
        <button class="filter-pill" data-filter="coding-dev">Coding &amp; Dev <span class="pill-count">35</span></button>
        <button class="filter-pill" data-filter="image-art">Image &amp; Art <span class="pill-count">35</span></button>
        <button class="filter-pill" data-filter="voice-audio">Voice &amp; Audio <span class="pill-count">30</span></button>
        <button class="filter-pill" data-filter="video-3d">Video &amp; 3D <span class="pill-count">35</span></button>
        <button class="filter-pill" data-filter="ai-search">AI Search &amp; Research <span class="pill-count">30</span></button>
      </div>

      <!-- Trust Bar -->
      <div class="trust-bar">
        <span>&#9889; <strong>&lt; 50ms</strong> First Paint</span>
        <span>&#129302; <strong>GPTBot &amp; Crawler</strong> Ready</span>
        <span>&#128194; <strong>JSON-LD ItemList</strong> Schema</span>
        <span>&#128260; <strong>Daily</strong> Live Indexing</span>
      </div>
    </div>
  </section>

  <!-- Main Directory Section -->
  <main id="featured" class="section">
    <div class="container">
      <div class="section-header">
        <div>
          <h2 class="section-title">Directory of AI Tools</h2>
          <p class="section-sub">Real-time faceted filtering across categories, pricing models, and search keywords</p>
        </div>
        <span id="results-counter" class="results-badge">Showing 200 Verified Tools</span>
      </div>

      <!-- Empty State -->
      <div id="empty-state" class="empty-state">
        <h3>No tools match your criteria</h3>
        <p>Try clearing your search query or switching category/pricing filters.</p>
        <button id="reset-filters-btn" class="filter-pill active" style="display:inline-flex;">Reset All Filters</button>
      </div>

      <!-- 200 Tools Grid -->
      <div id="tools-grid" class="tools-grid">
{cards_block}
      </div>
    </div>
  </main>

  <!-- Category Showcase Cards -->
  <section id="categories" class="section" style="border-top: 1px solid var(--border);">
    <div class="container">
      <div class="section-header">
        <div>
          <h2 class="section-title">Explore by Domain</h2>
          <p class="section-sub">High-signal indexing optimized for human discovery, autonomous crawlers, and LLM browsing agents.</p>
        </div>
      </div>

      <div class="cat-showcase-grid">
        <div class="cat-card" data-jump="chat-reasoning">
          <div>
            <h3>&#9997;&#65039; Chat &amp; Reasoning</h3>
            <p>Frontier LLMs, mathematical reasoning engines, academic writing copilot, and team workspace agents.</p>
          </div>
          <div class="cat-card-meta"><span>35 Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="coding-dev">
          <div>
            <h3>&#128187; Software &amp; Coding</h3>
            <p>Agentic IDEs, autonomous SWEs, in-browser full-stack generators, and local LLM runners.</p>
          </div>
          <div class="cat-card-meta"><span>35 Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="image-art">
          <div>
            <h3>&#127912; Image &amp; Visual Arts</h3>
            <p>Photorealistic synthesis, typography rendering, 8K hallucination upscalers, and vector graphic studios.</p>
          </div>
          <div class="cat-card-meta"><span>35 Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="voice-audio">
          <div>
            <h3>&#127897;&#65039; Voice &amp; Audio Synthesis</h3>
            <p>Sub-100ms voice streaming, full-song AI music, voice cloning, and AI podcast mastering.</p>
          </div>
          <div class="cat-card-meta"><span>30 Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="video-3d">
          <div>
            <h3>&#127909; Video &amp; Motion FX</h3>
            <p>World simulation video, high-motion camera controls, photoreal avatars, and 3D mesh auto-rigging.</p>
          </div>
          <div class="cat-card-meta"><span>35 Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="ai-search">
          <div>
            <h3>&#128269; Research &amp; Deep Search</h3>
            <p>Fact-grounded conversational search, systematic paper review agents, and citation verification graphs.</p>
          </div>
          <div class="cat-card-meta"><span>30 Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
      </div>

      <!-- Architecture Value Props -->
      <div class="arch-grid">
        <div class="arch-box">
          <h3>Sub-50ms Static Performance</h3>
          <p>Built with pure semantic HTML5 and vanilla CSS. Zero bulky JavaScript frameworks, zero external tracking tags, ensuring instantaneous First Contentful Paint globally.</p>
        </div>
        <div class="arch-box">
          <h3>Exhaustive &amp; Verified</h3>
          <p>Every tool listing is cross-checked against canonical domains, verified for HTTP 200 availability, and updated with current pricing and capabilities.</p>
        </div>
        <div class="arch-box">
          <h3>Agent &amp; Bot Friendly</h3>
          <p>Complete JSON-LD Schema ItemList and transparent robots.txt permissions empower ChatGPT, Claude, and Googlebot to ingest this entire directory seamlessly.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Section -->
  <section id="faq" class="section" style="border-top: 1px solid var(--border);">
    <div class="container">
      <div class="section-header" style="justify-content:center; text-align:center;">
        <div>
          <h2 class="section-title">Frequently Asked Questions</h2>
          <p class="section-sub">Everything you need to know about navigating the global AI tools ecosystem</p>
        </div>
      </div>

      <div class="faq-wrap">
        <div class="faq-item open">
          <button class="faq-q">What makes aallaitools.online different from other directories? <span>+</span></button>
          <div class="faq-a">Unlike bloated directories laden with ad networks and slow frameworks, aallaitools.online is engineered as an ultra-fast, zero-bloat static reference. It indexes 200+ verified tools worldwide with real-time multi-dimensional search and verified pricing models.</div>
        </div>
        <div class="faq-item">
          <button class="faq-q">How do I filter by free or open-source AI tools? <span>+</span></button>
          <div class="faq-a">Simply click the "100% Free" filter chip at the top of the directory. You can combine it with any category pill (e.g., Coding &amp; Dev) to instantly view open-weight and free tools like Ollama, DeepSeek, Whisper, and ComfyUI.</div>
        </div>
        <div class="faq-item">
          <button class="faq-q">How can AI search agents and LLMs access this dataset? <span>+</span></button>
          <div class="faq-a">Our robots.txt explicitly welcomes GPTBot, ClaudeBot, PerplexityBot, Google-Extended, and other autonomous web agents. Additionally, structured JSON-LD ItemList data and a machine-readable sitemap.xml are continuously published.</div>
        </div>
        <div class="faq-item">
          <button class="faq-q">How do I bookmark tools for later? <span>+</span></button>
          <div class="faq-a">Click the star icon (&#9734;) on any tool card to save it. Your saved stack persists in your local browser storage. Click the "Saved" button in the top navbar anytime to view your curated collection.</div>
        </div>
      </div>

      <!-- CTA -->
      <div id="submit" class="cta-banner">
        <h2>Submit an AI Tool or Agent</h2>
        <p>Are you building frontier artificial intelligence software? Get your platform in front of thousands of daily engineers, founders, and researchers.</p>
        <a href="mailto:submit@aallaitools.online?subject=Submit%20AI%20Tool" class="btn-white">Submit Your Tool Now &rarr;</a>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <a href="#" class="brand" style="margin-bottom:14px;">
            <span class="brand-icon">AI</span>
            <span>aallaitools.online</span>
          </a>
          <p>The definitive index of 200+ verified artificial intelligence platforms, reasoning models, custom GPTs, and autonomous agents.</p>
        </div>
        <div class="footer-col">
          <h4>Directory Categories</h4>
          <ul>
            <li><a href="#featured">Chat &amp; Frontier Reasoning</a></li>
            <li><a href="#featured">Coding &amp; Autonomous Agents</a></li>
            <li><a href="#featured">Image &amp; Vector Studios</a></li>
            <li><a href="#featured">Voice, Audio &amp; Music</a></li>
            <li><a href="#featured">Video, Motion FX &amp; 3D</a></li>
            <li><a href="#featured">AI Deep Search &amp; Research</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Machine Indexing</h4>
          <ul>
            <li><a href="/robots.txt">robots.txt Crawler Rules</a></li>
            <li><a href="/sitemap.xml">sitemap.xml Index</a></li>
            <li><a href="http://aallaitools.online/">Canonical Endpoint</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>About &amp; Architecture</h4>
          <p>Hosted at <strong>http://aallaitools.online</strong>.<br />Engineered with semantic HTML5, zero external scripts, and sub-50ms static delivery.</p>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 aallaitools.online. All rights reserved.</span>
        <span>Ultra-fast static web architecture.</span>
      </div>
    </div>
  </footer>

  <!-- Instant Search, Filtering & Bookmarking Engine -->
  <script>
    (function () {{
      var searchInput = document.getElementById('tool-search');
      var clearBtn = document.getElementById('clear-search-btn');
      var categoryPills = document.querySelectorAll('.filter-pill');
      var priceChips = document.querySelectorAll('.price-chip');
      var cards = document.querySelectorAll('.tool-card');
      var counter = document.getElementById('results-counter');
      var emptyState = document.getElementById('empty-state');
      var resetBtn = document.getElementById('reset-filters-btn');
      var showSavedBtn = document.getElementById('show-saved-btn');
      var savedCountEl = document.getElementById('saved-count');

      var activeCategory = 'all';
      var activePricing = 'all';
      var filterOnlySaved = false;

      // LocalStorage Bookmarks
      var savedTools = [];
      try {{
        savedTools = JSON.parse(localStorage.getItem('saved_ai_tools') || '[]');
      }} catch (e) {{
        savedTools = [];
      }}

      function updateSavedUI() {{
        savedCountEl.textContent = savedTools.length;
        document.querySelectorAll('.bookmark-btn').forEach(function (btn) {{
          var name = btn.getAttribute('data-tool');
          if (savedTools.indexOf(name) !== -1) {{
            btn.classList.add('saved');
            btn.innerHTML = '&#9733;';
          }} else {{
            btn.classList.remove('saved');
            btn.innerHTML = '&#9734;';
          }}
        }});
      }}

      function filterTools() {{
        var q = (searchInput.value || '').toLowerCase().trim();
        clearBtn.style.display = q ? 'block' : 'none';
        var visible = 0;

        cards.forEach(function (card) {{
          var cat = card.getAttribute('data-category');
          var price = card.getAttribute('data-pricing');
          var name = card.getAttribute('data-name');
          var searchBlob = card.getAttribute('data-search');

          var matchesCat = (activeCategory === 'all' || cat === activeCategory);
          var matchesPrice = (activePricing === 'all' || price === activePricing);
          var matchesQuery = (!q || searchBlob.indexOf(q) !== -1);
          var matchesSaved = (!filterOnlySaved || savedTools.indexOf(name) !== -1);

          if (matchesCat && matchesPrice && matchesQuery && matchesSaved) {{
            card.style.display = 'flex';
            visible++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        counter.textContent = 'Showing ' + visible + ' Verified Tool' + (visible === 1 ? '' : 's');
        emptyState.style.display = (visible === 0) ? 'block' : 'none';
      }}

      // Keyboard Shortcut '/' to focus search
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

      // Search input
      searchInput.addEventListener('input', filterTools);
      clearBtn.addEventListener('click', function () {{
        searchInput.value = '';
        searchInput.focus();
        filterTools();
      }});

      // Category filter pills
      categoryPills.forEach(function (pill) {{
        pill.addEventListener('click', function () {{
          categoryPills.forEach(function (p) {{ p.classList.remove('active'); }});
          pill.classList.add('active');
          activeCategory = pill.getAttribute('data-filter');
          filterOnlySaved = false;
          showSavedBtn.style.background = '';
          filterTools();
        }});
      }});

      // Pricing filter chips
      priceChips.forEach(function (chip) {{
        chip.addEventListener('click', function () {{
          priceChips.forEach(function (c) {{ c.classList.remove('active'); }});
          chip.classList.add('active');
          activePricing = chip.getAttribute('data-pricing');
          filterTools();
        }});
      }});

      // Category jump from cards
      document.querySelectorAll('.cat-card').forEach(function (catCard) {{
        catCard.addEventListener('click', function () {{
          var targetCat = catCard.getAttribute('data-jump');
          var targetPill = document.querySelector('.filter-pill[data-filter="' + targetCat + '"]');
          if (targetPill) targetPill.click();
          document.getElementById('featured').scrollIntoView({{ behavior: 'smooth' }});
        }});
      }});

      // Reset button
      resetBtn.addEventListener('click', function () {{
        searchInput.value = '';
        activeCategory = 'all';
        activePricing = 'all';
        filterOnlySaved = false;
        showSavedBtn.style.background = '';
        categoryPills.forEach(function (p) {{ p.classList.remove('active'); }});
        document.querySelector('.filter-pill[data-filter="all"]').classList.add('active');
        priceChips.forEach(function (c) {{ c.classList.remove('active'); }});
        document.querySelector('.price-chip[data-pricing="all"]').classList.add('active');
        filterTools();
      }});

      // Bookmark / Save buttons
      document.querySelectorAll('.bookmark-btn').forEach(function (btn) {{
        btn.addEventListener('click', function (e) {{
          e.stopPropagation();
          var name = btn.getAttribute('data-tool');
          var idx = savedTools.indexOf(name);
          if (idx === -1) {{
            savedTools.push(name);
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

      updateSavedUI();
    }})();
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated classy modern index.html with 200 tools!")
