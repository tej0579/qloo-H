import time
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class SessionState(BaseModel):
    session_id: str
    selected_games: List[Dict[str, Any]] = Field(default_factory=list)
    location: Optional[str] = None
    aesthetic_focus: Optional[str] = None
    stage: str = Field(default="SEED_GAMES", description="SEED_GAMES, AWAITING_CLARIFICATION, EXECUTED")
    history: List[Dict[str, Any]] = Field(default_factory=list)
    lootdrop_payload: Optional[Dict[str, Any]] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

class SessionStore:
    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}

    def get_or_create(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id=session_id)
        return self._sessions[session_id]

    def get(self, session_id: str) -> Optional[SessionState]:
        return self._sessions.get(session_id)

    def save(self, session: SessionState) -> None:
        session.updated_at = time.time()
        self._sessions[session.session_id] = session

    def update_games(self, session_id: str, games: List[Dict[str, Any]]) -> SessionState:
        session = self.get_or_create(session_id)
        session.selected_games = games
        session.stage = "AWAITING_CLARIFICATION"
        self.save(session)
        return session

    def update_answers(self, session_id: str, location: str, aesthetic_focus: str) -> SessionState:
        session = self.get_or_create(session_id)
        session.location = location
        session.aesthetic_focus = aesthetic_focus
        session.stage = "READY_FOR_EXECUTE"
        self.save(session)
        return session

    def store_payload(self, session_id: str, payload: Dict[str, Any]) -> SessionState:
        session = self.get_or_create(session_id)
        session.lootdrop_payload = payload
        session.stage = "EXECUTED"
        self.save(session)
        return session

    def clear(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]

# Global singleton store
session_store = SessionStore()
