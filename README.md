# IRL LootDrop: Gaming Taste to Real-World Lifestyle via Qloo Cultural Intelligence

> **Transforming video game obsession into authentic real-world lifestyle drops.**  
> Built for the **Qloo Taste AI Hackathon 2026** • Grounded in the Qloo Cultural Intelligence Graph.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](backend/)
[![Next.js 14](https://img.shields.io/badge/Frontend-Next.js%2014-black.svg?logo=next.js&logoColor=white)](web/)
[![Qloo API](https://img.shields.io/badge/Qloo_API-Hackathon_Connected-00f0ff.svg)](https://hackathon.api.qloo.com)

---

## Project Overview

IRL LootDrop turns favorite video games into a real-world lifestyle profile. It combines Qloo cultural insights with a no-tools LLM baseline to recommend fashion, music, city places, and films, then presents the difference in a split-screen dashboard. Aesthetic choices such as streetwear, techwear, minimalism, audiophile culture, vintage, cyberpunk, and dark academia can shape the fashion and music insight requests.

## Architecture at a Glance

- **Next.js 14 frontend:** game search, city and aesthetic selection, and recommendation dashboard.
- **FastAPI orchestrator:** resolves game entities, gathers the user's clarifications, and coordinates recommendation requests.
- **Qloo API:** `/search` resolves game entities; `/v2/insights` recommends brands, artists, places, and films from game and aesthetic signals.
- **Split-screen LLM comparator:** compares the Qloo recommendations with a live Gemini/OpenAI baseline or a deterministic offline baseline.
- **SQLite session store:** persists selected games, answers, and generated drops in `backend/sessions.db`.

The recommendation source is included in the result payload. Tagged brand and artist queries retry without aesthetic tags when no matches are returned, then use the offline demo catalog if Qloo still has no results.

## Current Branch Build Summary (`vamshi`)

This branch contains an end-to-end demo flow plus backend persistence and source transparency. The main additions are:

- **Game verification:** The backend resolves game names through Qloo `/search`. It only accepts a game ID as pre-resolved when it is a Qloo entity URN or a valid UUID; preset slugs are searched. Search tags are retained for the generated character class.
- **Personalized Qloo insights:** The city and selected aesthetic feed the recommendation flow. Aesthetic tag URNs are sent with brand and artist insight requests, with an unfiltered retry and offline demo fallback when needed.
- **Honest recommendations and scores:** Every synthesized drop includes `data_source` (`qloo_live` or `demo_fallback`), category affinity averages for the radar, and an overall affinity score. The dashboard labels live and fallback results distinctly.
- **IRL Character Class:** The synthesizer combines aesthetic choice and game signals into an `archetype_title`, shown at the top of the Qloo Grounded comparator panel.
- **IRL Saturday Quest Log:** Each new drop includes four timed steps built from the first returned brand, artist, local place, and film. The dashboard presents these in an expandable timeline.
- **Split-screen comparison:** Qloo recommendations appear alongside an unassisted LLM baseline. Gemini or OpenAI can provide the baseline when configured; deterministic benchmark examples are available offline.
- **Persistent sessions:** Conversation state and generated drops are stored in SQLite at `backend/sessions.db` and survive backend restarts.
- **Frontend helpers:** `web/src/lib/api.ts` centralizes backend calls and `web/src/lib/utils.ts` provides shared formatting and class-name helpers. The root `.gitignore` keeps these source files trackable.

### Main request flow

1. The user submits one or more favorite games.
2. FastAPI resolves the games and asks for a city and aesthetic preference.
3. The user submits the clarifications; the orchestrator requests Qloo insights across brands, artists, places, and films while generating the comparison baseline.
4. The synthesizer returns the recommendations, source label, affinity metrics, character class, and four-step quest log.
5. The Next.js dashboard renders the split-screen comparison, radar, recommendation categories, and expandable quest.

### Verification performed for this branch

```bash
python3 -m unittest discover -s backend/tests -v
cd web && npm run build
```

The backend smoke suite covers SQLite persistence, strict game ID handling, score and source synthesis, character class generation, and quest recommendations. The frontend production build completes successfully.

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
│   │   │   └── session_store.py            # SQLite store tracking conversation state (game seeds, answers)
│   │   └── services/
│   │       ├── qloo_client.py              # Async HTTPX client for Qloo (/search, /v2/insights, /v2/tags)
│   │       ├── agent_orchestrator.py       # Seed -> Clarify -> Fetch -> Synthesize request flow
│   │       ├── llm_comparator.py           # Parallel "Naked LLM" runner that generates generic clichés for contrast
│   │       └── loot_synthesizer.py         # Merges raw Qloo tags & affinity scores into the structured "Loot Drop"
│   ├── requirements.txt                    # Backend dependencies (fastapi, uvicorn, httpx, pydantic)
│   ├── Dockerfile                          # Container spec for Railway / Fly.io / Render deployment
│   └── .env.example                        # QLOO_API_KEY, GEMINI_API_KEY, optional OPENAI_API_KEY
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

## Local Setup

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer and npm

### Configure the backend

Create `backend/.env` with the following values. Keep API keys private and do not commit this file.

```dotenv
QLOO_API_KEY=your_qloo_api_key
GEMINI_API_KEY=your_gemini_api_key
QLOO_BASE_URL=https://hackathon.api.qloo.com
ENVIRONMENT=development
PORT=8000
HOST=0.0.0.0
```

`GEMINI_API_KEY` enables the live unassisted LLM comparison. `OPENAI_API_KEY` can also be set as an alternate live provider. Without either LLM key, the app uses its deterministic comparator baseline.

### Install dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../web
npm ci
cd ..
```

### Run both development servers

From the repository root, run the startup script:

```bash
./scripts/start-local.sh
```

Or start them in separate terminals:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

```bash
cd web
npm run dev
```

The frontend is at `http://localhost:3000`; the FastAPI docs are at `http://localhost:8000/docs`. SQLite creates `backend/sessions.db` automatically on first backend start.

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

1. **Split-screen comparator:** Contrasts the unassisted LLM baseline with Qloo-backed or clearly labeled offline demo recommendations.
2. **Multi-turn dialogue:** Collects favorite games, a scouting city, and an aesthetic preference before generating a drop.
3. **Resilient Qloo requests:** Normalizes insight results, retries brand and artist queries without aesthetic tags when needed, and falls back to the offline demo catalog.
4. **Affinity radar and overall score:** Calculates category metrics from returned recommendation scores.
5. **Actionable demo output:** Adds a generated IRL Character Class and a four-step Saturday quest connecting fashion, music, a local venue, and film.
6. **Persistent sessions:** Stores conversation and drop data in SQLite across server restarts.
