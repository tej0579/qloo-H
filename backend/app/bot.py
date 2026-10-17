from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.guardrail import check_guardrail, extract_game_title
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

class VideogameBot:
    async def process_turn(self, session_id: str, message: str) -> BotResponse:
        session: SessionState = memory_store.get_or_create(session_id)
        user_msg = message.strip()

        # Step 0: Domain Guardrail (Rollback on off-topic)
        is_valid, rollback_msg = check_guardrail(user_msg)
        if not is_valid:
            return BotResponse(
                session_id=session_id,
                turn=session.turn,
                status="ROLLBACK",
                is_rollback=True,
                message=rollback_msg or "Off-topic query intercepted.",
                qloo_data=session.anchor_game
            )

        # ================= Turn 0 -> 1: Anchor Seed Ingestion =================
        if session.turn == 0:
            extracted = extract_game_title(user_msg)
            anchor = await search_videogame(extracted)

            if not anchor:
                return BotResponse(
                    session_id=session_id,
                    turn=0,
                    status="NOT_FOUND",
                    is_rollback=False,
                    message=(
                        f"Could not find a video game matching **'{extracted}'** in Qloo's taste graph. "
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

            tags_str = ", ".join(anchor.get("tags", ["Videogame", "Action"]))
            cp1_question = (
                f"Identified **{anchor['name']}** in Qloo's taste graph (UUID: `{str(anchor.get('id', 'N/A'))[:12]}...`).\n"
                f"Tags: *{tags_str}*.\n\n"
                f"When you play **{anchor['name']}**, are you drawn primarily to the **tight, punishing combat mechanics & reflex mastery**, "
                f"or more to the **cryptic environmental lore & atmospheric exploration**?"
            )
            cp1_options = [
                "Tight combat mechanics & reflex mastery",
                "Cryptic environmental lore & atmospheric world",
                "Deep build variety, theorycrafting & RPG progression"
            ]

            return BotResponse(
                session_id=session_id,
                turn=1,
                status="SUCCESS",
                message=cp1_question,
                counter_prompt=CounterPrompt(question=cp1_question, options=cp1_options),
                qloo_data={"anchor": anchor}
            )

        # ================= Turn 1 -> 2: Mechanics Answer -> Qloo Insights =================
        elif session.turn == 1:
            session.answer_1 = user_msg

            # Query Qloo Insights API
            anchor_id = session.anchor_game.get("id", "") if session.anchor_game else ""
            anchor_name = session.anchor_game.get("name", "") if session.anchor_game else ""
            candidates = await get_insights(anchor_id, anchor_name=anchor_name, take=5)
            session.correlated_candidates = candidates
            session.turn = 2
            memory_store.save(session)

            cand_names = [c["name"] for c in candidates[:3]]
            cp2_question = (
                f"Calibrated gameplay preference: *{user_msg}*.\n"
                f"Correlated candidate pool from Qloo API: **{', '.join(cand_names)}**.\n\n"
                f"When it comes to art direction and world aesthetic, do you prefer **gritty, decaying Gothic realism (3D)**, "
                f"or are you open to **stylized, vibrant or minimalist indie worlds**?"
            )
            cp2_options = [
                "Gritty, dark Gothic realism (3D immersive)",
                "Stylized, atmospheric indie world (2D / Isometric)",
                "Sci-fi / futuristic dystopian aesthetic"
            ]

            return BotResponse(
                session_id=session_id,
                turn=2,
                status="SUCCESS",
                message=cp2_question,
                counter_prompt=CounterPrompt(question=cp2_question, options=cp2_options),
                qloo_data={"candidates": candidates}
            )

        # ================= Turn 2 -> 3: Aesthetic Answer -> Platform / Length =================
        elif session.turn == 2:
            session.answer_2 = user_msg
            session.turn = 3
            memory_store.save(session)

            cp3_question = (
                f"Locked in aesthetic preference: *{user_msg}*.\n\n"
                f"Last calibration: What is your target **platform** (PC, PS5, Xbox, Switch), and are you looking for a "
                f"**tight 15–25 hour focused campaign** or an **80+ hour massive open-world epic**?"
            )
            cp3_options = [
                "PC, tight 15 to 25 hours",
                "PS5, tight 15 to 25 hours",
                "PC / Console, massive 60-100+ hour epic",
                "Nintendo Switch / Steam Deck portable"
            ]

            return BotResponse(
                session_id=session_id,
                turn=3,
                status="SUCCESS",
                message=cp3_question,
                counter_prompt=CounterPrompt(question=cp3_question, options=cp3_options),
                qloo_data={"aesthetic": user_msg}
            )

        # ================= Turn 3 -> 4: Platform Answer -> Final LLM Synthesis =================
        elif session.turn >= 3:
            session.answer_3 = user_msg

            # Final Chat Model Call (LLM Synthesis)
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
