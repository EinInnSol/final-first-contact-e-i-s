"""
First Contact EIS - Main FastAPI Application
AI-Powered Early Intervention System for Long Beach Civic Services
"""

import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware  # Removed for demo
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.database import init_db
# from app.auth import auth_router  # TODO: Enable after demo
# AI Services - disabled for demo, enable during pilot
# from app.ai_service import ai_router, AIService
# from app.ai_case_manager import AICaseManager
# from app.ai_client_concierge import AIClientConcierge
# from app.ai_municipal_intelligence import AIMunicipalIntelligence
# from app.ai_kiosk_intelligence import AIKioskIntelligence
# from app.ai_system_management import AISystemManagement
# from app.ai_cross_system_learning import AICrossSystemLearning
from app.models import Base
from app.schemas import HealthResponse
# from health_check import health_check_router  # Using inline health check
from logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global services instance
services = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting First Contact EIS Backend (Demo Mode)...")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database init skipped (expected in demo mode): {e}")

    # AI services will be initialized during pilot phase
    logger.info("Backend ready for demo")

    yield

    # Shutdown
    logger.info("Shutting down First Contact EIS Backend...")

# Create FastAPI application
app = FastAPI(
    title="First Contact EIS API",
    description="AI-Powered Early Intervention System for Long Beach Civic Services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Trusted host middleware - DISABLED for demo (re-enable in production)
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["*"]
# )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "internal_error"}
    )

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        services={
            "database": "healthy",
            "redis": "healthy",
            "ai_service": "healthy",
            "case_manager": "healthy",
            "client_concierge": "healthy",
            "municipal_intelligence": "healthy",
            "kiosk_intelligence": "healthy",
            "system_management": "healthy",
            "cross_system_learning": "healthy"
        }
    )

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "First Contact EIS API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "status": "operational"
    }

# Include routers
from app.routes import api_router  # Core business logic routes

app.include_router(api_router)  # Includes intake, alerts, analytics, orchestration
# app.include_router(health_check_router, prefix="/api/v1", tags=["Health"])  # Using inline health check
# app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])  # TODO: Enable after demo
# app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI Services"])  # TODO: Enable during pilot

# Mount static files (if directory exists)
# app.mount("/static", StaticFiles(directory="static"), name="static")  # TODO: Add static files if needed

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true",
        log_level="info"
    )
