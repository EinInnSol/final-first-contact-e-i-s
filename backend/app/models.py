"""
SQLAlchemy models for First Contact EIS
Multi-tenant, geospatial, compliance-ready architecture
"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, Float, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

Base = declarative_base()

# ============================================================================
# ENUMS (Standardized values across system)
# ============================================================================

class UserRole(str, enum.Enum):
    """User role for RBAC"""
    ADMIN = "admin"
    CASEWORKER = "caseworker"
    ANALYST = "analyst"
    CLIENT = "client"
    SYSTEM = "system"

class CaseStatus(str, enum.Enum):
    """Case workflow states"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PAIRED = "paired"  # NEW: Mutual support pair identified
    HOUSED = "housed"
    CLOSED = "closed"
    ESCALATED = "escalated"

class CrisisLevel(str, enum.Enum):
    """Urgency classification"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class LocationType(str, enum.Enum):
    """QR code deployment location types"""
    KIOSK = "kiosk"
    BENCH = "bench"
    BUS_STOP = "bus_stop"
    SHELTER = "shelter"
    LIBRARY = "library"
    COMMUNITY_CENTER = "community_center"
    PARK = "park"
    MOBILE_UNIT = "mobile_unit"
    OTHER = "other"

class ServiceType(str, enum.Enum):
    """Service categories (HUD-aligned)"""
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
# MULTI-TENANT CORE
# ============================================================================

class Organization(Base):
    """
    Multi-tenant: Each CoC/city/partner gets their own organization
    Examples: Long Beach CoC, LA County, SF Homeless Coalition
    """
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)  # "Long Beach Continuum of Care"
    slug = Column(String(100), unique=True, index=True)  # "long-beach-coc"
    subdomain = Column(String(100), unique=True)  # "longbeach.einharjer.com"
    
    # Contact info
    primary_contact_name = Column(String(255))
    primary_contact_email = Column(String(255))
    primary_contact_phone = Column(String(20))
    
    # Settings
    settings = Column(JSON, default={})  # Branding, features enabled, integrations
    api_key = Column(String(255), unique=True)  # For their API access
    
    # Billing
    subscription_tier = Column(String(50), default="pilot")  # pilot, basic, pro, enterprise
    monthly_price = Column(Float, default=1200.0)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    locations = relationship("Location", back_populates="organization")
    users = relationship("User", back_populates="organization")
    clients = relationship("Client", back_populates="organization")

# ============================================================================
# GEOSPATIAL: QR CODE LOCATIONS
# ============================================================================

class Location(Base):
    """
    Physical QR code deployment sites
    Examples: Civic Center kiosk, MLK Park bench, Transit Mall bus stop
    """
    __tablename__ = "locations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    
    # Identifier
    location_code = Column(String(100), unique=True, index=True, nullable=False)  # "LB_MLK_042"
    display_name = Column(String(255), nullable=False)  # "MLK Jr Park Bench"
    location_type = Column(Enum(LocationType), nullable=False)
    
    # Address
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(2))
    zip_code = Column(String(10))
    
    # Geospatial (for heat maps)
    latitude = Column(Float)  # 33.7701
    longitude = Column(Float)  # -118.1937
    
    # QR Code
    qr_code_url = Column(String(500))  # Generated URL
    qr_code_image_url = Column(String(500))  # PNG image for printing
    
    # Status
    is_active = Column(Boolean, default=True)
    installed_date = Column(Date)
    last_maintenance_date = Column(Date)
    
    # Analytics metadata
    expected_monthly_scans = Column(Integer, default=0)
    actual_monthly_scans = Column(Integer, default=0)
    
    # Metadata
    notes = Column(Text)  # "High traffic area, check monthly for damage"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="locations")
    intakes = relationship("Intake", back_populates="location")

# ============================================================================
# USER MANAGEMENT
# ============================================================================

class User(Base):
    """
    System users: Admins, Caseworkers, Analysts, Clients
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CLIENT)
    
    # Security
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255))  # For TOTP
    
    # Session tracking
    last_login = Column(DateTime)
    login_count = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    assigned_cases = relationship("Case", back_populates="assigned_caseworker")
    created_cases = relationship("Case", back_populates="created_by_user", foreign_keys="Case.created_by")

# ============================================================================
# CLIENT DATA (PHI/PII)
# ============================================================================

class Client(Base):
    """
    Client records (PII/PHI - HIPAA protected)
    """
    __tablename__ = "clients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # If client has login
    
    # Personal Info (PII)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    ssn = Column(String(11))  # Encrypted at application layer
    
    # Contact
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(2))
    zip_code = Column(String(10))
    
    # Demographics (HUD Universal Data Elements)
    gender = Column(String(50))
    race = Column(JSON)  # Multiple selections allowed
    ethnicity = Column(String(50))
    veteran_status = Column(Boolean)
    
    # Mutual Support Indicators (THE INNOVATION!)
    living_with_someone = Column(Boolean, default=False)
    provides_care_to_someone = Column(Boolean, default=False)
    receives_care_from_someone = Column(Boolean, default=False)
    shared_residence = Column(Boolean, default=False)
    assists_with_daily_activities = Column(Boolean, default=False)
    daily_care_hours = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="clients")
    user = relationship("User")
    cases = relationship("Case", back_populates="client")
    intakes = relationship("Intake", back_populates="client")
    mutual_support_pairs_a = relationship("MutualSupportPair", foreign_keys="MutualSupportPair.client_a_id", back_populates="client_a")
    mutual_support_pairs_b = relationship("MutualSupportPair", foreign_keys="MutualSupportPair.client_b_id", back_populates="client_b")

