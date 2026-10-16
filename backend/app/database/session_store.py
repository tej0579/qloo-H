import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

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
    def __init__(self, db_path: Optional[str] = None):
        # session_store.py -> database -> app -> backend
        self.db_path = Path(db_path) if db_path else Path(__file__).resolve().parents[2] / "sessions.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, timeout=10.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    state_json TEXT NOT NULL
                )
                """
            )

    def create_session(self, session_id: str) -> SessionState:
        """Create an empty session, or return the existing session unchanged."""
        session = SessionState(session_id=session_id)
        with self._connection() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO sessions (session_id, state_json) VALUES (?, ?)",
                (session_id, session.model_dump_json()),
            )
        return self.get_session(session_id) or session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT state_json FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        if row is None:
            return None
        return SessionState.model_validate_json(row["state_json"])

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> SessionState:
        """Apply field updates to a session and persist the resulting state."""
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT state_json FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            session = (
                SessionState.model_validate_json(row["state_json"])
                if row is not None
                else SessionState(session_id=session_id)
            )
            state = session.model_dump()
            state.update(updates)
            state["updated_at"] = time.time()
            updated = SessionState.model_validate(state)
            connection.execute(
                """
                INSERT INTO sessions (session_id, state_json) VALUES (?, ?)
                ON CONFLICT(session_id) DO UPDATE SET state_json = excluded.state_json
                """,
                (session_id, updated.model_dump_json()),
            )
        return updated

    # Existing application interface. These methods retain their signatures so
    # the routes and orchestrator continue to work without changes.
    def get_or_create(self, session_id: str) -> SessionState:
        return self.create_session(session_id)

    def get(self, session_id: str) -> Optional[SessionState]:
        return self.get_session(session_id)

    def save(self, session: SessionState) -> None:
        session.updated_at = time.time()
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO sessions (session_id, state_json) VALUES (?, ?)
                ON CONFLICT(session_id) DO UPDATE SET state_json = excluded.state_json
                """,
                (session.session_id, session.model_dump_json()),
            )

    def update_games(self, session_id: str, games: List[Dict[str, Any]]) -> SessionState:
        return self.update_session(
            session_id,
            {"selected_games": games, "stage": "AWAITING_CLARIFICATION"},
        )

    def update_answers(self, session_id: str, location: str, aesthetic_focus: str) -> SessionState:
        return self.update_session(
            session_id,
            {
                "location": location,
                "aesthetic_focus": aesthetic_focus,
                "stage": "READY_FOR_EXECUTE",
            },
        )

    def store_payload(self, session_id: str, payload: Dict[str, Any]) -> SessionState:
        return self.update_session(
            session_id,
            {"lootdrop_payload": payload, "stage": "EXECUTED"},
        )

    def clear(self, session_id: str) -> None:
        with self._connection() as connection:
            connection.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))


# Global singleton store
session_store = SessionStore()
