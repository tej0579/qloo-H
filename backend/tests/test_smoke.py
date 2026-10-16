import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database.session_store import SessionStore, session_store
from app.models.schemas_api import ChatRequest, UserGameSelection
from app.services.agent_orchestrator import AgentOrchestrator
from app.services.qloo_client import qloo_client
from app.services.loot_synthesizer import LootSynthesizer


class SessionStoreSmokeTests(unittest.TestCase):
    def test_create_update_and_retrieve_persisted_session(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "sessions.db"
            store = SessionStore(str(db_path))
            created = store.create_session("session-smoke")
            self.assertEqual(created.session_id, "session-smoke")

            store.update_session(
                "session-smoke",
                {
                    "selected_games": [{"id": "game-1", "name": "Cyberpunk 2077"}],
                    "location": "Tokyo, Japan",
                },
            )

            # Read through a fresh store instance to cover persistence across restarts.
            restarted_store = SessionStore(str(db_path))
            retrieved = restarted_store.get_session("session-smoke")
            self.assertIsNotNone(retrieved)
            self.assertEqual(retrieved.location, "Tokyo, Japan")
            self.assertEqual(retrieved.selected_games[0]["name"], "Cyberpunk 2077")


class EntityVerificationSmokeTests(unittest.IsolatedAsyncioTestCase):
    async def test_preset_slug_is_searched_instead_of_bypassing_resolution(self):
        game_slug = "preset:cyberpunk-2077"
        self.assertFalse(AgentOrchestrator._is_resolved_entity_id(game_slug))
        self.assertFalse(AgentOrchestrator._is_resolved_entity_id("not-a-valid-uuid"))
        self.assertTrue(AgentOrchestrator._is_resolved_entity_id("urn:entity:videogame:cyberpunk"))
        self.assertTrue(
            AgentOrchestrator._is_resolved_entity_id("a4b7d201-9988-4f11-ae77-0099118833aa")
        )

        search = AsyncMock(
            return_value=[
                {
                    "id": "a4b7d201-9988-4f11-ae77-0099118833aa",
                    "name": "Cyberpunk 2077",
                    "types": ["urn:entity:videogame"],
                }
            ]
        )
        request = ChatRequest(
            action="SEED_GAMES",
            games=[UserGameSelection(id=game_slug, name="Cyberpunk 2077")],
        )

        with patch.object(qloo_client, "search_entity", search), patch.object(session_store, "update_games"):
            response = await AgentOrchestrator()._handle_seed_games("smoke-session", request)

        search.assert_awaited_once()
        self.assertEqual(response.verified_games[0].name, "Cyberpunk 2077")


class LootSynthesizerSmokeTests(unittest.TestCase):
    def build_payload(self, data_source):
        return LootSynthesizer().synthesize(
            session_id="synth-smoke",
            seed_games=[UserGameSelection(id="game-uuid", name="Cyberpunk 2077")],
            location="Tokyo, Japan",
            aesthetic_focus="streetwear_audio",
            qloo_brands=[
                {"id": "b1", "name": "Brand One", "affinity": 90},
                {"id": "b2", "name": "Brand Two", "affinity": 70},
            ],
            qloo_artists=[{"id": "a1", "name": "Artist One", "affinity": 80}],
            qloo_places=[{"id": "p1", "name": "Place One", "affinity": 100}],
            qloo_movies=[{"id": "m1", "name": "Film One", "affinity": 60}],
            data_source=data_source,
            llm_cliche_data={"items": [], "comparisons": []},
        )

    def test_dynamic_radar_and_overall_average_and_live_source(self):
        payload = self.build_payload("qloo_live")
        radar = {metric.subject: metric.qloo_affinity for metric in payload.radar_metrics}

        self.assertEqual(payload.data_source, "qloo_live")
        self.assertEqual(radar, {"Fashion": 80.0, "Music": 80.0, "Places": 100.0, "Films": 60.0})
        self.assertEqual(payload.overall_match_score, 80.0)

    def test_demo_fallback_source_is_preserved(self):
        payload = self.build_payload("demo_fallback")
        self.assertEqual(payload.data_source, "demo_fallback")
        self.assertTrue(payload.comparator.summary_verdict.startswith("Offline"))


if __name__ == "__main__":
    unittest.main()
