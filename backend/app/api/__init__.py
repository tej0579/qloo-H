"""
API Routers for IRL LootDrop Backend
"""
from .routes_system import router as system_router
from .routes_qloo import router as qloo_router
from .routes_agent import router as agent_router

__all__ = ["system_router", "qloo_router", "agent_router"]
