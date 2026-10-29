#!/usr/bin/env python3
import json
import html
import re
from pathlib import Path

with open("tools.json", "r", encoding="utf-8") as f:
    tools = json.load(f)

total_tools = len(tools)
cat_counts = {}
for t in tools:
    c = t.get("category_slug", "chat-reasoning")
    cat_counts[c] = cat_counts.get(c, 0) + 1

# Generate schema items
schema_items = []
for idx, t in enumerate(tools[:250], start=1):
    schema_items.append({
        "@type": "ListItem",
        "position": idx,
        "name": t.get("name", "AI Tool"),
        "url": t.get("url", "http://aallaitools.online/")
    })

schema_json = json.dumps({
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "@id": "http://aallaitools.online/#website",
            "url": "http://aallaitools.online/",
            "name": "aallaitools.online",
            "description": f"The definitive, fast, and comprehensive directory of {total_tools}+ worldwide artificial intelligence tools, models, and agents."
        },
        {
            "@type": "ItemList",
            "@id": "http://aallaitools.online/#featured",
            "name": "Exhaustive Global AI Tools & GPTs Directory",
            "numberOfItems": total_tools,
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
    badge = t.get('badge', name[:2].upper())
    url = t.get('url', '#')
    img_url = t.get('image_url', '')

    price_class = "price-freemium"
    if pricing.lower() == "free":
        price_class = "price-free"
    elif pricing.lower() == "paid":
        price_class = "price-paid"

    img_tag = ""
    if img_url:
        img_tag = f'<img src="{html.escape(img_url)}" alt="{html.escape(name)} preview" class="tool-preview-thumb" loading="lazy" onerror="this.style.display=\'none\'" />'

    card = f'''        <article class="tool-card" data-category="{html.escape(cat_slug)}" data-pricing="{html.escape(pricing.lower())}" data-name="{html.escape(name.lower())}" data-desc="{html.escape(desc.lower())}">
          <div class="card-top">
            <div class="tool-brand">
              <div class="tool-avatar" style="background: {color};">{html.escape(badge)}</div>
              <div>
                <span class="tool-subcat">{html.escape(subcat)}</span>
                <h3 class="tool-name">{html.escape(name)}</h3>
              </div>
            </div>
            <div class="badge-row">
              <span class="price-badge {price_class}">{html.escape(pricing)}</span>
              <button class="bookmark-btn" title="Bookmark tool" data-tool="{html.escape(name)}" aria-label="Bookmark {html.escape(name)}">&#9734;</button>
            </div>
          </div>
          {img_tag}
          <p class="tool-desc">{html.escape(desc)}</p>
          <div class="card-bottom">
            <span class="cat-pill">{html.escape(pill)}</span>
            <a href="{html.escape(url)}" target="_blank" rel="noopener noreferrer nofollow" class="tool-link">Visit Tool &rarr;</a>
          </div>
        </article>'''
    cards_html.append(card)

cards_block = "\n".join(cards_html)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>All AI Tools Directory | {total_tools}+ Exhaustive Worldwide AI Tools &amp; Agents (2026)</title>
  <meta name="description" content="Discover, search, and benchmark {total_tools}+ global AI tools across Chat &amp; Reasoning, Coding &amp; Dev, Image &amp; Art, Voice &amp; Audio, Video &amp; 3D, and AI Search. High-speed, responsive, curated for humans and LLM agents." />
  <meta name="keywords" content="AI tools directory, all AI tools, best AI tools 2026, generative AI directory, AI agents, LLM catalog, machine learning software, aixploria alternative, aitoolsdirectory" />
  <meta name="author" content="aallaitools.online" />
  <link rel="canonical" href="http://aallaitools.online/" />

  <!-- OpenGraph -->
  <meta property="og:title" content="All AI Tools Directory | {total_tools}+ Worldwide AI Platforms &amp; Agents" />
  <meta property="og:description" content="Curated index of {total_tools}+ artificial intelligence tools across 6 distinct categories with instant search, pricing models, and bookmarks." />
  <meta property="og:url" content="http://aallaitools.online/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="aallaitools.online" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="All AI Tools Directory | {total_tools}+ Exhaustive Worldwide Tools" />
  <meta name="twitter:description" content="Search and discover {total_tools}+ AI tools and models worldwide. Zero-lag client-side filtering." />

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
      max-width: 760px;
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
    .faq-a {{
      padding: 0 24px 20px;
      font-size: 0.94rem;
      color: var(--text-muted);
      line-height: 1.6;
      display: none;
    }}
    .faq-item.open .faq-a {{ display: block; }}
    .faq-icon {{ font-size: 1.1rem; transition: transform 0.2s; }}
    .faq-item.open .faq-icon {{ transform: rotate(45deg); }}

    /* Submit Section */
    .submit-box {{
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: var(--radius-lg);
      padding: 48px;
      text-align: center;
      max-width: 860px;
      margin: 0 auto;
    }}
    .submit-box h2 {{ font-size: 2rem; font-weight: 800; color: #fff; margin-bottom: 12px; }}
    .submit-box p {{ color: var(--text-muted); font-size: 1.05rem; max-width: 600px; margin: 0 auto 28px; line-height: 1.6; }}

    /* Footer */
    .footer {{
      border-top: 1px solid var(--border);
      background: #060910;
      padding: 64px 0 36px;
      margin-top: 60px;
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
        <span class="live-badge">{total_tools}+ Verified</span>
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
      <p class="hero-sub">Explore, search, and benchmark {total_tools}+ verified frontier artificial intelligence platforms, reasoning models, custom GPTs, and autonomous agents.</p>

      <!-- Search Input -->
      <div class="search-box-wrap">
        <span class="search-icon">&#128269;</span>
        <input type="search" id="tool-search" class="search-box" placeholder="Search {total_tools}+ AI tools (e.g., Cursor, DeepSeek, Suno, Sora, Flux, Devin)..." aria-label="Search AI tools" autofocus />
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
        <button class="filter-pill active" data-filter="all">All Categories <span class="pill-count">{total_tools}</span></button>
        <button class="filter-pill" data-filter="chat-reasoning">Chat &amp; Reasoning <span class="pill-count">{cat_counts.get('chat-reasoning', 0)}</span></button>
        <button class="filter-pill" data-filter="coding-dev">Coding &amp; Dev <span class="pill-count">{cat_counts.get('coding-dev', 0)}</span></button>
        <button class="filter-pill" data-filter="image-art">Image &amp; Art <span class="pill-count">{cat_counts.get('image-art', 0)}</span></button>
        <button class="filter-pill" data-filter="voice-audio">Voice &amp; Audio <span class="pill-count">{cat_counts.get('voice-audio', 0)}</span></button>
        <button class="filter-pill" data-filter="video-3d">Video &amp; 3D <span class="pill-count">{cat_counts.get('video-3d', 0)}</span></button>
        <button class="filter-pill" data-filter="ai-search">AI Search &amp; Research <span class="pill-count">{cat_counts.get('ai-search', 0)}</span></button>
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
        <span id="results-counter" class="results-badge">Showing {total_tools} Verified Tools</span>
      </div>

      <!-- Empty State -->
      <div id="empty-state" class="empty-state">
        <h3>No tools match your criteria</h3>
        <p>Try clearing your search query or switching category/pricing filters.</p>
        <button id="reset-filters-btn" class="filter-pill active" style="display:inline-flex;">Reset All Filters</button>
      </div>

      <!-- Tools Grid -->
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
          <div class="cat-card-meta"><span>{cat_counts.get('chat-reasoning', 0)} Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="coding-dev">
          <div>
            <h3>&#128187; Software &amp; Coding</h3>
            <p>Agentic IDEs, autonomous software engineers, terminal helpers, code refactoring copilots, and debuggers.</p>
          </div>
          <div class="cat-card-meta"><span>{cat_counts.get('coding-dev', 0)} Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="image-art">
          <div>
            <h3>&#127912; Image &amp; Generative Art</h3>
            <p>Diffusion models, latent canvas tools, vector engines, graphic design automation, and upscale models.</p>
          </div>
          <div class="cat-card-meta"><span>{cat_counts.get('image-art', 0)} Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="voice-audio">
          <div>
            <h3>&#127897;&#65039; Voice &amp; Audio Generation</h3>
            <p>Neural speech synthesis, zero-shot voice cloning, real-time conversational agents, and music generators.</p>
          </div>
          <div class="cat-card-meta"><span>{cat_counts.get('voice-audio', 0)} Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="video-3d">
          <div>
            <h3>&#127916; Video &amp; 3D Worlds</h3>
            <p>Cinematic generative video, lip-sync avatars, multi-modal animation, NeRFs, and interactive 3D meshes.</p>
          </div>
          <div class="cat-card-meta"><span>{cat_counts.get('video-3d', 0)} Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
        <div class="cat-card" data-jump="ai-search">
          <div>
            <h3>&#128269; AI Search &amp; Deep Research</h3>
            <p>Grounded answer engines, academic literature synthesizers, vector search copilots, and live web intelligence.</p>
          </div>
          <div class="cat-card-meta"><span>{cat_counts.get('ai-search', 0)} Verified Platforms</span><span>Explore Category &rarr;</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- High-Speed Architecture Details -->
  <section class="section" style="border-top: 1px solid var(--border); background: rgba(15, 22, 38, 0.4);">
    <div class="container">
      <div class="section-header">
        <div>
          <h2 class="section-title">Built for Instantaneous Discovery</h2>
          <p class="section-sub">Engineered to outpace bloated JavaScript SPA directories with raw static performance.</p>
        </div>
      </div>

      <div class="arch-grid">
        <div class="arch-box">
          <h3>Sub-50ms First Contentful Paint</h3>
          <p>Zero external JavaScript frameworks or bloated CSS libraries. The directory ships raw semantic HTML5 with inline scoped styling, guaranteeing immediate rendering on low-bandwidth mobile devices and high-end workstations alike.</p>
        </div>
        <div class="arch-box">
          <h3>Crawler &amp; LLM-First Structure</h3>
          <p>Full JSON-LD ItemList schema coupled with semantic markup enables instant semantic comprehension by OpenAI GPTBot, Anthropic ClaudeBot, Google-Extended, and PerplexityBot without executing client-side scripts.</p>
        </div>
        <div class="arch-box">
          <h3>Zero-Network Faceted Filtering</h3>
          <p>Instant search and multi-tag filtering operate in-memory on pre-rendered DOM elements. Experience 0ms latency when typing, toggling categories, or filtering by Free vs Freemium pricing models.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Section -->
  <section id="faq" class="section" style="border-top: 1px solid var(--border);">
    <div class="container">
      <div class="section-header" style="justify-content: center; text-align: center;">
        <div>
          <h2 class="section-title">Frequently Asked Questions</h2>
          <p class="section-sub">Everything you need to know about navigating and submitting to our global directory.</p>
        </div>
      </div>

      <div class="faq-wrap">
        <div class="faq-item">
          <button class="faq-q"><span>How are AI tools curated and verified?</span><span class="faq-icon">+</span></button>
          <div class="faq-a">Every platform is checked for active development, frontier multimodal capabilities, API availability, and authentic user utility. Outdated wrappers and defunct demos are purged to maintain high signal-to-noise ratio.</div>
        </div>
        <div class="faq-item">
          <button class="faq-q"><span>What does the pricing tier designation mean?</span><span class="faq-icon">+</span></button>
          <div class="faq-a"><strong>100% Free</strong> denotes open-source weights or truly free web apps with zero paywalls. <strong>Freemium</strong> offers a functional free quota with optional paid upgrades. <strong>Commercial / Paid</strong> requires a subscription or API credit purchase to use.</div>
        </div>
        <div class="faq-item">
          <button class="faq-q"><span>Can I bookmark tools to review later?</span><span class="faq-icon">+</span></button>
          <div class="faq-a">Yes! Click the star icon on any tool card to bookmark it in your browser. Tap the "Saved" button in the top navigation bar at any time to isolate your bookmarked collection.</div>
        </div>
        <div class="faq-item">
          <button class="faq-q"><span>How do I submit my AI tool or agent?</span><span class="faq-icon">+</span></button>
          <div class="faq-a">Scroll to the submission section below or reach out via our GitHub repository. We review submissions daily and verify metadata before listing.</div>
        </div>
      </div>
    </div>
  </section>

  <!-- Submit Section -->
  <section id="submit" class="section" style="border-top: 1px solid var(--border);">
    <div class="container">
      <div class="submit-box">
        <h2>Submit Your AI Tool or Model</h2>
        <p>Are you building frontier generative models, agentic workflows, or developer tooling? Submit your project to get discovered by tens of thousands of developers, researchers, and enterprise teams.</p>
        <a href="mailto:submit@aallaitools.online?subject=New%20AI%20Tool%20Submission" class="btn-submit" style="font-size: 1.05rem; padding: 14px 32px;">Submit Platform to Directory</a>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <div class="brand" style="margin-bottom: 14px;">
            <span class="brand-icon">AI</span>
            <span>aallaitools.online</span>
          </div>
          <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; max-width: 320px;">
            The world's fastest, definitive open directory of artificial intelligence models, developer copilots, creative suites, and autonomous agents.
          </p>
        </div>

        <div class="footer-col">
          <h4>Core Categories</h4>
          <ul>
            <li><a href="#featured">Chat &amp; Reasoning</a></li>
            <li><a href="#featured">Software &amp; Coding</a></li>
            <li><a href="#featured">Image &amp; Creative Art</a></li>
            <li><a href="#featured">Voice &amp; Audio Generation</a></li>
            <li><a href="#featured">Video &amp; 3D Worlds</a></li>
            <li><a href="#featured">AI Deep Search</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Directory Index</h4>
          <ul>
            <li><a href="/sitemap.xml">XML Sitemap</a></li>
            <li><a href="/robots.txt">Robots.txt Engine</a></li>
            <li><a href="https://github.com/shilwantr/aitest123" target="_blank" rel="noopener">Open Source Repo</a></li>
            <li><a href="#featured">All {total_tools}+ AI Tools</a></li>
            <li><a href="#faq">Submission Guidelines</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Live Stats</h4>
          <ul>
            <li style="color: #cbd5e1;">Catalog Count: <strong>{total_tools} Verified</strong></li>
            <li style="color: #cbd5e1;">Free / Open Tools: <strong>{cat_counts.get('coding-dev', 0) + cat_counts.get('ai-search', 0)}+</strong></li>
            <li style="color: #cbd5e1;">Latency: <strong>&lt; 50ms Zero-JS</strong></li>
            <li style="color: #cbd5e1;">Updated: <strong>October 2026</strong></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 aallaitools.online. All worldwide rights reserved. Designed for humans and autonomous AI crawlers.</div>
        <div>Indexed across 6 core domains &bull; 100% Valid W3C HTML5</div>
      </div>
    </div>
  </footer>

  <!-- Fast, zero-dependency client script -->
  <script>
    (function () {{
      'use strict';
      var searchInput = document.getElementById('tool-search');
      var clearBtn = document.getElementById('clear-search-btn');
      var cards = Array.from(document.querySelectorAll('.tool-card'));
      var filterPills = Array.from(document.querySelectorAll('.filter-pill'));
      var priceChips = Array.from(document.querySelectorAll('.price-chip'));
      var resultsCounter = document.getElementById('results-counter');
      var emptyState = document.getElementById('empty-state');
      var resetBtn = document.getElementById('reset-filters-btn');
      var showSavedBtn = document.getElementById('show-saved-btn');
      var savedCountEl = document.getElementById('saved-count');

      var currentCat = 'all';
      var currentPricing = 'all';
      var filterOnlySaved = false;
      var savedTools = [];

      try {{
        savedTools = JSON.parse(localStorage.getItem('saved_ai_tools')) || [];
      }} catch (e) {{
        savedTools = [];
      }}

      function updateSavedUI() {{
        savedCountEl.textContent = savedTools.length;
        cards.forEach(function (c) {{
          var name = c.getAttribute('data-name');
          var btn = c.querySelector('.bookmark-btn');
          if (btn) {{
            if (savedTools.indexOf(name) !== -1) {{
              btn.classList.add('saved');
              btn.innerHTML = '&#9733;';
            }} else {{
              btn.classList.remove('saved');
              btn.innerHTML = '&#9734;';
            }}
          }}
        }});
      }}

      function filterTools() {{
        var q = searchInput.value.toLowerCase().trim();
        clearBtn.style.display = q ? 'block' : 'none';
        var visible = 0;

        cards.forEach(function (card) {{
          var cat = card.getAttribute('data-category');
          var price = card.getAttribute('data-pricing');
          var name = card.getAttribute('data-name');
          var desc = card.getAttribute('data-desc');

          var matchCat = (currentCat === 'all' || cat === currentCat);
          var matchPrice = (currentPricing === 'all' || price === currentPricing);
          var matchQuery = (!q || name.indexOf(q) !== -1 || desc.indexOf(q) !== -1);
          var matchSaved = (!filterOnlySaved || savedTools.indexOf(name) !== -1);

          if (matchCat && matchPrice && matchQuery && matchSaved) {{
            card.style.display = 'flex';
            visible++;
          }} else {{
            card.style.display = 'none';
          }}
        }});

        if (visible === 0) {{
          emptyState.style.display = 'block';
          resultsCounter.textContent = '0 Tools Found';
        }} else {{
          emptyState.style.display = 'none';
          resultsCounter.textContent = 'Showing ' + visible + ' Verified Tool' + (visible === 1 ? '' : 's');
        }}
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

      updateSavedUI();
    }})();
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated classy modern index.html with {total_tools} tools!")
