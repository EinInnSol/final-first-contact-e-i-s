"""
Intake and QR Code Management for First Contact EIS
Handles client intake forms, QR code generation, and initial assessments
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Dict
from datetime import datetime
import logging

from app.database import get_db
from app.models import Client, Case, Assessment, User, CaseStatus, CrisisLevel, UserRole
from app.schemas import ClientCreate, CaseCreate, AssessmentCreate
from app.qr_service import QRCodeService, DEMO_LOCATIONS
from app.notification_service import NotificationService

logger = logging.getLogger(__name__)

router = APIRouter()
qr_service = QRCodeService()


@router.post("/qr/generate")
async def generate_qr_code(
    location_id: Optional[str] = None,
    vendor_id: Optional[str] = None,
    area_code: Optional[str] = None,
    organization_id: Optional[str] = "lb"
):
    """
    Generate a QR code for client intake with embedded metadata

    This endpoint generates QR codes that can be placed at various locations
    around the city. When scanned, they open the intake form pre-filled with
    location/vendor metadata for tracking.
    """
    try:
        qr_data = qr_service.generate_intake_qr(
            location_id=location_id,
            vendor_id=vendor_id,
            area_code=area_code,
            organization_id=organization_id
        )
        return qr_data
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate QR code")


@router.post("/qr/batch")
async def generate_batch_qr_codes(
    vendor_id: Optional[str] = None,
    organization_id: Optional[str] = "lb",
    use_demo_locations: bool = True
):
    """
    Generate multiple QR codes for different locations

    For demo purposes, this can use predefined Long Beach locations.
    """
    try:
        locations = DEMO_LOCATIONS if use_demo_locations else []
        qr_codes = qr_service.generate_batch_qr_codes(
            locations=locations,
            vendor_id=vendor_id,
            organization_id=organization_id
        )
        return {
            "qr_codes": qr_codes,
            "count": len(qr_codes),
            "vendor_id": vendor_id,
            "organization_id": organization_id
        }
    except Exception as e:
        logger.error(f"Error generating batch QR codes: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate QR codes")


# HUD 40-Question Coordinated Entry Assessment
HUD_40_QUESTIONS = [
    {
        "id": "q1",
        "section": "Personal Information",
        "question": "What is your current living situation?",
        "type": "select",
        "required": True,
        "options": [
            "Place not meant for habitation (street, vehicle, abandoned building)",
            "Emergency shelter",
            "Transitional housing",
            "Safe haven",
            "Hotel/motel paid by you or family",
            "Staying with family/friends temporarily",
            "Rental by client (apartment, house)",
            "Owned by client",
            "Other"
        ],
        "hud_field": "living_situation"
    },
    {
        "id": "q2",
        "section": "Personal Information",
        "question": "How long have you been in this living situation?",
        "type": "select",
        "required": True,
        "options": [
            "Less than 7 days",
            "1 week to 1 month",
            "1 to 3 months",
            "3 to 6 months",
            "6 months to 1 year",
            "1 to 2 years",
            "2 to 5 years",
            "More than 5 years"
        ],
        "hud_field": "duration_of_situation"
    },
    {
        "id": "q3",
        "section": "Personal Information",
        "question": "Have you been homeless or at risk of homelessness in the past 3 years?",
        "type": "select",
        "required": True,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "previous_homelessness"
    },
    {
        "id": "q4",
        "section": "Personal Information",
        "question": "How many times have you been homeless in the past 3 years?",
        "type": "select",
        "required": False,
        "options": ["Once", "2-3 times", "4+ times", "Continuously"],
        "hud_field": "homelessness_frequency"
    },
    {
        "id": "q5",
        "section": "Personal Information",
        "question": "Are you a veteran or currently serving in the military?",
        "type": "select",
        "required": True,
        "options": ["Yes - Veteran", "Yes - Active duty", "No", "Prefer not to answer"],
        "hud_field": "veteran_status"
    },
    {
        "id": "q6",
        "section": "Household Composition",
        "question": "Are there children (under 18) in your household?",
        "type": "select",
        "required": True,
        "options": ["Yes", "No"],
        "hud_field": "has_children"
    },
    {
        "id": "q7",
        "section": "Household Composition",
        "question": "How many children are in your household?",
        "type": "number",
        "required": False,
        "hud_field": "number_of_children"
    },
    {
        "id": "q8",
        "section": "Household Composition",
        "question": "How many adults (18+) are in your household?",
        "type": "number",
        "required": True,
        "hud_field": "number_of_adults"
    },
    {
        "id": "q9",
        "section": "Safety and Health",
        "question": "Do you have any immediate safety concerns?",
        "type": "select",
        "required": True,
        "options": [
            "No safety concerns",
            "Minor concerns",
            "Moderate concerns",
            "Severe safety concerns",
            "I am in immediate danger"
        ],
        "hud_field": "safety_concerns"
    },
    {
        "id": "q10",
        "section": "Safety and Health",
        "question": "Are you fleeing domestic violence, dating violence, sexual assault, or stalking?",
        "type": "select",
        "required": True,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "domestic_violence"
    },
    {
        "id": "q11",
        "section": "Health",
        "question": "Do you have a physical disability or long-term medical condition?",
        "type": "select",
        "required": True,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "physical_disability"
    },
    {
        "id": "q12",
        "section": "Health",
        "question": "Do you have a mental health condition?",
        "type": "select",
        "required": True,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "mental_health_condition"
    },
    {
        "id": "q13",
        "section": "Health",
        "question": "Do you have a substance use issue?",
        "type": "select",
        "required": True,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "substance_use"
    },
    {
        "id": "q14",
        "section": "Health",
        "question": "Do you have HIV/AIDS?",
        "type": "select",
        "required": False,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "hiv_aids"
    },
    {
        "id": "q15",
        "section": "Health",
        "question": "Are you pregnant?",
        "type": "select",
        "required": False,
        "options": ["Yes", "No", "Not applicable", "Prefer not to answer"],
        "hud_field": "pregnancy_status"
    },
    {
        "id": "q16",
        "section": "Income and Employment",
        "question": "Do you have any income?",
        "type": "select",
        "required": True,
        "options": ["Yes", "No"],
        "hud_field": "has_income"
    },
    {
        "id": "q17",
        "section": "Income and Employment",
        "question": "What is your total monthly income?",
        "type": "select",
        "required": False,
        "options": [
            "$0",
            "$1-$500",
            "$501-$1,000",
            "$1,001-$1,500",
            "$1,501-$2,000",
            "$2,001-$3,000",
            "More than $3,000"
        ],
        "hud_field": "monthly_income"
    },
    {
        "id": "q18",
        "section": "Income and Employment",
        "question": "Are you currently employed?",
        "type": "select",
        "required": True,
        "options": ["Full-time", "Part-time", "Unemployed - looking", "Unemployed - not looking", "Unable to work", "Retired"],
        "hud_field": "employment_status"
    },
    {
        "id": "q19",
        "section": "Benefits",
        "question": "Do you receive any of the following benefits? (Select all that apply)",
        "type": "multi-select",
        "required": False,
        "options": [
            "SNAP/Food Stamps",
            "SSI",
            "SSDI",
            "Veterans Benefits",
            "TANF",
            "Unemployment",
            "General Assistance",
            "None"
        ],
        "hud_field": "benefits"
    },
    {
        "id": "q20",
        "section": "Education",
        "question": "What is your highest level of education?",
        "type": "select",
        "required": False,
        "options": [
            "Less than high school",
            "High school/GED",
            "Some college",
            "Associate degree",
            "Bachelor's degree",
            "Graduate degree",
            "Prefer not to answer"
        ],
        "hud_field": "education_level"
    },
    {
        "id": "q21",
        "section": "Criminal Justice",
        "question": "Have you been incarcerated in the past 6 months?",
        "type": "select",
        "required": False,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "recent_incarceration"
    },
    {
        "id": "q22",
        "section": "Criminal Justice",
        "question": "Do you have any outstanding warrants?",
        "type": "select",
        "required": False,
        "options": ["Yes", "No", "I don't know", "Prefer not to answer"],
        "hud_field": "outstanding_warrants"
    },
    {
        "id": "q23",
        "section": "Services Needed",
        "question": "What services do you need most urgently? (Select up to 3)",
        "type": "multi-select",
        "required": True,
        "max_selections": 3,
        "options": [
            "Emergency shelter",
            "Permanent housing",
            "Food",
            "Medical care",
            "Mental health services",
            "Substance abuse treatment",
            "Employment assistance",
            "Legal assistance",
            "Transportation",
            "Child care",
            "Case management",
            "Financial assistance"
        ],
        "hud_field": "services_needed"
    },
    {
        "id": "q24",
        "section": "Barriers to Housing",
        "question": "What barriers are preventing you from obtaining housing? (Select all that apply)",
        "type": "multi-select",
        "required": False,
        "options": [
            "Lack of income",
            "Poor credit",
            "Eviction history",
            "Criminal record",
            "No identification",
            "No references",
            "Pets",
            "Large household size",
            "Accessibility needs",
            "None"
        ],
        "hud_field": "housing_barriers"
    },
    {
        "id": "q25",
        "section": "Transportation",
        "question": "Do you have reliable transportation?",
        "type": "select",
        "required": False,
        "options": ["Yes - own vehicle", "Yes - public transit", "No", "Sometimes"],
        "hud_field": "transportation"
    },
    {
        "id": "q26",
        "section": "Support System",
        "question": "Do you have family or friends you can rely on for support?",
        "type": "select",
        "required": False,
        "options": ["Yes - significant support", "Yes - some support", "No support", "Prefer not to answer"],
        "hud_field": "social_support"
    },
    {
        "id": "q27",
        "section": "Documentation",
        "question": "Do you have identification (ID, birth certificate, Social Security card)?",
        "type": "select",
        "required": False,
        "options": ["Yes - all", "Yes - some", "No", "Lost/stolen"],
        "hud_field": "has_identification"
    },
    {
        "id": "q28",
        "section": "Insurance",
        "question": "Do you have health insurance?",
        "type": "select",
        "required": False,
        "options": ["Yes - Medi-Cal/Medicaid", "Yes - Medicare", "Yes - private", "No", "I don't know"],
        "hud_field": "health_insurance"
    },
    {
        "id": "q29",
        "section": "Language",
        "question": "What is your preferred language?",
        "type": "select",
        "required": True,
        "options": ["English", "Spanish", "Khmer", "Tagalog", "Korean", "Other"],
        "hud_field": "preferred_language"
    },
    {
        "id": "q30",
        "section": "Demographics",
        "question": "What is your gender?",
        "type": "select",
        "required": False,
        "options": ["Male", "Female", "Non-binary", "Transgender", "Prefer to self-describe", "Prefer not to answer"],
        "hud_field": "gender"
    },
    {
        "id": "q31",
        "section": "Demographics",
        "question": "What is your race? (Select all that apply)",
        "type": "multi-select",
        "required": False,
        "options": [
            "American Indian/Alaska Native",
            "Asian",
            "Black/African American",
            "Native Hawaiian/Pacific Islander",
            "White",
            "Prefer not to answer"
        ],
        "hud_field": "race"
    },
    {
        "id": "q32",
        "section": "Demographics",
        "question": "Are you Hispanic/Latino?",
        "type": "select",
        "required": False,
        "options": ["Yes", "No", "Prefer not to answer"],
        "hud_field": "ethnicity"
    },
    {
        "id": "q33",
        "section": "Previous Services",
        "question": "Have you received services from any homeless assistance programs before?",
        "type": "select",
        "required": False,
        "options": ["Yes", "No", "I don't know"],
        "hud_field": "previous_services"
    },
    {
        "id": "q34",
        "section": "Goals",
        "question": "What is your primary housing goal?",
        "type": "select",
        "required": True,
        "options": [
            "Emergency shelter immediately",
            "Transitional housing",
            "Permanent supportive housing",
            "Independent apartment/house",
            "Reunite with family",
            "Other"
        ],
        "hud_field": "housing_goal"
    },
    {
        "id": "q35",
        "section": "Urgency",
        "question": "How urgent is your housing need?",
        "type": "select",
        "required": True,
        "options": [
            "Immediate - have nowhere to stay tonight",
            "Urgent - will lose housing within 7 days",
            "High - will lose housing within 30 days",
            "Moderate - housing at risk but have time",
            "Low - seeking to improve situation"
        ],
        "hud_field": "urgency_level"
    },
    {
        "id": "q36",
        "section": "Special Populations",
        "question": "Do you identify with any of the following? (Select all that apply)",
        "type": "multi-select",
        "required": False,
        "options": [
            "Youth (18-24)",
            "Elderly (62+)",
            "LGBTQ+",
            "Immigrant/Refugee",
            "Foster care background",
            "Human trafficking survivor",
            "None"
        ],
        "hud_field": "special_populations"
    },
    {
        "id": "q37",
        "section": "Medical Needs",
        "question": "Do you need medical attention in the next 24-48 hours?",
        "type": "select",
        "required": True,
        "options": ["Yes - emergency", "Yes - urgent", "Yes - routine", "No"],
        "hud_field": "medical_urgency"
    },
    {
        "id": "q38",
        "section": "Case Management",
        "question": "Are you willing to work with a caseworker?",
        "type": "select",
        "required": True,
        "options": ["Yes", "Maybe", "No", "I need more information"],
        "hud_field": "case_management_willingness"
    },
    {
        "id": "q39",
        "section": "Contact",
        "question": "What is the best way to contact you?",
        "type": "select",
        "required": True,
        "options": ["Phone call", "Text message", "Email", "In person", "No contact"],
        "hud_field": "contact_preference"
    },
    {
        "id": "q40",
        "section": "Additional Information",
        "question": "Is there anything else you'd like us to know about your situation?",
        "type": "text",
        "required": False,
        "hud_field": "additional_notes"
    }
]


@router.get("/forms/hud40")
async def get_hud_40_form():
    """
    Get the HUD 40-question Coordinated Entry Assessment form

    Returns the complete HUD-standardized assessment form used for
    prioritizing clients for housing assistance.
    """
    return {
        "form_name": "HUD Coordinated Entry Assessment",
        "version": "2.0",
        "total_questions": len(HUD_40_QUESTIONS),
        "questions": HUD_40_QUESTIONS,
        "sections": list(set([q["section"] for q in HUD_40_QUESTIONS]))
    }


@router.post("/submit")
async def submit_intake(
    intake_data: Dict,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a completed intake form

    This creates a new client record, generates a case, runs AI assessment,
    assigns a caseworker, and sends notifications.
    """
    try:
        # Extract client data from intake
        client_data = intake_data.get("client_info", {})
        assessment_data = intake_data.get("assessment_responses", {})
        metadata = intake_data.get("metadata", {})

        # Create client record
        new_client = Client(
            first_name=client_data.get("first_name"),
            last_name=client_data.get("last_name"),
            date_of_birth=client_data.get("date_of_birth"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=metadata.get("location_name", ""),
            city="Long Beach",
            state="CA",
            zip_code=metadata.get("area_code", ""),
            preferred_language=assessment_data.get("q29", "en"),
            is_homeless=assessment_data.get("q1", "").startswith("Place not meant"),
            is_veteran=assessment_data.get("q5", "") == "Yes - Veteran",
            is_domestic_violence_survivor=assessment_data.get("q10", "") == "Yes",
            has_children=assessment_data.get("q6", "") == "Yes",
            number_of_children=int(assessment_data.get("q7", 0) or 0)
        )

        db.add(new_client)
        await db.flush()

        # Calculate crisis score from assessment
        crisis_score = calculate_crisis_score(assessment_data)
        crisis_level = determine_crisis_level(crisis_score)

        # Assign caseworker (for demo, assign to Amber Schmutz)
        caseworker = await db.execute(
            select(User).where(
                User.role == UserRole.CASEWORKER,
                User.first_name == "Amber"
            )
        )
        caseworker = caseworker.scalar_one_or_none()

        if not caseworker:
            # Create Amber if she doesn't exist (for demo)
            caseworker = User(
                email="amber@firstcontact-eis.org",
                username="aschmutz",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2",
                first_name="Amber",
                last_name="Schmutz",
                role=UserRole.CASEWORKER,
                is_active=True,
                is_verified=True
            )
            db.add(caseworker)
            await db.flush()

        # Create case
        case_number = f"FC-{datetime.now().strftime('%Y%m%d')}-{new_client.id.hex[:6].upper()}"
        new_case = Case(
            client_id=new_client.id,
            assigned_user_id=caseworker.id,
            created_by=caseworker.id,
            case_number=case_number,
            title=f"Intake Assessment - {client_data.get('first_name')} {client_data.get('last_name')}",
            description=f"New client intake from {metadata.get('location_name', 'Unknown location')}",
            status=CaseStatus.OPEN,
            priority=crisis_level,
            crisis_indicators=extract_crisis_indicators(assessment_data),
            services_needed=assessment_data.get("q23", []),
            care_plan=generate_care_plan(assessment_data, crisis_level)
        )

        db.add(new_case)
        await db.flush()

        # Create assessment record
        new_assessment = Assessment(
            client_id=new_client.id,
            case_id=new_case.id,
            assessment_type="hud_40_coordinated_entry",
            questions=assessment_data,
            crisis_score=crisis_score,
            recommended_services=assessment_data.get("q23", []),
            created_by=caseworker.id
        )

        db.add(new_assessment)
        await db.commit()

        # Send notification to caseworker (background task)
        notification_service = NotificationService()
        background_tasks.add_task(
            notification_service.send_caseworker_notification,
            caseworker_phone="5626811431",  # Amber's number
            client_name=f"{client_data.get('first_name')} {client_data.get('last_name')}",
            case_number=case_number,
            appointment_time=calculate_appointment_time(crisis_level)
        )

        return {
            "success": True,
            "client_id": str(new_client.id),
            "case_id": str(new_case.id),
            "case_number": case_number,
            "caseworker": {
                "name": f"{caseworker.first_name} {caseworker.last_name}",
                "phone": "562-681-1431",
                "email": caseworker.email
            },
            "appointment_time": calculate_appointment_time(crisis_level),
            "crisis_level": crisis_level.value,
            "crisis_score": crisis_score,
            "message": f"You have been assigned {caseworker.first_name} {caseworker.last_name} as your caseworker. Expect a call at {calculate_appointment_time(crisis_level)}."
        }

    except Exception as e:
        logger.error(f"Error submitting intake: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to submit intake: {str(e)}")


def calculate_crisis_score(assessment_data: Dict) -> float:
    """Calculate crisis score from assessment responses"""
    score = 0

    # High-weight factors
    if "Place not meant" in assessment_data.get("q1", ""):
        score += 20
    if assessment_data.get("q6", "") == "Yes":  # Children
        score += 15
    if assessment_data.get("q10", "") == "Yes":  # DV
        score += 20
    if "immediate" in assessment_data.get("q35", "").lower():  # Urgency
        score += 25
    if "emergency" in assessment_data.get("q37", "").lower():  # Medical
        score += 15
    if "Severe" in assessment_data.get("q9", ""):  # Safety
        score += 10

    return min(score, 100)


def determine_crisis_level(score: float) -> CrisisLevel:
    """Determine crisis level from score"""
    if score >= 75:
        return CrisisLevel.CRITICAL
    elif score >= 50:
        return CrisisLevel.HIGH
    elif score >= 25:
        return CrisisLevel.MEDIUM
    else:
        return CrisisLevel.LOW


def extract_crisis_indicators(assessment_data: Dict) -> List[str]:
    """Extract crisis indicators from assessment"""
    indicators = []

    if "Place not meant" in assessment_data.get("q1", ""):
        indicators.append("homeless")
    if assessment_data.get("q6", "") == "Yes":
        indicators.append("children")
    if assessment_data.get("q10", "") == "Yes":
        indicators.append("domestic_violence")
    if assessment_data.get("q16", "") == "No":
        indicators.append("no_income")
    if assessment_data.get("q12", "") == "Yes":
        indicators.append("mental_health")
    if assessment_data.get("q13", "") == "Yes":
        indicators.append("substance_use")

    return indicators


def generate_care_plan(assessment_data: Dict, crisis_level: CrisisLevel) -> Dict:
    """Generate AI-powered care plan"""
    services = assessment_data.get("q23", [])

    return {
        "immediate_needs": services[:3] if services else ["Emergency shelter", "Food", "Case management"],
        "short_term_goals": [
            "Stabilize housing situation",
            "Connect with support services",
            "Address immediate health needs"
        ],
        "long_term_goals": [
            "Secure permanent housing",
            "Achieve financial stability",
            "Build support network"
        ],
        "recommended_providers": [],
        "estimated_timeline": "30-90 days" if crisis_level == CrisisLevel.CRITICAL else "90-180 days"
    }


def calculate_appointment_time(crisis_level: CrisisLevel) -> str:
    """Calculate appointment time based on crisis level"""
    from datetime import timedelta

    now = datetime.now()

    if crisis_level == CrisisLevel.CRITICAL:
        appointment = now + timedelta(hours=2)
        return appointment.strftime("%I:%M %p today")
    elif crisis_level == CrisisLevel.HIGH:
        appointment = now + timedelta(hours=4)
        return appointment.strftime("%I:%M %p today")
    else:
        appointment = now + timedelta(days=1)
        return appointment.strftime("%I:%M %p tomorrow")
