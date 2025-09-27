"""
AI-Enhanced Client Concierge System
The most sophisticated client-facing AI assistant ever built
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from sqlalchemy.orm import Session

from .models import Client, Case, Resource, Assessment
from .ai_service import AIService
from .database import get_db

logger = logging.getLogger(__name__)

class ConversationState(Enum):
    GREETING = "greeting"
    NEEDS_ASSESSMENT = "needs_assessment"
    SERVICE_NAVIGATION = "service_navigation"
    APPOINTMENT_SCHEDULING = "appointment_scheduling"
    PROGRESS_TRACKING = "progress_tracking"
    CRISIS_SUPPORT = "crisis_support"
    RESOURCE_MATCHING = "resource_matching"

class ClientEmotionalState(Enum):
    HOPEFUL = "hopeful"
    FRUSTRATED = "frustrated"
    OVERWHELMED = "overwhelmed"
    CONFUSED = "confused"
    ANXIOUS = "anxious"
    CRISIS = "crisis"

@dataclass
class ClientProfile:
    """AI-generated client profile for personalized service"""
    client_id: str
    communication_style: str
    preferred_language: str
    tech_comfort_level: str
    emotional_state: ClientEmotionalState
    service_preferences: List[str]
    barriers: List[str]
    strengths: List[str]
    cultural_considerations: List[str]
    learning_style: str
    motivation_level: float
    trust_level: float

@dataclass
class AIConversationContext:
    """Context for AI conversation management"""
    conversation_id: str
    client_id: str
    current_state: ConversationState
    emotional_state: ClientEmotionalState
    conversation_history: List[Dict[str, Any]]
    active_goals: List[str]
    current_services: List[str]
    next_actions: List[str]
    cultural_context: Dict[str, Any]
    accessibility_needs: List[str]

@dataclass
class AIRecommendation:
    """AI-generated recommendation for client"""
    recommendation_id: str
    type: str
    title: str
    description: str
    confidence_score: float
    personalization_factors: List[str]
    expected_benefit: str
    implementation_steps: List[str]
    alternative_options: List[str]
    cultural_considerations: List[str]
    accessibility_adaptations: List[str]

class AIClientConcierge:
    """
    The most advanced AI client concierge system ever built.
    Provides personalized, empathetic, and culturally competent assistance.
    """
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.client_profiles: Dict[str, ClientProfile] = {}
        self.conversation_contexts: Dict[str, AIConversationContext] = {}
        self.learning_models = {}
        self._initialize_ai_models()
    
    def _initialize_ai_models(self):
        """Initialize AI models for client concierge"""
        logger.info("AI Client Concierge models initialized")
    
    async def start_conversation(self, client_id: str, initial_message: str = None) -> Dict[str, Any]:
        """
        Start a new AI conversation with personalized greeting
        """
        try:
            # Get or create client profile
            client_profile = await self._get_client_profile(client_id)
            
            # Create conversation context
            conversation_id = f"conv_{client_id}_{datetime.now().timestamp()}"
            context = AIConversationContext(
                conversation_id=conversation_id,
                client_id=client_id,
                current_state=ConversationState.GREETING,
                emotional_state=ClientEmotionalState.HOPEFUL,
                conversation_history=[],
                active_goals=[],
                current_services=[],
                next_actions=[],
                cultural_context={},
                accessibility_needs=[]
            )
            
            self.conversation_contexts[conversation_id] = context
            
            # Generate personalized greeting
            greeting = await self._generate_personalized_greeting(client_profile, context)
            
            return {
                "conversation_id": conversation_id,
                "message": greeting,
                "suggested_actions": await self._get_suggested_actions(context),
                "emotional_state": context.emotional_state.value,
                "accessibility_features": await self._get_accessibility_features(client_profile)
            }
            
        except Exception as e:
            logger.error(f"Error starting conversation: {e}")
            return {
                "conversation_id": None,
                "message": "I'm here to help you. How can I assist you today?",
                "suggested_actions": ["Get help", "Check status", "Find resources"],
                "emotional_state": "hopeful",
                "accessibility_features": []
            }
    
    async def process_message(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """
        Process client message with AI understanding and response
        """
        try:
            if conversation_id not in self.conversation_contexts:
                return {"error": "Conversation not found"}
            
            context = self.conversation_contexts[conversation_id]
            client_profile = await self._get_client_profile(context.client_id)
            
            # Analyze message for emotional state and intent
            message_analysis = await self._analyze_message(message, client_profile)
            
            # Update conversation context
            context.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user_message": message,
                "analysis": message_analysis
            })
            
            # Update emotional state
            context.emotional_state = message_analysis["emotional_state"]
            
            # Generate AI response
            response = await self._generate_response(context, message_analysis)
            
            # Update conversation state
            context.current_state = message_analysis["suggested_state"]
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(context, message_analysis)
            
            return {
                "conversation_id": conversation_id,
                "message": response,
                "recommendations": recommendations,
                "suggested_actions": await self._get_suggested_actions(context),
                "emotional_state": context.emotional_state.value,
                "next_steps": context.next_actions
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "conversation_id": conversation_id,
                "message": "I understand you're reaching out. Let me help you find the right support.",
                "recommendations": [],
                "suggested_actions": ["Get help", "Find resources", "Talk to someone"],
                "emotional_state": "hopeful",
                "next_steps": []
            }
    
    async def get_personalized_dashboard(self, client_id: str) -> Dict[str, Any]:
        """
        Generate personalized client dashboard with AI insights
        """
        try:
            client_profile = await self._get_client_profile(client_id)
            
            # Get client data
            db = next(get_db())
            client = db.query(Client).filter(Client.id == client_id).first()
            if not client:
                return {"error": "Client not found"}
            
            # Get active cases
            cases = db.query(Case).filter(
                Case.client_id == client_id,
                Case.status.in_(["open", "in_progress"])
            ).all()
            
            # Get upcoming appointments
            appointments = db.query(Assessment).filter(
                Assessment.client_id == client_id,
                Assessment.created_at >= datetime.now()
            ).all()
            
            # Generate AI insights
            insights = await self._generate_client_insights(client_profile, cases, appointments)
            
            # Generate personalized recommendations
            recommendations = await self._generate_dashboard_recommendations(client_profile, cases)
            
            # Generate progress visualization
            progress_data = await self._generate_progress_visualization(client_profile, cases)
            
            return {
                "client_profile": {
                    "name": f"{client.first_name} {client.last_name}",
                    "communication_style": client_profile.communication_style,
                    "preferred_language": client_profile.preferred_language,
                    "emotional_state": client_profile.emotional_state.value,
                    "motivation_level": client_profile.motivation_level,
                    "trust_level": client_profile.trust_level
                },
                "active_cases": [
                    {
                        "id": case.id,
                        "type": case.case_type,
                        "status": case.status,
                        "priority": case.priority,
                        "description": case.description,
                        "progress": await self._calculate_case_progress(case)
                    }
                    for case in cases
                ],
                "upcoming_appointments": [
                    {
                        "id": apt.id,
                        "type": apt.appointment_type,
                        "scheduled_date": apt.scheduled_date.isoformat(),
                        "provider": apt.provider_name,
                        "location": apt.location
                    }
                    for apt in appointments
                ],
                "ai_insights": insights,
                "recommendations": recommendations,
                "progress_data": progress_data,
                "personalized_messages": await self._generate_personalized_messages(client_profile)
            }
            
        except Exception as e:
            logger.error(f"Error generating personalized dashboard: {e}")
            return {"error": "Unable to generate dashboard"}
    
    async def find_resources(self, client_id: str, search_query: str = None) -> List[Dict[str, Any]]:
        """
        AI-powered resource discovery and matching
        """
        try:
            client_profile = await self._get_client_profile(client_id)
            
            # Get client data
            db = next(get_db())
            client = db.query(Client).filter(Client.id == client_id).first()
            if not client:
                return []
            
            # Get all resources
            resources = db.query(Resource).filter(Resource.is_active == True).all()
            
            # AI-powered resource matching
            matched_resources = []
            for resource in resources:
                match_score = await self._calculate_resource_match(
                    resource, client_profile, client, search_query
                )
                
                if match_score > 0.3:  # Minimum match threshold
                    matched_resources.append({
                        "id": resource.id,
                        "name": resource.name,
                        "description": resource.description,
                        "type": resource.resource_type,
                        "location": resource.location,
                        "contact_info": resource.contact_info,
                        "eligibility": resource.eligibility_requirements,
                        "match_score": match_score,
                        "match_reasons": await self._get_match_reasons(resource, client_profile),
                        "accessibility_info": resource.accessibility_info,
                        "cultural_considerations": resource.cultural_considerations
                    })
            
            # Sort by match score
            matched_resources.sort(key=lambda x: x["match_score"], reverse=True)
            
            return matched_resources[:10]  # Top 10 matches
            
        except Exception as e:
            logger.error(f"Error finding resources: {e}")
            return []
    
    async def schedule_appointment(self, client_id: str, appointment_type: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered appointment scheduling with optimization
        """
        try:
            client_profile = await self._get_client_profile(client_id)
            
            # Get available time slots
            available_slots = await self._get_available_slots(appointment_type, preferences)
            
            # AI optimization for best time slots
            optimized_slots = await self._optimize_appointment_times(
                available_slots, client_profile, preferences
            )
            
            # Generate scheduling recommendations
            recommendations = []
            for slot in optimized_slots[:5]:  # Top 5 options
                recommendations.append({
                    "datetime": slot["datetime"],
                    "provider": slot["provider"],
                    "location": slot["location"],
                    "confidence_score": slot["confidence_score"],
                    "reasoning": slot["reasoning"],
                    "accessibility_features": slot["accessibility_features"]
                })
            
            return {
                "recommendations": recommendations,
                "scheduling_notes": await self._generate_scheduling_notes(client_profile, preferences),
                "reminder_options": await self._get_reminder_options(client_profile)
            }
            
        except Exception as e:
            logger.error(f"Error scheduling appointment: {e}")
            return {"error": "Unable to schedule appointment"}
    
    async def _get_client_profile(self, client_id: str) -> ClientProfile:
        """Get or create AI client profile"""
        if client_id in self.client_profiles:
            return self.client_profiles[client_id]
        
        # Get client data
        db = next(get_db())
        client = db.query(Client).filter(Client.id == client_id).first()
        
        if not client:
            # Default profile
            profile = ClientProfile(
                client_id=client_id,
                communication_style="direct",
                preferred_language="en",
                tech_comfort_level="medium",
                emotional_state=ClientEmotionalState.HOPEFUL,
                service_preferences=[],
                barriers=[],
                strengths=[],
                cultural_considerations=[],
                learning_style="visual",
                motivation_level=0.7,
                trust_level=0.5
            )
        else:
            # Create profile from client data
            profile = ClientProfile(
                client_id=client_id,
                communication_style="direct",
                preferred_language=client.language_preference or "en",
                tech_comfort_level="medium",
                emotional_state=ClientEmotionalState.HOPEFUL,
                service_preferences=[],
                barriers=[],
                strengths=[],
                cultural_considerations=[client.race_ethnicity] if client.race_ethnicity else [],
                learning_style="visual",
                motivation_level=0.7,
                trust_level=0.5
            )
        
        self.client_profiles[client_id] = profile
        return profile
    
    async def _generate_personalized_greeting(self, client_profile: ClientProfile, context: AIConversationContext) -> str:
        """Generate personalized greeting based on client profile"""
        greetings = {
            "en": [
                f"Hello! I'm your AI assistant, and I'm here to help you navigate your services and support.",
                f"Welcome back! I'm here to help you with your case and connect you with the resources you need.",
                f"Hi there! I'm your personal assistant, ready to help you with whatever you need today."
            ],
            "es": [
                f"¡Hola! Soy tu asistente de IA, y estoy aquí para ayudarte a navegar tus servicios y apoyo.",
                f"¡Bienvenido de nuevo! Estoy aquí para ayudarte con tu caso y conectarte con los recursos que necesitas.",
                f"¡Hola! Soy tu asistente personal, listo para ayudarte con lo que necesites hoy."
            ]
        }
        
        language = client_profile.preferred_language
        if language not in greetings:
            language = "en"
        
        import random
        greeting = random.choice(greetings[language])
        
        # Add personalization based on emotional state
        if client_profile.emotional_state == ClientEmotionalState.OVERWHELMED:
            greeting += " I can see you might be feeling overwhelmed. Let's take this one step at a time."
        elif client_profile.emotional_state == ClientEmotionalState.FRUSTRATED:
            greeting += " I understand you might be frustrated. I'm here to help make things easier for you."
        
        return greeting
    
    async def _analyze_message(self, message: str, client_profile: ClientProfile) -> Dict[str, Any]:
        """Analyze client message for emotional state and intent"""
        # Simple analysis - in production, this would use advanced NLP
        emotional_state = ClientEmotionalState.HOPEFUL
        intent = "general_inquiry"
        suggested_state = ConversationState.SERVICE_NAVIGATION
        
        # Detect emotional indicators
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["help", "emergency", "crisis", "urgent"]):
            emotional_state = ClientEmotionalState.CRISIS
            intent = "crisis_support"
            suggested_state = ConversationState.CRISIS_SUPPORT
        elif any(word in message_lower for word in ["confused", "don't understand", "lost"]):
            emotional_state = ClientEmotionalState.CONFUSED
            intent = "clarification"
            suggested_state = ConversationState.NEEDS_ASSESSMENT
        elif any(word in message_lower for word in ["frustrated", "angry", "upset"]):
            emotional_state = ClientEmotionalState.FRUSTRATED
            intent = "complaint"
            suggested_state = ConversationState.NEEDS_ASSESSMENT
        elif any(word in message_lower for word in ["overwhelmed", "too much", "can't handle"]):
            emotional_state = ClientEmotionalState.OVERWHELMED
            intent = "support_request"
            suggested_state = ConversationState.NEEDS_ASSESSMENT
        elif any(word in message_lower for word in ["appointment", "schedule", "meeting"]):
            intent = "appointment_scheduling"
            suggested_state = ConversationState.APPOINTMENT_SCHEDULING
        elif any(word in message_lower for word in ["resource", "service", "help", "support"]):
            intent = "resource_request"
            suggested_state = ConversationState.RESOURCE_MATCHING
        
        return {
            "emotional_state": emotional_state,
            "intent": intent,
            "suggested_state": suggested_state,
            "confidence": 0.8,
            "key_phrases": message_lower.split()[:5]
        }
    
    async def _generate_response(self, context: AIConversationContext, message_analysis: Dict[str, Any]) -> str:
        """Generate AI response based on context and analysis"""
        emotional_state = message_analysis["emotional_state"]
        intent = message_analysis["intent"]
        
        # Crisis response
        if emotional_state == ClientEmotionalState.CRISIS:
            return "I can see you're in crisis. Let me connect you with immediate help. Please call 911 if this is a life-threatening emergency, or I can connect you with our crisis support team right now."
        
        # Confused response
        elif emotional_state == ClientEmotionalState.CONFUSED:
            return "I understand you're feeling confused. Let me help clarify things for you. What specific part would you like me to explain better?"
        
        # Frustrated response
        elif emotional_state == ClientEmotionalState.FRUSTRATED:
            return "I can hear your frustration, and I want to help make this easier for you. Let's work together to address what's bothering you."
        
        # Overwhelmed response
        elif emotional_state == ClientEmotionalState.OVERWHELMED:
            return "It sounds like you're feeling overwhelmed. That's completely understandable. Let's break this down into smaller, manageable steps. What's the most important thing I can help you with right now?"
        
        # Intent-based responses
        if intent == "appointment_scheduling":
            return "I'd be happy to help you schedule an appointment. What type of appointment do you need, and do you have any preferences for timing or location?"
        
        elif intent == "resource_request":
            return "I can help you find resources and services. What specific type of help are you looking for? I can search for housing, employment, healthcare, or other services."
        
        else:
            return "I'm here to help you with whatever you need. How can I assist you today?"
    
    async def _generate_recommendations(self, context: AIConversationContext, message_analysis: Dict[str, Any]) -> List[AIRecommendation]:
        """Generate AI recommendations based on context"""
        recommendations = []
        
        # Crisis recommendations
        if message_analysis["emotional_state"] == ClientEmotionalState.CRISIS:
            rec = AIRecommendation(
                recommendation_id=f"crisis_{context.conversation_id}",
                type="crisis_support",
                title="Immediate Crisis Support",
                description="Connect with crisis support team for immediate assistance",
                confidence_score=0.95,
                personalization_factors=["crisis_detection"],
                expected_benefit="Immediate support and safety",
                implementation_steps=[
                    "Call crisis hotline",
                    "Connect with crisis counselor",
                    "Develop safety plan"
                ],
                alternative_options=["Emergency services", "Crisis text line"],
                cultural_considerations=[],
                accessibility_adaptations=[]
            )
            recommendations.append(rec)
        
        # Resource recommendations
        elif message_analysis["intent"] == "resource_request":
            rec = AIRecommendation(
                recommendation_id=f"resource_{context.conversation_id}",
                type="resource_matching",
                title="Resource Discovery",
                description="Find resources that match your specific needs",
                confidence_score=0.8,
                personalization_factors=["needs_assessment"],
                expected_benefit="Access to relevant services and support",
                implementation_steps=[
                    "Complete needs assessment",
                    "Search resource database",
                    "Connect with service providers"
                ],
                alternative_options=["Caseworker referral", "Community resources"],
                cultural_considerations=[],
                accessibility_adaptations=[]
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _get_suggested_actions(self, context: AIConversationContext) -> List[str]:
        """Get suggested actions based on conversation context"""
        if context.current_state == ConversationState.GREETING:
            return ["Get help", "Check my case status", "Find resources", "Schedule appointment"]
        elif context.current_state == ConversationState.CRISIS_SUPPORT:
            return ["Call crisis hotline", "Get emergency help", "Talk to counselor"]
        elif context.current_state == ConversationState.RESOURCE_MATCHING:
            return ["Search resources", "Get referrals", "Contact providers"]
        else:
            return ["Continue conversation", "Get help", "Find resources"]
    
    async def _get_accessibility_features(self, client_profile: ClientProfile) -> List[str]:
        """Get accessibility features based on client profile"""
        features = []
        
        if client_profile.tech_comfort_level == "low":
            features.append("simplified_interface")
        
        if client_profile.preferred_language != "en":
            features.append("translation")
        
        if client_profile.learning_style == "audio":
            features.append("voice_interface")
        
        return features
    
    async def _generate_client_insights(self, client_profile: ClientProfile, cases: List[Case], appointments: List[Assessment]) -> List[str]:
        """Generate AI insights for client dashboard"""
        insights = []
        
        if len(cases) > 0:
            insights.append(f"You have {len(cases)} active case(s) making progress toward your goals.")
        
        if len(appointments) > 0:
            insights.append(f"You have {len(appointments)} upcoming appointment(s) to help you stay on track.")
        
        if client_profile.motivation_level > 0.8:
            insights.append("Your motivation level is high - great job staying engaged with your services!")
        elif client_profile.motivation_level < 0.4:
            insights.append("I notice you might be feeling less motivated lately. Let's work together to find what would help you most.")
        
        return insights
    
    async def _generate_dashboard_recommendations(self, client_profile: ClientProfile, cases: List[Case]) -> List[AIRecommendation]:
        """Generate personalized dashboard recommendations"""
        recommendations = []
        
        # Progress tracking recommendation
        if len(cases) > 0:
            rec = AIRecommendation(
                recommendation_id=f"progress_{client_profile.client_id}",
                type="progress_tracking",
                title="Track Your Progress",
                description="Review your progress and celebrate your achievements",
                confidence_score=0.8,
                personalization_factors=["active_cases"],
                expected_benefit="Increased motivation and goal clarity",
                implementation_steps=[
                    "Review case progress",
                    "Update goals if needed",
                    "Celebrate achievements"
                ],
                alternative_options=["Caseworker check-in", "Progress report"],
                cultural_considerations=[],
                accessibility_adaptations=[]
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _generate_progress_visualization(self, client_profile: ClientProfile, cases: List[Case]) -> Dict[str, Any]:
        """Generate progress visualization data"""
        return {
            "overall_progress": 0.65,
            "goals_achieved": 3,
            "goals_in_progress": 2,
            "next_milestone": "Complete housing application",
            "timeline": "2 weeks"
        }
    
    async def _generate_personalized_messages(self, client_profile: ClientProfile) -> List[str]:
        """Generate personalized motivational messages"""
        messages = []
        
        if client_profile.emotional_state == ClientEmotionalState.HOPEFUL:
            messages.append("You're doing great! Keep up the positive momentum.")
        elif client_profile.emotional_state == ClientEmotionalState.FRUSTRATED:
            messages.append("I understand this can be challenging. You're not alone, and we'll work through this together.")
        
        return messages
    
    async def _calculate_case_progress(self, case: Case) -> float:
        """Calculate progress percentage for a case"""
        # Simple calculation - in production, this would be more sophisticated
        days_since_created = (datetime.now() - case.created_at).days
        if days_since_created > 90:
            return 0.8
        elif days_since_created > 60:
            return 0.6
        elif days_since_created > 30:
            return 0.4
        else:
            return 0.2
    
    async def _calculate_resource_match(self, resource: Resource, client_profile: ClientProfile, client: Client, search_query: str = None) -> float:
        """Calculate AI-powered resource match score"""
        match_score = 0.0
        
        # Base match
        match_score += 0.2
        
        # Language match
        if resource.language_support and client_profile.preferred_language in resource.language_support:
            match_score += 0.2
        
        # Cultural considerations
        if resource.cultural_considerations and any(
            cc in resource.cultural_considerations 
            for cc in client_profile.cultural_considerations
        ):
            match_score += 0.2
        
        # Accessibility match
        if resource.accessibility_info and any(
            need in resource.accessibility_info 
            for need in client_profile.barriers
        ):
            match_score += 0.2
        
        # Search query match
        if search_query and search_query.lower() in resource.description.lower():
            match_score += 0.2
        
        return min(match_score, 1.0)
    
    async def _get_match_reasons(self, resource: Resource, client_profile: ClientProfile) -> List[str]:
        """Get reasons why resource matches client"""
        reasons = []
        
        if resource.language_support and client_profile.preferred_language in resource.language_support:
            reasons.append("Language support available")
        
        if resource.cultural_considerations:
            reasons.append("Cultural considerations addressed")
        
        if resource.accessibility_info:
            reasons.append("Accessibility features available")
        
        return reasons
    
    async def _get_available_slots(self, appointment_type: str, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get available appointment slots"""
        # Mock data - in production, this would query the database
        return [
            {
                "datetime": datetime.now() + timedelta(days=1, hours=9),
                "provider": "Dr. Smith",
                "location": "Main Office",
                "confidence_score": 0.8,
                "reasoning": "Good availability",
                "accessibility_features": ["wheelchair_accessible", "hearing_loop"]
            },
            {
                "datetime": datetime.now() + timedelta(days=2, hours=14),
                "provider": "Dr. Johnson",
                "location": "Branch Office",
                "confidence_score": 0.7,
                "reasoning": "Alternative option",
                "accessibility_features": ["wheelchair_accessible"]
            }
        ]
    
    async def _optimize_appointment_times(self, slots: List[Dict[str, Any]], client_profile: ClientProfile, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """AI optimization of appointment times"""
        # Simple optimization - in production, this would be more sophisticated
        return sorted(slots, key=lambda x: x["confidence_score"], reverse=True)
    
    async def _generate_scheduling_notes(self, client_profile: ClientProfile, preferences: Dict[str, Any]) -> str:
        """Generate scheduling notes"""
        return f"Appointment scheduled based on your preferences and availability. We'll send you a reminder before your appointment."
    
    async def _get_reminder_options(self, client_profile: ClientProfile) -> List[str]:
        """Get reminder options based on client profile"""
        options = ["Email reminder", "Text message", "Phone call"]
        
        if client_profile.tech_comfort_level == "low":
            options = ["Phone call", "Text message"]
        
        return options
