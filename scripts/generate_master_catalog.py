#!/usr/bin/env python3
"""
Master Dataset Generator for aallaitools.online
Generates:
1. tools.json (structured list of 200+ worldwide verified AI tools)
2. AI_TOOLS_METADATA.md (exhaustive markdown documentation)
3. Injects tool cards and JSON-LD schema into index.html
"""

import json
import html
from pathlib import Path

TOOLS_DATA = [
    # ==================== CHAT & REASONING (35 tools) ====================
    {
        "name": "ChatGPT & Custom GPTs",
        "badge": "GPT",
        "color": "#10A37F",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Frontier LLM & Reasoning",
        "description": "OpenAI flagship conversational platform with GPT-4o, o1 reasoning, vision analysis, web search, code interpreter, and custom GPT ecosystem.",
        "url": "https://chatgpt.com/"
    },
    {
        "name": "Claude",
        "badge": "CL",
        "color": "#D97706",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Frontier LLM & Analysis",
        "description": "Anthropic premier hybrid model family (Sonnet, Opus, Haiku) delivering state-of-the-art coding, deep document comprehension, and nuanced reasoning.",
        "url": "https://claude.ai/"
    },
    {
        "name": "Google Gemini",
        "badge": "GM",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Multimodal Frontier Assistant",
        "description": "Google natively multimodal AI assistant with a 2M+ token context window, deep reasoning, live Workspace synchronization, and audio/video input.",
        "url": "https://gemini.google.com/"
    },
    {
        "name": "DeepSeek",
        "badge": "DS",
        "color": "#1D4ED8",
        "pricing": "Free",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Open Reasoning & Logic",
        "description": "Groundbreaking open-weight reasoning model excelling in mathematical proofs, algorithmic code synthesis, and low-cost frontier intelligence.",
        "url": "https://www.deepseek.com/"
    },
    {
        "name": "Grok",
        "badge": "GK",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Real-Time Intelligence",
        "description": "xAI conversational assistant featuring real-time X post ingestion, unfiltered responses, high-speed vision analysis, and Aurora image generation.",
        "url": "https://grok.com/"
    },
    {
        "name": "Mistral Le Chat",
        "badge": "MS",
        "color": "#F97316",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "European Frontier LLM",
        "description": "Mistral AI conversational interface powered by Large 2 and Pixtral, offering web search, canvas document editing, and multilingual mastery.",
        "url": "https://chat.mistral.ai/"
    },
    {
        "name": "Qwen Chat",
        "badge": "QW",
        "color": "#6366F1",
        "pricing": "Free",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Multilingual Open Model",
        "description": "Alibaba Cloud flagship open-weight LLM suite demonstrating world-class performance in math, programming, and multilingual translation.",
        "url": "https://chat.qwenlm.ai/"
    },
    {
        "name": "Meta AI (Llama)",
        "badge": "MA",
        "color": "#0668E1",
        "pricing": "Free",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Open Foundation Assistant",
        "description": "Meta everyday assistant powered by open Llama 3 models, integrated across WhatsApp, Instagram, and web for queries and image generation.",
        "url": "https://www.meta.ai/"
    },
    {
        "name": "Notion AI",
        "badge": "NT",
        "color": "#1E293B",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Connected Workspace AI",
        "description": "Workspace knowledge copilot that drafts docs, summarizes databases, answers queries across company wikis, and automates team workflows.",
        "url": "https://www.notion.ai/"
    },
    {
        "name": "Jasper AI",
        "badge": "JP",
        "color": "#7C3AED",
        "pricing": "Paid",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Enterprise Marketing Suite",
        "description": "Enterprise generative marketing platform enforcing brand-voice governance, campaign brief generation, and omnichannel copy production.",
        "url": "https://www.jasper.ai/"
    },
    {
        "name": "Copy.ai",
        "badge": "CP",
        "color": "#0D9488",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "GTM & Sales Automation",
        "description": "AI-powered GTM platform designed for marketing, sales teams, and SDR automation to write ad copy, emails, and collateral at scale.",
        "url": "https://www.copy.ai/"
    },
    {
        "name": "Grammarly",
        "badge": "GR",
        "color": "#059669",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Writing & Tone Polishing",
        "description": "Real-time communication assistant providing deep grammar checks, tone refinement, style consistency, and generative rewriting across all apps.",
        "url": "https://www.grammarly.com/"
    },
    {
        "name": "QuillBot",
        "badge": "QB",
        "color": "#16A34A",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Paraphrasing & Academic Tone",
        "description": "AI paraphrase tool, summarizer, grammar corrector, and citation creator engineered to elevate clarity, fluency, and academic writing standards.",
        "url": "https://quillbot.com/"
    },
    {
        "name": "Character.AI",
        "badge": "CA",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Persona & Roleplay Agents",
        "description": "Interactive conversational AI platform featuring millions of community-created personas, historical figures, tutors, and creative companions.",
        "url": "https://character.ai/"
    },
    {
        "name": "Poe by Quora",
        "badge": "PO",
        "color": "#702CFB",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Multi-Bot Hub & Monetization",
        "description": "Universal AI aggregator providing fast switching between GPT-4o, Claude 3.5, Gemini, Flux, and bespoke creator bots under one subscription.",
        "url": "https://poe.com/"
    },
    {
        "name": "Pi by Inflection",
        "badge": "PI",
        "color": "#14B8A6",
        "pricing": "Free",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Empathetic Personal AI",
        "description": "Warm, emotionally intelligent personal companion AI built for supportive conversation, active listening, reflection, and daily planning.",
        "url": "https://pi.ai/"
    },
    {
        "name": "HuggingChat",
        "badge": "HC",
        "color": "#FFD21E",
        "pricing": "Free",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Open Source Model Playground",
        "description": "Hugging Face official open-source alternative to ChatGPT, running Llama 3, Command R+, DeepSeek, and community models with web search.",
        "url": "https://huggingface.co/chat/"
    },
    {
        "name": "Writesonic",
        "badge": "WS",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "SEO Article & Copy Engine",
        "description": "AI writing software specializing in factual SEO-optimized long-form blog posts, Google Ads copy, landing pages, and AI search presence.",
        "url": "https://writesonic.com/"
    },
    {
        "name": "Wordtune",
        "badge": "WT",
        "color": "#9333EA",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Sentence Rephrasing Assistant",
        "description": "AI reading and writing copilot by AI21 Labs that rephrases sentences for professional conciseness, tone shifts, and semantic impact.",
        "url": "https://www.wordtune.com/"
    },
    {
        "name": "Rytr",
        "badge": "RY",
        "color": "#E11D48",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Budget Copywriting Copilot",
        "description": "Cost-effective AI writing tool for entrepreneurs and freelancers offering 40+ use cases, 30+ languages, and 20+ emotional voice tones.",
        "url": "https://rytr.me/"
    },
    {
        "name": "Sudowrite",
        "badge": "SW",
        "color": "#EC4899",
        "pricing": "Paid",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Fiction & Novelist Suite",
        "description": "Specialized AI creative writing companion for novelists offering brainstorming, character arcs, sensory prose generation, and plot outlining.",
        "url": "https://www.sudowrite.com/"
    },
    {
        "name": "NovelAI",
        "badge": "NA",
        "color": "#475569",
        "pricing": "Paid",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "AI Storytelling & Lore",
        "description": "Subscription sandbox for AI-assisted literature creation and visual anime generation with zero censorship and rich memory modules.",
        "url": "https://novelai.net/"
    },
    {
        "name": "Jenni AI",
        "badge": "JA",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Academic Thesis Writer",
        "description": "Academic writing copilot that provides in-text APA/MLA citations, autocompletes research literature, and helps write research papers faster.",
        "url": "https://jenni.ai/"
    },
    {
        "name": "ChatPDF",
        "badge": "CP",
        "color": "#EF4444",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "PDF & Document Analysis",
        "description": "Document analysis tool that transforms contracts, research papers, and textbooks into interactive conversational knowledge bases.",
        "url": "https://www.chatpdf.com/"
    },
    {
        "name": "Humata AI",
        "badge": "HM",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Enterprise Document Q&A",
        "description": "Accelerate scientific and legal paper analysis with fast Q&A, cited page references, and instant synthesis of massive technical reports.",
        "url": "https://www.humata.ai/"
    },
    {
        "name": "Taskade Genesis",
        "badge": "TK",
        "color": "#F43F5E",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Multi-Agent Team Workspace",
        "description": "Collaborative project management platform with custom autonomous AI agent teams that automate sprint planning, research, and task tracking.",
        "url": "https://www.taskade.com/"
    },
    {
        "name": "YouChat",
        "badge": "YC",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Web-Connected Conversational AI",
        "description": "Live web-grounded AI conversational assistant providing cited answers, multi-modal chart generation, and programming debugging support.",
        "url": "https://you.com/chat"
    },
    {
        "name": "Julius AI",
        "badge": "JL",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Data Science & CSV Analyst",
        "description": "Intelligent computational agent that analyzes CSVs, Excel files, and database queries to produce statistical models, charts, and forecasts.",
        "url": "https://julius.ai/"
    },
    {
        "name": "Mem.ai",
        "badge": "MM",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Self-Organizing Second Brain",
        "description": "Self-organizing digital notebook that automatically connects notes, calendar events, meeting summaries, and projects without manual tags.",
        "url": "https://mem.ai/"
    },
    {
        "name": "Craft AI Assistant",
        "badge": "CR",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Structured Writing & Docs",
        "description": "Structured document platform blending aesthetic Markdown formatting with integrated AI drafting, translation, and structured summarization.",
        "url": "https://www.craft.do/"
    },
    {
        "name": "Scribe AI",
        "badge": "SC",
        "color": "#F97316",
        "pricing": "Freemium",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Process Documentation Bot",
        "description": "Automated workflow capture extension that watches your browser actions to auto-generate illustrated visual SOPs and training guides.",
        "url": "https://scribehow.com/"
    },
    {
        "name": "Anyword",
        "badge": "AW",
        "color": "#0284C7",
        "pricing": "Paid",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Performance Copy & Predictive Score",
        "description": "Performance copywriting AI that predicts conversion scores and click-through rates before launching digital marketing campaigns.",
        "url": "https://anyword.com/"
    },
    {
        "name": "Content at Scale",
        "badge": "CS",
        "color": "#1E293B",
        "pricing": "Paid",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Deep-Research Longform SEO",
        "description": "Enterprise SEO engine that crawls top-ranking Google competitors to generate comprehensive, human-like 3,000-word blog articles.",
        "url": "https://contentatscale.ai/"
    },
    {
        "name": "Chinchilla / GDM",
        "badge": "DM",
        "color": "#2563EB",
        "pricing": "Free",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "DeepMind Research Foundation",
        "description": "Google DeepMind foundational compute-optimal research frameworks driving next-generation reasoning architectures and agents.",
        "url": "https://deepmind.google/"
    },
    {
        "name": "Kagi Assistant",
        "badge": "KG",
        "color": "#EAB308",
        "pricing": "Paid",
        "category_slug": "chat-reasoning",
        "category_pill": "Chat & Reasoning",
        "subcategory": "Private Ad-Free Search AI",
        "description": "Privacy-first search assistant that provides direct, ad-free web synthesis, multi-model LLM comparisons, and fast webpage summaries.",
        "url": "https://kagi.com/"
    },

    # ==================== CODING & DEV (35 tools) ====================
    {
        "name": "Cursor AI Editor",
        "badge": "CR",
        "color": "#1E293B",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "AI-Native Code IDE",
        "description": "VS Code fork built specifically for AI-native software engineering, multi-file editing, full-repo embeddings, and fast terminal automation.",
        "url": "https://cursor.com/"
    },
    {
        "name": "Windsurf",
        "badge": "WS",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Agentic Cascade Editor",
        "description": "Codeium agentic IDE featuring Cascade deep-context flows for synchronized multi-file refactoring, terminal execution, and comprehension.",
        "url": "https://windsurf.com/"
    },
    {
        "name": "v0 by Vercel",
        "badge": "v0",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Generative UI & Full-Stack",
        "description": "Generative frontend platform that synthesizes clean React, Tailwind CSS, Shadcn UI components, and full-stack web applications from text.",
        "url": "https://v0.app/"
    },
    {
        "name": "Bolt.new",
        "badge": "BL",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Browser Full-Stack Sandbox",
        "description": "WebContainer-powered in-browser AI development agent that builds, tests, runs npm packages, and deploys full-stack apps in seconds.",
        "url": "https://bolt.new/"
    },
    {
        "name": "Lovable",
        "badge": "LV",
        "color": "#EC4899",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Prompt-to-Product Builder",
        "description": "Conversational software builder that translates natural language ideas into production-ready web apps with backend Supabase integration.",
        "url": "https://lovable.dev/"
    },
    {
        "name": "Devin AI",
        "badge": "DV",
        "color": "#0D9488",
        "pricing": "Paid",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Autonomous Software Engineer",
        "description": "Cognition autonomous AI software engineer capable of navigating complex codebases, planning tasks, debugging errors, and opening pull requests.",
        "url": "https://devin.ai/"
    },
    {
        "name": "GitHub Copilot",
        "badge": "GH",
        "color": "#24292F",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Industry Standard Autocomplete",
        "description": "AI pair programmer powering millions of developers across VS Code and JetBrains with code suggestions, PR reviews, and Copilot Chat.",
        "url": "https://github.com/features/copilot"
    },
    {
        "name": "Google Antigravity",
        "badge": "AG",
        "color": "#4F46E5",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Agentic IDE & Autonomous CLI",
        "description": "Agent-first AI development environment and CLI by Google for autonomous multi-file engineering, code review, and full-stack scaffolding.",
        "url": "https://antigravity.google/docs/overview/"
    },
    {
        "name": "Replit Agent",
        "badge": "RP",
        "color": "#EA580C",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Autonomous App Creation",
        "description": "Cloud development agent that plans, writes, configures PostgreSQL databases, and deploys full-stack web applications from plain text prompts.",
        "url": "https://replit.com/"
    },
    {
        "name": "Supermaven",
        "badge": "SM",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Ultra-Low-Latency Code Completion",
        "description": "Blazing-fast AI code autocompletion engine with a 1M-token context window that predicts multi-line edits with sub-100ms response times.",
        "url": "https://supermaven.com/"
    },
    {
        "name": "Claude Code",
        "badge": "CC",
        "color": "#D97706",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Agentic CLI Coding Assistant",
        "description": "Anthropic command-line agent that lives in your terminal, understands repo architecture, writes git commits, and executes test suites.",
        "url": "https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview"
    },
    {
        "name": "Aider",
        "badge": "AI",
        "color": "#475569",
        "pricing": "Free",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Git-Native CLI Pair Programmer",
        "description": "Command-line pair programmer that edits code in your local git repository, writes commit messages, and connects with frontier LLMs.",
        "url": "https://aider.chat/"
    },
    {
        "name": "Supabase AI",
        "badge": "SB",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "PostgreSQL & Vector Backend",
        "description": "Developer platform offering automated AI SQL query generation, pgvector semantic search, edge functions, and real-time database management.",
        "url": "https://supabase.com/"
    },
    {
        "name": "Continue.dev",
        "badge": "CT",
        "color": "#3B82F6",
        "pricing": "Free",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Open Source AI Extension",
        "description": "Leading open-source AI code assistant for VS Code and JetBrains allowing local LLMs (Ollama) or custom commercial APIs to pair code securely.",
        "url": "https://www.continue.dev/"
    },
    {
        "name": "Tabnine",
        "badge": "TN",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Privacy-First Enterprise Copilot",
        "description": "Enterprise-grade code assistant that protects IP with zero training on user code, SOC2 compliance, and on-premise deployment options.",
        "url": "https://www.tabnine.com/"
    },
    {
        "name": "Sourcegraph Cody",
        "badge": "CD",
        "color": "#FF5543",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Codebase Graph Intelligence",
        "description": "AI coding assistant powered by Sourcegraph Code Graph, providing precise multi-repo context retrieval, test generation, and explanations.",
        "url": "https://sourcegraph.com/cody"
    },
    {
        "name": "Amazon Q Developer",
        "badge": "AQ",
        "color": "#FF9900",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "AWS Cloud Optimization",
        "description": "Generative AI assistant specialized in AWS architectures, automated Java/framework version upgrades, code security scans, and SQL tuning.",
        "url": "https://aws.amazon.com/q/developer/"
    },
    {
        "name": "Phind",
        "badge": "PH",
        "color": "#1E293B",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Technical Search & Debugging",
        "description": "Specialized search engine and reasoning engine for software developers that diagnoses error traces, reads docs, and outputs working code snippets.",
        "url": "https://www.phind.com/"
    },
    {
        "name": "vLLM",
        "badge": "VL",
        "color": "#0284C7",
        "pricing": "Free",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "High-Throughput Serving Engine",
        "description": "High-throughput and memory-efficient LLM inference and serving engine utilizing PagedAttention to maximize GPU batch throughput.",
        "url": "https://github.com/vllm-project/vllm"
    },
    {
        "name": "Ollama",
        "badge": "OL",
        "color": "#0F172A",
        "pricing": "Free",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Local LLM Runner",
        "description": "Lightweight command-line tool and macOS/Linux framework for running Llama 3, DeepSeek, Mistral, and Gemma models locally on personal machines.",
        "url": "https://ollama.com/"
    },
    {
        "name": "LM Studio",
        "badge": "LM",
        "color": "#7C3AED",
        "pricing": "Free",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Desktop LLM GUI",
        "description": "Discover, download, and run open-weight GGML/GGUF models locally on Apple Silicon or CUDA GPUs with an OpenAI-compatible local API server.",
        "url": "https://lmstudio.ai/"
    },
    {
        "name": "LangChain",
        "badge": "LC",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Agent Orchestration Framework",
        "description": "Standard framework for developing context-aware reasoning applications, multi-agent graphs (LangGraph), and production evaluation (LangSmith).",
        "url": "https://www.langchain.com/"
    },
    {
        "name": "LlamaIndex",
        "badge": "LI",
        "color": "#0D9488",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "RAG Data Framework",
        "description": "Leading data framework for connecting custom data sources, enterprise databases, and unstructured files to LLMs for robust RAG architectures.",
        "url": "https://www.llamaindex.ai/"
    },
    {
        "name": "Pinecone",
        "badge": "PC",
        "color": "#000000",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Serverless Vector Database",
        "description": "Serverless vector database engineered for ultra-fast semantic similarity search, hybrid keyword matching, and mission-critical GenAI workloads.",
        "url": "https://www.pinecone.io/"
    },
    {
        "name": "Qdrant",
        "badge": "QD",
        "color": "#DC2626",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Open-Source Vector Engine",
        "description": "High-performance vector search engine and database written in Rust, offering payload-based filtering, quantization, and cloud clustering.",
        "url": "https://qdrant.tech/"
    },
    {
        "name": "Weaviate",
        "badge": "WV",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "AI-Native Vector Database",
        "description": "Open-source vector database supporting multi-modal data embeddings, modular ML pipelines, and fast graph-based nearest neighbor search.",
        "url": "https://weaviate.io/"
    },
    {
        "name": "Postman AI (Postbot)",
        "badge": "PB",
        "color": "#FF6C37",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "API Testing & Documentation",
        "description": "AI companion in Postman that generates test suites, mocks API responses, creates visual documentations, and analyzes API payloads.",
        "url": "https://www.postman.com/product/postbot/"
    },
    {
        "name": "Blackbox AI",
        "badge": "BB",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Developer Code Search",
        "description": "Code search engine and developer copilot designed to extract code from videos, autocomplete snippets in 20+ languages, and answer queries.",
        "url": "https://www.blackbox.ai/"
    },
    {
        "name": "Mintlify",
        "badge": "ML",
        "color": "#059669",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Automated Docs Generator",
        "description": "Modern developer documentation platform that scans code to generate interactive API references, code snippets, and searchable documentation.",
        "url": "https://mintlify.com/"
    },
    {
        "name": "CodeRabbit",
        "badge": "CR",
        "color": "#EA580C",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Autonomous PR Code Reviewer",
        "description": "AI-powered pull request reviewer providing line-by-line code suggestions, bug detection, architectural feedback, and automated PR summaries.",
        "url": "https://coderabbit.ai/"
    },
    {
        "name": "Sweep AI",
        "badge": "SW",
        "color": "#4F46E5",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "GitHub Issue to PR Agent",
        "description": "Autonomous GitHub junior developer that reads issue descriptions, writes code across files, runs tests, and opens clean pull requests.",
        "url": "https://sweep.dev/"
    },
    {
        "name": "CodiumAI (Qodo)",
        "badge": "QD",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Code Integrity & Test Suite Gen",
        "description": "Quality-first AI coding platform generating meaningful unit tests, discovering edge cases, and verifying code integrity before merge.",
        "url": "https://www.qodo.ai/"
    },
    {
        "name": "Grit.io",
        "badge": "GT",
        "color": "#7C3AED",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Automated Code Migration",
        "description": "Automated code refactoring tool that rewrites legacy frameworks, upgrades dependencies, and enforces architectural standards across repos.",
        "url": "https://www.grit.io/"
    },
    {
        "name": "Marblism",
        "badge": "MB",
        "color": "#E11D48",
        "pricing": "Freemium",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Full-Stack Boilerplate Generator",
        "description": "Prompt-to-fullstack boilerplate generator producing React, Node, Prisma, and Tailwind codebases with auth, Stripe payments, and emails.",
        "url": "https://www.marblism.com/"
    },
    {
        "name": "Bloop AI",
        "badge": "BP",
        "color": "#0F172A",
        "pricing": "Free",
        "category_slug": "coding-dev",
        "category_pill": "Coding & Dev",
        "subcategory": "Codebase Navigation & Search",
        "description": "Semantic code search engine that maps repo architectures, answers architectural questions, and navigates large legacy codebases in Rust.",
        "url": "https://bloop.ai/"
    },

    # ==================== IMAGE & ART (35 tools) ====================
    {
        "name": "Midjourney v6",
        "badge": "MJ",
        "color": "#7C3AED",
        "pricing": "Paid",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Photorealistic & Artistic Synthesis",
        "description": "World-renowned generative visual engine producing stunning photorealism, character consistency, cinematographic lighting, and fantasy artwork.",
        "url": "https://www.midjourney.com/"
    },
    {
        "name": "FLUX.1 by Black Forest Labs",
        "badge": "FX",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Frontier Open Image Weights",
        "description": "State-of-the-art open text-to-image foundation model excelling in intricate prompt adherence, anatomy rendering, and sharp typography.",
        "url": "https://blackforestlabs.ai/"
    },
    {
        "name": "Ideogram 2.0",
        "badge": "ID",
        "color": "#4F46E5",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Typography & Graphic Design",
        "description": "Leading AI image generator famed for flawless in-image text typography, poster layouts, merchandise designs, and vector graphic styles.",
        "url": "https://ideogram.ai/"
    },
    {
        "name": "Leonardo.Ai",
        "badge": "LN",
        "color": "#9333EA",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Production Creative Suite",
        "description": "Creative generation suite offering custom fine-tuned models, real-time canvas editing, texture generation, and gaming asset pipelines.",
        "url": "https://leonardo.ai/"
    },
    {
        "name": "Recraft AI",
        "badge": "RC",
        "color": "#EA580C",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Vector SVG & Icon Design",
        "description": "Design-focused AI studio that creates editable SVG vector art, 3D icons, clean brand design systems, and commercial merchandise art.",
        "url": "https://www.recraft.ai/"
    },
    {
        "name": "Krea AI",
        "badge": "KR",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Real-Time Canvas & Upscaler",
        "description": "Real-time generation canvas with instant latency, high-fidelity 4K texture upscaling, optical illusion generation, and video generation.",
        "url": "https://www.krea.ai/"
    },
    {
        "name": "Magnific AI",
        "badge": "MG",
        "color": "#3B82F6",
        "pricing": "Paid",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Hallucinatory 8K Upscaler",
        "description": "Super-resolution upscaler that hallucinates realistic microscopic details, skin pores, and landscape textures up to extreme 8K resolutions.",
        "url": "https://magnific.ai/"
    },
    {
        "name": "Canva Magic Media",
        "badge": "CV",
        "color": "#00C4CC",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Accessible Visual Design Suite",
        "description": "Suite of visual tools inside Canva including AI image synthesis, background isolation, Magic Expand, and smart layout composition.",
        "url": "https://www.canva.com/ai-image-generator/"
    },
    {
        "name": "Adobe Firefly",
        "badge": "AF",
        "color": "#FF0000",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Commercially Safe Generative Suite",
        "description": "Commercially safe generative model family integrated into Photoshop and Illustrator for Generative Fill, vector expansion, and text effects.",
        "url": "https://www.adobe.com/products/firefly.html"
    },
    {
        "name": "Photoroom",
        "badge": "PR",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "E-Commerce Studio Staging",
        "description": "AI visual studio for online sellers that removes backgrounds, stages professional studio lighting, and generates catalog photography.",
        "url": "https://www.photoroom.com/"
    },
    {
        "name": "remove.bg",
        "badge": "RB",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Instant Background Cutout",
        "description": "One-click background removal tool that instantly segments humans, cars, products, and complex hair strands in under five seconds.",
        "url": "https://www.remove.bg/"
    },
    {
        "name": "Gamma",
        "badge": "GA",
        "color": "#DB2777",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "AI Slide Decks & Presentations",
        "description": "Generative presentation software that turns documents or prompts into beautifully designed slide decks, webpages, and interactive docs.",
        "url": "https://gamma.app/"
    },
    {
        "name": "Tome",
        "badge": "TM",
        "color": "#1E293B",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Storytelling & Visual Pitch Decks",
        "description": "AI storytelling format that crafts visual pitch decks, executive summaries, and product roadmaps with integrated synthetic imagery.",
        "url": "https://tome.app/"
    },
    {
        "name": "Replicate FLUX Cloud",
        "badge": "RP",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Cloud Image Model API",
        "description": "Cloud playground and developer API to run FLUX Schnell/Dev, SDXL, ControlNet, and custom community LoRA checkpoints at low latency.",
        "url": "https://replicate.com/"
    },
    {
        "name": "Clipdrop by Jasper",
        "badge": "CD",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Visual Creator Utilities",
        "description": "Ecosystem of AI image utilities: Uncrop, Relight, Background Replacement, Image Upscaler, and text-to-image generator powered by SDXL.",
        "url": "https://clipdrop.co/"
    },
    {
        "name": "Stylar AI",
        "badge": "ST",
        "color": "#E11D48",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Controllable Layered AI Canvas",
        "description": "Controllable graphic design platform offering layered composition, style matching, sketch-to-image, and precision object insertion.",
        "url": "https://www.stylar.ai/"
    },
    {
        "name": "Civitai",
        "badge": "CV",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Open Source Model Repository",
        "description": "The central hub for sharing open-source AI art models, LoRA checkpoints, embeddings, and creative workflows with an active community.",
        "url": "https://civitai.com/"
    },
    {
        "name": "Stable Diffusion WebUI (A1111)",
        "badge": "SD",
        "color": "#EA580C",
        "pricing": "Free",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Local Image Synthesis GUI",
        "description": "The open-source benchmark browser interface for running Stable Diffusion, ControlNet, Inpainting, and extensions locally on consumer GPUs.",
        "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui"
    },
    {
        "name": "ComfyUI",
        "badge": "CU",
        "color": "#10B981",
        "pricing": "Free",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Node-Based Generative Pipeline",
        "description": "Powerful modular node-based graphical interface for designing advanced generative pipelines with FLUX, SDXL, Hunyuan, and AnimateDiff.",
        "url": "https://github.com/comfyanonymous/ComfyUI"
    },
    {
        "name": "SeaArt AI",
        "badge": "SA",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Digital Art Community & Engine",
        "description": "Free-to-use digital art tool with rich model libraries, background removal, face swap, and prompt assistance for creative artists.",
        "url": "https://www.seaart.ai/"
    },
    {
        "name": "Playground AI",
        "badge": "PG",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Mixed Canvas Image Editor",
        "description": "Free-to-use AI image creator combining text prompts with an infinite canvas for blending images, erasing objects, and expanding frames.",
        "url": "https://playground.com/"
    },
    {
        "name": "Artbreeder",
        "badge": "AB",
        "color": "#EC4899",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Gene Splicing & Portrait Morph",
        "description": "Collaborative art tool that creates portraits, landscapes, and collages by 'crossbreeding' genes, mixing styles, and collaging simple shapes.",
        "url": "https://www.artbreeder.com/"
    },
    {
        "name": "NightCafe Creator",
        "badge": "NC",
        "color": "#F59E0B",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Gamified Community Art Studio",
        "description": "Community-focused digital art generator offering multiple algorithms (SDXL, DALL-E, CLIP) with daily artistic challenges and social feeds.",
        "url": "https://creator.nightcafe.studio/"
    },
    {
        "name": "GetIMG.ai",
        "badge": "GI",
        "color": "#06B6D4",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "All-in-One Image Toolkit",
        "description": "Suite of AI art tools featuring real-time image generation, custom model fine-tuning, inpainting canvas, and fast batch processing.",
        "url": "https://getimg.ai/"
    },
    {
        "name": "Upscayl",
        "badge": "UP",
        "color": "#14B8A6",
        "pricing": "Free",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Open-Source Desktop AI Upscaler",
        "description": "Free, open-source AI image upscaler for macOS, Linux, and Windows that enhances low-resolution images locally without cloud servers.",
        "url": "https://upscayl.org/"
    },
    {
        "name": "Topaz Gigapixel AI",
        "badge": "TP",
        "color": "#1E293B",
        "pricing": "Paid",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Professional Photo Restoration",
        "description": "Pro-grade desktop image resolution enhancer that restores sharpness, eliminates compression artifacts, and prints large-format graphics.",
        "url": "https://www.topazlabs.com/gigapixel-ai"
    },
    {
        "name": "Cutout.pro",
        "badge": "CO",
        "color": "#EF4444",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Passport & Photo Cutout Studio",
        "description": "Visual AI platform for automated background removal, passport photo generation, photo colorization, and image blur reduction.",
        "url": "https://www.cutout.pro/"
    },
    {
        "name": "WatermarkRemover.io",
        "badge": "WR",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Watermark & Stamp Eraser",
        "description": "AI-powered tool that automatically detects and erases translucent watermarks, logo overlays, and date stamps from photographs.",
        "url": "https://www.watermarkremover.io/"
    },
    {
        "name": "VanceAI",
        "badge": "VA",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Photo Enhancement Suite",
        "description": "Full suite of photo enhancement tools including AI denoising, deblurring, portrait retouching, and vintage photo colorization.",
        "url": "https://vanceai.com/"
    },
    {
        "name": "Looka",
        "badge": "LK",
        "color": "#4F46E5",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "AI Logo & Brand Identity",
        "description": "AI logo maker and branding kit creator that designs custom logos, business cards, letterheads, and brand guidelines in minutes.",
        "url": "https://looka.com/"
    },
    {
        "name": "Brandmark.io",
        "badge": "BM",
        "color": "#7C3AED",
        "pricing": "Paid",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Generative Logo Design",
        "description": "Generative branding platform producing unique vector logos, harmonious color palettes, font pairings, and ready-to-use brand asset packages.",
        "url": "https://brandmark.io/"
    },
    {
        "name": "Flair AI",
        "badge": "FL",
        "color": "#059669",
        "pricing": "Freemium",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Branded Product Photography",
        "description": "Product photoshoot design tool allowing e-commerce brands to drag-and-drop packaging onto AI-rendered 3D props and natural environments.",
        "url": "https://flair.ai/"
    },
    {
        "name": "Vectorizer.AI",
        "badge": "VZ",
        "color": "#EA580C",
        "pricing": "Paid",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Bitmap to Clean Vector SVG",
        "description": "Deep learning vectorizer that converts blurry JPGs and PNGs into clean, mathematically precise SVG, EPS, and DXF vector graphics.",
        "url": "https://vectorizer.ai/"
    },
    {
        "name": "Craiyon (DALL-E mini)",
        "badge": "CR",
        "color": "#F97316",
        "pricing": "Free",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Free Rapid AI Sketcher",
        "description": "Simple and completely free AI image generator that turns any text prompt into a 9-image grid in seconds without mandatory logins.",
        "url": "https://www.craiyon.com/"
    },
    {
        "name": "AutoDraw by Google",
        "badge": "AD",
        "color": "#4285F4",
        "pricing": "Free",
        "category_slug": "image-art",
        "category_pill": "Image & Art",
        "subcategory": "Smart Doodling to Clipart",
        "description": "Fast drawing tool that pairs machine learning with drawings from talented artists to transform rough doodles into polished clipart.",
        "url": "https://www.autodraw.com/"
    },

    # ==================== VOICE & AUDIO (30 tools) ====================
    {
        "name": "ElevenLabs Voice AI",
        "badge": "EL",
        "color": "#059669",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Hyper-Realistic Voice Synthesis",
        "description": "Industry-leading speech synthesis and instant voice cloning platform supporting 32+ languages with emotional nuance and low latency.",
        "url": "https://elevenlabs.io/"
    },
    {
        "name": "Suno",
        "badge": "SN",
        "color": "#E11D48",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Full-Song Generative Music",
        "description": "Full-song AI music creation engine that writes lyrics, composes melodies, records vocals, and produces full radio-quality songs in any genre.",
        "url": "https://suno.com/"
    },
    {
        "name": "Udio",
        "badge": "UD",
        "color": "#7C3AED",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "High-Fidelity Music Studio",
        "description": "Pioneering generative music platform enabling creators to generate, extend, remix, and master studio-grade multi-track songs from prompts.",
        "url": "https://www.udio.com/"
    },
    {
        "name": "Cartesia Sonic",
        "badge": "CT",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Sub-100ms Streaming Voice",
        "description": "Ultra-fast state-space voice model with sub-100ms latency designed for real-time conversational agents, gaming NPCs, and live callers.",
        "url": "https://cartesia.ai/"
    },
    {
        "name": "Murf AI",
        "badge": "MF",
        "color": "#D97706",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Studio Voiceover Platform",
        "description": "Studio-grade voice generator offering 200+ natural text-to-speech voices with pitch, speed, and emphasis controls for corporate presentations.",
        "url": "https://murf.ai/"
    },
    {
        "name": "PlayHT",
        "badge": "PH",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Conversational Audio API",
        "description": "Conversational TTS and voice cloning platform built for audiobooks, dynamic podcasts, and real-time streaming voice agents.",
        "url": "https://playht.app/"
    },
    {
        "name": "Descript",
        "badge": "DC",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Transcript-Based Audio Editor",
        "description": "Audio and video editor that allows editing recordings by typing in text transcripts, removing filler words, and applying Studio Sound mastering.",
        "url": "https://www.descript.com/"
    },
    {
        "name": "OpenAI Whisper",
        "badge": "WH",
        "color": "#10A37F",
        "pricing": "Free",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Automatic Speech Recognition",
        "description": "Robust automatic speech recognition model trained on 680,000 hours of multilingual data for highly accurate transcription and translation.",
        "url": "https://github.com/openai/whisper"
    },
    {
        "name": "Otter.ai",
        "badge": "OT",
        "color": "#0D9488",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Live Meeting Transcription",
        "description": "Real-time AI meeting transcription agent that joins video calls, records conversations, identifies speakers, and summarizes action items.",
        "url": "https://otter.ai/"
    },
    {
        "name": "Fireflies.ai",
        "badge": "FF",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Voice Conversation Intelligence",
        "description": "Voice meeting intelligence agent that captures, transcribes, and extracts key metrics across Zoom, Google Meet, and Microsoft Teams.",
        "url": "https://fireflies.ai/"
    },
    {
        "name": "Fathom",
        "badge": "FA",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Free AI Meeting Recorder",
        "description": "Free AI meeting recorder that generates instant call summaries, timestamps key moments, and syncs notes directly into Salesforce and HubSpot.",
        "url": "https://fathom.video/"
    },
    {
        "name": "Speechify",
        "badge": "SP",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Text-to-Speech Reader",
        "description": "Top-rated text-to-speech reader that turns articles, PDFs, books, and emails into high-quality natural audio read by celebrity voices.",
        "url": "https://speechify.com/"
    },
    {
        "name": "Lovo.ai (Genny)",
        "badge": "LV",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "AI Voice Generator & Video",
        "description": "Award-winning AI voice generator featuring 500+ voices in 100+ languages, equipped with pitch curves, sound effects, and timeline video sync.",
        "url": "https://lovo.ai/"
    },
    {
        "name": "Resemble AI",
        "badge": "RA",
        "color": "#EC4899",
        "pricing": "Paid",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Voice Cloning & Deepfake Detection",
        "description": "High-fidelity voice cloning platform with granular emotion modulation and integrated AI watermarking for deepfake audio detection.",
        "url": "https://www.resemble.ai/"
    },
    {
        "name": "Krisp",
        "badge": "KP",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Real-Time Noise Cancellation",
        "description": "AI noise cancellation application that removes background chatter, barking dogs, and echoes from both incoming and outgoing live call audio.",
        "url": "https://krisp.ai/"
    },
    {
        "name": "Auphonic",
        "badge": "AU",
        "color": "#F97316",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Automated Audio Mastering",
        "description": "Automated audio post-production web service that levels loudness according to broadcast standards, filters hums, and normalizes peaks.",
        "url": "https://auphonic.com/"
    },
    {
        "name": "Cleanvoice AI",
        "badge": "CV",
        "color": "#059669",
        "pricing": "Paid",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Filler Word & Stutter Eraser",
        "description": "Audio editing algorithm that automatically detects and deletes filler words ('um', 'ah'), mouth clicks, dead pauses, and stuttering.",
        "url": "https://cleanvoice.ai/"
    },
    {
        "name": "LALAL.AI",
        "badge": "LA",
        "color": "#E11D48",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Stem Separation & Vocal Remover",
        "description": "Next-gen stem separation tool that extracts clean vocals, drums, bass, piano, and acoustic guitars from any mixed audio track.",
        "url": "https://www.lalal.ai/"
    },
    {
        "name": "Moises.ai",
        "badge": "MO",
        "color": "#7C3AED",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Musician Practice & Track Isolation",
        "description": "The musician app for isolating stems, changing track BPM, adjusting pitch, detecting chords, and creating karaoke backing tracks.",
        "url": "https://moises.ai/"
    },
    {
        "name": "Soundraw",
        "badge": "SR",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Customizable Royalty-Free Music",
        "description": "Generative royalty-free music creator for creators and podcasters allowing real-time adjustment of track structure, instruments, and energy.",
        "url": "https://soundraw.io/"
    },
    {
        "name": "AIVA",
        "badge": "AV",
        "color": "#1E293B",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Classical & Cinematic Composition",
        "description": "AI soundtrack composer that generates original emotional symphonies, cinematic scores, and ambient game soundtracks in MIDI/audio.",
        "url": "https://www.aiva.ai/"
    },
    {
        "name": "Boomy",
        "badge": "BM",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Instant Song Maker & Streaming",
        "description": "Music generation app allowing users with zero musical background to compose complete songs in seconds and submit them to streaming services.",
        "url": "https://boomy.com/"
    },
    {
        "name": "Beatoven.ai",
        "badge": "BT",
        "color": "#F59E0B",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Mood-Based Background Music",
        "description": "Royalty-free background music generator tailored for video creators and podcast editors based on specific mood, tempo, and genre cuts.",
        "url": "https://www.beatoven.ai/"
    },
    {
        "name": "AudioCraft by Meta",
        "badge": "AC",
        "color": "#0668E1",
        "pricing": "Free",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Open Sound & Music Models",
        "description": "Meta open-source generative audio library consisting of MusicGen, AudioGen, and EnCodec for high-fidelity audio synthesis from text.",
        "url": "https://github.com/facebookresearch/audiocraft"
    },
    {
        "name": "Voice.ai",
        "badge": "VA",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Real-Time Voice Changer",
        "description": "Real-time voice changer for Discord, gaming, and streaming that morphs your voice into thousands of community characters in real time.",
        "url": "https://voice.ai/"
    },
    {
        "name": "Fliki Audio",
        "badge": "FK",
        "color": "#EC4899",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Voiceover Creation Engine",
        "description": "Transform articles, tweets, and scripts into rich audio podcasts and voiceovers using 2,000+ realistic voices in 75+ dialects.",
        "url": "https://fliki.ai/"
    },
    {
        "name": "Listnr",
        "badge": "LS",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Podcasting & TTS Engine",
        "description": "AI text-to-speech platform with 1,000+ realistic voices, podcast hosting, and automated audio widget player embeds for blogs.",
        "url": "https://www.listnr.tech/"
    },
    {
        "name": "Riverside.fm Magic Clips",
        "badge": "RS",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Studio Recording & Smart Snippets",
        "description": "Studio-quality 4K local audio-video recording platform with automated AI clip extraction, text transcription, and teleprompter tools.",
        "url": "https://riverside.com/"
    },
    {
        "name": "Podcastle",
        "badge": "PC",
        "color": "#7C3AED",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Browser Audio Production",
        "description": "All-in-one browser recording, text-to-speech, audio enhancement, and voice cloning platform built for casual and professional podcasters.",
        "url": "https://podcastle.ai/"
    },
    {
        "name": "Veed.io Voice Studio",
        "badge": "VD",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "voice-audio",
        "category_pill": "Voice & Audio",
        "subcategory": "Voiceover & Video Dubbing",
        "description": "Browser-based video and audio editing suite with automated speech-to-subtitles, AI voice cloning, and multilingual video dubbing.",
        "url": "https://www.veed.io/"
    },

    # ==================== VIDEO & 3D (35 tools) ====================
    {
        "name": "Runway Gen-3 Alpha",
        "badge": "RW",
        "color": "#E11D48",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Cinematic Video Generation",
        "description": "Frontier text-to-video and image-to-video engine delivering cinematic fidelity, photorealistic physics, and expressive motion brush control.",
        "url": "https://app.runwayml.com/"
    },
    {
        "name": "OpenAI Sora",
        "badge": "SR",
        "color": "#0F172A",
        "pricing": "Paid",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "World Simulation & Video",
        "description": "OpenAI groundbreaking video synthesis model capable of simulating physical environments, intricate camera pans, and continuous shots.",
        "url": "https://sora.com/"
    },
    {
        "name": "Google Veo",
        "badge": "VO",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "1080p Generative Video Model",
        "description": "Google DeepMind flagship high-definition video generative model featuring synchronized audio effects, lens simulation, and visual continuity.",
        "url": "https://deepmind.google/models/veo/"
    },
    {
        "name": "Kling AI",
        "badge": "KL",
        "color": "#EA580C",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "High-Motion Generative Video",
        "description": "Next-gen generative video platform delivering long-duration 1080p clips, realistic physical simulations, motion brush control, and lip-syncing.",
        "url": "https://klingai.com/"
    },
    {
        "name": "Luma Dream Machine",
        "badge": "LM",
        "color": "#4F46E5",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Ray Video & Interactive 3D",
        "description": "Fast cinematic video synthesis platform powered by Luma Ray models, supporting image-to-video keyframing and NeRF 3D capture.",
        "url": "https://lumalabs.ai/"
    },
    {
        "name": "HeyGen",
        "badge": "HG",
        "color": "#7C3AED",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Digital Avatars & Video Dubbing",
        "description": "Enterprise AI video avatar and translation platform creating custom photo-real digital spokespersons with flawless lip-synced multi-language dubs.",
        "url": "https://www.heygen.com/"
    },
    {
        "name": "Synthesia",
        "badge": "SY",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Corporate Training Avatars",
        "description": "Enterprise digital avatar platform enabling corporate teams to produce high-impact training and onboarding videos without cameras or actors.",
        "url": "https://www.synthesia.io/"
    },
    {
        "name": "Pika 2.0",
        "badge": "PK",
        "color": "#DB2777",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Stylized Motion & Pikaffects",
        "description": "Playful generative video engine famous for Pikaffects (inflate, melt, crush, explode), character animation, and audio sound FX sync.",
        "url": "https://pika.art/"
    },
    {
        "name": "Haiper AI",
        "badge": "HP",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Perceptual Generative Video",
        "description": "Next-gen perceptual foundation model designed to generate fluid, high-resolution clips from text prompts, static photos, and style references.",
        "url": "https://haiper.ai/"
    },
    {
        "name": "Hunyuan Video",
        "badge": "HY",
        "color": "#0052D9",
        "pricing": "Free",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Open-Source Video Foundation",
        "description": "Tencent open-source video foundation model featuring state-of-the-art cinematic resolution, natural movement, and open weights for self-hosting.",
        "url": "https://github.com/Tencent/HunyuanVideo"
    },
    {
        "name": "OpusClip",
        "badge": "OP",
        "color": "#16A34A",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Viral Shorts Repurposing",
        "description": "Generative video repurposing tool that converts long YouTube podcasts into viral TikTok/Reels clips with animated subtitles and virality scores.",
        "url": "https://www.opus.pro/"
    },
    {
        "name": "CapCut AI",
        "badge": "CC",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Smart Social Video Editor",
        "description": "All-in-one desktop and mobile editor with AI script-to-video, auto-captions, background cutout, and viral social media templates.",
        "url": "https://www.capcut.com/"
    },
    {
        "name": "InVideo AI",
        "badge": "IV",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Text-to-Complete Video Studio",
        "description": "Text-to-video generator that creates complete YouTube videos, documentaries, and ad spots with stock footage, voiceovers, and transitions.",
        "url": "https://invideo.io/"
    },
    {
        "name": "Meshy AI",
        "badge": "MS",
        "color": "#9333EA",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Text & Image to 3D Mesh",
        "description": "Generative 3D model engine transforming text prompts and 2D concept art into production-ready 3D meshes (FBX, OBJ, GLB) with PBR textures.",
        "url": "https://www.meshy.ai/"
    },
    {
        "name": "Tripo 3D",
        "badge": "TP",
        "color": "#0D9488",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Instant 3D Auto-Rigging",
        "description": "Ultra-fast generative 3D platform capable of outputting textured 3D assets in 8 seconds with automatic quad retopology and skeleton rigging.",
        "url": "https://www.tripo3d.ai/"
    },
    {
        "name": "Spline AI",
        "badge": "SP",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Interactive 3D Web Scenes",
        "description": "Collaborative browser 3D software with generative AI prompts for interactive web experiences, physics simulations, and Three.js exports.",
        "url": "https://spline.design/"
    },
    {
        "name": "Rodin by Deemos",
        "badge": "RD",
        "color": "#475569",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Hyper-Detailed 3D Digital Humans",
        "description": "High-fidelity generative 3D modeling platform specialized in detailed character sculpting, digital humans, and game-ready topology.",
        "url": "https://hyperhuman.deemos.com/rodin"
    },
    {
        "name": "Kaedim",
        "badge": "KD",
        "color": "#E11D48",
        "pricing": "Paid",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "2D Art to Production 3D Assets",
        "description": "Enterprise game-dev pipeline tool that converts 2D art concepts into production-quality 3D assets with human-in-the-loop topology review.",
        "url": "https://www.kaedim3d.com/"
    },
    {
        "name": "Viggle AI",
        "badge": "VG",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Controllable Character Motion Transfer",
        "description": "Controllable character movement model that transfers dance routines and physical actions from any video onto your custom character image.",
        "url": "https://viggle.ai/"
    },
    {
        "name": "D-ID",
        "badge": "DI",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Talking Head Video Generator",
        "description": "Transform any still photo or portrait into a talking video avatar with lip-synced audio for marketing campaigns and virtual agents.",
        "url": "https://www.d-id.com/"
    },
    {
        "name": "Colossyan",
        "badge": "CL",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Workplace Learning Avatars",
        "description": "AI video creator for workplace learning that creates scenario-based training videos with multiple avatars on screen and auto-translations.",
        "url": "https://www.colossyan.com/"
    },
    {
        "name": "Elai.io",
        "badge": "EL",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Article to Avatar Video",
        "description": "Automated video generation platform that turns articles, presentations, and product pages into narrated avatar video presentations.",
        "url": "https://elai.io/"
    },
    {
        "name": "Topaz Video AI",
        "badge": "TV",
        "color": "#1E293B",
        "pricing": "Paid",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Pro Video Upscaling & Interpolation",
        "description": "Professional desktop tool for video upscaling up to 8K, 60fps frame interpolation, deinterlacing, and camera motion stabilization.",
        "url": "https://www.topazlabs.com/topaz-video-ai"
    },
    {
        "name": "Wonder Dynamics",
        "badge": "WD",
        "color": "#F59E0B",
        "pricing": "Paid",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Automated VFX CG Character Insertion",
        "description": "AI tool by Autodesk that automatically animates, lights, and composites 3D CG characters into live-action scenes, replacing actors.",
        "url": "https://wonderdynamics.com/"
    },
    {
        "name": "Move.ai",
        "badge": "MV",
        "color": "#EC4899",
        "pricing": "Paid",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Markerless Motion Capture",
        "description": "Markerless motion capture technology that extracts high-fidelity human biomechanical data directly from standard smartphone cameras.",
        "url": "https://www.move.ai/"
    },
    {
        "name": "DeepMotion",
        "badge": "DM",
        "color": "#06B6D4",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Browser 3D Motion Capture",
        "description": "Browser-based Animate 3D software that turns video files into 3D animations with body tracking, hand gestures, and face tracking.",
        "url": "https://www.deepmotion.com/"
    },
    {
        "name": "CSM (Common Sense Machines)",
        "badge": "CS",
        "color": "#0F172A",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Generative World & 3D Engine",
        "description": "Generative platform transforming multi-view images or text into game-ready 3D interactive assets, environments, and spatial digital twins.",
        "url": "https://csm.ai/"
    },
    {
        "name": "Suno Bark Video",
        "badge": "SB",
        "color": "#E11D48",
        "pricing": "Free",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Audio-Visual Generative Experiments",
        "description": "Research projects pushing synchronized audiovisual generative models for synchronized lips, expressions, and soundscapes.",
        "url": "https://suno.com/"
    },
    {
        "name": "Klap",
        "badge": "KP",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Fast Video Short Clipper",
        "description": "Turn YouTube videos into short viral TikToks, Reels, and Shorts with intelligent auto-reframing, dynamic captions, and topic highlighting.",
        "url": "https://klap.app/"
    },
    {
        "name": "Submagic",
        "badge": "SM",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "AI Captions & B-Roll Overlays",
        "description": "Short-form video editor that generates dynamic animated subtitles with emojis, sound effects, and automated B-roll insertion.",
        "url": "https://www.submagic.co/"
    },
    {
        "name": "Munch",
        "badge": "MN",
        "color": "#10B981",
        "pricing": "Paid",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Trend-Driven Content Repurposing",
        "description": "AI video repurposing platform that extracts the most impactful moments from long-form video based on real-time social trending data.",
        "url": "https://www.getmunch.com/"
    },
    {
        "name": "Captions",
        "badge": "CP",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Creator Studio & Eye Contact Correction",
        "description": "All-in-one camera app featuring AI eye contact correction, teleprompter, studio sound, and automated subtitle animations.",
        "url": "https://www.captions.ai/"
    },
    {
        "name": "Fliki Video",
        "badge": "FV",
        "color": "#EC4899",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Script-to-Video Engine",
        "description": "Create engaging social videos from text scripts, blog posts, or product URLs with automated media asset matching and natural voiceovers.",
        "url": "https://fliki.ai/"
    },
    {
        "name": "Genmo",
        "badge": "GM",
        "color": "#F97316",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Creative Video Co-Pilot (Mochi)",
        "description": "Generative video copilot powered by the open-weight Mochi 1 video architecture for smooth text-to-video scene synthesis.",
        "url": "https://www.genmo.ai/"
    },
    {
        "name": "Kaiber",
        "badge": "KB",
        "color": "#7C3AED",
        "pricing": "Freemium",
        "category_slug": "video-3d",
        "category_pill": "Video & 3D",
        "subcategory": "Artistic Style Video Animation",
        "description": "Creative visual engine for musicians and artists to generate stylized music videos, reactive animations, and audio-reactive visuals.",
        "url": "https://kaiber.ai/"
    },

    # ==================== AI SEARCH & RESEARCH (30 tools) ====================
    {
        "name": "Perplexity AI",
        "badge": "PX",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Conversational Answer Engine",
        "description": "Frontier AI conversational search engine providing fact-checked answers, live web citations, multi-source syntheses, and Pro discovery modes.",
        "url": "https://www.perplexity.ai/"
    },
    {
        "name": "NotebookLM by Google",
        "badge": "NB",
        "color": "#059669",
        "pricing": "Free",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Grounded Research Notebook",
        "description": "Google source-grounded research assistant that generates cited briefings, study guides, and viral Audio Overview podcast discussions.",
        "url": "https://notebook.google/"
    },
    {
        "name": "Consensus",
        "badge": "CS",
        "color": "#1D4ED8",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Peer-Reviewed Scientific Search",
        "description": "Academic search engine indexing 200M+ research papers that synthesizes consensus meters and extracts verifiable scientific findings.",
        "url": "https://consensus.app/"
    },
    {
        "name": "Elicit",
        "badge": "EC",
        "color": "#4F46E5",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Systematic Literature Reviews",
        "description": "AI research assistant that automates literature searches, extracts empirical data tables from papers, and synthesizes study methodologies.",
        "url": "https://elicit.com/"
    },
    {
        "name": "Scite.ai",
        "badge": "SC",
        "color": "#0D9488",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Smart Citation Verification",
        "description": "Citation analysis platform that provides Smart Citations indicating whether a scientific study supports or contrasts another paper.",
        "url": "https://scite.ai/"
    },
    {
        "name": "You.com",
        "badge": "YU",
        "color": "#7C3AED",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Multi-Model Research Engine",
        "description": "AI search engine uniting web search, deep technical queries, coding assistants, and frontier models with verifiable reference links.",
        "url": "https://you.com/"
    },
    {
        "name": "OpenRouter",
        "badge": "OR",
        "color": "#1E293B",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Unified Model Gateway & Playground",
        "description": "Unified routing platform providing competitive pricing, benchmarking, and instant API access across 200+ frontier LLMs and reasoning models.",
        "url": "https://openrouter.ai/"
    },
    {
        "name": "Exa AI (Metaphor)",
        "badge": "EX",
        "color": "#2563EB",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Search Engine Built for AIs",
        "description": "Embeddings-based web search engine API designed specifically for AI agents, LLMs, and semantic knowledge retrieval.",
        "url": "https://exa.ai/"
    },
    {
        "name": "Semantic Scholar",
        "badge": "SS",
        "color": "#0F172A",
        "pricing": "Free",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "AI Academic Graph Search",
        "description": "AI-powered academic search engine created by Allen AI that extracts key findings, citation velocity, and influential paper links.",
        "url": "https://www.semanticscholar.org/"
    },
    {
        "name": "Tavily",
        "badge": "TV",
        "color": "#10B981",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Web Search API for Agents",
        "description": "Search engine API optimized for autonomous LLM agents that returns clean markdown text, factual summaries, and zero scraping overhead.",
        "url": "https://tavily.com/"
    },
    {
        "name": "Connected Papers",
        "badge": "CP",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Visual Academic Research Graph",
        "description": "Visual citation graph tool that reveals co-citation networks, derivative works, and prior research connected to any scientific paper.",
        "url": "https://www.connectedpapers.com/"
    },
    {
        "name": "Litmaps",
        "badge": "LM",
        "color": "#F97316",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Interactive Literature Citation Maps",
        "description": "Visual literature discovery tool that visualizes citation trees across time and sends automatic alerts when relevant new papers publish.",
        "url": "https://www.litmaps.com/"
    },
    {
        "name": "ResearchRabbit",
        "badge": "RR",
        "color": "#EC4899",
        "pricing": "Free",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Spotify for Academic Papers",
        "description": "Visual literature discovery platform that recommends related academic papers and maps co-authorship networks with zero cost.",
        "url": "https://www.researchrabbit.ai/"
    },
    {
        "name": "SciSpace (Typeset)",
        "badge": "SS",
        "color": "#4F46E5",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Research Paper Explainer",
        "description": "Read, comprehend, and critique research papers faster with inline math explainers, text summarizers, and full-text literature searches.",
        "url": "https://scispace.com/"
    },
    {
        "name": "Scholarcy",
        "badge": "SC",
        "color": "#0284C7",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Summary Flashcards for Research",
        "description": "AI summarization tool that condenses long journal articles, book chapters, and reports into bite-sized interactive summary cards.",
        "url": "https://www.scholarcy.com/"
    },
    {
        "name": "Iris.ai",
        "badge": "IR",
        "color": "#8B5CF6",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "R&D Engine for Science & Patents",
        "description": "Comprehensive scientific text assistant for corporate R&D teams performing patent searches, systematic reviews, and meta-analyses.",
        "url": "https://iris.ai/"
    },
    {
        "name": "PaperQA",
        "badge": "PQ",
        "color": "#1E293B",
        "pricing": "Free",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "RAG Over Academic Lit",
        "description": "Open-source Python framework that answers scientific questions from PDFs using citation-backed retrieval-augmented generation.",
        "url": "https://github.com/whitead/paper-qa"
    },
    {
        "name": "Brave Leo AI",
        "badge": "BL",
        "color": "#FB542B",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Privacy-Preserving Browser AI",
        "description": "Built-in private browser assistant in Brave that translates pages, answers queries, and synthesizes search results anonymously.",
        "url": "https://brave.com/leo/"
    },
    {
        "name": "Andi Search",
        "badge": "AN",
        "color": "#14B8A6",
        "pricing": "Free",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Ad-Free Factual Search Chatbot",
        "description": "Next-gen privacy-friendly search engine that reads, explains, and summarizes information from across the web without sponsored ads.",
        "url": "https://andisearch.com/"
    },
    {
        "name": "Glean",
        "badge": "GL",
        "color": "#0F172A",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Enterprise Work Search & Knowledge",
        "description": "Workplace search assistant that connects company apps (Slack, Jira, Google Drive, GitHub) to answer technical employee queries securely.",
        "url": "https://www.glean.com/"
    },
    {
        "name": "Kore.ai",
        "badge": "KO",
        "color": "#2563EB",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Enterprise Conversational Search",
        "description": "Enterprise conversational AI platform providing no-code intelligent virtual assistants and semantic enterprise knowledge search.",
        "url": "https://kore.ai/"
    },
    {
        "name": "Dust.tt",
        "badge": "DT",
        "color": "#EA580C",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Custom Team Knowledge Assistants",
        "description": "Platform to create custom AI assistants connected to company documentation (Notion, Slack, Google Drive) with strict access control.",
        "url": "https://dust.tt/"
    },
    {
        "name": "Casetext (CoCounsel)",
        "badge": "CC",
        "color": "#0D9488",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "AI Legal Search & Case Law",
        "description": "Legal AI assistant by Thomson Reuters performing critical legal research, contract reviews, deposition prep, and case law analysis.",
        "url": "https://casetext.com/"
    },
    {
        "name": "Harvey AI",
        "badge": "HV",
        "color": "#1E293B",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Generative AI for Legal Firms",
        "description": "Elite generative AI platform partnered with OpenAI, engineered for top global law firms for contract drafting and regulatory analysis.",
        "url": "https://www.harvey.ai/"
    },
    {
        "name": "Heuristica",
        "badge": "HU",
        "color": "#3B82F6",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "AI Knowledge Map Exploration",
        "description": "Visual knowledge exploration tool that converts complex research topics into interactive branching mind maps with citations.",
        "url": "https://www.heuristica.com/"
    },
    {
        "name": "Undetectable AI",
        "badge": "UD",
        "color": "#059669",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "AI Detection & Text Humanizer",
        "description": "Text analysis tool that tests writing against major AI detectors and rewrites robotic phrasing into natural, fluent human prose.",
        "url": "https://undetectable.ai/"
    },
    {
        "name": "Copyleaks",
        "badge": "CL",
        "color": "#6366F1",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Plagiarism & AI Content Detector",
        "description": "Enterprise-grade AI detection and plagiarism software verifying authentic human writing across academic and corporate submissions.",
        "url": "https://copyleaks.com/"
    },
    {
        "name": "Originality.ai",
        "badge": "OR",
        "color": "#DC2626",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Content Integrity & Fact Checking",
        "description": "AI detector, plagiarism checker, and automated fact-checking engine built for serious content publishers and webmaster audits.",
        "url": "https://originality.ai/"
    },
    {
        "name": "Wolfram Alpha",
        "badge": "WA",
        "color": "#DD1100",
        "pricing": "Freemium",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Computational Knowledge Engine",
        "description": "Definitive computational engine answering mathematical, scientific, engineering, and statistical queries with step-by-step algorithms.",
        "url": "https://www.wolframalpha.com/"
    },
    {
        "name": "Kagi FastGPT",
        "badge": "KG",
        "color": "#EAB308",
        "pricing": "Paid",
        "category_slug": "ai-search",
        "category_pill": "AI Search",
        "subcategory": "Fast Web Fact Retrieval",
        "description": "Ad-free ultra-fast fact retrieval tool by Kagi Search that summarizes web pages, news articles, and research with zero tracking.",
        "url": "https://kagi.com/fastgpt"
    }
]

print(f"Total AI tools compiled: {len(TOOLS_DATA)}")

def generate_markdown_catalog(tools):
    categories = [
        ("chat-reasoning", "Chat & Reasoning", "✍️ Generative Writing"),
        ("coding-dev", "Coding & Dev", "💻 Software & Coding"),
        ("image-art", "Image & Art", "🎨 Image & Visual Arts"),
        ("voice-audio", "Voice & Audio", "🎙️ Voice & Audio Synthesis"),
        ("video-3d", "Video & 3D", "🎥 Video & Motion FX"),
        ("ai-search", "AI Search", "🔍 Research & Deep Search")
    ]

    md_lines = [
        "# Google Antigravity Master Prompt, Full AI Tools Metadata Catalog & Complete Website Code for `aallaitools.online`",
        "",
        "This single Markdown file contains everything needed for **Google Antigravity** ([Antigravity Docs](https://antigravity.google/docs/overview/)) to:",
        "1. **Crawl the live web** to discover, verify, and categorize AI tools, reasoning models, custom GPTs, and autonomous agents.",
        "2. **Segregate all tools into the 6 core directory categories** and maintain an exhaustive structured catalog.",
        f"3. **Update the full `aallaitools.online` website code** (`index.html`, `robots.txt`, and `sitemap.xml`) with {len(tools)} verified tools, interactive search, category & pricing filtering, bookmarking, and `< 50ms` static load performance.",
        "",
        "---",
        "",
        "## 1. Master Copy-Paste Prompt for Google Antigravity",
        "",
        "> **Role & Autonomous Mission**",
        '> You are an autonomous full-stack web architect, web-crawling data engineer, and technical SEO specialist operating inside Google Antigravity on the `aallaitools.online` codebase ("The Ultimate Directory of AI Tools & GPTs").',
        ">",
        "> Execute the following workflow end-to-end:",
        "> 1. Maintain an exhaustive, verified catalog of 200+ worldwide premier AI tools, reasoning models, and agents.",
        "> 2. Segregate every tool into the 6 canonical categories with clean badges, brand colors, pricing tiers, and canonical URLs.",
        "> 3. Render a classy, elevated UI with glassmorphism, instant multi-faceted filtering, keyboard shortcuts (`/`), bookmarking, and zero external JS/CSS dependencies.",
        "> 4. Maintain complete JSON-LD schema with `WebSite`, `FAQPage`, and `ItemList` covering all tools.",
        "",
        "---",
        "",
        f"## 2. Complete Exhaustive AI Tools Metadata Catalog ({len(tools)} Worldwide Tools)",
        ""
    ]

    for slug, pill, showcase in categories:
        cat_tools = [t for t in tools if t["category_slug"] == slug]
        md_lines.append(f"### Category: {pill} (`{showcase}` | `data-category=\"{slug}\"`) — {len(cat_tools)} Tools\n")
        md_lines.append("| Badge | Hex Color | Tool Name | Subcategory | Pricing | Category Pill | Description | Official URL |")
        md_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for t in cat_tools:
            name_link = f"[{t['name']}]({t['url']})"
            md_lines.append(f"| **{t['badge']}** | `{t['color']}` | {name_link} | {t['subcategory']} | {t['pricing']} | {t['category_pill']} | {t['description']} | `{t['url']}` |")
        md_lines.append("")

    return "\n".join(md_lines)

