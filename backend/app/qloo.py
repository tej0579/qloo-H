import os
import re
import httpx
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

QLOO_API_KEY = os.getenv("QLOO_API_KEY", "hack_cc337563ea74c0bb0424096700fbdbc0bfa87739")
QLOO_BASE_URL = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com").rstrip("/")

HEADERS = {
    "X-Api-Key": QLOO_API_KEY,
    "Accept": "application/json"
}

# Reliable fallback catalog for standard demo anchors
FALLBACK_CATALOG: Dict[str, Dict[str, Any]] = {
    "elden ring": {
        "id": "46CBADC5-F4A6-4E97-93B2-959066C9F608",
        "name": "Elden Ring",
        "tags": ["Action RPG", "High Difficulty", "Dark Fantasy", "Open World", "Atmospheric"],
        "correlated": [
            {"name": "Bloodborne", "score": 96.5, "tags": ["Cosmic Horror", "Gothic Victorian", "Aggressive Combat"]},
            {"name": "Lies of P", "score": 93.8, "tags": ["Souls-like", "Parry Combat", "Victorian Steampunk"]},
            {"name": "Hollow Knight", "score": 91.2, "tags": ["Dark Fantasy", "Cryptic Lore", "Metroidvania"]},
            {"name": "Shadow of the Colossus", "score": 89.0, "tags": ["Melancholic", "Minimalist Lore", "Grand Scale"]},
            {"name": "Mortal Shell", "score": 85.4, "tags": ["Compact Souls-like", "Dark Fantasy", "Atmospheric"]}
        ]
    },
    "cyberpunk 2077": {
        "id": "A4B7D201-9988-4F11-AE77-0099118833AA",
        "name": "Cyberpunk 2077",
        "tags": ["Cyberpunk", "First-Person RPG", "Dystopian", "Story Rich", "Sci-Fi"],
        "correlated": [
            {"name": "Deus Ex: Human Revolution", "score": 95.0, "tags": ["Cyberpunk", "Immersive Sim", "Conspiracy"]},
            {"name": "Ghostrunner", "score": 92.0, "tags": ["Fast-Paced", "Cyberpunk", "Katana Combat"]},
            {"name": "The Ascent", "score": 88.5, "tags": ["Arcology", "Twin-Stick Shooter", "Gritty Cyberpunk"]},
            {"name": "Ruiner", "score": 87.0, "tags": ["Dark Cyberpunk", "Industrial", "Isometric Action"]}
        ]
    },
    "hades": {
        "id": "H1D2E3S4-AABB-CCDD-EEFF-001122334455",
        "name": "Hades",
        "tags": ["Roguelike", "Fast-Paced Action", "Greek Mythology", "Isometric", "Narrative Rich"],
        "correlated": [
            {"name": "Dead Cells", "score": 95.2, "tags": ["Fast Combat", "Rogue-lite", "Pixel Art"]},
            {"name": "Bastion", "score": 92.4, "tags": ["Isometric Action", "Narrative Driven", "Stylized"]},
            {"name": "Transistor", "score": 90.1, "tags": ["Tactical Combat", "Sci-Fi Noir", "Stylized OST"]},
            {"name": "Returnal", "score": 88.6, "tags": ["Sci-Fi Horror", "Fast-Paced Roguelike", "Third-Person"]}
        ]
    }
}

GAME_ALIASES: Dict[str, str] = {
    "gta": "Grand Theft Auto",
    "gta 5": "Grand Theft Auto V",
    "gta v": "Grand Theft Auto V",
    "gta iv": "Grand Theft Auto IV",
    "gta 4": "Grand Theft Auto IV",
    "gta sa": "Grand Theft Auto: San Andreas",
    "gta san andreas": "Grand Theft Auto: San Andreas",
    "gta vice city": "Grand Theft Auto: Vice City",
    "rdr": "Red Dead Redemption",
    "rdr2": "Red Dead Redemption 2",
    "rdr 2": "Red Dead Redemption 2",
    "cod": "Call of Duty",
    "cod mw": "Call of Duty: Modern Warfare",
    "cod mw2": "Call of Duty: Modern Warfare II",
    "cod warzone": "Call of Duty: Warzone",
    "gow": "God of War",
    "gow ragnarok": "God of War Ragnarök",
    "gow 2018": "God of War",
    "bg3": "Baldur's Gate 3",
    "cs": "Counter-Strike",
    "csgo": "Counter-Strike: Global Offensive",
    "cs 2": "Counter-Strike 2",
    "cs2": "Counter-Strike 2",
    "tf2": "Team Fortress 2",
    "ff7": "Final Fantasy VII",
    "ff7 remake": "Final Fantasy VII Remake",
    "ffvii": "Final Fantasy VII",
    "ff14": "Final Fantasy XIV",
    "ffxiv": "Final Fantasy XIV",
    "ff16": "Final Fantasy XVI",
    "botw": "The Legend of Zelda: Breath of the Wild",
    "totk": "The Legend of Zelda: Tears of the Kingdom",
    "zelda": "The Legend of Zelda",
    "ac": "Assassin's Creed",
    "ac valhalla": "Assassin's Creed Valhalla",
    "ac odyssey": "Assassin's Creed Odyssey",
    "re4": "Resident Evil 4",
    "re2": "Resident Evil 2",
    "re7": "Resident Evil 7",
    "re village": "Resident Evil Village",
    "mhw": "Monster Hunter: World",
    "ds1": "Dark Souls",
    "ds2": "Dark Souls II",
    "ds3": "Dark Souls III",
    "dks": "Dark Souls",
    "er": "Elden Ring",
    "cp2077": "Cyberpunk 2077",
    "cyberpunk": "Cyberpunk 2077",
    "eldenring": "Elden Ring",
    "lol": "League of Legends",
    "dota": "Dota 2",
    "dota 2": "Dota 2",
    "wow": "World of Warcraft",
    "poe": "Path of Exile",
    "destiny 2": "Destiny 2",
    "d2": "Diablo II",
    "d4": "Diablo IV"
}

