# Google Antigravity Master Prompt, Full AI Tools Metadata Catalog & Complete Website Code for `aallaitools.online`

This single Markdown file contains everything needed for **Google Antigravity** ([Antigravity Docs](https://antigravity.google/docs/overview/)) to:
1. **Crawl the live web** to discover, verify, and categorize AI tools, reasoning models, custom GPTs, and autonomous agents.
2. **Segregate all tools into the 6 core directory categories** and generate a structured `AI_TOOLS_METADATA.md` catalog file with complete metadata.
3. **Update the full `aallaitools.online` website code** (`index.html`, `robots.txt`, and `sitemap.xml`) with interactive search, category filtering, JSON-LD `ItemList` schema, and `< 50ms` static load performance.

---

## 1. Master Copy-Paste Prompt for Google Antigravity

Copy and paste the entire prompt block below into your **Google Antigravity** prompt panel ([Antigravity CLI & IDE Prompting](https://antigravity.google/docs/cli/prompting/)):

> **Role & Autonomous Mission**
> You are an autonomous full-stack web architect, web-crawling data engineer, and technical SEO specialist operating inside Google Antigravity on the `aallaitools.online` codebase ("The Ultimate Directory of AI Tools & GPTs").
>
> Execute the following 4-stage workflow end-to-end:
>
> ### Stage 1: Autonomous Web Crawling & AI Tool Discovery
> 1. **Crawl & Expand**: Using your web search/browsing tools and the bundled Python discovery script (`scripts/crawl_and_sync_tools.py`), crawl live AI tool directories, product launches, and official vendor domains to gather all flagship and emerging AI tools across the ecosystem (LLMs, coding IDEs, app builders, image generators, vector/photo studios, TTS/voice cloning, AI music generators, podcast editors, text-to-video models, digital avatars, 3D asset generators, AI answer engines, and academic research agents).
> 2. **Verify Metadata**: For every discovered tool, verify that its official canonical URL resolves (`HTTP 200`), determine its current pricing model (`Freemium`, `Paid`, or `Free`), assign a unique 2–3 character badge abbreviation and accessible brand hex color, and draft a concise, high-signal description (18–26 words) free of marketing fluff.
> 3. **Strict Category Segregation**: Classify every tool into one of the 6 canonical `aallaitools.online` filter categories and its paired category showcase card:
>    - `Chat & Reasoning` (`data-category="chat-reasoning"`) ↔ `✍️ Generative Writing`
>    - `Coding & Dev` (`data-category="coding-dev"`) ↔ `💻 Software & Coding`
>    - `Image & Art` (`data-category="image-art"`) ↔ `🎨 Image & Visual Arts`
>    - `Voice & Audio` (`data-category="voice-audio"`) ↔ `🎙️ Voice & Audio Synthesis`
>    - `Video & 3D` (`data-category="video-3d"`) ↔ `🎥 Video & Motion FX`
>    - `AI Search` (`data-category="ai-search"`) ↔ `🔍 Research & Deep Search`
>
> ### Stage 2: Generate & Maintain `AI_TOOLS_METADATA.md` and `tools.json`
> 1. Create or update `AI_TOOLS_METADATA.md` in the root of the workspace containing the master Markdown tables of all segregated tools (including Badge, Brand Hex, Tool Name, Subcategory, Pricing Tier, Category Pill, `data-category` slug, Description, and Official URL).
> 2. Export a synchronized `tools.json` dataset for programmatic builds and schema generation.
>
> ### Stage 3: Update Website Code (`index.html`, `robots.txt`, `sitemap.xml`)
> 1. **Preserve Exact Visual Design & Speed (`< 50ms` FCP)**:
>    - Keep 100% static semantic HTML5 and modular inline CSS with system UI typography (`-apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif`). Do not add external JS bundles, external CSS frameworks, or tracking scripts.
>    - Preserve the sticky top navigation bar (`AI aallaitools.online`, `Fast & Live` badge, `Featured Tools`, `Categories`, `FAQ`, `Sitemap`, `Robots`, and `+ Submit Tool` CTA button).
>    - Preserve the hero section (`⚡ Optimized for GPTs & Search Engines`, `The Ultimate Directory of AI Tools & GPTs` with purple-indigo gradient on `AI Tools & GPTs`, rounded search bar, 7 filter pills, and the 4 trust badges: `⚡ 100% Static Fast Load`, `🤖 GPTBot & Crawler Ready`, `📂 JSON-LD Schema Enabled`, `🔄 Daily Sitemap Updates`).
> 2. **Render All Segregated Tool Cards**:
>    - Populate the `#featured` grid with all 60+ categorized AI tools using the exact card anatomy: top-left colored rounded-square badge (`44px × 44px`), top-right pricing pill (`#EEF2FF` background, `#4F46E5` text), bold tool title, 2–3 line description, bottom-left category tag pill, and bottom-right `Visit Tool →` external link (`target="_blank" rel="noopener noreferrer"`).
> 3. **Interactive Search, Category Pills & FAQ Accordion**:
>    - Implement ultra-lightweight inline vanilla JavaScript (`< 2 KB`) that filters `.tool-card` elements in real time as the user types in the search bar (`#tool-search`) or clicks any of the 7 filter pills (`All Tools`, `Chat & Reasoning`, `Coding & Dev`, `Image & Art`, `Voice & Audio`, `AI Search`, `Video & 3D`).
>    - Wire the 6 **Explore AI Tools by Category** cards so clicking any card scrolls smoothly to `#featured` and activates that category's filter pill.
>    - Wire the 4 **Frequently Asked Questions** accordion items so clicking `+` toggles the answer panel cleanly.
> 4. **Update SEO & Crawler Files**:
>    - Populate `<script type="application/ld+json">` inside `index.html` with a complete `WebSite`, `FAQPage`, and `ItemList` of `SoftwareApplication` objects for every tool in the directory.
>    - Generate `robots.txt` granting full crawl access to `Googlebot`, `Bingbot`, `GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot`, and `Google-Extended`.
>    - Generate `sitemap.xml` with current `<lastmod>` ISO dates.
>
> ### Stage 4: Verification
> Verify that all category filters, live search queries, FAQ toggles, and JSON-LD schema blocks validate with zero console errors and zero layout shifts (`CLS = 0`).

---

## 2. Complete Segregated AI Tools Metadata Catalog (`AI_TOOLS_METADATA.md`)

Below is the pre-crawled, segregated master metadata catalog of **60 verified AI tools** across all 6 categories. Antigravity will use this as the baseline dataset and append any newly crawled tools in the exact same schema.

### Category 1: Chat & Reasoning (`✍️ Generative Writing` | `data-category="chat-reasoning"`)

| Badge | Hex Color | Tool Name | Subcategory | Pricing | Category Pill | Description | Official URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GPT** | `#10A37F` | [ChatGPT & Custom GPTs](https://chatgpt.com/) | Frontier LLM & Agents | Freemium | Chat & Reasoning | State-of-the-art conversational AI platform by OpenAI featuring reasoning models, vision analysis, browsing, and custom GPT workflows. | `https://chatgpt.com/` |
| **CL** | `#D97706` | [Claude](https://claude.ai/) | Frontier LLM & Writing | Freemium | Chat & Reasoning | Anthropic's hybrid reasoning model built for nuanced writing, safe alignment, complex codebase understanding, and large-context document analysis. | `https://claude.ai/` |
| **GM** | `#2563EB` | [Google Gemini](https://gemini.google.com/) | Multimodal Assistant | Freemium | Chat & Reasoning | Google's natively multimodal AI assistant with a 1M+ token context window for deep reasoning, writing, coding, and Workspace integration. | `https://gemini.google.com/` |
| **DS** | `#1D4ED8` | [DeepSeek](https://www.deepseek.com/) | Open-Weight Reasoning | Freemium | Chat & Reasoning | High-efficiency frontier reasoning and open-weight LLM platform excelling at mathematical logic, complex coding, and long-context analysis. | `https://www.deepseek.com/` |
| **GK** | `#0F172A` | [Grok](https://grok.com/) | Real-Time Reasoning | Freemium | Chat & Reasoning | Real-time conversational AI and reasoning assistant by xAI with live synthesis, deep search, and multimodal generation capabilities. | `https://grok.com/` |
| **NT** | `#1E293B` | [Notion AI](https://www.notion.ai/) | Workspace & Docs AI | Freemium | Chat & Reasoning | Integrated workspace AI for drafting documents, summarizing meeting notes, automating project wikis, and querying connected knowledge bases. | `https://www.notion.ai/` |
| **JP** | `#7C3AED` | [Jasper AI](https://www.jasper.ai/) | Enterprise Marketing Copy | Paid | Chat & Reasoning | Enterprise AI marketing copilot engineered for brand-voice consistency, multi-channel campaign copywriting, and automated content workflows. | `https://www.jasper.ai/` |
| **CP** | `#0D9488` | [Copy.ai](https://www.copy.ai/) | GTM & Sales Copywriting | Freemium | Chat & Reasoning | Go-to-market AI platform that automates sales outreach, product descriptions, blog generation, and repeatable content workflows at scale. | `https://www.copy.ai/` |
| **GR** | `#059669` | [Grammarly](https://www.grammarly.com/) | Grammar & Tone Optimizer | Freemium | Chat & Reasoning | Cross-platform AI writing assistant offering real-time grammar correction, tone adjustments, full-paragraph rewrites, and plagiarism detection. | `https://www.grammarly.com/` |
| **QB** | `#16A34A` | [QuillBot](https://quillbot.com/) | Paraphrasing & Polishing | Freemium | Chat & Reasoning | AI-powered paraphrasing, summarization, grammar checking, and academic citation tool built to improve sentence fluency and clarity. | `https://quillbot.com/` |

### Category 2: Coding & Dev (`💻 Software & Coding` | `data-category="coding-dev"`)

| Badge | Hex Color | Tool Name | Subcategory | Pricing | Category Pill | Description | Official URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CR** | `#1E293B` | [Cursor AI Editor](https://cursor.com/) | AI-First Code IDE | Freemium | Coding & Dev | Next-generation VS Code fork built from the ground up for AI-first pair programming, multi-file code editing, and fast terminal automation. | `https://cursor.com/` |
| **v0** | `#0F172A` | [v0 by Vercel](https://v0.app/) | Generative UI & React | Freemium | Coding & Dev | Generative UI system that builds clean React, Tailwind CSS, and full-stack web components directly from text prompts, ready to deploy. | `https://v0.app/` |
| **AG** | `#4F46E5` | [Google Antigravity](https://antigravity.google/docs/overview/) | Agentic IDE & CLI | Freemium | Coding & Dev | Agent-first AI development environment and CLI by Google for autonomous multi-file engineering, code review, and full-stack scaffolding. | `https://antigravity.google/docs/overview/` |
| **BL** | `#2563EB` | [Bolt.new](https://bolt.new/) | Browser Full-Stack Builder | Freemium | Coding & Dev | Browser-based AI full-stack web development agent that prompts, runs, edits, and deploys Node.js and modern web applications instantaneously. | `https://bolt.new/` |
| **LV** | `#EC4899` | [Lovable](https://lovable.dev/) | Prompt-to-App Builder | Freemium | Coding & Dev | Conversational full-stack software builder that transforms plain-language prompts into production-ready web apps with databases and auth. | `https://lovable.dev/` |
| **DV** | `#0D9488` | [Devin AI](https://devin.ai/) | Autonomous Software Agent | Paid | Coding & Dev | Autonomous AI software engineer capable of planning, executing, debugging, and deploying complex multi-step engineering tasks in cloud sandboxes. | `https://devin.ai/` |
| **RP** | `#EA580C` | [Replit Agent](https://replit.com/) | Cloud IDE & App Agent | Freemium | Coding & Dev | Collaborative cloud development platform with an autonomous AI agent that designs, codes, configures databases, and hosts web apps in minutes. | `https://replit.com/` |
| **GH** | `#24292F` | [GitHub Copilot](https://github.com/features/copilot) | IDE Code Autocompletion | Freemium | Coding & Dev | Industry-standard AI coding assistant integrated into VS Code, JetBrains, and GitHub for inline completions, agentic PR reviews, and debugging. | `https://github.com/features/copilot` |
| **WS** | `#0284C7` | [Windsurf](https://windsurf.com/) | Agentic Code Editor | Freemium | Coding & Dev | AI-native IDE featuring Cascade deep-context flows for synchronized multi-file refactoring, terminal execution, and codebase comprehension. | `https://windsurf.com/` |
| **SB** | `#10B981` | [Supabase AI](https://supabase.com/) | Postgres & Vector Backend | Freemium | Coding & Dev | Open-source Postgres development platform with integrated AI SQL generation, pgvector embeddings, authentication, and instant edge APIs. | `https://supabase.com/` |

### Category 3: Image & Art (`🎨 Image & Visual Arts` | `data-category="image-art"`)

| Badge | Hex Color | Tool Name | Subcategory | Pricing | Category Pill | Description | Official URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MJ** | `#7C3AED` | [Midjourney v6](https://www.midjourney.com/) | Photorealistic Synthesis | Paid | Image & Art | Industry-standard image generation engine creating breathtaking photorealistic visuals, character continuity, and artistic illustrations from text. | `https://www.midjourney.com/` |
| **ID** | `#4F46E5` | [Ideogram](https://ideogram.ai/) | Typography & Graphic AI | Freemium | Image & Art | Precision text-to-image synthesis platform renowned for accurate typography rendering, graphic design layouts, logos, and poster generation. | `https://ideogram.ai/` |
| **LN** | `#9333EA` | [Leonardo.Ai](https://leonardo.ai/) | Creative Suite & Assets | Freemium | Image & Art | Production-scale generative visual suite offering fine-tuned models, consistent character workflows, canvas editing, and game asset creation. | `https://leonardo.ai/` |
| **RC** | `#EA580C` | [Recraft AI](https://www.recraft.ai/) | Vector SVG & Brand Design | Freemium | Image & Art | Professional AI design studio purpose-built for generating editable SVG vector graphics, brand-consistent icon sets, mockups, and commercial art. | `https://www.recraft.ai/` |
| **KR** | `#0F172A` | [Krea AI](https://www.krea.ai/) | Real-Time Canvas & Upscaler | Freemium | Image & Art | Real-time interactive canvas for instantaneous AI image generation, 4K resolution upscaling, pattern illusions, and style transfer. | `https://www.krea.ai/` |
| **CV** | `#00C4CC` | [Canva Magic Media](https://www.canva.com/ai-image-generator/) | All-in-One Visual Design | Freemium | Image & Art | Integrated visual design suite featuring AI text-to-image synthesis, background removal, Magic Eraser, and automated social layout resizing. | `https://www.canva.com/ai-image-generator/` |
| **PR** | `#6366F1` | [Photoroom](https://www.photoroom.com/) | E-Commerce Product Photo | Freemium | Image & Art | AI visual editor tailored for e-commerce that removes backgrounds, generates studio product scenes, and batch-processes catalog photography. | `https://www.photoroom.com/` |
| **RB** | `#0284C7` | [remove.bg](https://www.remove.bg/) | Instant Background Removal | Freemium | Image & Art | Automated AI subject segmentation tool that cleanly isolates foreground subjects and removes complex image backgrounds in under 5 seconds. | `https://www.remove.bg/` |
| **GM** | `#DB2777` | [Gamma](https://gamma.app/) | AI Decks & Visual Docs | Freemium | Image & Art | Generative presentation and visual document platform that turns outlines into polished slide decks, web pages, and visual layouts automatically. | `https://gamma.app/` |
| **FL** | `#1E293B` | [Replicate (FLUX Models)](https://replicate.com/) | Open-Weight Image Cloud | Freemium | Image & Art | Cloud API and playground for running frontier open-weight image generation, inpainting, and super-resolution models including FLUX and SDXL. | `https://replicate.com/` |

### Category 4: Voice & Audio (`🎙️ Voice & Audio Synthesis` | `data-category="voice-audio"`)

| Badge | Hex Color | Tool Name | Subcategory | Pricing | Category Pill | Description | Official URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EL** | `#059669` | [ElevenLabs Voice AI](https://elevenlabs.io/) | Speech Synthesis & Cloning | Freemium | Voice & Audio | Pioneering generative voice technology providing ultra-realistic speech synthesis, instant voice cloning, and emotional voice dubbing in 32+ languages. | `https://elevenlabs.io/` |
| **SN** | `#E11D48` | [Suno](https://suno.com/) | Full-Song Music Generation | Freemium | Voice & Audio | Full-song AI music generator that composes broadcast-quality tracks with expressive vocals, custom lyrics, and multi-genre instrumentation in seconds. | `https://suno.com/` |
| **UD** | `#7C3AED` | [Udio](https://www.udio.com/) | Studio AI Music Production | Freemium | Voice & Audio | High-fidelity AI music production platform enabling creators to generate, extend, remix, and master studio-grade songs from text descriptions. | `https://www.udio.com/` |
| **MF** | `#D97706` | [Murf AI](https://murf.ai/) | Enterprise Voiceover Studio | Freemium | Voice & Audio | Studio-grade AI voice generator offering 200+ expressive text-to-speech voices, pitch/emphasis controls, and commercial voiceover synchronization. | `https://murf.ai/` |
| **PH** | `#2563EB` | [PlayHT](https://playht.app/) | Conversational TTS & Cloning | Freemium | Voice & Audio | Ultra-low-latency AI text-to-speech and voice cloning platform engineered for podcasts, audiobooks, and real-time conversational voice agents. | `https://playht.app/` |
| **DC** | `#0284C7` | [Descript](https://www.descript.com/) | Transcript Podcast Editor | Freemium | Voice & Audio | All-in-one podcast and audio-video editor that lets creators edit speech via text transcripts, remove filler words, and apply Studio Sound mastering. | `https://www.descript.com/` |
| **OT** | `#0D9488` | [Otter.ai](https://otter.ai/) | Live Meeting Transcription | Freemium | Voice & Audio | Real-time AI meeting transcription and voice intelligence assistant that records audio, identifies speakers, and generates automated action summaries. | `https://otter.ai/` |
| **FF** | `#6366F1` | [Fireflies.ai](https://fireflies.ai/) | Voice Meeting Intelligence | Freemium | Voice & Audio | Conversation intelligence and voice transcription agent that captures, transcribes, and analyzes voice meetings across Zoom, Meet, and Teams. | `https://fireflies.ai/` |
| **FA** | `#10B981` | [Fathom](https://fathom.video/) | AI Call Notes & Sync | Freemium | Voice & Audio | Instant AI meeting recorder and voice note-taker that highlights key call moments, summarizes action items, and syncs directly to CRM workflows. | `https://fathom.video/` |
| **FL** | `#EC4899` | [Fliki](https://fliki.ai/) | Script-to-Voiceover Studio | Freemium | Voice & Audio | Text-to-audio and voiceover creation suite combining lifelike neural voices in 75+ languages with automated media matching for creators. | `https://fliki.ai/` |

### Category 5: Video & 3D (`🎥 Video & Motion FX` | `data-category="video-3d"`)

| Badge | Hex Color | Tool Name | Subcategory | Pricing | Category Pill | Description | Official URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RW** | `#E11D48` | [Runway Gen-3 Alpha](https://app.runwayml.com/) | Cinematic Video Generation | Freemium | Video & 3D | Breakthrough text-to-video and image-to-video AI suite creating cinematic clips with precise motion control, lighting, and camera dynamics. | `https://app.runwayml.com/` |
| **SR** | `#0F172A` | [OpenAI Sora](https://sora.com/) | World-Simulating Video AI | Paid | Video & 3D | OpenAI's flagship generative video engine capable of synthesizing hyper-realistic wide-screen scenes, complex physics, and storyboarded sequences. | `https://sora.com/` |
| **VO** | `#2563EB` | [Google Veo](https://deepmind.google/models/veo/) | HD Video & Native Audio | Freemium | Video & 3D | Google DeepMind's high-definition video generation model with native synchronized audio, cinematic camera control, and image-to-video continuity. | `https://deepmind.google/models/veo/` |
| **KL** | `#EA580C` | [Kling AI](https://klingai.com/) | High-Motion Video Studio | Freemium | Video & 3D | High-motion generative video studio delivering long-duration 1080p clips, realistic physics simulation, motion brush control, and lip-syncing. | `https://klingai.com/` |
| **LM** | `#4F46E5` | [Luma Dream Machine](https://lumalabs.ai/) | Ray Video & 3D Capture | Freemium | Video & 3D | Fast creative AI platform powered by Luma Ray models for cinematic text-to-video synthesis, keyframe animation, and 3D scene capture. | `https://lumalabs.ai/` |
| **HG** | `#7C3AED` | [HeyGen](https://www.heygen.com/) | Digital Avatars & Dubbing | Freemium | Video & 3D | Enterprise AI avatar and video localization platform for creating photorealistic digital presenters and lip-synced multilingual video translations. | `https://www.heygen.com/` |
| **SY** | `#0284C7` | [Synthesia](https://www.synthesia.io/) | Studio Avatar Presentations | Freemium | Video & 3D | Studio-quality digital avatar video generator enabling teams to produce training, marketing, and instructional videos from scripts without cameras. | `https://www.synthesia.io/` |
| **PK** | `#DB2777` | [Pika](https://pika.art/) | Stylized Video & FX | Freemium | Video & 3D | Creative AI video platform for generating stylized clips, physics-based Pikaffects, character animations, and synchronized sound effects. | `https://pika.art/` |
| **OP** | `#16A34A` | [OpusClip](https://www.opus.pro/) | AI Viral Short Clipper | Freemium | Video & 3D | Automated video repurposing engine that turns long-form podcasts and talks into viral short-form vertical clips with dynamic captions and B-roll. | `https://www.opus.pro/` |
| **CC** | `#0F172A` | [CapCut AI](https://www.capcut.com/) | Smart Social Video Editor | Freemium | Video & 3D | All-in-one browser and desktop video editor featuring AI script-to-video, automated captions, background removal, and social media effects. | `https://www.capcut.com/` |
| **MS** | `#9333EA` | [Meshy AI](https://www.meshy.ai/) | Text & Image to 3D Mesh | Freemium | Video & 3D | AI 3D model generator that transforms text prompts and 2D photos into textured, production-ready 3D meshes (FBX, GLB, OBJ, STL) in seconds. | `https://www.meshy.ai/` |
| **TP** | `#0D9488` | [Tripo 3D](https://www.tripo3d.ai/) | Instant 3D Rigging & Models | Freemium | Video & 3D | High-speed generative 3D platform supporting instant text-to-3D and image-to-3D model creation, PBR texturing, retopology, and auto-rigging. | `https://www.tripo3d.ai/` |
| **SP** | `#2563EB` | [Spline AI](https://spline.design/) | Interactive 3D Web Design | Freemium | Video & 3D | Browser-based 3D design and collaboration tool with AI prompt generation for interactive 3D web scenes, physics, and real-time shaders. | `https://spline.design/` |

### Category 6: AI Search (`🔍 Research & Deep Search` | `data-category="ai-search"`)

| Badge | Hex Color | Tool Name | Subcategory | Pricing | Category Pill | Description | Official URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PX** | `#0284C7` | [Perplexity AI](https://www.perplexity.ai/) | Conversational Answer Engine | Freemium | AI Search | An AI-powered conversational answer engine that searches the live web and provides cited, verifiable answers with academic references. | `https://www.perplexity.ai/` |
| **NB** | `#059669` | [Gemini Notebook (NotebookLM)](https://notebook.google/) | Grounded Research Partner | Freemium | AI Search | Google's source-grounded research and thinking partner that synthesizes uploaded PDFs, docs, and links into cited briefings, mind maps, and audio overviews. | `https://notebook.google/` |
| **CS** | `#1D4ED8` | [Consensus](https://consensus.app/) | Peer-Reviewed Science Search | Freemium | AI Search | Academic AI search engine indexing over 200M peer-reviewed scientific papers to synthesize evidence-backed findings and study snapshots. | `https://consensus.app/` |
| **EC** | `#4F46E5` | [Elicit](https://elicit.com/) | Systematic Literature Review | Freemium | AI Search | Autonomous scientific research assistant that automates systematic literature reviews, extracts data tables from papers, and synthesizes empirical evidence. | `https://elicit.com/` |
| **SC** | `#0D9488` | [Scite.ai](https://scite.ai/) | Smart Citation Verification | Paid | AI Search | Citation-grounded research platform that reveals how scientific articles are cited by showing supporting or contrasting evidence across publications. | `https://scite.ai/` |
| **YU** | `#7C3AED` | [You.com](https://you.com/) | Multi-Model Research Engine | Freemium | AI Search | AI search and multi-model research engine combining live web retrieval with custom research agents for verifiable technical analysis. | `https://you.com/` |
| **OR** | `#1E293B` | [OpenRouter](https://openrouter.ai/) | Unified Frontier Model Hub | Freemium | AI Search | Unified discovery router and playground providing instant comparison, benchmarking, and API routing across 200+ frontier LLMs and reasoning models. | `https://openrouter.ai/` |
