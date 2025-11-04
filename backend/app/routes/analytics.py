"""
First Contact E.I.S. - Analytics Router
Provides data for city dashboards, heat maps, and ROI tracking
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import logging

from app.database import get_db
from app.models import (
    Intake, Location, MutualSupportPair,
    Client, Organization
)
from app.schemas import (
    GeospatialAnalytics,
    LocationHeatMapData,
    CostSavingsAnalytics,
    IntakeVolumeTrends
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/heatmap", response_model=List[LocationHeatMapData])
async def get_location_heatmap(
    organization_id: str,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
) -> List[LocationHeatMapData]:
    """
    Get geographic heat map data for intake locations.
    
    Shows where people are accessing services, enabling data-driven
    decisions about resource deployment.
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Aggregate intakes by location
        location_stats = db.query(
            Location.id,
            Location.name,
            Location.address,
            Location.latitude,
            Location.longitude,
            Location.qr_code,
            func.count(Intake.id).label('intake_count'),
            func.count(func.distinct(Intake.client_id)).label('unique_clients')
        ).join(
            Intake, Intake.location_id == Location.id
        ).filter(
            and_(
                Location.organization_id == organization_id,
                Intake.created_at >= cutoff_date
            )
        ).group_by(
            Location.id
        ).all()
        
        # Calculate mutual support pairs per location
        heatmap_data = []
        for stat in location_stats:
            # Count pairs detected at this location
            pairs_count = db.query(func.count(MutualSupportPair.id)).join(
                Intake, or_(
                    Intake.client_id == MutualSupportPair.client_a_id,
                    Intake.client_id == MutualSupportPair.client_b_id
                )
            ).filter(
                and_(
                    Intake.location_id == stat.id,
                    MutualSupportPair.created_at >= cutoff_date
                )
            ).scalar()
            
            # Calculate pairing rate
            pairing_rate = (pairs_count * 2 / stat.intake_count * 100) if stat.intake_count > 0 else 0
            
            heatmap_data.append(LocationHeatMapData(
                location_id=str(stat.id),
                location_name=stat.name,
                address=stat.address,
                latitude=stat.latitude,
                longitude=stat.longitude,
                qr_code=stat.qr_code,
                intake_count=stat.intake_count,
                unique_clients=stat.unique_clients,
                pairs_detected=pairs_count,
                pairing_rate=round(pairing_rate, 1)
            ))
        
        return heatmap_data
        
    except Exception as e:
        logger.error(f"Error generating heatmap: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating heatmap: {str(e)}"
        )


@router.get("/cost-savings", response_model=CostSavingsAnalytics)
async def get_cost_savings_analytics(
    organization_id: str,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
) -> CostSavingsAnalytics:
    """
    Calculate ROI and cost savings from mutual support pairs.
    
    THIS IS THE MONEY SHOT for city administrators - shows
    tangible financial impact of the system.
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all pairs in period
        pairs = db.query(MutualSupportPair).filter(
            and_(
                MutualSupportPair.organization_id == organization_id,
                MutualSupportPair.created_at >= cutoff_date
            )
        ).all()
        
        # Calculate totals
        total_pairs = len(pairs)
        total_cost_savings = sum(pair.cost_savings_estimate or 0 for pair in pairs)
        ihss_eligible_pairs = sum(1 for pair in pairs if pair.ihss_eligible)
        
        # Estimate annual projections
        days_elapsed = (datetime.utcnow() - cutoff_date).days
        annual_projection = (total_cost_savings / days_elapsed) * 365 if days_elapsed > 0 else 0
        
        # Calculate traditional cost (separate case management)
        # Avg cost per client: $45K/year, so $90K for separated pair
        traditional_cost = total_pairs * 90000
        our_cost = total_pairs * 42000  # Paired cost
        actual_savings = traditional_cost - our_cost
        
        return CostSavingsAnalytics(
            total_pairs_detected=total_pairs,
            ihss_eligible_pairs=ihss_eligible_pairs,
            total_estimated_savings=int(total_cost_savings),
            annual_projection=int(annual_projection),
            traditional_cost=traditional_cost,
            paired_cost=our_cost,
            savings_percentage=round((actual_savings / traditional_cost * 100) if traditional_cost > 0 else 0, 1),
            period_days=days
        )
        
    except Exception as e:
        logger.error(f"Error calculating cost savings: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating cost savings: {str(e)}"
        )


@router.get("/volume-trends", response_model=IntakeVolumeTrends)
async def get_intake_volume_trends(
    organization_id: str,
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db)
) -> IntakeVolumeTrends:
    """
    Get intake volume trends over time.
    
    Shows system adoption and usage patterns.
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily intake counts
        daily_intakes = db.query(
            func.date(Intake.created_at).label('date'),
            func.count(Intake.id).label('count')
        ).join(
            Client, Client.id == Intake.client_id
        ).filter(
            and_(
                Client.organization_id == organization_id,
                Intake.created_at >= cutoff_date
            )
        ).group_by(
            func.date(Intake.created_at)
        ).order_by(
            func.date(Intake.created_at)
        ).all()
        
        # Format for charting
        dates = [day.date.isoformat() for day in daily_intakes]
        counts = [day.count for day in daily_intakes]
        
        # Calculate statistics
        total_intakes = sum(counts)
        avg_daily = total_intakes / len(counts) if counts else 0
        peak_day = max(counts) if counts else 0
        
        return IntakeVolumeTrends(
            dates=dates,
            intake_counts=counts,
            total_intakes=total_intakes,
            average_daily=round(avg_daily, 1),
            peak_daily=peak_day,
            period_days=days
        )
        
    except Exception as e:
        logger.error(f"Error calculating volume trends: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating volume trends: {str(e)}"
        )


@router.get("/dashboard-summary")
async def get_dashboard_summary(
    organization_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get high-level summary for city administrator dashboard.
    
    One-stop shop for key metrics.
    """
    try:
        # Last 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        # Total intakes
        total_intakes = db.query(func.count(Intake.id)).join(
            Client, Client.id == Intake.client_id
        ).filter(
            and_(
                Client.organization_id == organization_id,
                Intake.created_at >= cutoff_date
            )
        ).scalar()
        
        # Total pairs
        total_pairs = db.query(func.count(MutualSupportPair.id)).filter(
            and_(
                MutualSupportPair.organization_id == organization_id,
                MutualSupportPair.created_at >= cutoff_date
            )
        ).scalar()
        
        # Total savings
        total_savings = db.query(
            func.sum(MutualSupportPair.cost_savings_estimate)
        ).filter(
            and_(
                MutualSupportPair.organization_id == organization_id,
                MutualSupportPair.created_at >= cutoff_date
            )
        ).scalar() or 0
        
        # Active locations
        active_locations = db.query(func.count(func.distinct(Intake.location_id))).join(
            Client, Client.id == Intake.client_id
        ).filter(
            and_(
                Client.organization_id == organization_id,
                Intake.created_at >= cutoff_date
            )
        ).scalar()
        
        return {
            "period": "Last 30 days",
            "total_intakes": total_intakes,
            "total_pairs_detected": total_pairs,
            "pairing_rate": round((total_pairs * 2 / total_intakes * 100) if total_intakes > 0 else 0, 1),
            "total_cost_savings": int(total_savings),
            "active_locations": active_locations,
            "avg_savings_per_pair": int(total_savings / total_pairs) if total_pairs > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Error generating dashboard summary: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating dashboard summary: {str(e)}"
        )
