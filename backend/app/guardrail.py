import re
from typing import Dict, Any, Optional, Tuple, List

GREETING_WORDS = {
    "hi", "hello", "hey", "hola", "yo", "sup", "greetings", "good morning",
    "good afternoon", "good evening", "howdy", "wassup", "what's up", "whats up",
    "hey there", "hi there", "hello there", "no hi"
}

QUESTION_STARTERS = (
    "who", "what", "where", "when", "why", "how", "are you", "you are",
    "is it", "can you", "could you", "do you", "tell me", "explain",
    "which", "whose", "whom"
)

CONVERSATIONAL_KEYWORDS = [
    r"\b(where are you from|where do you live|what country|who made you|who created you)\b",
    r"\b(who are you|what are you|what can you do|what do you do|help me|tell me about yourself)\b",
    r"\b(you are.*bot|are you.*bot|are you.*ai|gaming bot|game bot|ai bot|chatbot)\b"
]

OFF_TOPIC_PATTERNS = [
    r"\b(cook|recipe|pasta|bake|pizza|baking|cooking|ingredients|cake|chocolate|food|dinner|lunch|breakfast|dessert|coffee|tea|meal)\b",
    r"\b(election|president|biden|trump|politics|democrat|republican|senate|government|vote|voting)\b",
    r"\b(weather|forecast|rain|temperature|climate|snow|humidity|storm)\b",
    r"\b(stock|crypto|bitcoin|ethereum|forex|investing|dividends|finance|shares|wallet)\b",
    r"\b(solve|math|calculus|algebra|equation|derivative|integral)\b",
    r"\b(python|javascript|write a function|debug this code|css|html|react|backend code)\b",
    r"\b(flight ticket|hotel booking|medical advice|symptoms of|disease|doctor|medicine)\b"
]

VAGUE_RESPONSES = {
    "yes", "no", "yeah", "nope", "ok", "okay", "k", "sure", "fine", "give",
    "tell", "show", "what", "idk", "cool", "nice", "maybe", "why", "idk", "dunno"
}

TURN_1_KEYWORDS = {
    "combat", "mechanic", "mechanics", "parry", "parrying", "reflex", "reflexes",
    "timing", "lore", "story", "world", "atmosphere", "atmospheric", "exploration",
    "explore", "build", "builds", "rpg", "progression", "difficulty", "hard", "boss",
    "bosses", "gameplay", "action", "fight", "fighting", "shooting", "shooter", "stealth",
    "tactical", "turn-based", "hack and slash", "guns", "melee", "magic", "skills"
}

TURN_2_KEYWORDS = {
    "gothic", "dark", "gritty", "realism", "realistic", "3d", "2d", "indie", "stylized",
    "isometric", "pixel", "pixel art", "art", "vibes", "vibe", "sci-fi", "scifi", "cyberpunk",
    "fantasy", "dystopian", "anime", "minimalist", "hand-drawn", "fpp", "fps", "first person",
    "tpp", "third person", "retro", "colorful", "aesthetic", "ruins", "decaying"
}

TURN_3_KEYWORDS = {
    "pc", "ps5", "playstation", "ps4", "ps3", "ps2", "xbox", "series x", "switch",
    "nintendo", "steam deck", "deck", "portable", "handheld", "console", "hours", "hour",
    "hrs", "hr", "campaign", "short", "long", "epic", "quick", "tight", "open world",
    "focused", "massive", "15", "20", "25", "30", "40", "50", "60", "80", "100"
}

