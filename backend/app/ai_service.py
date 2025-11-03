"""
AI Service integration for First Contact EIS
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import asyncio

from app.database import get_db
from app.auth import get_current_active_user
from app.models import User, Case, Client, Assessment, CrisisLevel, ServiceType
from app.schemas import (
    AIRequest, AIResponse, TriageRequest, TriageResponse, 
    CarePlanRequest, CarePlanResponse, CrisisDetectionRequest, 
    CrisisDetectionResponse, HUDReportRequest, HUDReportResponse
)

logger = logging.getLogger(__name__)

# Router
ai_router = APIRouter()

# Demo mode configuration
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
MOCK_AI_RESPONSES = os.getenv("MOCK_AI_RESPONSES", "true").lower() == "true"

class DemoModeService:
    """Service for handling demo mode without API keys"""
    
    @staticmethod
    def is_demo_mode() -> bool:
        return DEMO_MODE or not os.getenv("OPENAI_API_KEY")
    
    @staticmethod
    def get_mock_ai_response(query: str, context: Dict[str, Any] = None) -> str:
        """Generate realistic mock AI responses for demos"""
        query_lower = query.lower()
        
        # Crisis detection responses
        if "crisis" in query_lower or "emergency" in query_lower:
            return """Based on the information provided, I've identified several crisis indicators that require immediate attention:

1. **Housing Instability**: The client is experiencing homelessness with children
2. **Safety Concerns**: There are indicators of domestic violence
3. **Financial Stress**: No stable income source identified

**Immediate Actions Required:**
- Contact emergency shelter services
- Initiate safety planning protocol
- Connect with domestic violence resources
- Arrange for emergency financial assistance

**Priority Level**: CRITICAL - Immediate intervention needed"""
        
        # Triage responses
        elif "triage" in query_lower or "assessment" in query_lower:
            return """Triage Assessment Complete:

**Crisis Score**: 85/100 (HIGH RISK)

**Identified Needs:**
- Emergency housing placement
- Childcare services
- Employment assistance
- Mental health support
- Legal advocacy

**Recommended Services:**
1. Long Beach Housing Authority - Emergency placement
2. WomenShelter of Long Beach - Safety planning
3. CalWORKs - Financial assistance
4. Mental Health America - Counseling services

**Next Steps:**
- Schedule immediate intake appointment
- Prepare care plan with client
- Assign caseworker within 24 hours"""
        
        # Care plan responses
        elif "care plan" in query_lower or "plan" in query_lower:
            return """AI-Generated Care Plan:

**Phase 1: Immediate Stabilization (0-30 days)**
- Secure emergency housing
- Ensure safety and basic needs met
- Connect with emergency resources
- Begin mental health assessment

**Phase 2: Stabilization (30-90 days)**
- Transition to stable housing
- Begin employment search
- Enroll children in school/childcare
- Continue mental health services

**Phase 3: Self-Sufficiency (90-180 days)**
- Maintain stable housing
- Secure employment
- Build support network
- Plan for long-term stability

**Success Metrics:**
- Housing stability: 90+ days
- Employment: Part-time or full-time job
- Mental health: Regular therapy attendance
- Children: Enrolled in school/childcare"""
        
        # General responses
        else:
            return f"""I understand you're looking for help with: {query}

Based on your situation, I can help you with:

1. **Housing Assistance**: Emergency shelter, transitional housing, permanent housing
2. **Employment Services**: Job training, resume building, interview prep
3. **Healthcare**: Medical care, mental health services, substance abuse treatment
4. **Financial Support**: Emergency assistance, benefits enrollment, budgeting
5. **Family Services**: Childcare, parenting support, family counseling

Would you like me to help you get started with any of these services? I can connect you with local resources and help you create a plan to address your needs."""

    @staticmethod
    def get_mock_triage_response(responses: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock triage assessment"""
        crisis_indicators = []
        crisis_score = 0
        
        # Analyze responses for crisis indicators
        for key, value in responses.items():
            if isinstance(value, str):
                value_lower = value.lower()
                if any(word in value_lower for word in ["homeless", "no home", "sleeping outside"]):
                    crisis_indicators.append("homelessness")
                    crisis_score += 25
                if any(word in value_lower for word in ["abuse", "violence", "threat", "fear"]):
                    crisis_indicators.append("domestic_violence")
                    crisis_score += 30
                if any(word in value_lower for word in ["suicide", "hurt myself", "end it all"]):
                    crisis_indicators.append("suicidal_ideation")
                    crisis_score += 40
                if any(word in value_lower for word in ["children", "kids", "baby"]):
                    crisis_indicators.append("children_at_risk")
                    crisis_score += 20
        
        # Determine crisis level
        if crisis_score >= 80:
            crisis_level = "critical"
        elif crisis_score >= 60:
            crisis_level = "high"
        elif crisis_score >= 40:
            crisis_level = "medium"
        else:
            crisis_level = "low"
        
        return {
            "crisis_level": crisis_level,
            "crisis_score": crisis_score,
            "crisis_indicators": crisis_indicators,
            "recommended_services": ["housing", "mental_health", "domestic_violence", "childcare"],
            "immediate_actions": [
                "Contact emergency services if immediate danger",
                "Schedule intake appointment within 24 hours",
                "Connect with appropriate service providers",
                "Develop safety plan if needed"
            ],
            "care_plan": {
                "immediate_needs": ["safety", "housing", "basic_needs"],
                "short_term_goals": ["stabilization", "service_connection"],
                "long_term_goals": ["self_sufficiency", "independence"]
            }
        }

