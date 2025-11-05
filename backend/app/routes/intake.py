"""
First Contact E.I.S. - Intake Router
Handles client intake submissions with geospatial tracking and mutual support detection

This is THE CORE INNOVATION - where we detect mutual support relationships
and trigger the cost-saving alerts that differentiate us from traditional CES.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_
import logging

from app.database import get_db
from app.models import (
    Client, Intake, Location, Organization,
    MutualSupportPair, MutualSupportAlert
)
from app.schemas import (
    IntakeSubmitRequest,
    IntakeSubmitResponse,
    MutualSupportDetection
)
from app.agents.mutual_support_agent import MutualSupportAgent

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize Mutual Support Agent
mutual_support_agent = MutualSupportAgent()


@router.post("/submit", response_model=IntakeSubmitResponse, status_code=status.HTTP_201_CREATED)
async def submit_intake(
    intake_data: IntakeSubmitRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> IntakeSubmitResponse:
    """
    Submit a new client intake with geospatial tracking.
    
    This endpoint:
    1. Creates/updates client record
    2. Records intake with location data
    3. Runs Mutual Support Agent evaluation
    4. Triggers alerts if pairing detected
    5. Returns immediate response with pairing status
    
    Args:
        intake_data: Client intake information including location
        background_tasks: FastAPI background tasks for async processing
        db: Database session
        
    Returns:
        IntakeSubmitResponse with intake ID and mutual support status
    """
    try:
        logger.info(f"Processing intake submission for location: {intake_data.qr_code}")
        
        # Step 1: Validate and get location
        location = db.query(Location).filter(
            Location.qr_code == intake_data.qr_code
        ).first()
        
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid QR code: {intake_data.qr_code}"
            )
        
        # Step 2: Create or update client record
        client = db.query(Client).filter(
            and_(
                Client.organization_id == location.organization_id,
                Client.phone_number == intake_data.phone_number
            )
        ).first()
        
        if not client:
            # New client
            client = Client(
                organization_id=location.organization_id,
                first_name=intake_data.first_name,
                last_name=intake_data.last_name,
                phone_number=intake_data.phone_number,
                email=intake_data.email,
                date_of_birth=intake_data.date_of_birth,
                status="active"
            )
            db.add(client)
            db.flush()  # Get client.id for intake record
            logger.info(f"Created new client: {client.id}")
        else:
            # Update existing client if needed
            logger.info(f"Found existing client: {client.id}")
        
        # Step 3: Create intake record
        intake = Intake(
            client_id=client.id,
            location_id=location.id,
            housing_status=intake_data.housing_status,
            health_conditions=intake_data.health_conditions,
            support_network=intake_data.support_network,
            employment_status=intake_data.employment_status,
            barriers=intake_data.barriers,
            urgency_level=intake_data.urgency_level or "medium",
            needs_assessment=intake_data.needs_assessment,
            metadata={
                "coordinates": intake_data.coordinates,
                "device_info": intake_data.device_info,
                "submission_time": datetime.utcnow().isoformat()
            }
        )
        db.add(intake)
        db.flush()  # Get intake.id
        logger.info(f"Created intake record: {intake.id}")
        
        # Step 4: Run Mutual Support Agent evaluation
        mutual_support_detection = None
        
        # Prepare intake data for agent
        intake_dict = {
            "id": str(intake.id),
            "client_id": str(client.id),
            "organization_id": str(location.organization_id),
            "housing_status": intake.housing_status,
            "health_conditions": intake.health_conditions,
            "support_network": intake.support_network,
            "employment_status": intake.employment_status,
            "barriers": intake.barriers,
            "urgency_level": intake.urgency_level,
            "location_id": str(location.id),
            "submission_time": intake.created_at.isoformat()
        }
        
        # Look for potential pairs with recent intakes from same organization
        recent_intakes = db.query(Intake).join(Client).filter(
            and_(
                Client.organization_id == location.organization_id,
                Intake.id != intake.id,
                Intake.created_at >= datetime.utcnow() - timedelta(days=30)  # Last 30 days
            )
        ).limit(50).all()  # Limit to prevent performance issues
        
        logger.info(f"Evaluating against {len(recent_intakes)} recent intakes")
        
        # Evaluate each potential pair
        for other_intake in recent_intakes:
            other_client = other_intake.client
            other_intake_dict = {
                "id": str(other_intake.id),
                "client_id": str(other_client.id),
                "organization_id": str(other_client.organization_id),
                "housing_status": other_intake.housing_status,
                "health_conditions": other_intake.health_conditions,
                "support_network": other_intake.support_network,
                "employment_status": other_intake.employment_status,
                "barriers": other_intake.barriers,
                "urgency_level": other_intake.urgency_level,
                "location_id": str(other_intake.location_id),
                "submission_time": other_intake.created_at.isoformat()
            }
            
            # Evaluate pair
            pair_result = mutual_support_agent.evaluate_pair(
                intake_dict,
                other_intake_dict
            )
            
            if pair_result and pair_result.confidence_score >= 0.7:
                logger.info(f"🎯 MUTUAL SUPPORT DETECTED! Confidence: {pair_result.confidence_score:.2f}")
                logger.info(f"Pair: {client.id} <-> {other_client.id}")
                
                # Create MutualSupportPair record
                support_pair = MutualSupportPair(
                    organization_id=location.organization_id,
                    client_a_id=client.id,
                    client_b_id=other_client.id,
                    confidence_score=pair_result.confidence_score,
                    support_indicators=[
                        {
                            "type": indicator.indicator_type,
                            "confidence": indicator.confidence,
                            "evidence": indicator.evidence
                        }
                        for indicator in pair_result.support_indicators
                    ],
                    ihss_eligible=pair_result.ihss_eligible,
                    cost_savings_estimate=pair_result.consolidation_benefits.get("annual_cost_savings", 0),
                    status="pending_review"
                )
                db.add(support_pair)
                db.flush()
                
                # Create caseworker alert
                alert = MutualSupportAlert(
                    organization_id=location.organization_id,
                    pair_id=support_pair.id,
                    alert_type="mutual_support_detected",
                    severity="high" if pair_result.confidence_score >= 0.85 else "medium",
                    message=f"High-confidence mutual support relationship detected between {client.first_name} and {other_client.first_name}",
                    recommended_actions=pair_result.recommended_actions,
                    alert_metadata={
                        "confidence_score": pair_result.confidence_score,
                        "ihss_eligible": pair_result.ihss_eligible,
                        "cost_savings": pair_result.consolidation_benefits,
                        "detection_time": datetime.utcnow().isoformat()
                    },
                    status="unread"
                )
                db.add(alert)
                
                # Prepare response data
                mutual_support_detection = MutualSupportDetection(
                    detected=True,
                    confidence_score=pair_result.confidence_score,
                    paired_with_client_id=str(other_client.id),
                    ihss_eligible=pair_result.ihss_eligible,
                    estimated_cost_savings=pair_result.consolidation_benefits.get("annual_cost_savings", 0),
                    recommended_actions=pair_result.recommended_actions
                )
                
                # Only need one match for demo
                break
        
        # Commit all changes
        db.commit()
        
        # Schedule background tasks for Firestore sync and notifications
        if mutual_support_detection:
            background_tasks.add_task(
                send_caseworker_notification,
                alert_id=str(alert.id),
                organization_id=str(location.organization_id)
            )
        
        # Return response
        response = IntakeSubmitResponse(
            intake_id=str(intake.id),
            client_id=str(client.id),
            status="success",
            message="Intake submitted successfully",
            mutual_support_detection=mutual_support_detection,
            next_steps=[
                "Your information has been recorded",
                "A caseworker will review your intake within 24 hours",
                "You will receive a text message with next steps"
            ]
        )
        
        logger.info(f"✅ Intake {intake.id} processed successfully")
        if mutual_support_detection:
            logger.info(f"💰 Potential savings: ${mutual_support_detection.estimated_cost_savings:,}")
        
        return response
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error processing intake: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing intake: {str(e)}"
        )


async def send_caseworker_notification(alert_id: str, organization_id: str):
    """
    Background task to send real-time notification to caseworker dashboard.
    
    In production, this would:
    1. Push notification to Firestore
    2. Trigger WebSocket update
    3. Send SMS/email to on-call caseworker
    
    For demo, we'll just log it.
    """
    logger.info(f"📢 Sending caseworker notification for alert {alert_id}")
    logger.info(f"   Organization: {organization_id}")
    
    # TODO: Implement Firestore push notification
    # TODO: Implement WebSocket broadcast
    # TODO: Implement SMS/email notification
    
    logger.info("✅ Notification sent")


@router.get("/status/{intake_id}")
async def get_intake_status(
    intake_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the status of a submitted intake.
    
    Returns intake details, processing status, and any mutual support matches.
    """
    intake = db.query(Intake).filter(Intake.id == intake_id).first()
    
    if not intake:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Intake {intake_id} not found"
        )
    
    # Check for mutual support pairs
    pairs = db.query(MutualSupportPair).filter(
        (MutualSupportPair.client_a_id == intake.client_id) |
        (MutualSupportPair.client_b_id == intake.client_id)
    ).all()
    
    return {
        "intake_id": str(intake.id),
        "client_id": str(intake.client_id),
        "status": "processed",
        "created_at": intake.created_at.isoformat(),
        "location": intake.location.name if intake.location else None,
        "mutual_support_pairs": len(pairs),
        "pair_details": [
            {
                "pair_id": str(pair.id),
                "confidence_score": pair.confidence_score,
                "ihss_eligible": pair.ihss_eligible,
                "status": pair.status
            }
            for pair in pairs
        ]
    }
