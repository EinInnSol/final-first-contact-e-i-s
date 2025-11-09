"""
First Contact E.I.S. - Orchestration API Routes
Exposes the Brain's functionality via REST API

Author: Claude (CTO, EINHARJER INNOVATIVE SOLUTIONS LLC)
Date: November 7, 2025
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime
import logging
import asyncio

from ..database import get_db
from ..services.orchestrator import OrchestrationEngine, Event
from ..services.executor import ExecutionService
from ..services.event_listener import EventListenerService

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory storage for demo (replace with Firestore in production)
recommendations_store: Dict[str, Dict[str, Any]] = {}


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

@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations():
    """
    Get all recommendations
    
    Returns list of pending, executing, and completed recommendations
    """
    try:
        # Return recommendations from in-memory store
        recommendations = list(recommendations_store.values())
        
        # Sort by created_at (newest first)
        recommendations.sort(key=lambda x: x['created_at'], reverse=True)
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


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
        
        # Create response
        response = RecommendationResponse(
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
        
        # Store recommendation with execution plan for later approval
        recommendations_store[recommendation.recommendation_id] = {
            **response.dict(),
            "execution_plan": recommendation.execution_plan  # Store plan for execution
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error triggering event: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommendations/{recommendation_id}/approve", response_model=ExecutionResultResponse)
async def approve_recommendation(
    recommendation_id: str,
    request: ApproveRecommendationRequest,
    background_tasks: BackgroundTasks,
    executor = Depends(get_executor)
):
    """
    Approve a recommendation and execute the plan
    
    This is the caseworker's one-click approval
    """
    try:
        # Get recommendation from store
        if recommendation_id not in recommendations_store:
            raise HTTPException(
                status_code=404,
                detail=f"Recommendation {recommendation_id} not found"
            )
        
        stored_rec = recommendations_store[recommendation_id]
        
        # Update status to executing
        stored_rec['status'] = 'executing'
        
        # Get execution plan
        execution_plan = stored_rec.get('execution_plan')
        if not execution_plan:
            raise HTTPException(
                status_code=400,
                detail="No execution plan found for this recommendation"
            )
        
        # Execute in background
        async def execute_and_update():
            try:
                # Execute the plan
                result = await executor.execute_plan(execution_plan, request.approved_by)
                
                # Update status based on result
                if result.status == "success":
                    stored_rec['status'] = 'completed'
                elif result.status == "failed":
                    stored_rec['status'] = 'failed'
                else:
                    stored_rec['status'] = 'partial_success'
                    
                logger.info(f"Recommendation {recommendation_id} execution completed: {result.status}")
                
            except Exception as e:
                logger.error(f"Error executing recommendation: {e}", exc_info=True)
                stored_rec['status'] = 'failed'
        
        # Start execution in background
        background_tasks.add_task(execute_and_update)
        
        # Return immediate response
        return ExecutionResultResponse(
            plan_id=execution_plan.plan_id,
            status="executing",
            actions_completed=0,
            actions_failed=0,
            total_duration_seconds=0,
            rollback_performed=False
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving recommendation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recommendations/{recommendation_id}/reject")
async def reject_recommendation(
    recommendation_id: str
):
    """
    Reject a recommendation
    """
    try:
        if recommendation_id not in recommendations_store:
            raise HTTPException(
                status_code=404,
                detail=f"Recommendation {recommendation_id} not found"
            )
        
        # Update status
        recommendations_store[recommendation_id]['status'] = 'rejected'
        
        return {"status": "rejected", "recommendation_id": recommendation_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rejecting recommendation: {e}", exc_info=True)
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
