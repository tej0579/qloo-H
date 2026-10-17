from typing import List, Optional, Dict, Any, Union, Literal
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str
    timestamp: Optional[str] = None

class UserGameSelection(BaseModel):
    id: str = Field(..., description="Qloo entity UUID or temporary ID")
    name: str = Field(..., description="Display title of the video game")
    types: List[str] = Field(default_factory=lambda: ["urn:entity:videogame"])
    entity_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True

class ClarificationAnswer(BaseModel):
    location: str = Field(..., description="City or metro area (e.g. 'Austin, TX' or 'Tokyo, Japan')")
    aesthetic_focus: str = Field(..., description="Wardrobe, room decor, or session audio")

class ComparatorItem(BaseModel):
    category: str
    item_name: str
    detail: str
    vibe_or_tag: str
    score: Optional[float] = None

class ComparatorComparison(BaseModel):
    dimension: str
    unassisted_llm_cliche: str
    qloo_grounded_reality: str
    why_it_matters: str
    cultural_tag_contrast: Dict[str, str] = Field(default_factory=dict)

class ComparatorPayload(BaseModel):
    unassisted_llm_response: List[ComparatorItem]
    qloo_grounded_response: List[ComparatorItem]
    comparisons: List[ComparatorComparison]
    summary_verdict: str

class RadarMetric(BaseModel):
    subject: str
    qloo_affinity: Optional[float] = None
    llm_relevance: Optional[float] = None

class LootDropItem(BaseModel):
    id: str
    name: str
    category: str
    affinity_score: Optional[float] = None
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    location: Optional[str] = None
    price_level: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)

class LootDropCategory(BaseModel):
    id: str
    display_title: str
    icon: str
    description: str
    items: List[LootDropItem] = Field(default_factory=list)

class QuestLogStep(BaseModel):
    time: str
    title: str
    recommendation: str
    description: str

class LootDropPayload(BaseModel):
    session_id: str
    seed_games: List[UserGameSelection]
    persona_title: str
    persona_description: str
    archetype_title: str = ""
    quest_log: List[QuestLogStep] = Field(default_factory=list)
    location: Optional[str] = None
    aesthetic_focus: Optional[str] = None
    categories: List[LootDropCategory] = Field(default_factory=list)
    comparator: ComparatorPayload
    radar_metrics: List[RadarMetric] = Field(default_factory=list)
    data_source: Literal["qloo_live", "demo_fallback"]
    overall_match_score: Optional[float] = None
    created_at: str

class ClarificationOption(BaseModel):
    id: str
    label: str
    description: Optional[str] = None

class ClarificationQuestion(BaseModel):
    id: str
    step: int
    title: str
    prompt: str
    options: List[ClarificationOption] = Field(default_factory=list)
    default_value: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    action: str = Field(default="SEED_GAMES", description="SEED_GAMES, CLARIFY, EXECUTE, RESET")
    games: Optional[List[UserGameSelection]] = Field(default_factory=list)
    query: Optional[str] = None
    clarification: Optional[ClarificationAnswer] = None

class ChatResponse(BaseModel):
    session_id: str
    status: str
    action: str
    message: str
    verified_games: List[UserGameSelection] = Field(default_factory=list)
    clarification_questions: Optional[List[ClarificationQuestion]] = None
    lootdrop: Optional[LootDropPayload] = None

class HealthResponse(BaseModel):
    status: str
    qloo_connected: bool
    qloo_latency_ms: Optional[float] = None
    environment: str
    timestamp: str