# ============================================================================
# INTAKE TRACKING (Links QR location to client)
# ============================================================================

class Intake(Base):
    """
    Intake form submissions - tracks WHERE client entered system
    Critical for geospatial analytics
    """
    __tablename__ = "intakes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)  # QR code location
    
    # Timestamps (for conversion analytics)
    qr_scanned_at = Column(DateTime)  # When QR was scanned
    form_started_at = Column(DateTime)  # When form opened
    form_submitted_at = Column(DateTime)  # When form submitted
    
    # Device info (for accessibility insights, anonymized)
    user_agent = Column(String(500))  # Browser/device type
    ip_address_hash = Column(String(64))  # Hashed IP (not stored raw for privacy)
    
    # Form data (snapshot at time of intake)
    form_data = Column(JSON)  # Complete form responses
    services_requested = Column(JSON)  # Array of ServiceType
    crisis_level = Column(Enum(CrisisLevel))
    
    # Mutual Support Agent evaluation result
    mutual_support_score = Column(Float)  # 0.0 to 1.0
    mutual_support_detected = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="intakes")
    location = relationship("Location", back_populates="intakes")

# ============================================================================
# CASE MANAGEMENT
# ============================================================================

class Case(Base):
    """
    Case records - tracks client journey through services
    """
    __tablename__ = "cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    assigned_caseworker_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Case details
    status = Column(Enum(CaseStatus), nullable=False, default=CaseStatus.OPEN)
    crisis_level = Column(Enum(CrisisLevel), nullable=False)
    description = Column(Text)
    
    # Services
    services_provided = Column(JSON, default=[])  # Array of ServiceType
    referrals_made = Column(JSON, default=[])  # Array of referral details
    
    # Outcomes
    housing_status = Column(String(100))  # Housed, temporary, street, etc.
    employment_status = Column(String(100))
    
    # Mutual support link
    mutual_support_pair_id = Column(UUID(as_uuid=True), ForeignKey("mutual_support_pairs.id"), nullable=True)
    
    # Timestamps
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="cases")
    assigned_caseworker = relationship("User", foreign_keys=[assigned_caseworker_id], back_populates="assigned_cases")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="created_cases")
    mutual_support_pair = relationship("MutualSupportPair", back_populates="cases")

# ============================================================================
# MUTUAL SUPPORT PAIRS (THE INNOVATION!)
# ============================================================================

class MutualSupportPair(Base):
    """
    Detected mutual support relationships between clients
    THIS IS THE CORE INNOVATION - what makes First Contact EIS unique
    """
    __tablename__ = "mutual_support_pairs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # The pair
    client_a_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    client_b_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    
    # Detection metadata
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    detected_at = Column(DateTime, default=datetime.utcnow)
    detected_by = Column(String(50), default="mutual_support_agent")  # "mutual_support_agent" or "caseworker_manual"
    
    # Support indicators (what triggered the match)
    support_indicators = Column(JSON)  # Array of matched indicators
    
    # IHSS eligibility
    ihss_eligible = Column(Boolean, default=False)
    ihss_application_submitted = Column(Boolean, default=False)
    ihss_approved = Column(Boolean, default=False)
    ihss_monthly_payment = Column(Float)  # e.g., 1800.0
    
    # Cost savings calculation
    traditional_cost = Column(Float, default=90000.0)  # $90K for 2 separate cases
    paired_cost = Column(Float, default=42000.0)  # $42K for 1 consolidated pair
    estimated_savings = Column(Float, default=48000.0)  # $48K savings
    
    # Caseworker review
    caseworker_reviewed = Column(Boolean, default=False)
    caseworker_approved = Column(Boolean, default=False)
    caseworker_notes = Column(Text)
    reviewed_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime)
    
    # Status
    status = Column(String(50), default="detected")  # detected, reviewed, approved, formalized, rejected
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client_a = relationship("Client", foreign_keys=[client_a_id], back_populates="mutual_support_pairs_a")
    client_b = relationship("Client", foreign_keys=[client_b_id], back_populates="mutual_support_pairs_b")
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_id])
    cases = relationship("Case", back_populates="mutual_support_pair")

# ============================================================================
# CASEWORKER ALERTS
# ============================================================================

class CaseworkerAlert(Base):
    """
    Real-time alerts for caseworkers (Mutual Support detection, high crisis, etc.)
    """
    __tablename__ = "caseworker_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caseworker_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Alert details
    alert_type = Column(String(50), nullable=False)  # "mutual_support_detected", "high_crisis", "follow_up_due"
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Links
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=True)
    mutual_support_pair_id = Column(UUID(as_uuid=True), ForeignKey("mutual_support_pairs.id"), nullable=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    read_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    caseworker = relationship("User")
    client = relationship("Client")
    case = relationship("Case")
    mutual_support_pair = relationship("MutualSupportPair")
    location = relationship("Location")

# ============================================================================
# AUDIT LOG (Compliance)
# ============================================================================

class AuditLog(Base):
    """
    Immutable audit trail (HIPAA/SOC 2 requirement)
    Logs every action taken on PHI/PII
    """
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Who
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user_email = Column(String(255))  # Denormalized for audit persistence
    user_role = Column(String(50))
    
    # What
    action = Column(String(100), nullable=False)  # "client_created", "client_viewed", "case_updated"
    resource_type = Column(String(50))  # "client", "case", "user"
    resource_id = Column(UUID(as_uuid=True))
    
    # Details
    changes = Column(JSON)  # Before/after values
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    # When
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User")