GENRE_SCOUT_MAP = {
    "fpp": {
        "label": "First-Person Perspective (FPP / FPS)",
        "anchors": ["Cyberpunk 2077", "DOOM Eternal", "BioShock Infinite", "Half-Life 2"]
    },
    "fps": {
        "label": "First-Person Shooter (FPS / FPP)",
        "anchors": ["DOOM Eternal", "Cyberpunk 2077", "BioShock Infinite", "Half-Life 2"]
    },
    "tpp": {
        "label": "Third-Person Perspective (TPP)",
        "anchors": ["Elden Ring", "The Witcher 3: Wild Hunt", "God of War", "Red Dead Redemption 2"]
    },
    "rpg": {
        "label": "Role-Playing Games (RPG)",
        "anchors": ["Elden Ring", "Baldur's Gate 3", "The Witcher 3: Wild Hunt", "Persona 5"]
    },
    "soulslike": {
        "label": "Souls-like / Action RPG",
        "anchors": ["Elden Ring", "Dark Souls III", "Bloodborne", "Lies of P"]
    },
    "souls": {
        "label": "Souls-like / Action RPG",
        "anchors": ["Elden Ring", "Dark Souls III", "Bloodborne", "Lies of P"]
    },
    "horror": {
        "label": "Survival Horror",
        "anchors": ["Resident Evil 4", "Dead Space", "Silent Hill 2", "Alien: Isolation"]
    },
    "open world": {
        "label": "Open World Exploration",
        "anchors": ["Elden Ring", "Red Dead Redemption 2", "Grand Theft Auto V", "The Witcher 3: Wild Hunt"]
    },
    "roguelike": {
        "label": "Roguelike / Action",
        "anchors": ["Hades", "Dead Cells", "Returnal", "The Binding of Isaac"]
    },
    "action": {
        "label": "Action / Hack and Slash",
        "anchors": ["Devil May Cry 5", "God of War", "Sekiro: Shadows Die Twice", "Hades"]
    },
    "stealth": {
        "label": "Stealth & Infiltration",
        "anchors": ["Metal Gear Solid V", "Dishonored 2", "Hitman 3", "Deus Ex: Human Revolution"]
    },
    "racing": {
        "label": "Racing & Driving",
        "anchors": ["Forza Horizon 5", "Gran Turismo 7", "Need for Speed Unbound", "F1 23"]
    },
    "coop": {
        "label": "Cooperative Multiplayer",
        "anchors": ["It Takes Two", "Deep Rock Galactic", "Helldivers 2", "Portal 2"]
    },
    "co-op": {
        "label": "Cooperative Multiplayer",
        "anchors": ["It Takes Two", "Deep Rock Galactic", "Helldivers 2", "Portal 2"]
    }
}

def extract_game_title(query: str) -> str:
    """
    Cleans user input to isolate the game title.
    e.g. 'I love Elden Ring' -> 'Elden Ring'
    """
    clean = query.strip()
    cleaned = re.sub(
        r"^(i love|i like|i play|games like|game like|recommend like|something like|similar to|looking for games like|best games like)\s+",
        "",
        clean,
        flags=re.IGNORECASE
    ).strip().strip("\"'.,")
    return cleaned if cleaned else clean

def is_conversational_or_question(clean_lower: str) -> bool:
    words = clean_lower.split()
    # Single word question starters like 'why', 'what' alone are vague calibration inputs, not full questions
    if len(words) <= 1 and words and words[0] in {"why", "what", "who", "how", "when", "where"}:
        return False

    if clean_lower.endswith("?") or clean_lower.endswith("right"):
        return True

    for starter in QUESTION_STARTERS:
        if clean_lower.startswith(starter):
            return True

    for pattern in CONVERSATIONAL_KEYWORDS:
        if re.search(pattern, clean_lower):
            return True

    return False

def check_turn_keyword_relevance(clean_lower: str, current_turn: int) -> bool:
    words = set(re.findall(r"\b[a-zA-Z0-9_\-']+\b", clean_lower))
    # Handle composite phrases like 'play station'
    if "play station" in clean_lower or "first person" in clean_lower or "third person" in clean_lower or "open world" in clean_lower or "steam deck" in clean_lower:
        return True

    if current_turn == 1:
        return bool(words & TURN_1_KEYWORDS)
    elif current_turn == 2:
        return bool(words & TURN_2_KEYWORDS)
    elif current_turn >= 3:
        return bool(words & TURN_3_KEYWORDS)
    return True

