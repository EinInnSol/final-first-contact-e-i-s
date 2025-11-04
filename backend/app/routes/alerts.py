"""
First Contact E.I.S. - Alerts Router
Handles caseworker alerts and notifications for mutual support pairs
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import logging

from app.database import get_db
from app.models import MutualSupportAlert, MutualSupportPair, Client
from app.schemas import AlertResponse, AlertListResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=AlertListResponse)
async def get_alerts(
    organization_id: str,
    status_filter: Optional[str] = Query(None, description="Filter by status: unread, read, dismissed"),
    severity: Optional[str] = Query(None, description="Filter by severity: high, medium, low"),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
) -> AlertListResponse:
    """
    Get alerts for an organization's caseworkers.
    
    Returns list of mutual support alerts with pair details.
    Caseworkers see this on their dashboard for real-time triage.
    """
    try:
        # Build query
        query = db.query(MutualSupportAlert).filter(
            MutualSupportAlert.organization_id == organization_id
        )
        
        if status_filter:
            query = query.filter(MutualSupportAlert.status == status_filter)
        
        if severity:
            query = query.filter(MutualSupportAlert.severity == severity)
        
        # Get total count
        total = query.count()
        
        # Get paginated alerts
        alerts = query.order_by(
            MutualSupportAlert.created_at.desc()
        ).limit(limit).offset(offset).all()
        
        # Build response with pair details
        alert_responses = []
        for alert in alerts:
            pair = alert.mutual_support_pair
            if pair:
                client_a = pair.client_a
                client_b = pair.client_b
                
                alert_responses.append(AlertResponse(
                    alert_id=str(alert.id),
                    pair_id=str(pair.id),
                    alert_type=alert.alert_type,
                    severity=alert.severity,
                    message=alert.message,
                    confidence_score=pair.confidence_score,
                    ihss_eligible=pair.ihss_eligible,
                    estimated_savings=pair.cost_savings_estimate,
                    client_a_name=f"{client_a.first_name} {client_a.last_name}",
                    client_b_name=f"{client_b.first_name} {client_b.last_name}",
                    recommended_actions=alert.recommended_actions,
                    status=alert.status,
                    created_at=alert.created_at,
                    read_at=alert.read_at
                ))
        
        return AlertListResponse(
            alerts=alert_responses,
            total=total,
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        logger.error(f"Error fetching alerts: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching alerts: {str(e)}"
        )


@router.patch("/{alert_id}/read")
async def mark_alert_read(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """
    Mark an alert as read by caseworker.
    """
    alert = db.query(MutualSupportAlert).filter(
        MutualSupportAlert.id == alert_id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found"
        )
    
    alert.status = "read"
    alert.read_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"Alert {alert_id} marked as read")
    
    return {"status": "success", "alert_id": alert_id}


@router.patch("/{alert_id}/dismiss")
async def dismiss_alert(
    alert_id: str,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Dismiss an alert (e.g., false positive or already addressed).
    """
    alert = db.query(MutualSupportAlert).filter(
        MutualSupportAlert.id == alert_id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found"
        )
    
    alert.status = "dismissed"
    alert.dismissed_at = datetime.utcnow()
    if reason:
        alert.metadata["dismissal_reason"] = reason
    db.commit()
    
    logger.info(f"Alert {alert_id} dismissed: {reason}")
    
    return {"status": "success", "alert_id": alert_id}


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert_detail(
    alert_id: str,
    db: Session = Depends(get_db)
) -> AlertResponse:
    """
    Get detailed information about a specific alert.
    """
    alert = db.query(MutualSupportAlert).filter(
        MutualSupportAlert.id == alert_id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found"
        )
    
    pair = alert.mutual_support_pair
    client_a = pair.client_a
    client_b = pair.client_b
    
    return AlertResponse(
        alert_id=str(alert.id),
        pair_id=str(pair.id),
        alert_type=alert.alert_type,
        severity=alert.severity,
        message=alert.message,
        confidence_score=pair.confidence_score,
        ihss_eligible=pair.ihss_eligible,
        estimated_savings=pair.cost_savings_estimate,
        client_a_name=f"{client_a.first_name} {client_a.last_name}",
        client_b_name=f"{client_b.first_name} {client_b.last_name}",
        recommended_actions=alert.recommended_actions,
        status=alert.status,
        created_at=alert.created_at,
        read_at=alert.read_at
    )