def resolve_alias(query: str) -> str:
    clean = query.lower().strip()
    return GAME_ALIASES.get(clean, query)

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "you", "your", "i", "me", "my",
    "he", "she", "it", "they", "we", "us", "who", "what", "where", "when", "why",
    "how", "from", "in", "on", "at", "to", "for", "of", "with", "about", "by",
    "bro", "dude", "bot", "right", "yeah", "no", "yes", "not", "game", "games"
}

def is_title_match(query: str, candidate_name: str) -> bool:
    clean_q = query.lower().strip()
    clean_cand = candidate_name.lower().strip()

    if clean_q == clean_cand:
        return True

    content_words = [w for w in re.findall(r"\b[a-zA-Z0-9]+\b", clean_q) if w not in STOP_WORDS]
    # Filter out standalone numbers so '5' doesn't match 'Yakuza 5'
    alpha_words = [w for w in content_words if not w.isdigit() and len(w) > 1]
    if not alpha_words:
        # If the query had NO content words or alpha words (e.g. 'the game', '5', 'is'),
        # require exact match only!
        return clean_q == clean_cand

    # If the alias expanded or exact phrase is contained
    if len(clean_q) >= 4 and (clean_q in clean_cand or clean_cand in clean_q):
        return True

    cand_words = set(re.findall(r"\b[a-zA-Z0-9]+\b", clean_cand))
    matches = sum(1 for w in alpha_words if w in cand_words)
    return (matches / len(alpha_words)) >= 0.6

async def search_videogame(query: str) -> Optional[Dict[str, Any]]:
    """
    Calls Qloo API: GET /search?query={game}&type=urn:entity:videogame
    Returns {id, name, tags} or None.
    """
    clean = query.strip()
    expanded = resolve_alias(clean)
    url = f"{QLOO_BASE_URL}/search"
    params = {"query": expanded, "type": "urn:entity:videogame", "limit": 5}

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            res = await client.get(url, headers=HEADERS, params=params)
            if res.status_code == 200:
                results = res.json().get("results", [])
                for item in results:
                    types = item.get("types", [])
                    if not types and item.get("type"):
                        types = [item.get("type")]
                    if any("videogame" in str(t).lower() for t in types):
                        name = item.get("name", "")
                        # Strictly verify the returned game title actually matches the query
                        if not (is_title_match(expanded, name) or is_title_match(clean, name)):
                            continue
                        raw_tags = item.get("tags", [])
                        tags = [t.get("name") if isinstance(t, dict) else str(t) for t in raw_tags if (t.get("name") if isinstance(t, dict) else str(t))][:5]
                        return {
                            "id": item.get("entity_id") or item.get("id"),
                            "name": name,
                            "tags": tags if tags else ["Action", "Adventure", "Immersive"]
                        }
    except Exception as e:
        print(f"[Qloo Search Error] {e}")

    # Fallback catalog check
    q_lower = expanded.lower()
    for key, entry in FALLBACK_CATALOG.items():
        if key in q_lower or q_lower in key:
            return {
                "id": entry["id"],
                "name": entry["name"],
                "tags": entry["tags"]
            }

    return None

async def get_insights(entity_id: str, anchor_name: str = "", take: int = 5) -> List[Dict[str, Any]]:
    """
    Calls Qloo API: GET /v2/insights?signal.interests.entities={entity_id}&filter.type=urn:entity:videogame
    Returns correlated entities with tags and scores.
    """
    url = f"{QLOO_BASE_URL}/v2/insights"
    params = {
        "signal.interests.entities": entity_id,
        "filter.type": "urn:entity:videogame",
        "take": take
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.get(url, headers=HEADERS, params=params)
            if res.status_code == 200:
                entities = res.json().get("results", {}).get("entities", [])
                matches = []
                for e in entities:
                    raw_tags = e.get("tags", [])
                    clean_tags = [t.get("name") if isinstance(t, dict) else str(t) for t in raw_tags if (t.get("name") if isinstance(t, dict) else str(t))][:4]
                    pop = e.get("popularity") or 0.90
                    score = round(float(pop) * 100, 1) if float(pop) <= 1.0 else round(float(pop), 1)

                    matches.append({
                        "id": e.get("entity_id") or e.get("id"),
                        "name": e.get("name", "Unknown Game"),
                        "score": score,
                        "tags": clean_tags if clean_tags else ["Correlated", "Atmospheric"]
                    })
                if matches:
                    return matches
    except Exception as e:
        print(f"[Qloo Insights Error] {e}")

    # Fallback catalog check
    name_lower = anchor_name.lower()
    for key, entry in FALLBACK_CATALOG.items():
        if key in name_lower or entry["id"] == entity_id:
            return entry["correlated"][:take]

    return FALLBACK_CATALOG["elden ring"]["correlated"][:take]
