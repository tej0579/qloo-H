import time
import httpx
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logger import logger
from app.core.constants import QlooEntityType

# Curated Fallback Intelligence for reliable offline/rate-limit demonstration
DEMO_GAME_DATABASE: Dict[str, Dict[str, Any]] = {
    "elden ring": {
        "id": "BAF6317A-DF94-4C90-92AE-63F86560C21B",
        "name": "Elden Ring",
        "brands": [
            {"id": "b-1", "name": "Razer", "tags": ["Gaming Hardware", "Chroma RGB", "Precision"], "score": 94.2},
            {"id": "b-2", "name": "Acronym", "tags": ["Techwear", "Avant-Garde", "Brutalist"], "score": 91.8},
            {"id": "b-3", "name": "Square Enix", "tags": ["Dark Fantasy", "Soundtracks", "Merchandise"], "score": 88.5},
            {"id": "b-4", "name": "Twitch", "tags": ["Speedrunning", "Community", "Live"], "score": 85.0}
        ],
        "artists": [
            {"id": "a-1", "name": "Mick Gordon", "tags": ["Industrial Metal", "OST", "Aggressive Synth"], "score": 96.1},
            {"id": "a-2", "name": "Polyphia", "tags": ["Math Rock", "Instrumental", "Virtuoso"], "score": 93.4},
            {"id": "a-3", "name": "Clown Core", "tags": ["Grindcore Jazz", "Chaos", "Experimental"], "score": 89.2},
            {"id": "a-4", "name": "Chelsea Wolfe", "tags": ["Gothic Rock", "Doom Folk", "Atmospheric"], "score": 87.0}
        ],
        "movies": [
            {"id": "m-1", "name": "The Northman", "tags": ["Dark Folklore", "Visceral", "Mythology"], "score": 92.0},
            {"id": "m-2", "name": "The Green Knight", "tags": ["A24", "Arthurian", "Surrealist"], "score": 90.5},
            {"id": "m-3", "name": "Berserk: The Golden Age", "tags": ["Dark Fantasy", "Eclipse", "Anime"], "score": 95.8}
        ],
        "places": [
            {"id": "p-1", "name": "The Foundry Speakeasy", "tags": ["Dimly Lit", "Craft Cocktails", "Stone Interior"], "score": 92.4, "address": "Downtown Arts District", "price": "$$$"},
            {"id": "p-2", "name": "Obsidian Coffee Roasters", "tags": ["Brutalist Concrete", "Pour-over", "Quiet"], "score": 89.7, "address": "East Warehouse Corridor", "price": "$$"},
            {"id": "p-3", "name": "Catacomb Listening Lounge", "tags": ["Vinyl Hi-Fi", "Dark Ambient", "Natural Wine"], "score": 93.1, "address": "Historic Sub-Level", "price": "$$$"}
        ]
    },
    "cyberpunk 2077": {
        "id": "A4B7D201-9988-4F11-AE77-0099118833AA",
        "name": "Cyberpunk 2077",
        "brands": [
            {"id": "b-21", "name": "Hamcus", "tags": ["Post-Apocalyptic", "Dystopian", "Technical Wear"], "score": 95.4},
            {"id": "b-22", "name": "Razer", "tags": ["High Performance", "Cyber-Aesthetic", "Keyboards"], "score": 92.1},
            {"id": "b-23", "name": "Nothing Tech", "tags": ["Transparent Design", "Glyph Interface", "Minimal Neon"], "score": 89.7},
            {"id": "b-24", "name": "Aimé Leon Dore", "tags": ["Elevated Streetwear", "Subculture", "Urban"], "score": 84.3}
        ],
        "artists": [
            {"id": "a-21", "name": "HEALTH", "tags": ["Cyber Industrial", "Noise Rock", "EBM"], "score": 97.2},
            {"id": "a-22", "name": "Carpenter Brut", "tags": ["Darksynth", "French Electro", "Heavy Bass"], "score": 94.6},
            {"id": "a-23", "name": "Perturbator", "tags": ["Retrowave", "Cyberpunk", "Dark Electronic"], "score": 93.0},
            {"id": "a-24", "name": "Grimes", "tags": ["Art Pop", "Transhumanist", "Experimental"], "score": 88.5}
        ],
        "movies": [
            {"id": "m-21", "name": "Blade Runner 2049", "tags": ["Neo-Noir", "Denis Villeneuve", "Atmospheric"], "score": 98.4},
            {"id": "m-22", "name": "Akira", "tags": ["Anime Classic", "Cyberpunk", "Megacity"], "score": 96.1},
            {"id": "m-23", "name": "Ghost in the Shell", "tags": ["Philosophical", "Cyborg", "Cybernetic"], "score": 95.0}
        ],
        "places": [
            {"id": "p-21", "name": "Neo-Tokyo Noodle Lab", "tags": ["Neon Lighting", "Cyber Counter", "Ramen & Cocktails"], "score": 94.8, "address": "Subway Arcade Level 1", "price": "$$"},
            {"id": "p-22", "name": "Glitch Basement Bar", "tags": ["Synthwave Audio", "Industrial Decor", "Craft Spirits"], "score": 91.5, "address": "District 4 Warehouse", "price": "$$$"},
            {"id": "p-23", "name": "Kuro Modern Tea Room", "tags": ["Minimalist Steel", "Matcha Hi-Fi", "Late Night"], "score": 88.9, "address": "Tech Plaza", "price": "$$"}
        ]
    },
    "persona 5": {
        "id": "C7D8E9F0-1122-3344-5566-778899AABBCC",
        "name": "Persona 5",
        "brands": [
            {"id": "b-31", "name": "Undercover (Jun Takahashi)", "tags": ["Punk Tailoring", "Tokyo Streetwear", "Rebellious"], "score": 96.0},
            {"id": "b-32", "name": "Comme des Garçons", "tags": ["Avant-Garde", "Monochrome", "Bold Accents"], "score": 93.2},
            {"id": "b-33", "name": "Audio-Technica", "tags": ["Studio Monitors", "Japanese Audio", "Retro Hi-Fi"], "score": 91.0}
        ],
        "artists": [
            {"id": "a-31", "name": "CASIOPEA", "tags": ["Japanese Jazz Fusion", "City Pop", "Upbeat Grooves"], "score": 95.5},
            {"id": "a-32", "name": "Tatsuro Yamashita", "tags": ["City Pop", "Funk", "Melodic"], "score": 93.8},
            {"id": "a-33", "name": "BADBADNOTGOOD", "tags": ["Neo-Jazz", "Hip Hop Instrumental", "Atmospheric"], "score": 92.4}
        ],
        "movies": [
            {"id": "m-31", "name": "Baby Driver", "tags": ["Music Sync", "Heist Style", "Action"], "score": 91.2},
            {"id": "m-32", "name": "Lupin the Third: The Castle of Cagliostro", "tags": ["Gentleman Thief", "Jazz Soundtrack", "Classic"], "score": 95.0}
        ],
        "places": [
            {"id": "p-31", "name": "Velvet Room Jazz Bar", "tags": ["Live Bebop", "Speakeasy", "Signature Bourbon"], "score": 96.5, "address": "Historic Basement Lane", "price": "$$$"},
            {"id": "p-32", "name": "Siphon & Vinyl Cafe", "tags": ["Pour-over Syphon", "Antique Leather", "City Pop LPs"], "score": 94.0, "address": "Old Quarter Alley", "price": "$$"}
        ]
    }
}

