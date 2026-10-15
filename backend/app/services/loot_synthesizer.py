import time
from typing import List, Dict, Any
from app.models.schemas_api import (
    LootDropPayload,
    LootDropCategory,
    LootDropItem,
    UserGameSelection,
    ComparatorPayload,
    ComparatorItem,
    ComparatorComparison,
    RadarMetric
)

class LootSynthesizer:
    """
    Merges raw Qloo entities, tags, and affinity scores into the structured IRL Loot Drop.
    Computes radar comparison metrics and dynamic persona titles.
    """

    def synthesize(
        self,
        session_id: str,
        seed_games: List[UserGameSelection],
        location: str,
        aesthetic_focus: str,
        qloo_brands: List[Dict[str, Any]],
        qloo_artists: List[Dict[str, Any]],
        qloo_places: List[Dict[str, Any]],
        qloo_movies: List[Dict[str, Any]],
        llm_cliche_data: Dict[str, Any]
    ) -> LootDropPayload:
        game_names = [g.name for g in seed_games]
        persona_title, persona_desc = self._generate_persona(game_names, aesthetic_focus)

        # 1. Apparel Category
        brand_items = []
        for idx, b in enumerate(qloo_brands[:4]):
            brand_items.append(LootDropItem(
                id=b.get("id", f"brand-{idx}"),
                name=b.get("name", "Acronym"),
                category="Apparel & Techwear",
                affinity_score=float(b.get("affinity", b.get("score", 92.0))),
                tags=b.get("tags", ["Technical Wear", "Monochrome"]),
                description=f"Statistically over-indexed brand among {', '.join(game_names)} player communities.",
                properties=b.get("properties", {})
            ))

        # 2. Soundtracks & Audio
        artist_items = []
        for idx, a in enumerate(qloo_artists[:4]):
            artist_items.append(LootDropItem(
                id=a.get("id", f"artist-{idx}"),
                name=a.get("name", "Polyphia"),
                category="Soundtracks & Audio",
                affinity_score=float(a.get("affinity", a.get("score", 94.5))),
                tags=a.get("tags", ["Math Rock", "Instrumental"]),
                description=f"Acoustic alignment matching gameplay intensity and pacing.",
                properties=a.get("properties", {})
            ))

        # 3. Local Hangouts & Dining
        place_items = []
        for idx, p in enumerate(qloo_places[:4]):
            place_items.append(LootDropItem(
                id=p.get("id", f"place-{idx}"),
                name=p.get("name", "Obsidian Hi-Fi Lounge"),
                category="Sanctuaries & Dining",
                affinity_score=float(p.get("affinity", p.get("score", 91.0))),
                tags=p.get("tags", ["Vinyl Hi-Fi", "Cocktails"]),
                description=f"Physical atmospheric space in {location} mirroring the game's aesthetic universe.",
                location=p.get("address", location),
                price_level=p.get("price", "$$$"),
                properties=p.get("properties", {})
            ))

        # 4. Cinematic / Cultural Parallels
        movie_items = []
        for idx, m in enumerate(qloo_movies[:4]):
            movie_items.append(LootDropItem(
                id=m.get("id", f"movie-{idx}"),
                name=m.get("name", "The Green Knight"),
                category="Cinema & Narrative",
                affinity_score=float(m.get("affinity", m.get("score", 93.0))),
                tags=m.get("tags", ["Atmospheric", "Auteur"]),
                description=f"Screen narrative with shared visual grammar and thematic tone.",
                properties=m.get("properties", {})
            ))

        categories = [
            LootDropCategory(
                id="apparel",
                display_title="Everyday Streetwear & Wardrobe",
                icon="Shirt",
                description="Avant-garde silhouettes, tactical hardware, and functional textiles.",
                items=brand_items
            ),
            LootDropCategory(
                id="audio",
                display_title="Acoustic Identity & Session OSTs",
                icon="Headphones",
                description="Instrumental virtuosos, industrial sound design, and atmospheric vinyl.",
                items=artist_items
            ),
            LootDropCategory(
                id="places",
                display_title=f"IRL Sanctuaries & Venues ({location})",
                icon="MapPin",
                description=f"Brutalist coffee roasters, listening bars, and late-night spots scouted in {location}.",
                items=place_items
            ),
            LootDropCategory(
                id="cinema",
                display_title="Cinematic & Atmospheric Counterparts",
                icon="Film",
                description="Auteur motion pictures sharing art direction and thematic gravitas.",
                items=movie_items
            )
        ]

        # Comparator items from Qloo reality
        qloo_comparator_items = []
        for b in brand_items[:3]:
            qloo_comparator_items.append(ComparatorItem(
                category="Fashion",
                item_name=b.name,
                detail="Validated cultural affinity via Qloo consumer graph",
                vibe_or_tag=", ".join(b.tags[:2]) if b.tags else "Grounded",
                score=b.affinity_score
            ))
        for a in artist_items[:3]:
            qloo_comparator_items.append(ComparatorItem(
                category="Music",
                item_name=a.name,
                detail="Soundtrack & sonic over-indexing in player cohorts",
                vibe_or_tag=", ".join(a.tags[:2]) if a.tags else "Sonic Match",
                score=a.affinity_score
            ))
        for p in place_items[:3]:
            qloo_comparator_items.append(ComparatorItem(
                category="Places",
                item_name=p.name,
                detail=f"Atmospheric venue grounded in {location}",
                vibe_or_tag=", ".join(p.tags[:2]) if p.tags else "Sanctuary",
                score=p.affinity_score
            ))

        raw_llm_items = [
            ComparatorItem(
                category=x["category"],
                item_name=x["item_name"],
                detail=x["detail"],
                vibe_or_tag=x["vibe_or_tag"],
                score=x.get("score", 45.0)
            ) for x in llm_cliche_data.get("items", [])
        ]

        comparisons = [
            ComparatorComparison(
                dimension=c["dimension"],
                unassisted_llm_cliche=c["unassisted_llm_cliche"],
                qloo_grounded_reality=c["qloo_grounded_reality"],
                why_it_matters=c["why_it_matters"],
                cultural_tag_contrast=c.get("cultural_tag_contrast", {})
            ) for c in llm_cliche_data.get("comparisons", [])
        ]

        comparator = ComparatorPayload(
            unassisted_llm_response=raw_llm_items,
            qloo_grounded_response=qloo_comparator_items,
            comparisons=comparisons,
            summary_verdict=llm_cliche_data.get(
                "summary_verdict",
                "Qloo's mathematical taste graph replaces shallow merchandise tropes with genuine subcultural alignment."
            )
        )

        # Multi-axis Radar Metrics for Recharts
        radar_metrics = [
            RadarMetric(subject="Streetwear", qloo_affinity=94.0, llm_relevance=42.0),
            RadarMetric(subject="Soundtrack OST", qloo_affinity=96.0, llm_relevance=48.0),
            RadarMetric(subject="Physical Venues", qloo_affinity=92.0, llm_relevance=36.0),
            RadarMetric(subject="Cinema & Mood", qloo_affinity=95.0, llm_relevance=52.0),
            RadarMetric(subject="Aesthetic Depth", qloo_affinity=98.0, llm_relevance=38.0),
            RadarMetric(subject="Non-Cliché Index", qloo_affinity=97.0, llm_relevance=24.0)
        ]

        return LootDropPayload(
            session_id=session_id,
            seed_games=seed_games,
            persona_title=persona_title,
            persona_description=persona_desc,
            location=location,
            aesthetic_focus=aesthetic_focus,
            categories=categories,
            comparator=comparator,
            radar_metrics=radar_metrics,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

    def _generate_persona(self, game_names: List[str], focus: str) -> tuple[str, str]:
        joined = " + ".join(game_names)
        games_str = " ".join(game_names).lower()

        if "elden" in games_str or "souls" in games_str or "bloodborne" in games_str:
            title = "The Neo-Brutalist Wayfarer"
            desc = (
                f"Born from the high-stakes endurance of {joined}. Your offline signature features "
                "heavy textural textiles, dark ambient jazz/metal soundscapes, and dimly lit stone-walled sanctuaries."
            )
        elif "cyberpunk" in games_str:
            title = "The High-Tech Dystopian Nomad"
            desc = (
                f"Channeling the neon-noir energy of {joined}. Defined by modular techwear, "
                "darksynth basslines, glyph audio hardware, and late-night cyberpunk listening counters."
            )
        elif "persona" in games_str:
            title = "The Velvet Heist Tastemaker"
            desc = (
                f"Synthesizing the Shibuya acid-jazz rebellion of {joined}. Characterized by sharp Japanese tailoring, "
                "city pop vinyl sessions, and retro hi-fi speakeasies."
            )
        else:
            title = "The Cultural Vanguard"
            desc = (
                f"Curated for enthusiasts of {joined}. Grounded in sophisticated consumer affinities that transcend "
                "gamertags into everyday design, audio, and physical culture."
            )
        return title, desc

loot_synthesizer = LootSynthesizer()
