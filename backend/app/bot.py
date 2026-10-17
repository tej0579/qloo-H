from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.guardrail import classify_user_prompt
from app.qloo import search_videogame, get_insights
from app.memory import memory_store, SessionState
from app.llm import generate_final_synthesis

class CounterPrompt(BaseModel):
    question: str
    options: List[str]

class BotResponse(BaseModel):
    session_id: str
    turn: int
    status: str                         # "SUCCESS", "ROLLBACK", "NOT_FOUND", "COMPLETED"
    is_rollback: bool = False
    message: str
    counter_prompt: Optional[CounterPrompt] = None
    qloo_data: Optional[Dict[str, Any]] = None
    final_synthesis: Optional[Dict[str, Any]] = None

def get_turn_1_counter(anchor_name: str, anchor_id: str, tags: List[str]) -> CounterPrompt:
    tags_str = ", ".join(tags)
    q = (
        f"Identified **{anchor_name}** in Qloo's taste graph (UUID: `{str(anchor_id)[:12]}...`).\n"
        f"Tags: *{tags_str}*.\n\n"
        f"When you play **{anchor_name}**, are you drawn primarily to the **tight, punishing combat mechanics & reflex mastery**, "
        f"or more to the **cryptic environmental lore & atmospheric exploration**?"
    )
    return CounterPrompt(
        question=q,
        options=[
            "Tight combat mechanics & reflex mastery",
            "Cryptic environmental lore & atmospheric world",
            "Deep build variety, theorycrafting & RPG progression"
        ]
    )

def get_turn_2_counter(anchor_name: str, candidates: List[Dict[str, Any]], answer_1: str) -> CounterPrompt:
    cand_names = [c["name"] for c in candidates[:3]]
    q = (
        f"Calibrated gameplay preference: *{answer_1}*.\n"
        f"Correlated candidate pool from Qloo API: **{', '.join(cand_names)}**.\n\n"
        f"When it comes to art direction and world aesthetic, do you prefer **gritty, decaying Gothic realism (3D)**, "
        f"or are you open to **stylized, vibrant or minimalist indie worlds**?"
    )
    return CounterPrompt(
        question=q,
        options=[
            "Gritty, dark Gothic realism (3D immersive)",
            "Stylized, atmospheric indie world (2D / Isometric)",
            "Sci-fi / futuristic dystopian aesthetic"
        ]
    )

def get_turn_3_counter(answer_2: str) -> CounterPrompt:
    q = (
        f"Locked in aesthetic preference: *{answer_2}*.\n\n"
        f"Last calibration: What is your target **platform** (PC, PS5, Xbox, Switch), and are you looking for a "
        f"**tight 15–25 hour focused campaign** or an **80+ hour massive open-world epic**?"
    )
    return CounterPrompt(
        question=q,
        options=[
            "PC, tight 15 to 25 hours",
            "PS5, tight 15 to 25 hours",
            "PC / Console, massive 60-100+ hour epic",
            "Nintendo Switch / Steam Deck portable"
        ]
    )

