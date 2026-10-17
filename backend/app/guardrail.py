import re
from typing import Tuple, Optional

OFF_TOPIC_PATTERNS = [
    r"\b(cook|recipe|pasta|bake|pizza|baking|cooking|ingredients|cake|chocolate|food|dinner|lunch|breakfast|dessert|coffee|tea|meal)\b",
    r"\b(election|president|biden|trump|politics|democrat|republican|senate|government|vote|voting)\b",
    r"\b(weather|forecast|rain|temperature|climate|snow|humidity|storm)\b",
    r"\b(stock|crypto|bitcoin|ethereum|forex|investing|dividends|finance|shares|wallet)\b",
    r"\b(solve|math|calculus|algebra|equation|derivative|integral)\b",
    r"\b(python|javascript|write a function|debug this code|css|html|react|backend code)\b",
    r"\b(flight ticket|hotel booking|medical advice|symptoms of|disease|doctor|medicine)\b"
]

def check_guardrail(query: str) -> Tuple[bool, Optional[str]]:
    """
    Step 0 Domain Guardrail:
    Returns (is_valid, rollback_message).
    """
    clean = query.strip().lower()
    if not clean:
        return False, "Please enter a message to begin."

    for pattern in OFF_TOPIC_PATTERNS:
        if re.search(pattern, clean):
            return False, "⚠️ I am strictly a Video Game Cultural Intelligence agent. Please provide a video game title, franchise, or gaming preference to begin."

    return True, None

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