class QlooClient:
    def __init__(self):
        self.base_url = settings.QLOO_BASE_URL.rstrip("/")
        self.api_key = settings.QLOO_API_KEY
        self.headers = {
            "X-Api-Key": self.api_key,
            "Accept": "application/json"
        }
        self.timeout = settings.QLOO_TIMEOUT_SECONDS

    async def search(self, query: str, limit: int = 10, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Calls /search endpoint to map human text to Qloo entities.
        """
        params = {"query": query, "limit": limit}
        url = f"{self.base_url}/search"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(url, headers=self.headers, params=params)
                if res.status_code == 200:
                    data = res.json()
                    results = data.get("results", []) if isinstance(data, dict) else data
                    # Normalize entity IDs and types
                    normalized = []
                    for item in results:
                        entity_id = item.get("id") or item.get("entity_id") or ""
                        types = item.get("types", [])
                        if not types and item.get("type"):
                            types = [item.get("type")]
                        normalized.append({
                            "id": entity_id,
                            "entity_id": entity_id,
                            "name": item.get("name", "Unknown"),
                            "types": types,
                            "subtype": item.get("subtype"),
                            "tags": item.get("tags", []),
                            "popularity": item.get("popularity", 50.0),
                            "properties": item.get("properties", {})
                        })
                    
                    if entity_type:
                        # Prioritize matches containing the target URN
                        matching = [x for x in normalized if entity_type in x.get("types", [])]
                        non_matching = [x for x in normalized if entity_type not in x.get("types", [])]
                        return matching + non_matching
                    return normalized
                else:
                    logger.warning(f"Qloo /search returned HTTP {res.status_code}: {res.text[:120]}")
        except Exception as e:
            logger.error(f"Error querying Qloo /search: {e}")

        # Fallback to local catalog if network/API fails
        q_lower = query.lower().strip()
        matched_local = []
        for key, demo_game in DEMO_GAME_DATABASE.items():
            if q_lower in key or key in q_lower:
                matched_local.append({
                    "id": demo_game["id"],
                    "entity_id": demo_game["id"],
                    "name": demo_game["name"],
                    "types": ["urn:entity:videogame"],
                    "subtype": "videogame",
                    "tags": ["Action RPG", "Immersive", "Cult Following"],
                    "popularity": 95.0,
                    "properties": {}
                })
        return matched_local

    async def search_entity(
        self,
        query: str,
        limit: int = 10,
        entity_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Resolve a named entity through Qloo search (or its configured demo fallback)."""
        return await self.search(query=query, limit=limit, entity_type=entity_type)

    async def get_insights(
        self,
        seed_entity_ids: List[str],
        filter_type: str,
        location_query: Optional[str] = None,
        take: int = 5
    ) -> Dict[str, Any]:
        """
        Queries /v2/insights for statistical cross-domain taste correlation.
        """
        if not seed_entity_ids:
            return {"entities": [], "data_source": "demo_fallback"}

        clean_seeds = [s for s in seed_entity_ids if s]
        params: Dict[str, Any] = {
            "signal.interests.entities": ",".join(clean_seeds),
            "filter.type": filter_type,
            "take": take
        }

        if location_query and filter_type == QlooEntityType.PLACE.value:
            if "global" not in location_query.lower():
                params["filter.location.query"] = location_query

        url = f"{self.base_url}/v2/insights"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(url, headers=self.headers, params=params)
                if res.status_code == 200:
                    data = res.json()
                    entities = data.get("results", {}).get("entities", [])
                    normalized = []
                    for e in entities:
                        e_id = e.get("id") or e.get("entity_id") or ""
                        tags = e.get("tags", [])
                        tag_names = []
                        for t in tags:
                            if isinstance(t, str):
                                tag_names.append(t)
                            elif isinstance(t, dict):
                                tag_names.append(t.get("name") or t.get("id") or "")
                        normalized_entity = {
                            "id": e_id,
                            "entity_id": e_id,
                            "name": e.get("name", "Unknown"),
                            "tags": [t for t in tag_names if t][:4],
                            "properties": e.get("properties", {})
                        }
                        affinity = e.get("affinity")
                        if affinity is not None:
                            normalized_entity["affinity"] = float(affinity)
                        normalized.append(normalized_entity)
                    return {"entities": normalized, "data_source": "qloo_live"}
                else:
                    logger.warning(f"Qloo /v2/insights {filter_type} returned HTTP {res.status_code}: {res.text[:120]}")
        except Exception as e:
            logger.error(f"Error querying Qloo /v2/insights: {e}")

        # Fallback offline intelligence
        return {
            "entities": self._get_fallback_insights(seed_entity_ids, filter_type, location_query, take),
            "data_source": "demo_fallback"
        }

    def _get_fallback_insights(
        self,
        seed_entity_ids: List[str],
        filter_type: str,
        location_query: Optional[str] = None,
        take: int = 4
    ) -> List[Dict[str, Any]]:
        # Match seed to demo database
        fallback_profile = DEMO_GAME_DATABASE["elden ring"]
        for key, game in DEMO_GAME_DATABASE.items():
            if any(game["id"] == sid for sid in seed_entity_ids):
                fallback_profile = game
                break

        if filter_type == QlooEntityType.BRAND.value:
            return fallback_profile.get("brands", [])[:take]
        elif filter_type == QlooEntityType.ARTIST.value:
            return fallback_profile.get("artists", [])[:take]
        elif filter_type == QlooEntityType.MOVIE.value:
            return fallback_profile.get("movies", [])[:take]
        elif filter_type == QlooEntityType.PLACE.value:
            places = fallback_profile.get("places", [])
            # Tailor address if location query provided
            if location_query:
                city_name = location_query.split(",")[0].strip()
                for p in places:
                    p["address"] = f"{city_name} Cultural District"
            return places[:take]
        return []

    async def health_check(self) -> Dict[str, Any]:
        """
        Pings /search to measure latency and verify API readiness.
        """
        start = time.time()
        connected = False
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.get(f"{self.base_url}/search", headers=self.headers, params={"query": "test", "limit": 1})
                latency = round((time.time() - start) * 1000, 1)
                connected = (res.status_code == 200)
                return {"connected": connected, "latency_ms": latency, "status_code": res.status_code}
        except Exception as e:
            latency = round((time.time() - start) * 1000, 1)
            return {"connected": False, "latency_ms": latency, "error": str(e)}

qloo_client = QlooClient()
