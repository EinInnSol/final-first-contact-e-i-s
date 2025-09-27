"""
SQLAlchemy models for First Contact EIS
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

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CASEWORKER = "caseworker"
    SUPERVISOR = "supervisor"
    ANALYST = "analyst"
    CLIENT = "client"

class CaseStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    ESCALATED = "escalated"

class CrisisLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ServiceType(str, enum.Enum):
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

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CLIENT)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cases = relationship("Case", back_populates="assigned_user")
    created_cases = relationship("Case", back_populates="created_by_user", foreign_keys="Case.created_by")

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    ssn = Column(String(11), nullable=True)  # Encrypted
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(2))
    zip_code = Column(String(10))
    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(50))
    preferred_language = Column(String(10), default="en")
    is_homeless = Column(Boolean, default=False)
    is_veteran = Column(Boolean, default=False)
    is_domestic_violence_survivor = Column(Boolean, default=False)
    has_children = Column(Boolean, default=False)
    number_of_children = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cases = relationship("Case", back_populates="client")
    assessments = relationship("Assessment", back_populates="client")

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    assigned_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    case_number = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(CaseStatus), default=CaseStatus.OPEN)
    priority = Column(Enum(CrisisLevel), default=CrisisLevel.LOW)
    crisis_indicators = Column(JSON)  # List of crisis indicators
    services_needed = Column(JSON)  # List of service types
    care_plan = Column(JSON)  # AI-generated care plan
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime)
    
    # Relationships
    client = relationship("Client", back_populates="cases")
    assigned_user = relationship("User", back_populates="cases", foreign_keys=[assigned_user_id])
    created_by_user = relationship("User", back_populates="created_cases", foreign_keys=[created_by])
    assessments = relationship("Assessment", back_populates="case")
    interventions = relationship("Intervention", back_populates="case")
    documents = relationship("Document", back_populates="case")

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=True)
    assessment_type = Column(String(50), nullable=False)  # triage, comprehensive, follow_up
    questions = Column(JSON)  # Assessment questions and responses
    ai_analysis = Column(JSON)  # AI analysis results
    crisis_score = Column(Float)  # 0-100 crisis score
    recommended_services = Column(JSON)  # AI-recommended services
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="assessments")
    case = relationship("Case", back_populates="assessments")
    created_by_user = relationship("User")

class Intervention(Base):
    __tablename__ = "interventions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False)
    intervention_type = Column(String(50), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    provider_name = Column(String(200))
    provider_contact = Column(String(200))
    description = Column(Text)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, cancelled
    scheduled_date = Column(DateTime)
    completed_date = Column(DateTime)
    outcome = Column(Text)
    notes = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    case = relationship("Case", back_populates="interventions")
    created_by_user = relationship("User")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    document_type = Column(String(50))  # assessment, care_plan, compliance, other
    description = Column(Text)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case = relationship("Case", back_populates="documents")
    uploaded_by_user = relationship("User")

class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    service_type = Column(Enum(ServiceType), nullable=False)
    provider_name = Column(String(200), nullable=False)
    contact_phone = Column(String(20))
    contact_email = Column(String(255))
    website = Column(String(500))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(2))
    zip_code = Column(String(10))
    eligibility_requirements = Column(JSON)
    hours_of_operation = Column(JSON)
    languages_supported = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_type = Column(String(50), nullable=False)  # hud, hmis, ces
    report_period_start = Column(Date, nullable=False)
    report_period_end = Column(Date, nullable=False)
    data = Column(JSON, nullable=False)
    status = Column(String(50), default="draft")  # draft, submitted, approved
    submitted_at = Column(DateTime)
    approved_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    created_by_user = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100))
    old_values = Column(JSON)
    new_values = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

# Demo data creation function
async def create_demo_data(db_session):
    """Create demo data for the system"""
    from sqlalchemy.orm import sessionmaker
    
    # Create demo users
    demo_users = [
        User(
            email="admin@firstcontact-eis.org",
            username="admin",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2",  # password: admin123
            first_name="System",
            last_name="Administrator",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        ),
        User(
            email="caseworker@firstcontact-eis.org",
            username="caseworker1",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2",  # password: admin123
            first_name="Maria",
            last_name="Rodriguez",
            role=UserRole.CASEWORKER,
            is_active=True,
            is_verified=True
        ),
        User(
            email="analyst@firstcontact-eis.org",
            username="analyst1",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2",  # password: admin123
            first_name="David",
            last_name="Kim",
            role=UserRole.ANALYST,
            is_active=True,
            is_verified=True
        )
    ]
    
    for user in demo_users:
        db_session.add(user)
    
    await db_session.commit()
    
    # Create demo clients
    demo_clients = [
        Client(
            first_name="Maria",
            last_name="Rodriguez",
            date_of_birth=date(1985, 3, 15),
            phone="(562) 555-0123",
            email="maria.rodriguez@email.com",
            address="123 Main St",
            city="Long Beach",
            state="CA",
            zip_code="90802",
            preferred_language="es",
            is_homeless=True,
            has_children=True,
            number_of_children=2
        ),
        Client(
            first_name="James",
            last_name="Wilson",
            date_of_birth=date(1978, 7, 22),
            phone="(562) 555-0456",
            email="james.wilson@email.com",
            address="456 Oak Ave",
            city="Long Beach",
            state="CA",
            zip_code="90803",
            preferred_language="en",
            is_veteran=True,
            is_homeless=False
        ),
        Client(
            first_name="Sokha",
            last_name="Chen",
            date_of_birth=date(1992, 11, 8),
            phone="(562) 555-0789",
            email="sokha.chen@email.com",
            address="789 Pine St",
            city="Long Beach",
            state="CA",
            zip_code="90804",
            preferred_language="km",
            is_domestic_violence_survivor=True,
            has_children=True,
            number_of_children=1
        )
    ]
    
    for client in demo_clients:
        db_session.add(client)
    
    await db_session.commit()
    
    # Create demo cases
    demo_cases = [
        Case(
            client_id=demo_clients[0].id,
            assigned_user_id=demo_users[1].id,
            created_by=demo_users[1].id,
            case_number="FC-2024-001",
            title="Housing Crisis - Family with Children",
            description="Family of 3 experiencing homelessness, need immediate housing assistance",
            status=CaseStatus.OPEN,
            priority=CrisisLevel.HIGH,
            crisis_indicators=["homeless", "children", "no_income"],
            services_needed=["housing", "childcare", "employment", "financial"]
        ),
        Case(
            client_id=demo_clients[1].id,
            assigned_user_id=demo_users[1].id,
            created_by=demo_users[1].id,
            case_number="FC-2024-002",
            title="Veteran Services - Employment Support",
            description="Veteran seeking employment assistance and benefits",
            status=CaseStatus.IN_PROGRESS,
            priority=CrisisLevel.MEDIUM,
            crisis_indicators=["veteran", "unemployed"],
            services_needed=["employment", "veteran_services", "mental_health"]
        ),
        Case(
            client_id=demo_clients[2].id,
            assigned_user_id=demo_users[1].id,
            created_by=demo_users[1].id,
            case_number="FC-2024-003",
            title="Domestic Violence - Safety Planning",
            description="Survivor seeking safety planning and support services",
            status=CaseStatus.OPEN,
            priority=CrisisLevel.CRITICAL,
            crisis_indicators=["domestic_violence", "children", "safety_risk"],
            services_needed=["domestic_violence", "legal", "mental_health", "childcare"]
        )
    ]
    
    for case in demo_cases:
        db_session.add(case)
    
    await db_session.commit()
    
    # Create demo resources
    demo_resources = [
        Resource(
            name="Long Beach Housing Authority",
            description="Provides affordable housing and rental assistance",
            service_type=ServiceType.HOUSING,
            provider_name="City of Long Beach",
            contact_phone="(562) 570-6944",
            contact_email="housing@longbeach.gov",
            website="https://www.longbeach.gov/housing",
            address="1800 E Wardlow Rd",
            city="Long Beach",
            state="CA",
            zip_code="90807",
            eligibility_requirements=["low_income", "citizen_or_eligible_immigrant"],
            hours_of_operation={"monday": "8:00-17:00", "tuesday": "8:00-17:00", "wednesday": "8:00-17:00", "thursday": "8:00-17:00", "friday": "8:00-17:00"},
            languages_supported=["en", "es"]
        ),
        Resource(
            name="Veterans Affairs Long Beach",
            description="Comprehensive services for veterans",
            service_type=ServiceType.HEALTHCARE,
            provider_name="U.S. Department of Veterans Affairs",
            contact_phone="(562) 826-8000",
            website="https://www.longbeach.va.gov",
            address="5901 E 7th St",
            city="Long Beach",
            state="CA",
            zip_code="90822",
            eligibility_requirements=["veteran_status"],
            hours_of_operation={"monday": "8:00-16:30", "tuesday": "8:00-16:30", "wednesday": "8:00-16:30", "thursday": "8:00-16:30", "friday": "8:00-16:30"},
            languages_supported=["en", "es"]
        ),
        Resource(
            name="WomenShelter of Long Beach",
            description="Emergency shelter and support services for domestic violence survivors",
            service_type=ServiceType.DOMESTIC_VIOLENCE,
            provider_name="WomenShelter of Long Beach",
            contact_phone="(562) 437-4663",
            website="https://www.womenshelterlb.org",
            address="Confidential Location",
            city="Long Beach",
            state="CA",
            eligibility_requirements=["domestic_violence_survivor"],
            hours_of_operation={"24/7": "24/7"},
            languages_supported=["en", "es", "km", "tl", "ko"]
        )
    ]
    
    for resource in demo_resources:
        db_session.add(resource)
    
    await db_session.commit()
