import uuid
import asyncio
from uuid import UUID
from typing import List, Dict, Any, Optional
from app.core.logger import logger
from app.core.constants import (
    QlooEntityType,
    POPULAR_LOCATIONS,
    AESTHETIC_PRIORITIES,
    AESTHETIC_TAG_MAPPING,
)
from app.models.schemas_api import (
    ChatRequest,
    ChatResponse,
    UserGameSelection,
    ClarificationQuestion,
    ClarificationOption,
    ClarificationAnswer,
    LootDropPayload
)
from app.database.session_store import session_store
from app.services.qloo_client import qloo_client
from app.services.llm_comparator import llm_comparator
from app.services.loot_synthesizer import loot_synthesizer

class AgentOrchestrator:
    """
    Agent State Machine controlling the 2-step dialogue loop:
    Input Games -> Halt for 2 Clarifications -> Parallel Qloo / LLM Execution -> Final Drop
    """

    async def handle_request(self, request: ChatRequest) -> ChatResponse:
        session_id = request.session_id or f"sess_{uuid.uuid4().hex[:10]}"
        action = (request.action or "SEED_GAMES").upper()

        if action == "RESET":
            session_store.clear(session_id)
            return ChatResponse(
                session_id=session_id,
                status="RESET",
                action="RESET",
                message="Session reset. Ready for your favorite video games!"
            )

        if action == "SEED_GAMES":
            return await self._handle_seed_games(session_id, request)

        elif action in ["CLARIFY", "EXECUTE"]:
            return await self._handle_execute_drop(session_id, request)

        return ChatResponse(
            session_id=session_id,
            status="UNKNOWN_ACTION",
            action=action,
            message=f"Action '{action}' is not supported."
        )

    async def _handle_seed_games(self, session_id: str, request: ChatRequest) -> ChatResponse:
        input_games: List[UserGameSelection] = []

        if request.games:
            input_games = request.games
        elif request.query:
            # Parse query (e.g. "Elden Ring and Cyberpunk 2077")
            raw_titles = [t.strip() for t in request.query.replace(" and ", ",").replace("&", ",").split(",") if t.strip()]
            for title in raw_titles[:3]:
                input_games.append(UserGameSelection(id="", name=title))

        if not input_games:
            return ChatResponse(
                session_id=session_id,
                status="AWAITING_INPUT",
                action="SEED_GAMES",
                message="Please select or enter 1 to 3 video games (e.g. 'Elden Ring', 'Cyberpunk 2077', 'Persona 5')."
            )

        # Step 1: Verify & Resolve Qloo UUIDs for each game
        verified_games: List[UserGameSelection] = []
        for g in input_games:
            if self._is_resolved_entity_id(g.id):
                verified_games.append(g)
            else:
                search_results = await qloo_client.search_entity(
                    query=g.name,
                    limit=5,
                    entity_type=QlooEntityType.VIDEOGAME.value
                )
                videogame_results = [
                    result for result in search_results
                    if QlooEntityType.VIDEOGAME.value in result.get("types", [])
                ]
                if videogame_results:
                    top = videogame_results[0]
                    verified_games.append(UserGameSelection(
                        id=top["id"],
                        name=top["name"],
                        entity_id=top["id"],
                        types=top.get("types", [QlooEntityType.VIDEOGAME.value])
                    ))
                else:
                    verified_games.append(UserGameSelection(
                        id=f"fallback-{uuid.uuid4().hex[:6]}",
                        name=g.name,
                        types=[QlooEntityType.VIDEOGAME.value]
                    ))

        # Save verified games to session store
        session_store.update_games(session_id, [g.model_dump() for g in verified_games])

        # Step 2: Halt execution and formulate the 2 mandatory clarification questions
        q1_options = [
            ClarificationOption(id=loc["city"], label=loc["label"], description="Scout physical venues & hangouts")
            for loc in POPULAR_LOCATIONS
        ]
        q2_options = [
            ClarificationOption(id=aes["id"], label=aes["label"], description=aes["description"])
            for aes in AESTHETIC_PRIORITIES
        ]

        questions = [
            ClarificationQuestion(
                id="location",
                step=1,
                title="IRL Scouting Territory",
                prompt="What city or metro area should we scout for IRL hangouts, dining, and venues?",
                options=q1_options,
                default_value="Tokyo, Japan"
            ),
            ClarificationQuestion(
                id="aesthetic_focus",
                step=2,
                title="Aesthetic Upgrade Priority",
                prompt="What area are you looking to upgrade first: your everyday streetwear wardrobe, your room decor, or your session audio?",
                options=q2_options,
                default_value="streetwear_audio"
            )
        ]

        game_titles = ", ".join([g.name for g in verified_games])
        message = (
            f"Locked in seed games: {game_titles}. "
            "To personalize your IRL Loot Drop with spatial and aesthetic precision, "
            "please answer these 2 quick questions:"
        )

        return ChatResponse(
            session_id=session_id,
            status="AWAITING_CLARIFICATION",
            action="CLARIFY",
            message=message,
            verified_games=verified_games,
            clarification_questions=questions
        )

    @staticmethod
    def _is_resolved_entity_id(entity_id: str) -> bool:
        if entity_id.startswith("urn:entity:"):
            return True
        if len(entity_id) != 36:
            return False
        try:
            return str(UUID(entity_id)) == entity_id.lower()
        except ValueError:
            return False

    async def _handle_execute_drop(self, session_id: str, request: ChatRequest) -> ChatResponse:
        session = session_store.get(session_id)
        games_data = session.selected_games if session and session.selected_games else []

        if not games_data and request.games:
            games_data = [g.model_dump() for g in request.games]

        if not games_data:
            # Fallback default seed
            games_data = [{"id": "BAF6317A-DF94-4C90-92AE-63F86560C21B", "name": "Elden Ring", "types": ["urn:entity:videogame"]}]

        verified_games = [UserGameSelection(**g) for g in games_data]
        game_ids = [g.id for g in verified_games]
        game_names = [g.name for g in verified_games]

        # Extract clarification answers
        location = "Austin, TX"
        aesthetic = "streetwear_audio"

        if request.clarification:
            location = request.clarification.location or location
            aesthetic = request.clarification.aesthetic_focus or aesthetic
        elif session:
            location = session.location or location
            aesthetic = session.aesthetic_focus or aesthetic

        session_store.update_answers(session_id, location, aesthetic)
        aesthetic_tag_urns = AESTHETIC_TAG_MAPPING.get(aesthetic, [])

        logger.info(f"Executing LootDrop for session {session_id} - Games: {game_names}, Location: {location}, Focus: {aesthetic}")

        # Step 3 & 4: Concurrent Qloo Graph Query + Naked LLM Baseline
        brand_task = qloo_client.get_insights(
            game_ids,
            filter_type=QlooEntityType.BRAND.value,
            take=4,
            tag_urns=aesthetic_tag_urns,
        )
        artist_task = qloo_client.get_insights(
            game_ids,
            filter_type=QlooEntityType.ARTIST.value,
            take=4,
            tag_urns=aesthetic_tag_urns,
        )
        place_task = qloo_client.get_insights(game_ids, filter_type=QlooEntityType.PLACE.value, location_query=location, take=4)
        movie_task = qloo_client.get_insights(game_ids, filter_type=QlooEntityType.MOVIE.value, take=4)
        cliche_task = llm_comparator.generate_cliches(game_names, location)

        brand_result, artist_result, place_result, movie_result, cliches = await asyncio.gather(
            brand_task,
            artist_task,
            place_task,
            movie_task,
            cliche_task
        )

        insight_results = [brand_result, artist_result, place_result, movie_result]
        data_source = (
            "qloo_live"
            if all(result["data_source"] == "qloo_live" for result in insight_results)
            else "demo_fallback"
        )

        # Step 5: Merge and synthesize the finalized Loot Drop Payload
        payload: LootDropPayload = loot_synthesizer.synthesize(
            session_id=session_id,
            seed_games=verified_games,
            location=location,
            aesthetic_focus=aesthetic,
            qloo_brands=brand_result["entities"],
            qloo_artists=artist_result["entities"],
            qloo_places=place_result["entities"],
            qloo_movies=movie_result["entities"],
            data_source=data_source,
            llm_cliche_data=cliches
        )

        session_store.store_payload(session_id, payload.model_dump())

        return ChatResponse(
            session_id=session_id,
            status="COMPLETED",
            action="EXECUTE",
            message=f"IRL Loot Drop synthesized for {', '.join(game_names)} in {location}!",
            verified_games=verified_games,
            lootdrop=payload
        )

agent_orchestrator = AgentOrchestrator()
