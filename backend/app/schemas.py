"""
Pydantic schemas for First Contact EIS API
Request/response models with validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from enum import Enum

# ============================================================================
# ENUMS (Match SQLAlchemy models)
# ============================================================================

class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    CASEWORKER = "caseworker"
    ANALYST = "analyst"
    CLIENT = "client"

class CaseStatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PAIRED = "paired"
    HOUSED = "housed"
    CLOSED = "closed"
    ESCALATED = "escalated"

class CrisisLevelEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LocationTypeEnum(str, Enum):
    KIOSK = "kiosk"
    BENCH = "bench"
    BUS_STOP = "bus_stop"
    SHELTER = "shelter"
    LIBRARY = "library"
    COMMUNITY_CENTER = "community_center"
    PARK = "park"
    MOBILE_UNIT = "mobile_unit"
    OTHER = "other"

class ServiceTypeEnum(str, Enum):
    HOUSING = "housing"
    EMPLOYMENT = "employment"
    HEALTHCARE = "healthcare"
    MENTAL_HEALTH = "mental_health"
    SUBSTANCE_ABUSE = "substance_abuse"
    DOMESTIC_VIOLENCE = "domestic_violence"
    CHILD_CARE = "child_care"
    TRANSPORTATION = "transportation"
    LEGAL = "legal"
    FINANCIAL = "financial"

# ============================================================================
# LOCATION SCHEMAS (Geospatial + QR Codes)
# ============================================================================

class LocationCreate(BaseModel):
    """Create new QR code location"""
    location_code: str = Field(..., description="Unique code like LB_MLK_042")
    display_name: str = Field(..., description="Human-readable name")
    location_type: LocationTypeEnum
    address: Optional[str] = None
    city: Optional[str] = "Long Beach"
    state: Optional[str] = "CA"
    zip_code: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    expected_monthly_scans: Optional[int] = Field(0, ge=0)
    notes: Optional[str] = None

class LocationResponse(BaseModel):
    """Location data returned to API consumers"""
    id: UUID
    organization_id: UUID
    location_code: str
    display_name: str
    location_type: LocationTypeEnum
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    qr_code_url: Optional[str]
    is_active: bool
    actual_monthly_scans: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class LocationAnalytics(BaseModel):
    """Analytics for a specific location"""
    location: LocationResponse
    total_intakes: int
    intakes_this_month: int
    mutual_support_pairs_detected: int
    mutual_support_rate: float  # Percentage
    top_services_requested: List[Dict[str, Any]]
    peak_times: List[str]  # ["7-9am", "5-7pm"]
    avg_crisis_level: str
    ai_recommendations: List[str]

# ============================================================================
# INTAKE SCHEMAS
# ============================================================================

class IntakeRequest(BaseModel):
    """Client intake form submission"""
    # Location context (from QR code)
    location_code: str = Field(..., description="QR code location identifier")
    
    # Personal info
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = "Long Beach"
    state: Optional[str] = "CA"
    zip_code: Optional[str] = None
    
    # Demographics (HUD Universal Data Elements)
    gender: Optional[str] = None
    race: Optional[List[str]] = None
    ethnicity: Optional[str] = None
    veteran_status: Optional[bool] = False
    
    # Mutual Support indicators (THE INNOVATION!)
    living_with_someone: bool = False
    provides_care_to_someone: bool = False
    receives_care_from_someone: bool = False
    shared_residence: bool = False
    assists_with_daily_activities: bool = False
    daily_care_hours: Optional[int] = Field(0, ge=0, le=24)
    
    # Service needs
    services_requested: Optional[List[ServiceTypeEnum]] = []
    crisis_level: Optional[CrisisLevelEnum] = CrisisLevelEnum.MEDIUM
    notes: Optional[str] = Field(None, max_length=2000)
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            # Remove common separators
            cleaned = v.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
            if not cleaned.isdigit() or len(cleaned) < 10:
                raise ValueError('Phone must be at least 10 digits')
        return v

class IntakeResponse(BaseModel):
    """Response after intake submission"""
    client_id: UUID
    intake_id: UUID
    case_id: UUID
    status: str = "success"
    message: str
    
    # Mutual Support detection results
    mutual_support_detected: bool = False
    mutual_support_confidence: Optional[float] = None
    estimated_savings: Optional[float] = None
    
    # Location context
    location_name: Optional[str] = None
    next_steps: List[str] = []

# ============================================================================
# MUTUAL SUPPORT PAIR SCHEMAS
# ============================================================================

class MutualSupportPairResponse(BaseModel):
    """Mutual support pair details"""
    id: UUID
    client_a_id: UUID
    client_a_name: str
    client_b_id: UUID
    client_b_name: str
    confidence_score: float
    support_indicators: List[str]
    ihss_eligible: bool
    estimated_savings: float
    status: str
    detected_at: datetime
    caseworker_reviewed: bool
    
    class Config:
        from_attributes = True

class MutualSupportEvaluation(BaseModel):
    """Evaluation result from Mutual Support Agent"""
    status: str  # "mutual_support_detected" or "no_alert"
    score: float
    client_id: Optional[UUID] = None
    support_indicators: List[str] = []
    ihss_eligible: bool = False
    estimated_savings: Optional[float] = None
    action: str  # "notify_caseworker" or "none"

# ============================================================================
# CASEWORKER ALERT SCHEMAS
# ============================================================================

class CaseworkerAlertResponse(BaseModel):
    """Alert displayed to caseworker"""
    id: UUID
    alert_type: str
    priority: str
    title: str
    message: str
    client_id: Optional[UUID]
    case_id: Optional[UUID]
    mutual_support_pair_id: Optional[UUID]
    location_id: Optional[UUID]
    location_name: Optional[str] = None
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# ANALYTICS SCHEMAS (City Dashboard)
# ============================================================================

class GeospatialHeatmapPoint(BaseModel):
    """Single point on heat map"""
    latitude: float
    longitude: float
    weight: int  # Number of intakes
    location_name: str
    location_code: str

class CityAnalyticsSummary(BaseModel):
    """High-level city metrics"""
    total_intakes: int
    intakes_this_month: int
    mutual_support_pairs_detected: int
    estimated_total_savings: float
    active_locations: int
    avg_crisis_level: str
    top_services_requested: List[Dict[str, Any]]
    
class CityAnalyticsGeospatial(BaseModel):
    """Geospatial analytics for city dashboard"""
    heatmap_points: List[GeospatialHeatmapPoint]
    location_rankings: List[LocationAnalytics]
    trend_analysis: Dict[str, Any]
    ai_recommendations: List[str]

# ============================================================================
# QR CODE GENERATION
# ============================================================================

class QRCodeRequest(BaseModel):
    """Generate QR code for a location"""
    location_code: str
    size: Optional[int] = Field(300, ge=100, le=1000)  # Pixels
    format: Optional[str] = Field("PNG", pattern="^(PNG|SVG)$")

class QRCodeResponse(BaseModel):
    """Generated QR code details"""
    location_code: str
    qr_code_url: str  # URL that QR code points to
    qr_code_image_url: str  # PNG/SVG image download link
    display_name: str
    location_type: str
    instructions: str = "Scan this code to connect with services"

# ============================================================================
# HEALTH CHECK
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    timestamp: str
    services: Dict[str, str] = {}

# ============================================================================
# ERROR RESPONSES
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
