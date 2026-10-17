# Qloo Videogame Cultural Intelligence Agent

A multi-turn conversational agent powered by **Qloo's Cultural Taste Graph (250M+ entities)** for `urn:entity:videogame`.

## Architecture Flow

```text
User Input -> Step 0: Guardrail (Rollback on off-topic)
           -> Turn 1: Anchor Game -> Qloo /search -> Counter-Prompt #1 (Gameplay/Mechanics)
           -> Turn 2: User Answer #1 -> Qloo /v2/insights -> Counter-Prompt #2 (World/Aesthetic)
           -> Turn 3: User Answer #2 -> Counter-Prompt #3 (Platform & Length)
           -> Turn 4: User Answer #3 -> Final Chat Model Synthesis (Qloo Grounded Report)
```

## Setup & Run

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser to access the built-in interactive chat UI.
