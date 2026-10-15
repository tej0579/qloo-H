import time
from fastapi import APIRouter
from app.core.config import settings
from app.services.qloo_client import qloo_client
from app.models.schemas_api import HealthResponse

router = APIRouter(tags=["System"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Readiness and liveness probe verifying Qloo API connectivity and latency.
    """
    qloo_status = await qloo_client.health_check()
    return HealthResponse(
        status="healthy",
        qloo_connected=qloo_status.get("connected", False),
        qloo_latency_ms=qloo_status.get("latency_ms"),
        environment=settings.ENVIRONMENT,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )
