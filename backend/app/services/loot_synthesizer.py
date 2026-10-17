import time
from math import isfinite
from typing import List, Dict, Any
from app.models.schemas_api import (
    LootDropPayload,
    LootDropCategory,
    LootDropItem,
    UserGameSelection,
    ComparatorPayload,
    ComparatorItem,
    ComparatorComparison,
    RadarMetric,
    QuestLogStep,
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
        data_source: str,
        llm_cliche_data: Dict[str, Any]
    ) -> LootDropPayload:
        game_names = [g.name for g in seed_games]
        persona_title, persona_desc = self._generate_persona(game_names, aesthetic_focus)
        game_tags = [tag for game in seed_games for tag in game.tags]
        archetype_title = self._generate_archetype_title(aesthetic_focus, game_names, game_tags)

        # 1. Apparel Category
        brand_items = []
        for idx, b in enumerate(qloo_brands[:4]):
            brand_items.append(LootDropItem(
                id=b.get("id", f"brand-{idx}"),
                name=b.get("name", "Acronym"),
                category="Apparel & Techwear",
                affinity_score=self._score(b),
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
                affinity_score=self._score(a),
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
                affinity_score=self._score(p),
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
                affinity_score=self._score(m),
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
        qloo_detail = (
            "Returned by Qloo's live cultural insights graph"
            if data_source == "qloo_live"
            else "Illustrative offline demo recommendation; not returned by live Qloo"
        )
        for b in brand_items[:3]:
            qloo_comparator_items.append(ComparatorItem(
                category="Fashion",
                item_name=b.name,
                detail=qloo_detail,
                vibe_or_tag=", ".join(b.tags[:2]) if b.tags else "Grounded",
                score=b.affinity_score
            ))
        for a in artist_items[:3]:
            qloo_comparator_items.append(ComparatorItem(
                category="Music",
                item_name=a.name,
                detail=qloo_detail,
                vibe_or_tag=", ".join(a.tags[:2]) if a.tags else "Sonic Match",
                score=a.affinity_score
            ))
        for p in place_items[:3]:
            qloo_comparator_items.append(ComparatorItem(
                category="Places",
                item_name=p.name,
                detail=(
                    f"Venue recommendation for {location} returned by Qloo"
                    if data_source == "qloo_live"
                    else f"Illustrative venue example for {location}; not returned by live Qloo"
                ),
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
            summary_verdict=(
                llm_cliche_data.get(
                    "summary_verdict",
                    "Qloo's taste graph provides cross-domain cultural recommendations."
                )
                if data_source == "qloo_live"
                else "Offline demo recommendations are illustrative examples; live Qloo affinity data was unavailable for this drop."
            )
        )

        # Compare category averages from the returned recommendation scores.
        radar_categories = [
            ("Fashion", brand_items, "Fashion"),
            ("Music", artist_items, "Music"),
            ("Places", place_items, "Places"),
            ("Films", movie_items, "Films"),
        ]
        radar_metrics = [
            RadarMetric(
                subject=subject,
                qloo_affinity=self._average_score(items, "affinity_score"),
                llm_relevance=self._average_score(
                    [item for item in raw_llm_items if item.category.casefold() == llm_category.casefold()],
                    "score"
                ),
            )
            for subject, items, llm_category in radar_categories
        ]
        overall_match_score = self._average_score(
            brand_items + artist_items + place_items + movie_items,
            "affinity_score"
        )
        quest_log = self._build_quest_log(brand_items, artist_items, place_items, movie_items, location)

        return LootDropPayload(
            session_id=session_id,
            seed_games=seed_games,
            persona_title=persona_title,
            persona_description=persona_desc,
            archetype_title=archetype_title,
            quest_log=quest_log,
            location=location,
            aesthetic_focus=aesthetic_focus,
            categories=categories,
            comparator=comparator,
            radar_metrics=radar_metrics,
            data_source=data_source,
            overall_match_score=overall_match_score,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

    @staticmethod
    def _generate_archetype_title(aesthetic_focus: str, game_names: List[str], game_tags: List[str]) -> str:
        signals = " ".join([*game_tags[:8], *game_names]).casefold()
        if any(signal in signals for signal in ("cyber", "neon", "dystop", "transhuman", "tech")):
            bridge = "Cybernetic"
        elif any(signal in signals for signal in ("gothic", "dark", "folklore", "fantasy", "souls")):
            bridge = "Gothic"
        elif any(signal in signals for signal in ("urban", "city", "jazz", "vinyl", "heist", "tokyo", "noir")):
            bridge = "Metropolis"
        elif any(signal in signals for signal in ("ambient", "audio", "instrumental", "music")):
            bridge = "Analog"
        else:
            bridge = "Cultural"

        archetype_by_aesthetic = {
            "streetwear_audio": "Street-Tactician",
            "streetwear": "Street-Tactician",
            "techwear": "Signal Runner",
            "minimalist": "Quiet Modernist",
            "audiophile": "Vinyl Flâneur",
            "vintage": "Archive Seeker",
            "cyberpunk": "Neon Nomad",
            "dark_academia": "Avant-Garde Wanderer",
            "cozy_dark_academia": "Avant-Garde Wanderer",
            "nightlife_dining": "Vinyl Flâneur",
            "full_immersion": "Cultural Wayfarer",
        }
        archetype = archetype_by_aesthetic.get(aesthetic_focus.casefold(), "Cultural Wayfarer")
        return f"{bridge} {archetype}"

    @staticmethod
    def _build_quest_log(
        brand_items: List[LootDropItem],
        artist_items: List[LootDropItem],
        place_items: List[LootDropItem],
        movie_items: List[LootDropItem],
        location: str,
    ) -> List[QuestLogStep]:
        brand = brand_items[0].name if brand_items else "No brand match available"
        artist = artist_items[0].name if artist_items else "No artist match available"
        place = place_items[0] if place_items else None
        movie = movie_items[0].name if movie_items else "No film match available"
        place_name = place.name if place else "No local venue match available"
        place_location = place.location if place and place.location else location

        return [
            QuestLogStep(
                time="2:00 PM",
                title="Afternoon Gear",
                recommendation=brand,
                description=f"Build your look around {brand} before heading out.",
            ),
            QuestLogStep(
                time="4:30 PM",
                title="Transit Soundtrack",
                recommendation=artist,
                description=f"Queue {artist} for the trip across {location}.",
            ),
            QuestLogStep(
                time="7:00 PM",
                title="Evening Spot",
                recommendation=place_name,
                description=f"Spend the evening at {place_name} ({place_location}).",
            ),
            QuestLogStep(
                time="10:30 PM",
                title="Late Night Watch",
                recommendation=movie,
                description=f"Close the day with {movie}.",
            ),
        ]

    @staticmethod
    def _score(item: Dict[str, Any]) -> float | None:
        score = item.get("affinity", item.get("score"))
        if score is None:
            return None
        numeric_score = float(score)
        return numeric_score if isfinite(numeric_score) else None

    @staticmethod
    def _average_score(items: List[Any], field: str) -> float | None:
        scores = []
        for item in items:
            score = getattr(item, field, None) if not isinstance(item, dict) else item.get(field)
            if score is not None and isfinite(float(score)):
                scores.append(float(score))
        return round(sum(scores) / len(scores), 2) if scores else None

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
