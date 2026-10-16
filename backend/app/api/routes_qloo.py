from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, HTTPException
from app.services.qloo_client import qloo_client
from app.core.constants import QlooEntityType

router = APIRouter(prefix="/qloo", tags=["Qloo Proxy & Inspection"])

@router.get("/search")
async def proxy_search(
    query: str = Query(..., min_length=1, description="Entity title or search query"),
    limit: int = Query(10, ge=1, le=25, description="Max results to return"),
    entity_type: Optional[str] = Query(None, description="Optional filter URN e.g. urn:entity:videogame")
):
    """
    Direct proxy to Qloo /search with type filtering and normalization.
    Used for frontend search autocomplete.
    """
    results = await qloo_client.search(query=query, limit=limit, entity_type=entity_type)
    return {"results": results, "count": len(results)}

@router.get("/insights")
async def proxy_insights(
    seeds: str = Query(..., description="Comma-separated Qloo entity UUIDs"),
    filter_type: str = Query(..., description="Target category URN (e.g. urn:entity:brand)"),
    location: Optional[str] = Query(None, description="City filter for place queries"),
    take: int = Query(5, ge=1, le=20)
):
    """
    Direct proxy to Qloo /v2/insights for debugging or manual exploration.
    """
    seed_list = [s.strip() for s in seeds.split(",") if s.strip()]
    if not seed_list:
        raise HTTPException(status_code=400, detail="At least one seed entity UUID required.")

    result = await qloo_client.get_insights(
        seed_entity_ids=seed_list,
        filter_type=filter_type,
        location_query=location,
        take=take
    )
    entities = result["entities"]
    return {"entities": entities, "count": len(entities), "data_source": result["data_source"]}
