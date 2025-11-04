"""
First Contact E.I.S. - API Routes
Aggregates all API routers for the FastAPI application
"""

from fastapi import APIRouter
from .intake import router as intake_router
from .alerts import router as alerts_router
from .analytics import router as analytics_router

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Include all sub-routers
api_router.include_router(intake_router, prefix="/intake", tags=["intake"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])

__all__ = ["api_router"]
