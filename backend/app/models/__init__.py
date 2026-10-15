"""
Data models and schemas for IRL LootDrop API and Qloo Integration.
"""
from .schemas_qloo import QlooEntity, QlooTag, QlooAddress, QlooSearchResponse, QlooInsightsResponse
from .schemas_api import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ClarificationQuestion,
    LootDropItem,
    LootDropCategory,
    ComparatorComparison,
    LootDropPayload,
    HealthResponse
)

__all__ = [
    "QlooEntity",
    "QlooTag",
    "QlooAddress",
    "QlooSearchResponse",
    "QlooInsightsResponse",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "ClarificationQuestion",
    "LootDropItem",
    "LootDropCategory",
    "ComparatorComparison",
    "LootDropPayload",
    "HealthResponse"
]