class AIService:
    """AI service for handling Vertex AI calls"""
    
    def __init__(self):
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID", "einharjer-valhalla")
        self.gcp_region = os.getenv("GCP_REGION", "us-west1")
        self.timeout = int(os.getenv("AI_SERVICE_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("AI_MAX_RETRIES", "3"))
        self.vertex_client = None
        
        # Initialize Vertex AI client if not in demo mode
        if not DEMO_MODE:
            try:
                from anthropic import AnthropicVertex
                self.vertex_client = AnthropicVertex(
                    project_id=self.gcp_project_id,
                    region=self.gcp_region
                )
                logger.info(f"Vertex AI Claude client initialized for project {self.gcp_project_id}, region {self.gcp_region}")
            except Exception as e:
                logger.error(f"Failed to initialize Vertex AI client: {e}")
                logger.warning("Falling back to demo mode")
    
    async def get_ai_response(self, query: str, context: Dict[str, Any] = None) -> str:
        """Get AI response from Vertex AI Claude"""
        if not self.vertex_client:
            return DemoModeService.get_mock_ai_response(query, context)
        
        try:
            return await self._call_vertex_ai(query, context)
        except Exception as e:
            logger.error(f"Vertex AI API error: {e}")
            # Fallback to demo mode on error
            return DemoModeService.get_mock_ai_response(query, context)
    
    async def _call_vertex_ai(self, query: str, context: Dict[str, Any] = None) -> str:
        """Call Vertex AI Claude API"""
        try:
            # Construct system message based on context
            system_message = "You are an AI assistant for a civic services early intervention system. Help clients with housing, employment, healthcare, and other social services."
            
            if context:
                system_message += f"\n\nContext: {json.dumps(context)}"
            
            # Vertex AI Claude call (synchronous, run in thread pool)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.vertex_client.messages.create(
                    model="claude-sonnet-4-5@20250929",  # Latest Claude model on Vertex
                    max_tokens=1024,
                    system=system_message,
                    messages=[
                        {"role": "user", "content": query}
                    ]
                )
            )
            
            # Extract text from response
            return response.content[0].text
        except Exception as e:
            logger.error(f"Vertex AI call failed: {e}")
            raise

# Initialize AI service
ai_service = AIService()

