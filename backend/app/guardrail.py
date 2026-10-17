import re
from typing import Dict, Any, Optional, Tuple

GREETING_WORDS = {
    "hi", "hello", "hey", "hola", "yo", "sup", "greetings", "good morning",
    "good afternoon", "good evening", "howdy", "wassup", "what's up", "whats up",
    "hey there", "hi there", "hello there"
}

META_PATTERNS = [
    r"\b(who are you|what are you|what do you do|what can you do|help|who made you|how does this work|what is this|tell me about yourself)\b",
    r"\b(who created you|are you an ai|are you a bot|what is qloo|what are you bro|who are you bro)\b"
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
    "yes", "no", "yeah", "nope", "ok", "okay", "k", "sure", "fine", "give", "tell", "show", "what", "idk", "cool", "nice", "maybe", "why"
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
    - META (Questions about the bot)
    - VAGUE (Gibberish / single non-answers during calibration)
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

    # 4. Greeting Check (e.g. 'hi', 'hello', 'hey')
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
                    f"Hey! We're currently in the middle of calibrating your taste for **{anchor_name or 'your game'}**.\n"
                    "Please answer the question above or click one of the options to continue!"
                )
            }

    # 5. Meta Questions (e.g. 'who are you bro', 'what can you do')
    for pattern in META_PATTERNS:
        if re.search(pattern, clean_lower):
            if current_turn == 0:
                return {
                    "type": "META",
                    "message": (
                        "I am an agent powered by **Qloo's Cultural Taste Graph** (250M+ entities).\n\n"
                        "Instead of relying on LLM clichés (which just recommend the same 3 famous games to everyone), "
                        "I use Qloo's mathematical correlation matrix to calibrate your gameplay mechanics, visual aesthetics, "
                        "and platform needs.\n\n"
                        "Name a video game you enjoy to start!"
                    )
                }
            else:
                return {
                    "type": "META_IN_LOOP",
                    "message": (
                        f"I'm your Qloo Cultural Intelligence Agent! We're currently in Step {current_turn} "
                        f"calibrating your taste profile for **{anchor_name or 'your game'}**.\n\n"
                        "To proceed, please select one of the options above or tell me what style you prefer."
                    )
                }

    # 6. Vague / Gibberish Check during calibration (Turn 1, 2, 3)
    if current_turn > 0:
        if clean_lower in VAGUE_RESPONSES or (len(words) == 1 and len(clean) < 4):
            return {
                "type": "VAGUE",
                "message": (
                    "Could you be a bit more specific? Please select one of the option chips above, "
                    "or describe your preference in a few words so I can query Qloo's graph accurately."
                )
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

# Backward compatibility alias
def check_guardrail(query: str) -> Tuple[bool, Optional[str]]:
    res = classify_user_prompt(query, current_turn=0)
    if res["type"] == "OFF_TOPIC":
        return False, res["message"]
    return True, None
