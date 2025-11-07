"""
First Contact E.I.S. - Orchestration API Routes
Exposes the Brain's functionality via REST API

Author: Claude (CTO, EINHARJER INNOVATIVE SOLUTIONS LLC)
Date: November 6, 2025
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime
import logging

from ..database import get_db
from ..services.orchestrator import OrchestrationEngine, Event
from ..services.executor import ExecutionService
from ..services.event_listener import EventListenerService

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

from pydantic import BaseModel

class TriggerEventRequest(BaseModel):
    """Request to manually trigger an event (for testing/demo)"""
    event_type: str
    client_id: str = None
    provider_id: str = None
    metadata: Dict[str, Any] = {}


class RecommendationResponse(BaseModel):
    """Recommendation for caseworker approval"""
    recommendation_id: str
    summary: str
    reasoning: List[str]
    impact: Dict[str, Any]
    confidence_score: float
    actions_count: int
    estimated_duration_seconds: int
    affected_systems: List[str]
    status: str = "pending_approval"
    created_at: datetime


class ApproveRecommendationRequest(BaseModel):
    """Request to approve a recommendation"""
    approved_by: str  # User ID


class ExecutionResultResponse(BaseModel):
    """Result of executing a plan"""
    plan_id: str
    status: str
    actions_completed: int
    actions_failed: int
    total_duration_seconds: float
    rollback_performed: bool


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_orchestrator(db: Session = Depends(get_db)):
    """Get orchestrator instance"""
    # TODO: Initialize with AI service if needed
    return OrchestrationEngine(db_session=db, ai_service=None)


def get_executor(db: Session = Depends(get_db)):
    """Get executor instance"""
    # TODO: Initialize with notification service and API clients
    return ExecutionService(
        db_session=db,
        notification_service=None,
        external_api_clients={},
        demo_mode=True  # Set to True for demo
    )


def get_event_listener(
    orchestrator = Depends(get_orchestrator)
):
    """Get event listener instance"""
    return EventListenerService(
        orchestrator=orchestrator,
        firestore_client=None,
        demo_mode=True  # Set to True for demo
    )


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/trigger-event", response_model=RecommendationResponse)
async def trigger_event(
    request: TriggerEventRequest,
    event_listener = Depends(get_event_listener),
    orchestrator = Depends(get_orchestrator)
):
    """
    Manually trigger an event for testing/demo
    
    This is useful for:
    - Demo scenarios (trigger appointment cancellation)
    - Testing the orchestration engine
    - Manual coordination triggers
    """
    try:
        # Create event
        event = Event(
            event_id=f"manual_{datetime.now().timestamp()}",
            event_type=request.event_type,
            timestamp=datetime.now(),
            client_id=request.client_id,
            provider_id=request.provider_id,
            metadata=request.metadata
        )
        
        # Trigger orchestration
        recommendation = await orchestrator.handle_event(event)
        
        if not recommendation:
            raise HTTPException(
                status_code=404,
                detail="No recommendation generated for this event"
            )
        
        # Return recommendation
        return RecommendationResponse(
            recommendation_id=recommendation.recommendation_id,
            summary=recommendation.summary,
            reasoning=recommendation.reasoning,
            impact=recommendation.impact,
            confidence_score=recommendation.confidence_score,
            actions_count=len(recommendation.execution_plan.actions),
            estimated_duration_seconds=recommendation.execution_plan.estimated_duration_seconds,
            affected_systems=recommendation.execution_plan.affected_systems,
            status="pending_approval",
            created_at=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error triggering event: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommendations/{recommendation_id}/approve", response_model=ExecutionResultResponse)
async def approve_recommendation(
    recommendation_id: str,
    request: ApproveRecommendationRequest,
    background_tasks: BackgroundTasks,
    orchestrator = Depends(get_orchestrator),
    executor = Depends(get_executor)
):
    """
    Approve a recommendation and execute the plan
    
    This is the caseworker's one-click approval
    """
    try:
        # TODO: Retrieve recommendation from database/cache
        # For now, we'll need to store recommendations somewhere accessible
        
        # TODO: Get execution plan from recommendation
        # execution_plan = recommendation.execution_plan
        
        # For demo, return mock result
        raise HTTPException(
            status_code=501,
            detail="Approval endpoint needs recommendation storage implementation"
        )
        
        # Real implementation would be:
        # result = await executor.execute_plan(execution_plan, request.approved_by)
        # return ExecutionResultResponse(**result.__dict__)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving recommendation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics(
    orchestrator = Depends(get_orchestrator),
    executor = Depends(get_executor),
    event_listener = Depends(get_event_listener)
):
    """
    Get orchestration system statistics
    
    Returns metrics about:
    - Events detected and processed
    - Decisions made (rules vs AI)
    - Executions completed
    """
    return {
        "orchestrator": orchestrator.get_statistics(),
        "executor": executor.get_statistics(),
        "event_listener": event_listener.get_statistics(),
        "timestamp": datetime.now()
    }


@router.post("/webhook/{path:path}")
async def handle_webhook(
    path: str,
    payload: Dict[str, Any],
    event_listener = Depends(get_event_listener)
):
    """
    Handle incoming webhooks from external systems
    
    External systems (doctor offices, housing providers, etc.) can send
    events via webhook to trigger orchestration
    """
    try:
        webhook_path = f"/{path}"
        await event_listener.handle_webhook(webhook_path, payload)
        
        return {"status": "received", "webhook_path": webhook_path}
        
    except Exception as e:
        logger.error(f"Error handling webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
