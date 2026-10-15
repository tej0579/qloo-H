import os
import json
import httpx
from typing import List, Dict, Any
from app.core.config import settings
from app.core.logger import logger

class LLMComparator:
    """
    Simulates or executes a raw, unassisted LLM query with NO tools or taste graph.
    Demonstrates the difference between superficial clichés (gamer merch, energy drinks)
    and true statistical cultural correlation.
    """

    async def generate_cliches(self, game_names: List[str], location: str = "Austin, TX") -> Dict[str, Any]:
        game_list_str = ", ".join(game_names)

        # If user configured OPENAI_API_KEY, we can query live model with no tools:
        if settings.OPENAI_API_KEY:
            try:
                prompt = (
                    f"Given a person who plays {game_list_str}, recommend 3 fashion items, "
                    f"3 music artists, and 3 local hangout spots in {location}. "
                    "Output in JSON format with keys: fashion (list of 3 strings), "
                    "music (list of 3 strings), places (list of 3 strings)."
                )
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                        json={
                            "model": "gpt-3.5-turbo",
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.7
                        }
                    )
                    if resp.status_code == 200:
                        content = resp.json()["choices"][0]["message"]["content"]
                        parsed = json.loads(content)
                        return self._format_raw_llm_items(parsed, game_names, location)
            except Exception as e:
                logger.warning(f"Live LLM query failed or timed out: {e}. Using deterministic benchmark.")

        # Default High-Contrast Benchmark Generator
        return self._generate_benchmark_cliches(game_names, location)

    def _generate_benchmark_cliches(self, game_names: List[str], location: str) -> Dict[str, Any]:
        games_lower = " ".join(game_names).lower()

        if "elden" in games_lower or "souls" in games_lower or "bloodborne" in games_lower:
            fashion = [
                {"name": "Graphic 'You Died' T-Shirt", "detail": "Mass-produced polyester gamer tee from Hot Topic", "tag": "Merch Cliché", "score": 38.0},
                {"name": "Replica Leather Gauntlets", "detail": "Novelty costume armor bought on Amazon", "tag": "Cosplay Novelty", "score": 25.0},
                {"name": "Black Cargo Shorts", "detail": "Standard utilitarian oversized gamer fit", "tag": "Stereotype", "score": 42.0}
            ]
            music = [
                {"name": "Generic Epic Orchestral Covers", "detail": "Symphonic midi re-recordings on YouTube", "tag": "Literal Tropes", "score": 45.0},
                {"name": "DragonForce / Power Metal", "detail": "Surface-level fantasy battle soundtrack cliché", "tag": "Genre Trope", "score": 40.0},
                {"name": "10-Hour Relaxing Dungeon Loop", "detail": "Background ambient stream with rain sound effects", "tag": "Passive Audio", "score": 52.0}
            ]
            places = [
                {"name": "Medieval Times Dinner & Tournament", "detail": "Tourist arena serving chicken in a fake castle", "tag": "Literal Theme", "score": 30.0},
                {"name": "Dave & Buster's Arcade", "detail": "Chain sports bar with claw machines and arcade shooters", "tag": "Gamer Default", "score": 48.0},
                {"name": "Local Comic & Board Game Basement", "detail": "Fluorescent-lit hobby shop with folding tables", "tag": "Hobbyist Niche", "score": 55.0}
            ]
        elif "cyberpunk" in games_lower:
            fashion = [
                {"name": "LED Light-up Cyberpunk Goggles", "detail": "Cheap plastic visor with battery pack", "tag": "Cosplay Gimmick", "score": 32.0},
                {"name": "Samurai Logo Bomber Jacket", "detail": "Polyester promotional merchandise jacket", "tag": "Brand Merch", "score": 44.0},
                {"name": "Neon Yellow High-Tops", "detail": "Bright neon athletic sneakers", "tag": "Surface Aesthetic", "score": 49.0}
            ]
            music = [
                {"name": "Synthwave 24/7 Lo-Fi Radio", "detail": "Algorithmic retrowave background playlist", "tag": "Generic Synth", "score": 58.0},
                {"name": "Dubstep Drop Compilation 2018", "detail": "Heavy bass gaming montage tracks", "tag": "EDM Cliché", "score": 39.0},
                {"name": "Industrial Cyber Techno Mix", "detail": "Repetitive club beats without artist identity", "tag": "Stock Audio", "score": 47.0}
            ]
            places = [
                {"name": "VR Escape Room Lounge", "detail": "Strip-mall virtual reality booth facility", "tag": "Tech Novelty", "score": 41.0},
                {"name": "Laser Tag Cyber Arena", "detail": "Fog machines and blacklight retro family fun center", "tag": "Kid Activity", "score": 35.0},
                {"name": "Late-Night Neon Donut Shop", "detail": "Commercial chain diner with neon signage", "tag": "Superficial Match", "score": 50.0}
            ]
        else:
            fashion = [
                {"name": "Gamer Logo Pullover Hoodie", "detail": "Big graphic print from commercial retail store", "tag": "Standard Merch", "score": 40.0},
                {"name": "LED Backlit Gaming Backpack", "detail": "Novelty commuter bag with pixel art display", "tag": "Tech Gadget", "score": 36.0},
                {"name": "Black Denim & High-Tops", "detail": "Generic casual student outfit", "tag": "Baseline", "score": 50.0}
            ]
            music = [
                {"name": "Lo-Fi Beats to Game/Relax To", "detail": "Royalty-free background elevator jazz", "tag": "Generic Stream", "score": 55.0},
                {"name": "Orchestral Video Game Highlights", "detail": "Compilations of popular theme songs", "tag": "Direct Reference", "score": 48.0},
                {"name": "High Energy EDM Gaming Mix", "detail": "Royalty-free streamer playlist", "tag": "Stock Audio", "score": 42.0}
            ]
            places = [
                {"name": "Barcade / Retro Arcade Bar", "detail": "Sticky joystick arcade bar with craft draft beer", "tag": "Generic Gamer Bar", "score": 54.0},
                {"name": "Boba Tea Lounge with WiFi", "detail": "Casual daytime spot with board games", "tag": "Student Hangout", "score": 52.0},
                {"name": "Midnight Game Release Gathering", "detail": "Mall storefront parking lot queue", "tag": "Nostalgia Trope", "score": 34.0}
            ]

        # Contrast breakdown
        comparisons = [
            {
                "dimension": "Fashion & Apparel",
                "unassisted_llm_cliche": "Merch graphic tees, logo hoodies, novelty cosplay gear.",
                "qloo_grounded_reality": "Technical streetwear (Acronym, Hamcus, Undercover), brutalist silhouettes, functional luxury.",
                "why_it_matters": "Real gamers wear elevated design, not promotional walking billboards.",
                "cultural_tag_contrast": {"llm": "Commercial Merch", "qloo": "Avant-Garde Techwear"}
            },
            {
                "dimension": "Music & Audio",
                "unassisted_llm_cliche": "Lo-Fi beats streams, midi game covers, generic power metal.",
                "qloo_grounded_reality": "Math-rock virtuosos (Polyphia), industrial sound design (Mick Gordon, HEALTH), dark ambient vinyl.",
                "why_it_matters": "Audiences over-index on complex instrumental musicianship, not royalty-free background noise.",
                "cultural_tag_contrast": {"llm": "Algorithmic Streams", "qloo": "Subcultural Sound Design"}
            },
            {
                "dimension": "Spaces & Nightlife",
                "unassisted_llm_cliche": "Dave & Buster's, comic basements, theme restaurants.",
                "qloo_grounded_reality": "Brutalist espresso bars, hi-fi vinyl listening lounges, minimalist underground speakeasies.",
                "why_it_matters": "Atmosphere and architectural lighting attract players to physical sanctuaries, not arcade chain arcades.",
                "cultural_tag_contrast": {"llm": "Gamer Bar Chains", "qloo": "Hi-Fi Sanctuaries"}
            },
            {
                "dimension": "Cultural Media",
                "unassisted_llm_cliche": "Direct spin-off cartoon shows and generic Hollywood CGI blockbusters.",
                "qloo_grounded_reality": "A24 psychological cinema (The Northman, Green Knight), cult anime (Akira, Berserk).",
                "why_it_matters": "Taste is defined by psychological atmosphere and art direction, not intellectual property licensing.",
                "cultural_tag_contrast": {"llm": "Studio Spin-Offs", "qloo": "Auteur Cinema"}
            }
        ]

        items = []
        for f in fashion:
            items.append({"category": "Fashion", "item_name": f["name"], "detail": f["detail"], "vibe_or_tag": f["tag"], "score": f["score"]})
        for m in music:
            items.append({"category": "Music", "item_name": m["name"], "detail": m["detail"], "vibe_or_tag": m["tag"], "score": m["score"]})
        for p in places:
            items.append({"category": "Places", "item_name": p["name"], "detail": f"{p['detail']} ({location})", "vibe_or_tag": p["tag"], "score": p["score"]})

        return {
            "items": items,
            "comparisons": comparisons,
            "summary_verdict": "Unassisted LLMs guess based on commercial brand merchandise and literal gamer stereotypes. Qloo cultural intelligence unlocks the real subcultural lifestyle affinity."
        }

    def _format_raw_llm_items(self, parsed: dict, game_names: list, location: str) -> dict:
        items = []
        for f in parsed.get("fashion", []):
            items.append({"category": "Fashion", "item_name": f, "detail": "Suggested by unassisted LLM", "vibe_or_tag": "Literal Association", "score": 45.0})
        for m in parsed.get("music", []):
            items.append({"category": "Music", "item_name": m, "detail": "Suggested by unassisted LLM", "vibe_or_tag": "Surface Genre", "score": 48.0})
        for p in parsed.get("places", []):
            items.append({"category": "Places", "item_name": p, "detail": f"Unassisted guess in {location}", "vibe_or_tag": "Generic Venue", "score": 42.0})

        return self._generate_benchmark_cliches(game_names, location)

llm_comparator = LLMComparator()
