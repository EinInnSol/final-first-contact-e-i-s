"""
Pydantic schemas for First Contact EIS
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum

# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    CASEWORKER = "caseworker"
    SUPERVISOR = "supervisor"
    ANALYST = "analyst"
    CLIENT = "client"

class CaseStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    ESCALATED = "escalated"

class CrisisLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ServiceType(str, Enum):
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

class LanguageCode(str, Enum):
    EN = "en"
    ES = "es"
    KM = "km"
    TL = "tl"
    KO = "ko"

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        use_enum_values = True

# Health check schemas
class ServiceStatus(BaseModel):
    status: str
    response_time_ms: float
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    response_time_ms: Optional[float] = None
    services: Dict[str, ServiceStatus]

# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: str
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseSchema):
    username: str
    password: str

class Token(BaseSchema):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseSchema):
    username: Optional[str] = None

# Client schemas
class ClientBase(BaseSchema):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    preferred_language: LanguageCode = LanguageCode.EN
    is_homeless: bool = False
    is_veteran: bool = False
    is_domestic_violence_survivor: bool = False
    has_children: bool = False
    number_of_children: int = 0

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    preferred_language: Optional[LanguageCode] = None
    is_homeless: Optional[bool] = None
    is_veteran: Optional[bool] = None
    is_domestic_violence_survivor: Optional[bool] = None
    has_children: Optional[bool] = None
    number_of_children: Optional[int] = None

class Client(ClientBase):
    id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Case schemas
class CaseBase(BaseSchema):
    title: str
    description: Optional[str] = None
    status: CaseStatus = CaseStatus.OPEN
    priority: CrisisLevel = CrisisLevel.LOW
    crisis_indicators: Optional[List[str]] = None
    services_needed: Optional[List[ServiceType]] = None
    notes: Optional[str] = None

class CaseCreate(CaseBase):
    client_id: str
    assigned_user_id: Optional[str] = None

class CaseUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CrisisLevel] = None
    crisis_indicators: Optional[List[str]] = None
    services_needed: Optional[List[ServiceType]] = None
    notes: Optional[str] = None
    assigned_user_id: Optional[str] = None

class Case(CaseBase):
    id: str
    client_id: str
    assigned_user_id: Optional[str] = None
    created_by: str
    case_number: str
    care_plan: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None

# Assessment schemas
class AssessmentBase(BaseSchema):
    assessment_type: str
    questions: Optional[Dict[str, Any]] = None
    crisis_score: Optional[float] = None
    recommended_services: Optional[List[ServiceType]] = None

class AssessmentCreate(AssessmentBase):
    client_id: str
    case_id: Optional[str] = None

class Assessment(AssessmentBase):
    id: str
    client_id: str
    case_id: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    created_by: str
    created_at: datetime

# Intervention schemas
class InterventionBase(BaseSchema):
    intervention_type: str
    service_type: ServiceType
    provider_name: Optional[str] = None
    provider_contact: Optional[str] = None
    description: Optional[str] = None
    status: str = "pending"
    scheduled_date: Optional[datetime] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None

class InterventionCreate(InterventionBase):
    case_id: str

class InterventionUpdate(BaseSchema):
    intervention_type: Optional[str] = None
    service_type: Optional[ServiceType] = None
    provider_name: Optional[str] = None
    provider_contact: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None

class Intervention(InterventionBase):
    id: str
    case_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime

# Document schemas
class DocumentBase(BaseSchema):
    filename: str
    original_filename: str
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    document_type: Optional[str] = None
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    case_id: str

class Document(DocumentBase):
    id: str
    case_id: str
    uploaded_by: str
    created_at: datetime

# Resource schemas
class ResourceBase(BaseSchema):
    name: str
    description: Optional[str] = None
    service_type: ServiceType
    provider_name: str
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    eligibility_requirements: Optional[List[str]] = None
    hours_of_operation: Optional[Dict[str, str]] = None
    languages_supported: Optional[List[LanguageCode]] = None
    is_active: bool = True

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    service_type: Optional[ServiceType] = None
    provider_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    eligibility_requirements: Optional[List[str]] = None
    hours_of_operation: Optional[Dict[str, str]] = None
    languages_supported: Optional[List[LanguageCode]] = None
    is_active: Optional[bool] = None

class Resource(ResourceBase):
    id: str
    created_at: datetime
    updated_at: datetime

# Compliance schemas
class ComplianceReportBase(BaseSchema):
    report_type: str
    report_period_start: date
    report_period_end: date
    data: Dict[str, Any]
    status: str = "draft"

class ComplianceReportCreate(ComplianceReportBase):
    pass

class ComplianceReport(ComplianceReportBase):
    id: str
    submitted_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    created_by: str
    created_at: datetime

# AI Service schemas
class AIRequest(BaseSchema):
    query: str
    context: Optional[Dict[str, Any]] = None
    client_id: Optional[str] = None
    case_id: Optional[str] = None

class AIResponse(BaseSchema):
    response: str
    confidence: float
    suggestions: Optional[List[str]] = None
    crisis_indicators: Optional[List[str]] = None
    recommended_actions: Optional[List[str]] = None

class TriageRequest(BaseSchema):
    client_id: str
    responses: Dict[str, Any]
    language: LanguageCode = LanguageCode.EN

class TriageResponse(BaseSchema):
    crisis_level: CrisisLevel
    crisis_score: float
    crisis_indicators: List[str]
    recommended_services: List[ServiceType]
    immediate_actions: List[str]
    care_plan: Dict[str, Any]

class CarePlanRequest(BaseSchema):
    case_id: str
    client_profile: Dict[str, Any]
    services_needed: List[ServiceType]
    crisis_level: CrisisLevel

class CarePlanResponse(BaseSchema):
    care_plan: Dict[str, Any]
    timeline: List[Dict[str, Any]]
    resources: List[Dict[str, Any]]
    success_metrics: Dict[str, Any]

# Crisis Detection schemas
class CrisisDetectionRequest(BaseSchema):
    text: str
    context: Optional[Dict[str, Any]] = None
    client_id: Optional[str] = None

class CrisisDetectionResponse(BaseSchema):
    risk_level: CrisisLevel
    confidence: float
    triggers: List[str]
    recommended_actions: List[str]
    escalation_required: bool
    emergency_contacts: Optional[List[Dict[str, str]]] = None

# Compliance schemas
class HUDReportRequest(BaseSchema):
    start_date: date
    end_date: date
    include_clients: bool = True
    include_services: bool = True

class HUDReportResponse(BaseSchema):
    report_data: Dict[str, Any]
    export_url: str
    record_count: int

class HMISExportRequest(BaseSchema):
    start_date: date
    end_date: date
    format: str = "xml"  # xml, csv, json

class HMISExportResponse(BaseSchema):
    export_data: str
    format: str
    record_count: int

# Analytics schemas
class AnalyticsRequest(BaseSchema):
    start_date: date
    end_date: date
    metrics: List[str]
    filters: Optional[Dict[str, Any]] = None

class AnalyticsResponse(BaseSchema):
    metrics: Dict[str, Any]
    charts: List[Dict[str, Any]]
    insights: List[str]
    recommendations: List[str]

# WebSocket schemas
class WebSocketMessage(BaseSchema):
    type: str
    data: Dict[str, Any]
    timestamp: datetime

class NotificationMessage(BaseSchema):
    user_id: str
    title: str
    message: str
    type: str
    priority: str = "normal"
    data: Optional[Dict[str, Any]] = None

# Error schemas
class ErrorResponse(BaseSchema):
    error: str
    detail: Optional[str] = None
    type: str
    timestamp: datetime

# Pagination schemas
class PaginationParams(BaseSchema):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: str = "asc"

class PaginatedResponse(BaseSchema):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