class VideogameBot:
    async def process_turn(self, session_id: str, message: str) -> BotResponse:
        session: SessionState = memory_store.get_or_create(session_id)
        user_msg = message.strip()

        anchor_name = session.anchor_game.get("name") if session.anchor_game else None
        cls = classify_user_prompt(user_msg, current_turn=session.turn, anchor_name=anchor_name)
        p_type = cls["type"]

        # 1. Reset
        if p_type == "RESET":
            memory_store.reset(session_id)
            return BotResponse(
                session_id=session_id,
                turn=0,
                status="SUCCESS",
                message=cls["message"],
                counter_prompt=CounterPrompt(
                    question="Pick one of these popular anchor games to start:",
                    options=["Elden Ring", "Cyberpunk 2077", "Hades", "DOOM", "Persona 5"]
                )
            )

        # 2. Step 0 Guardrail Rollback (Off-topic)
        if p_type == "OFF_TOPIC":
            return BotResponse(
                session_id=session_id,
                turn=session.turn,
                status="ROLLBACK",
                is_rollback=True,
                message=cls["message"],
                qloo_data=session.anchor_game
            )

        # 3. Greetings or Meta Questions at Turn 0 (STAY AT TURN 0)
        if p_type in ("GREETING", "META"):
            return BotResponse(
                session_id=session_id,
                turn=0,
                status="SUCCESS",
                is_rollback=False,
                message=cls["message"],
                counter_prompt=CounterPrompt(
                    question="To begin, pick an anchor game or name any video game you love:",
                    options=["Elden Ring", "Cyberpunk 2077", "Hades", "DOOM", "Persona 5"]
                )
            )

        # 4. Greetings, Meta Questions, or Vague input during Calibration (STAY AT CURRENT TURN)
        if p_type in ("GREETING_IN_LOOP", "META_IN_LOOP", "VAGUE"):
            last_cp = None
            if session.turn == 1 and session.anchor_game:
                last_cp = get_turn_1_counter(
                    session.anchor_game["name"],
                    session.anchor_game["id"],
                    session.anchor_game.get("tags", [])
                )
            elif session.turn == 2 and session.anchor_game:
                last_cp = get_turn_2_counter(
                    session.anchor_game["name"],
                    session.correlated_candidates,
                    session.answer_1 or "Combat Mastery"
                )
            elif session.turn == 3:
                last_cp = get_turn_3_counter(session.answer_2 or "Atmospheric")

            return BotResponse(
                session_id=session_id,
                turn=session.turn,
                status="SUCCESS",
                is_rollback=False,
                message=f"{cls['message']}\n\nPlease select one of the options below to continue calibration:",
                counter_prompt=last_cp,
                qloo_data={"anchor": session.anchor_game} if session.anchor_game else None
            )

        # ================= Turn 0 -> 1: Anchor Seed Ingestion =================
        if session.turn == 0:
            title = cls.get("title", user_msg)
            anchor = await search_videogame(title)

            if not anchor:
                return BotResponse(
                    session_id=session_id,
                    turn=0,
                    status="NOT_FOUND",
                    is_rollback=False,
                    message=(
                        f"Could not find a video game matching **'{title}'** in Qloo's taste graph. "
                        "Please provide a known video game title (e.g. *Elden Ring*, *Cyberpunk 2077*, *Hades*, *DOOM*, *Bloodborne*) to begin."
                    ),
                    counter_prompt=CounterPrompt(
                        question="Pick one of these popular anchor games to start:",
                        options=["Elden Ring", "Cyberpunk 2077", "Hades", "Persona 5"]
                    )
                )

            session.anchor_game = anchor
            session.turn = 1
            memory_store.save(session)

            cp1 = get_turn_1_counter(anchor["name"], anchor["id"], anchor.get("tags", ["Videogame", "Action"]))
            return BotResponse(
                session_id=session_id,
                turn=1,
                status="SUCCESS",
                message=cp1.question,
                counter_prompt=cp1,
                qloo_data={"anchor": anchor}
            )

        # ================= Turn 1 -> 2: Mechanics Answer -> Qloo Insights =================
        elif session.turn == 1:
            session.answer_1 = user_msg

            anchor_id = session.anchor_game.get("id", "") if session.anchor_game else ""
            anchor_name = session.anchor_game.get("name", "") if session.anchor_game else ""
            candidates = await get_insights(anchor_id, anchor_name=anchor_name, take=5)
            session.correlated_candidates = candidates
            session.turn = 2
            memory_store.save(session)

            cp2 = get_turn_2_counter(anchor_name, candidates, user_msg)
            return BotResponse(
                session_id=session_id,
                turn=2,
                status="SUCCESS",
                message=cp2.question,
                counter_prompt=cp2,
                qloo_data={"candidates": candidates}
            )

        # ================= Turn 2 -> 3: Aesthetic Answer -> Platform / Length =================
        elif session.turn == 2:
            session.answer_2 = user_msg
            session.turn = 3
            memory_store.save(session)

            cp3 = get_turn_3_counter(user_msg)
            return BotResponse(
                session_id=session_id,
                turn=3,
                status="SUCCESS",
                message=cp3.question,
                counter_prompt=cp3,
                qloo_data={"aesthetic": user_msg}
            )

        # ================= Turn 3 -> 4: Platform Answer -> Final LLM Synthesis =================
        elif session.turn >= 3:
            session.answer_3 = user_msg

            synthesis = await generate_final_synthesis(
                anchor=session.anchor_game or {},
                answer_1=session.answer_1 or "",
                candidates=session.correlated_candidates,
                answer_2=session.answer_2 or "",
                answer_3=session.answer_3 or ""
            )

            session.final_synthesis = synthesis
            session.turn = 4
            memory_store.save(session)

            return BotResponse(
                session_id=session_id,
                turn=4,
                status="COMPLETED",
                message=synthesis.get("text", "Recommendation complete."),
                qloo_data={"candidates": session.correlated_candidates},
                final_synthesis=synthesis
            )

videogame_bot = VideogameBot()
