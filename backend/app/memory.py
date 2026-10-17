from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SessionState(BaseModel):
    session_id: str
    turn: int = 0
    anchor_game: Optional[Dict[str, Any]] = None
    answer_1: Optional[str] = None          # Mechanics priority
    correlated_candidates: List[Dict[str, Any]] = Field(default_factory=list)
    answer_2: Optional[str] = None          # World / Aesthetic priority
    answer_3: Optional[str] = None          # Platform & Length
    final_synthesis: Optional[Dict[str, Any]] = None

class MemoryStore:
    def __init__(self):
        self._store: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: str) -> SessionState:
        if session_id not in self._store:
            self._store[session_id] = SessionState(session_id=session_id)
        return self._store[session_id]

    def save(self, session: SessionState):
        self._store[session.session_id] = session

    def reset(self, session_id: str) -> SessionState:
        new_session = SessionState(session_id=session_id)
        self._store[session_id] = new_session
        return new_session

memory_store = MemoryStore()
