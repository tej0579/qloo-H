from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import logger
from app.api.routes_system import router as system_router
from app.api.routes_qloo import router as qloo_router
from app.api.routes_agent import router as agent_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing IRL LootDrop API with Qloo Cultural Intelligence...")
    logger.info(f"Targeting Qloo API Base: {settings.QLOO_BASE_URL}")
    logger.info(f"Allowed CORS Origins: {settings.cors_origins_list}")
    yield
    logger.info("Shutting down IRL LootDrop API.")

app = FastAPI(
    title="IRL LootDrop API",
    description="Translating Video Games into Real-World Cultural Lifestyle via Qloo Taste Intelligence",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers under /api
app.include_router(system_router, prefix="/api")
app.include_router(qloo_router, prefix="/api")
app.include_router(agent_router, prefix="/api")

@app.get("/")
def root():
    return {
        "service": "IRL LootDrop API",
        "description": "Translates gamer virtual obsessions into real-world cultural taste profiles",
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "qloo_search": "/api/qloo/search",
            "qloo_insights": "/api/qloo/insights"
        }
    }