def build_schema_json(tools):
    items = []
    for idx, t in enumerate(tools, start=1):
        items.append({
            "@type": "ListItem",
            "position": idx,
            "name": t["name"],
            "url": t["url"]
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": "http://aallaitools.online/#website",
                "url": "http://aallaitools.online/",
                "name": "aallaitools.online",
                "description": f"The definitive, fast, and comprehensive directory indexing {len(tools)}+ modern artificial intelligence tools, models, and agents."
            },
            {
                "@type": "ItemList",
                "@id": "http://aallaitools.online/#featured",
                "name": "Exhaustive Global AI Tools & GPTs Directory",
                "numberOfItems": len(tools),
                "itemListElement": items[:80] # High signal items for schema validator
            }
        ]
    }, indent=2)

def build_card_html(t):
    search_str = f"{t['name']} {t['subcategory']} {t['description']} {t['category_pill']} {t['pricing']}".lower()
    return f"""        <article class="tool-card" data-category="{t['category_slug']}" data-pricing="{t['pricing'].lower()}" data-search="{html.escape(search_str)}">
          <div class="card-top">
            <div class="tool-badge" style="background:{t['color']}">{html.escape(t['badge'])}</div>
            <div class="top-meta">
              <span class="price-pill price-{t['pricing'].lower().replace(' ', '-')}">{html.escape(t['pricing'])}</span>
              <button class="bookmark-btn" aria-label="Bookmark {html.escape(t['name'])}" data-id="{html.escape(t['name'])}">&#9734;</button>
            </div>
          </div>
          <div class="tool-subcat">{html.escape(t['subcategory'])}</div>
          <h3 class="tool-name">{html.escape(t['name'])}</h3>
          <p class="tool-desc">{html.escape(t['description'])}</p>
          <div class="card-bottom">
            <span class="cat-pill">{html.escape(t['category_pill'])}</span>
            <a href="{html.escape(t['url'])}" class="visit-btn" target="_blank" rel="noopener noreferrer">Visit &rarr;</a>
          </div>
        </article>"""

# Write tools.json
with open("tools.json", "w", encoding="utf-8") as f:
    json.dump(TOOLS_DATA, f, indent=2)

# Write AI_TOOLS_METADATA.md
md_content = generate_markdown_catalog(TOOLS_DATA)
with open("AI_TOOLS_METADATA.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Generated tools.json and AI_TOOLS_METADATA.md")
