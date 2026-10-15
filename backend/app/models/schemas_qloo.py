from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class QlooTag(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    weight: Optional[float] = None

class QlooAddress(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    formatted: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class QlooEntity(BaseModel):
    entity_id: str = Field(..., alias="id", description="Unique Qloo UUID")
    name: str = Field(..., description="Display name of the entity")
    types: List[str] = Field(default_factory=list, description="Array of category URNs")
    subtype: Optional[str] = None
    popularity: Optional[float] = None
    affinity_score: Optional[float] = Field(default=None, alias="affinity")
    tags: List[Union[QlooTag, str, Dict[str, Any]]] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        populate_by_name = True

    def normalized_tags(self) -> List[str]:
        cleaned = []
        for tag in self.tags:
            if isinstance(tag, str):
                cleaned.append(tag)
            elif isinstance(tag, dict):
                cleaned.append(tag.get("name") or tag.get("id") or str(tag))
            elif isinstance(tag, QlooTag) and tag.name:
                cleaned.append(tag.name)
        return cleaned[:5]

    def formatted_address(self) -> Optional[str]:
        if "address" in self.properties:
            addr = self.properties["address"]
            if isinstance(addr, str):
                return addr
            if isinstance(addr, dict):
                parts = [addr.get("street"), addr.get("city"), addr.get("state")]
                return ", ".join([p for p in parts if p])
        return None

class QlooSearchResponse(BaseModel):
    results: List[QlooEntity] = Field(default_factory=list)

class QlooInsightsResponse(BaseModel):
    entities: List[QlooEntity] = Field(default_factory=list)
    count: Optional[int] = None
