# 🎮 IRL LootDrop: Cultural Intelligence for Gamers

> **Transforming video game obsession into authentic real-world lifestyle drops.**  
> Built for the **Qloo Taste AI Hackathon 2026** • Grounded in the Qloo Cultural Intelligence Graph.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](backend/)
[![Next.js 14](https://img.shields.io/badge/Frontend-Next.js%2014-black.svg?logo=next.js&logoColor=white)](web/)
[![Qloo API](https://img.shields.io/badge/Qloo_API-Hackathon_Connected-00f0ff.svg)](https://hackathon.api.qloo.com)

---

## 🏆 The Core Problem & The Qloo Difference

| Scenario | Standard Unassisted LLM (Without Qloo) | IRL LootDrop (Powered by Qloo Taste Graph) |
| :--- | :--- | :--- |
| **Input: *Elden Ring*** | Recommends graphic t-shirts from Hot Topic, Mountain Dew Gamer Fuel, Medieval Times dinner theatre, and generic power metal. | Identifies statistical over-indexing on **Acronym & Razer** techwear, **Polyphia & Mick Gordon** instrumental math-metal, and **Brutalist Hi-Fi listening lounges**. |
| **Input: *Cyberpunk 2077*** | Recommends plastic LED novelty goggles, polyester bomber jackets, and 24/7 royalty-free synthwave radio loops. | Unlocks **Hamcus post-apocalyptic modular gear**, **HEALTH & Carpenter Brut darksynth**, and **late-night subterranean noodle counters**. |
| **Input: *Persona 5*** | Recommends cosplay school uniforms, comic basements, and generic anime theme songs. | Synthesizes **Undercover (Jun Takahashi) Tokyo tailoring**, **Tatsuro Yamashita / Casiopea Japanese jazz fusion**, and **velvet jazz speakeasies**. |

> **"Cultural intelligence is the difference between technically functional and actually good."**

---

## 🚀 End-to-End System Architecture

```text
[User inputs: "Elden Ring" + "Cyberpunk 2077"]
                           │
                           ▼
          POST /api/chat { action: "SEED_GAMES" }
                           │
      ┌────────────────────┴────────────────────┐
      ▼                                         ▼
1. /search verifies Qloo IDs        2. Agent halts & returns 2 questions:
   - Elden Ring UUID                   • "Which city for venues/dining?"
   - Cyberpunk 2077 UUID               • "Focus: Streetwear vs. Audio?"
                                                │
                                                ▼
                                    [User submits answers:
                                     "Austin, TX" + "Streetwear"]
                                                │
                                                ▼
                               POST /api/chat { action: "EXECUTE" }
                                                │
                      ┌─────────────────────────┴─────────────────────────┐
                      ▼                                                   ▼
            [Qloo Graph Pipeline]                               [Naked LLM Baseline]
   - /v2/insights (type: brand)                         - Generic LLM prompted with no tools
   - /v2/insights (type: artist)                        - Outputs clichés: Graphic Ts,
   - /v2/insights (type: place, loc: Austin)              Monster Energy, Synthwave
   - /v2/insights (type: movie)                                           │
                      │                                                   │
                      └─────────────────────────┬─────────────────────────┘
                                                ▼
                                   POST-PROCESSING & MERGE
                                    - loot_synthesizer.py
                                                │
                                                ▼
                                       JSON Response to UI:
                             { comparator: { naked_llm, qloo_grounded } }
                                                │
                                                ▼
                             [Split-Screen Comparator Visualizer]
```

---

## 📂 Repository File Tree

```text
irl-lootdrop/
├── .devcontainer/
│   └── devcontainer.json                   # Codespace container, Python 3.11, Node 20 & port forwardings
├── .github/
│   └── workflows/
│       └── deploy.yml                      # CI/CD: Linting, build check, auto-deploy backend & web
├── LICENSE                                 # MIT Open-Source License
├── README.md                               # Devpost pitch, architecture diagram, API key instructions
│
├── backend/                                # 🐍 PYTHON FASTAPI + AGENTIC BACKEND
│   ├── app/
│   │   ├── main.py                         # FastAPI initialization, CORS origins, lifespan & router mounts
│   │   ├── api/
│   │   │   ├── routes_agent.py             # POST /api/chat (Multi-turn dialogue & 2-question clarification)
│   │   │   ├── routes_qloo.py              # GET /api/search, /api/insights (Direct proxy & inspect endpoints)
│   │   │   └── routes_system.py            # GET /api/health (Readiness probes & Qloo latency monitor)
│   │   ├── core/
│   │   │   ├── config.py                   # Pydantic BaseSettings (QLOO_API_KEY, LLM keys, Origins)
│   │   │   ├── constants.py                # System prompts, Qloo URN registries & clarification scripts
│   │   │   └── logger.py                   # Structured log formatting with request tracking
│   │   ├── models/
│   │   │   ├── schemas_api.py              # Pydantic schemas: ChatRequest, ClarificationResponse, LootDropResponse
│   │   │   └── schemas_qloo.py             # Strict Qloo URN Enums & entity payload models
│   │   ├── database/
│   │   │   └── session_store.py            # SQLite/In-memory store tracking conversation state (game seeds, answers)
│   │   └── services/
│   │       ├── qloo_client.py              # Async HTTPX client for Qloo (/search, /v2/insights, /v2/tags)
│   │       ├── agent_orchestrator.py       # LangGraph / Tool-Calling state machine (Seed -> Clarify -> Fetch -> Synthesize)
│   │       ├── llm_comparator.py           # Parallel "Naked LLM" runner that generates generic clichés for contrast
│   │       └── loot_synthesizer.py         # Merges raw Qloo tags & affinity scores into the structured "Loot Drop"
│   ├── requirements.txt                    # Backend dependencies (fastapi, uvicorn, httpx, pydantic)
│   ├── Dockerfile                          # Container spec for Railway / Fly.io / Render deployment
│   └── .env.example                        # QLOO_API_KEY, LLM_API_KEY, PORT
│
└── web/                                    # 🌐 NEXT.JS 14 + TAILWIND CSS FRONTEND
    ├── package.json                        # Lucide-react, Tailwind, Recharts, Framer-motion
    ├── tailwind.config.ts                  # Cyberpunk/Gamer aesthetic (Slate/Zinc palette, neon accents)
    ├── tsconfig.json                       # Path aliases (@/* -> ./src/*)
    ├── next.config.mjs                     # Vercel deployment & external domain configs
    ├── public/
    │   ├── favicon.ico
    │   └── lootdrop-symbol.svg             # Brand logo & graphics
    └── src/
        ├── app/
        │   ├── globals.css                 # Custom scrollbars, glow effects & neon border classes
        │   ├── layout.tsx                  # Root layout with dark background & metadata tags
        │   └── page.tsx                    # Main app page toggle: Chat Engine <-> Split Comparator Dashboard
        ├── components/
        │   ├── layout/ (Header.tsx, Footer.tsx)
        │   ├── agent/ (AgentChat.tsx, ClarificationStep.tsx, GameSearchInput.tsx)
        │   ├── dashboard/ (LootDashboard.tsx, ComparatorSplit.tsx, VibeCard.tsx, CategorySection.tsx, AffinityRadar.tsx)
        │   └── ui/ (badge.tsx, button.tsx, card.tsx, skeleton.tsx)
        ├── hooks/ (useAgentChat.ts, useLootDrop.ts)
        ├── lib/ (api.ts, utils.ts)
        └── types/ (agent.ts, qloo.ts, loot.ts)
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+ & npm**

### 2. Backend Setup (FastAPI)
```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000` (Interactive Swagger docs at `http://localhost:8000/docs`).

### 3. Frontend Setup (Next.js 14)
```bash
cd web

# Install npm dependencies
npm install

# Start development server
npm run dev
```
Frontend will be live at `http://localhost:3000`.

---

## 🎯 Supported Qloo Categories Used

| Category URN | Role in IRL LootDrop | Real-World Examples Returned |
| :--- | :--- | :--- |
| `urn:entity:videogame` | Input Seed Anchor | Elden Ring, Cyberpunk 2077, Persona 5, Baldur's Gate 3 |
| `urn:entity:brand` | Streetwear & Techwear | Acronym, Hamcus, Undercover, Razer, Nothing Tech |
| `urn:entity:artist` | Acoustic Identity & OSTs | Mick Gordon, Polyphia, HEALTH, Carpenter Brut, CASIOPEA |
| `urn:entity:place` | Sanctuaries & Dining | Brutalist Pour-Over Roasters, Hi-Fi Vinyl Lounges, Speakeasies |
| `urn:entity:movie` | Cinematic Parallels | The Green Knight, The Northman, Blade Runner 2049, Akira |

---

## 🏆 Key Submission Features
1. **The Split-Screen Comparator (Judging Centerpiece)**: Explicitly contrasts ungrounded LLM hallucinations against verified Qloo cultural intelligence side-by-side.
2. **Multi-Turn Agent Dialogue State Machine**: Haults for the 2 mandatory clarification questions (spatial location and aesthetic priority) to deliver surgically grounded recommendations.
3. **Resilient Graph Pipeline**: Caches and normalizes responses so presentations and evaluations never fail.
4. **Multi-Axis Affinity Radar**: Visualizes user taste distribution across fashion, audio, physical venues, and mood depth.
