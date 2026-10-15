from fastapi import APIRouter, HTTPException
from app.models.schemas_api import ChatRequest, ChatResponse, UserGameSelection, ClarificationAnswer
from app.services.agent_orchestrator import agent_orchestrator
from app.database.session_store import session_store

router = APIRouter(tags=["Agent Orchestrator"])

@router.post("/chat", response_model=ChatResponse)
async def chat_interaction(request: ChatRequest):
    """
    Multi-turn agent endpoint handling:
    1. action='SEED_GAMES': Verifies game IDs & returns 2 clarifying questions
    2. action='EXECUTE': Executes Qloo pipeline + unassisted LLM comparison
    """
    try:
        response = await agent_orchestrator.handle_request(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent orchestration failed: {str(e)}")

@router.post("/lootdrop/direct", response_model=ChatResponse)
async def direct_lootdrop(
    game_names: list[str],
    location: str = "Austin, TX",
    aesthetic: str = "streetwear_audio"
):
    """
    Convenience endpoint to execute a full Loot Drop in a single invocation.
    """
    req = ChatRequest(
        action="EXECUTE",
        games=[UserGameSelection(id="", name=name) for name in game_names],
        clarification=ClarificationAnswer(location=location, aesthetic_focus=aesthetic)
    )
    return await agent_orchestrator.handle_request(req)

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Retrieves stored state or cached loot drop for a session.
    """
    session = session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session
