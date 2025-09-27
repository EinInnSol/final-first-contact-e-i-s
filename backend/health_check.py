"""
Health check endpoints for First Contact EIS
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as redis
import httpx

from app.database import get_db
from app.schemas import HealthResponse, ServiceStatus

logger = logging.getLogger(__name__)

health_check_router = APIRouter()

async def check_database(db: AsyncSession) -> ServiceStatus:
    """Check database connectivity"""
    try:
        result = await db.execute(text("SELECT 1"))
        result.fetchone()
        return ServiceStatus(status="healthy", response_time_ms=0)
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return ServiceStatus(status="unhealthy", response_time_ms=0, error=str(e))

async def check_redis() -> ServiceStatus:
    """Check Redis connectivity"""
    try:
        start_time = datetime.utcnow()
        redis_client = redis.from_url("redis://localhost:6379")
        await redis_client.ping()
        response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        await redis_client.close()
        return ServiceStatus(status="healthy", response_time_ms=response_time)
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return ServiceStatus(status="unhealthy", response_time_ms=0, error=str(e))

async def check_ai_service() -> ServiceStatus:
    """Check AI service connectivity"""
    try:
        start_time = datetime.utcnow()
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/v1/ai/health", timeout=5.0)
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            if response.status_code == 200:
                return ServiceStatus(status="healthy", response_time_ms=response_time)
            else:
                return ServiceStatus(status="unhealthy", response_time_ms=response_time, error=f"HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"AI service health check failed: {e}")
        return ServiceStatus(status="unhealthy", response_time_ms=0, error=str(e))

@health_check_router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """Comprehensive health check endpoint"""
    start_time = datetime.utcnow()
    
    # Run health checks in parallel
    db_status, redis_status, ai_status = await asyncio.gather(
        check_database(db),
        check_redis(),
        check_ai_service(),
        return_exceptions=True
    )
    
    # Handle exceptions
    if isinstance(db_status, Exception):
        db_status = ServiceStatus(status="unhealthy", response_time_ms=0, error=str(db_status))
    if isinstance(redis_status, Exception):
        redis_status = ServiceStatus(status="unhealthy", response_time_ms=0, error=str(redis_status))
    if isinstance(ai_status, Exception):
        ai_status = ServiceStatus(status="unhealthy", response_time_ms=0, error=str(ai_status))
    
    # Determine overall health
    overall_status = "healthy"
    if any(service.status == "unhealthy" for service in [db_status, redis_status, ai_status]):
        overall_status = "unhealthy"
    
    response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    
    return HealthResponse(
        status=overall_status,
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        response_time_ms=response_time,
        services={
            "database": db_status,
            "redis": redis_status,
            "ai_service": ai_status
        }
    )

@health_check_router.get("/health/ready", response_model=Dict[str, Any])
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Readiness check for Kubernetes"""
    try:
        # Check if database is ready
        await db.execute(text("SELECT 1"))
        
        # Check if Redis is ready
        redis_client = redis.from_url("redis://localhost:6379")
        await redis_client.ping()
        await redis_client.close()
        
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")

@health_check_router.get("/health/live", response_model=Dict[str, Any])
async def liveness_check():
    """Liveness check for Kubernetes"""
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