def classify_user_prompt(
    query: str,
    current_turn: int = 0,
    anchor_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Intermediate classifier determining whether a prompt is:
    - EMPTY
    - RESET
    - OFF_TOPIC (Step 0 Guardrail)
    - GREETING
    - QUESTION / META (Questions about the bot or where it's from)
    - VAGUE (Gibberish / single non-answers / unrelated to turn topic)
    - GAME_ANCHOR (Turn 0 game seed)
    - VALID_ANSWER (Turns 1-3 calibration answer)
    """
    clean = query.strip()
    clean_lower = clean.lower()
    words = re.findall(r"\b[a-zA-Z0-9_\-']+\b", clean_lower)

    # 1. Empty check
    if not clean or not words:
        return {
            "type": "EMPTY",
            "message": "Please enter a message to begin."
        }

    # 2. Reset check
    if clean_lower in {"reset", "restart", "start over", "clear", "/reset"}:
        return {
            "type": "RESET",
            "message": "Session reset. Enter any video game title or franchise to begin scouting."
        }

    # 3. Off-Topic Check (Step 0 Guardrail)
    for pattern in OFF_TOPIC_PATTERNS:
        if re.search(pattern, clean_lower):
            return {
                "type": "OFF_TOPIC",
                "message": "⚠️ **Domain Guardrail**: I am strictly a Video Game Cultural Intelligence agent. Please provide a video game title, franchise, or gaming preference to begin."
            }

    # 4. Greeting Check (e.g. 'hi', 'hello', 'hey', 'no hi')
    is_greeting = clean_lower in GREETING_WORDS or (len(words) <= 2 and any(w in GREETING_WORDS for w in words))
    if is_greeting:
        if current_turn == 0:
            return {
                "type": "GREETING",
                "message": (
                    "Hey there! 👋 I am the **Qloo Videogame Cultural Intelligence Agent**.\n\n"
                    "I scout recommendations using Qloo's 250M+ taste graph without guessing or generic clichés. "
                    "Tell me a video game you love (e.g. **Elden Ring**, **Cyberpunk 2077**, **Hades**, or **DOOM**) to begin!"
                )
            }
        else:
            return {
                "type": "GREETING_IN_LOOP",
                "message": (
                    f"Hello! We're currently in the middle of calibrating your taste for **{anchor_name or 'your game'}**.\n"
                    "Please answer the question above or click one of the options to continue!"
                )
            }

    # 5. Question or Conversational Remark (e.g. 'where are you from', 'you are gaming bot right', 'who are you')
    if is_conversational_or_question(clean_lower):
        if "where are you from" in clean_lower or "where do you live" in clean_lower:
            reply = "I'm an AI agent built for the **Qloo Hackathon**, running locally and powered by Qloo's global Cultural Taste Graph (250M+ entities)!"
        elif "bot" in clean_lower or "who are you" in clean_lower or "what are you" in clean_lower:
            reply = "Yes, I am the **Qloo Videogame Cultural Intelligence Agent**! I specialize strictly in gaming cultural correlation (`urn:entity:videogame`)."
        else:
            reply = "I'm your Qloo cultural gaming agent. I map your gameplay mechanics and aesthetic taste against Qloo's 250M+ entity graph."

        if current_turn == 0:
            return {
                "type": "META",
                "message": f"{reply}\n\nTo start scouting, tell me a video game you enjoy (e.g. **Elden Ring**, **Cyberpunk 2077**, **Hades**, **DOOM**)!"
            }
        else:
            return {
                "type": "META_IN_LOOP",
                "message": f"{reply}\n\nWe're currently in Step {current_turn} calibrating your preferences for **{anchor_name or 'your game'}**."
            }

    # 5.5 Genre Scouting at Turn 0 (e.g. 'fpp games', 'suggest horror games', 'rpg')
    if current_turn == 0:
        for genre_key, genre_info in GENRE_SCOUT_MAP.items():
            pattern = rf"\b{re.escape(genre_key)}\b"
            if re.search(pattern, clean_lower):
                genre_intent = any(w in clean_lower for w in ["game", "games", "suggest", "recommend", "looking for", "best", "some", "interested in", "like"]) or len(words) <= 3
                if genre_intent:
                    return {
                        "type": "GENRE_SCOUT",
                        "label": genre_info["label"],
                        "anchors": genre_info["anchors"],
                        "message": (
                            f"You're exploring **{genre_info['label']}**!\n\n"
                            "To calibrate Qloo's taste graph, pick an anchor game below or name your favorite:"
                        )
                    }

    # 6. Calibration Step Validation (Turns 1, 2, 3)
    if current_turn > 0:
        # Check if vague response ('yes', 'no', 'give', 'f', 'ps7')
        is_vague = clean_lower in VAGUE_RESPONSES or len(clean) < 2
        is_relevant = check_turn_keyword_relevance(clean_lower, current_turn)

        if is_vague or not is_relevant:
            step_hints = {
                1: "Please choose your preferred gameplay focus (e.g. tight combat mechanics vs environmental lore).",
                2: "Please choose your preferred visual art style (e.g. gritty 3D Gothic realism vs stylized indie worlds).",
                3: "Please choose your platform (PC, PS5, Xbox, Switch) and campaign length (15-25h vs 80+h open world)."
            }
            hint = step_hints.get(current_turn, "Please choose one of the options above.")
            return {
                "type": "VAGUE",
                "message": f"Could you be a bit more specific? {hint}"
            }

    # 7. Valid Turn 0 Game Anchor
    if current_turn == 0:
        cleaned_title = extract_game_title(clean)
        return {
            "type": "GAME_ANCHOR",
            "title": cleaned_title
        }

    # 8. Valid Turn 1-3 Calibration Answer
    return {
        "type": "VALID_ANSWER",
        "answer": clean
    }

def check_guardrail(query: str) -> Tuple[bool, Optional[str]]:
    res = classify_user_prompt(query, current_turn=0)
    if res["type"] == "OFF_TOPIC":
        return False, res["message"]
    return True, None
