from enum import Enum
from typing import Dict, List

class QlooEntityType(str, Enum):
    VIDEOGAME = "urn:entity:videogame"
    PLACE = "urn:entity:place"
    ARTIST = "urn:entity:artist"
    BRAND = "urn:entity:brand"
    MOVIE = "urn:entity:movie"
    TV_SHOW = "urn:entity:tv_show"
    PODCAST = "urn:entity:podcast"
    BOOK = "urn:entity:book"
    PERSON = "urn:entity:person"
    DESTINATION = "urn:entity:destination"
    DEMOGRAPHICS = "urn:demographics"
    HEATMAP = "urn:heatmap"

AESTHETIC_PRIORITIES = [
    {
        "id": "streetwear_audio",
        "label": "High-Tech Streetwear & Audio",
        "description": "Apparel brands, technical gear, and cutting-edge music/soundtracks"
    },
    {
        "id": "cozy_dark_academia",
        "label": "Cozy Cafes & Dark Academia",
        "description": "Artisan coffee roasters, vinyl spots, atmospheric reads, and indie artists"
    },
    {
        "id": "nightlife_dining",
        "label": "Nightlife & Underground Venues",
        "description": "Speakeasies, craft cocktail bars, late-night dining, and DJ sets"
    },
    {
        "id": "full_immersion",
        "label": "Full 360° IRL Loot Drop",
        "description": "Comprehensive mix of brands, audio, local spots, and cultural media"
    }
]

# Qloo tag IDs used as additional interest signals for brand and artist insights.
# Combined UI selections are mapped alongside the individual preference slugs.
AESTHETIC_TAG_MAPPING: Dict[str, List[str]] = {
    "streetwear": ["urn:tag:keyword:style:streetwear"],
    "techwear": ["urn:tag:keyword:style:techwear"],
    "minimalist": ["urn:tag:keyword:style:minimalist"],
    "audiophile": ["urn:tag:keyword:music:audiophile"],
    "vintage": ["urn:tag:keyword:style:vintage"],
    "cyberpunk": ["urn:tag:genre:media:cyberpunk"],
    "dark_academia": ["urn:tag:keyword:style:dark_academia"],
    "streetwear_audio": [
        "urn:tag:keyword:style:streetwear",
        "urn:tag:keyword:style:techwear",
        "urn:tag:keyword:music:audiophile",
    ],
    "cozy_dark_academia": [
        "urn:tag:keyword:style:minimalist",
        "urn:tag:keyword:style:vintage",
        "urn:tag:keyword:style:dark_academia",
        "urn:tag:keyword:music:audiophile",
    ],
    "nightlife_dining": [
        "urn:tag:genre:media:cyberpunk",
        "urn:tag:keyword:style:vintage",
    ],
    "full_immersion": [
        "urn:tag:keyword:style:streetwear",
        "urn:tag:keyword:style:techwear",
        "urn:tag:keyword:style:minimalist",
        "urn:tag:keyword:music:audiophile",
        "urn:tag:keyword:style:vintage",
        "urn:tag:genre:media:cyberpunk",
        "urn:tag:keyword:style:dark_academia",
    ],
}

POPULAR_LOCATIONS = [
    {"city": "Tokyo, Japan", "label": "Tokyo (Akihabara / Shibuya)"},
    {"city": "New York, NY", "label": "New York, NY"},
    {"city": "Austin, TX", "label": "Austin, TX"},
    {"city": "London, UK", "label": "London, UK"},
    {"city": "Berlin, Germany", "label": "Berlin, Germany"},
    {"city": "Seoul, South Korea", "label": "Seoul, South Korea"},
    {"city": "Los Angeles, CA", "label": "Los Angeles, CA"},
    {"city": "Seattle, WA", "label": "Seattle, WA"},
    {"city": "San Francisco, CA", "label": "San Francisco, CA"},
    {"city": "Global / Online", "label": "Global (No Physical Venue Filter)"}
]

DEFAULT_SYSTEM_PROMPT = """
You are the IRL LootDrop Cultural Intelligence Agent, powered by Qloo's real-world behavioral taste graph.
Your job is to translate a gamer's virtual obsession (video games) into a tailored real-world lifestyle drop ("IRL Loot Drop"):
1. Contrast the difference between standard LLM clichés (e.g. gamer graphic tees, Mountain Dew, plastic swords) and real statistical cultural crossover (e.g. techwear brands like Acronym/Razer, math-rock artists like Polyphia/Mick Gordon, brutalist cocktail lounges, A24 cinema).
2. Synthesize factual Qloo entity recommendations, tags, addresses, and affinity scores into a cohesive aesthetic persona.
3. Keep explanations grounded in cultural taxonomy, aesthetic movements, and demographic affinity data.
"""