@ai_router.post("/chat", response_model=AIResponse)
async def chat_with_ai(
    request: AIRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Chat with AI assistant"""
    try:
        response_text = await ai_service.get_ai_response(request.query, request.context)
        
        # Analyze for crisis indicators
        crisis_indicators = []
        if any(word in response_text.lower() for word in ["crisis", "emergency", "urgent", "immediate"]):
            crisis_indicators.append("crisis_mentioned")
        
        return AIResponse(
            response=response_text,
            confidence=0.85,
            suggestions=[
                "Would you like to schedule an appointment?",
                "Do you need help with housing?",
                "Are you looking for employment services?"
            ],
            crisis_indicators=crisis_indicators,
            recommended_actions=[
                "Schedule intake appointment",
                "Connect with caseworker",
                "Access emergency resources if needed"
            ]
        )
    except Exception as e:
        logger.error(f"AI chat error: {e}")
        raise HTTPException(status_code=500, detail="AI service error")

@ai_router.post("/triage", response_model=TriageResponse)
async def triage_assessment(
    request: TriageRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Perform AI-powered triage assessment"""
    try:
        if DemoModeService.is_demo_mode():
            triage_data = DemoModeService.get_mock_triage_response(request.responses)
        else:
            # Real AI triage analysis
            query = f"Analyze this client assessment for crisis indicators: {json.dumps(request.responses)}"
            ai_response = await ai_service.get_ai_response(query)
            triage_data = json.loads(ai_response)
        
        # Create assessment record
        assessment = Assessment(
            client_id=request.client_id,
            assessment_type="triage",
            questions=request.responses,
            ai_analysis=triage_data,
            crisis_score=triage_data.get("crisis_score", 0),
            recommended_services=triage_data.get("recommended_services", []),
            created_by=current_user.id
        )
        
        db.add(assessment)
        await db.commit()
        
        return TriageResponse(
            crisis_level=CrisisLevel(triage_data["crisis_level"]),
            crisis_score=triage_data["crisis_score"],
            crisis_indicators=triage_data["crisis_indicators"],
            recommended_services=[ServiceType(s) for s in triage_data["recommended_services"]],
            immediate_actions=triage_data["immediate_actions"],
            care_plan=triage_data["care_plan"]
        )
    except Exception as e:
        logger.error(f"Triage assessment error: {e}")
        raise HTTPException(status_code=500, detail="Triage assessment error")

@ai_router.post("/care-plan", response_model=CarePlanResponse)
async def generate_care_plan(
    request: CarePlanRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate AI-powered care plan"""
    try:
        if DemoModeService.is_demo_mode():
            care_plan = {
                "phases": [
                    {
                        "name": "Immediate Stabilization",
                        "duration": "0-30 days",
                        "goals": ["Safety", "Basic needs", "Crisis intervention"],
                        "services": ["Emergency housing", "Crisis counseling", "Basic needs"]
                    },
                    {
                        "name": "Stabilization",
                        "duration": "30-90 days",
                        "goals": ["Housing stability", "Service connection", "Goal setting"],
                        "services": ["Transitional housing", "Case management", "Employment services"]
                    },
                    {
                        "name": "Self-Sufficiency",
                        "duration": "90-180 days",
                        "goals": ["Independence", "Employment", "Long-term stability"],
                        "services": ["Permanent housing", "Job placement", "Ongoing support"]
                    }
                ],
                "success_metrics": {
                    "housing_stability": "90+ days in stable housing",
                    "employment": "Part-time or full-time employment",
                    "mental_health": "Regular therapy attendance",
                    "children": "Children enrolled in school/childcare"
                }
            }
        else:
            # Real AI care plan generation
            query = f"Generate a comprehensive care plan for client with profile: {json.dumps(request.client_profile)}"
            ai_response = await ai_service.get_ai_response(query)
            care_plan = json.loads(ai_response)
        
        return CarePlanResponse(
            care_plan=care_plan,
            timeline=[
                {"phase": "Immediate", "duration": "0-30 days", "priority": "high"},
                {"phase": "Stabilization", "duration": "30-90 days", "priority": "medium"},
                {"phase": "Self-Sufficiency", "duration": "90-180 days", "priority": "low"}
            ],
            resources=[
                {"name": "Long Beach Housing Authority", "type": "housing", "contact": "(562) 570-6944"},
                {"name": "WomenShelter of Long Beach", "type": "domestic_violence", "contact": "(562) 437-4663"},
                {"name": "CalWORKs", "type": "financial", "contact": "(562) 570-3800"}
            ],
            success_metrics=care_plan.get("success_metrics", {})
        )
    except Exception as e:
        logger.error(f"Care plan generation error: {e}")
        raise HTTPException(status_code=500, detail="Care plan generation error")

@ai_router.post("/crisis-detection", response_model=CrisisDetectionResponse)
async def detect_crisis(
    request: CrisisDetectionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Detect crisis indicators in text"""
    try:
        crisis_keywords = [
            "suicide", "kill myself", "end it all", "hurt myself",
            "abuse", "violence", "threat", "fear", "scared",
            "homeless", "no home", "sleeping outside",
            "hungry", "starving", "no food",
            "children", "kids", "baby", "child"
        ]
        
        text_lower = request.text.lower()
        triggers = [keyword for keyword in crisis_keywords if keyword in text_lower]
        
        # Calculate risk level
        risk_score = len(triggers) * 20
        if risk_score >= 80:
            risk_level = CrisisLevel.CRITICAL
        elif risk_score >= 60:
            risk_level = CrisisLevel.HIGH
        elif risk_score >= 40:
            risk_level = CrisisLevel.MEDIUM
        else:
            risk_level = CrisisLevel.LOW
        
        return CrisisDetectionResponse(
            risk_level=risk_level,
            confidence=min(risk_score / 100, 1.0),
            triggers=triggers,
            recommended_actions=[
                "Contact emergency services if immediate danger",
                "Schedule crisis intervention appointment",
                "Connect with appropriate mental health services",
                "Develop safety plan"
            ],
            escalation_required=risk_level in [CrisisLevel.HIGH, CrisisLevel.CRITICAL],
            emergency_contacts=[
                {"name": "National Suicide Prevention Lifeline", "phone": "988"},
                {"name": "National Domestic Violence Hotline", "phone": "1-800-799-7233"},
                {"name": "Long Beach Crisis Line", "phone": "(562) 434-4949"}
            ]
        )
    except Exception as e:
        logger.error(f"Crisis detection error: {e}")
        raise HTTPException(status_code=500, detail="Crisis detection error")

@ai_router.get("/health")
async def ai_health_check():
    """AI service health check"""
    return {
        "status": "healthy",
        "demo_mode": DemoModeService.is_demo_mode(),
        "vertex_ai": {
            "enabled": ai_service.vertex_client is not None,
            "project_id": ai_service.gcp_project_id,
            "region": ai_service.gcp_region
        }
    }
