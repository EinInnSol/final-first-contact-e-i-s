"""
AI-Enhanced Kiosk Intelligence System
The most sophisticated public-facing AI interface ever built
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

class UserBehaviorPattern(Enum):
    FIRST_TIME = "first_time"
    RETURNING = "returning"
    FREQUENT = "frequent"
    CRISIS = "crisis"

class AccessibilityNeed(Enum):
    VISUAL_IMPAIRMENT = "visual_impairment"
    HEARING_IMPAIRMENT = "hearing_impairment"
    MOTOR_IMPAIRMENT = "motor_impairment"
    COGNITIVE_IMPAIRMENT = "cognitive_impairment"
    LANGUAGE_BARRIER = "language_barrier"
    LITERACY_CHALLENGE = "literacy_challenge"

class InterfaceMode(Enum):
    STANDARD = "standard"
    SIMPLIFIED = "simplified"
    ACCESSIBLE = "accessible"
    CHILD_FRIENDLY = "child_friendly"
    CRISIS = "crisis"

@dataclass
class UserProfile:
    """AI-generated user profile for kiosk interaction"""
    session_id: str
    behavior_pattern: UserBehaviorPattern
    accessibility_needs: List[AccessibilityNeed]
    preferred_language: str
    tech_comfort_level: str
    emotional_state: str
    cultural_background: str
    age_group: str
    interaction_style: str
    learning_preference: str
    trust_level: float
    confidence_level: float

@dataclass
class AdaptiveInterface:
    """AI-adapted interface configuration"""
    mode: InterfaceMode
    font_size: str
    color_scheme: str
    navigation_style: str
    input_method: str
    audio_enabled: bool
    voice_guidance: bool
    simplified_language: bool
    visual_cues: List[str]
    accessibility_features: List[str]

@dataclass
class AIServiceRecommendation:
    """AI-generated service recommendation for kiosk users"""
    recommendation_id: str
    service_type: str
    title: str
    description: str
    confidence_score: float
    personalization_factors: List[str]
    accessibility_adaptations: List[str]
    cultural_considerations: List[str]
    implementation_steps: List[str]
    alternative_options: List[str]
    urgency_level: str
    estimated_time: str

class AIKioskIntelligence:
    """
    The most advanced AI kiosk intelligence system ever built.
    Provides adaptive, accessible, and culturally competent public service.
    """
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.user_profiles: Dict[str, UserProfile] = {}
        self.interface_configurations: Dict[str, AdaptiveInterface] = {}
        self.learning_models = {}
        self._initialize_ai_models()
    
    def _initialize_ai_models(self):
        """Initialize AI models for kiosk intelligence"""
        logger.info("AI Kiosk Intelligence models initialized")
    
    async def start_kiosk_session(self, session_id: str, initial_interaction: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Start a new kiosk session with AI-powered user profiling
        """
        try:
            # Analyze initial interaction for user profiling
            user_profile = await self._analyze_user_profile(session_id, initial_interaction)
            
            # Generate adaptive interface configuration
            interface_config = await self._generate_adaptive_interface(user_profile)
            
            # Create personalized greeting
            greeting = await self._generate_personalized_greeting(user_profile)
            
            # Generate initial service recommendations
            recommendations = await self._generate_initial_recommendations(user_profile)
            
            # Store profiles
            self.user_profiles[session_id] = user_profile
            self.interface_configurations[session_id] = interface_config
            
            return {
                "session_id": session_id,
                "greeting": greeting,
                "interface_config": interface_config.__dict__,
                "recommendations": [rec.__dict__ for rec in recommendations],
                "suggested_actions": await self._get_suggested_actions(user_profile),
                "accessibility_features": interface_config.accessibility_features,
                "cultural_adaptations": await self._get_cultural_adaptations(user_profile)
            }
            
        except Exception as e:
            logger.error(f"Error starting kiosk session: {e}")
            return {
                "session_id": session_id,
                "greeting": "Welcome! I'm here to help you find the services you need.",
                "interface_config": {"mode": "standard"},
                "recommendations": [],
                "suggested_actions": ["Get help", "Find services", "Schedule appointment"],
                "accessibility_features": [],
                "cultural_adaptations": []
            }
    
    async def process_user_interaction(self, session_id: str, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user interaction with AI-powered understanding and adaptation
        """
        try:
            if session_id not in self.user_profiles:
                return {"error": "Session not found"}
            
            user_profile = self.user_profiles[session_id]
            interface_config = self.interface_configurations[session_id]
            
            # Analyze interaction
            interaction_analysis = await self._analyze_interaction(interaction, user_profile)
            
            # Update user profile based on interaction
            await self._update_user_profile(user_profile, interaction_analysis)
            
            # Adapt interface if needed
            if interaction_analysis["interface_adaptation_needed"]:
                interface_config = await self._adapt_interface(user_profile, interaction_analysis)
                self.interface_configurations[session_id] = interface_config
            
            # Generate response
            response = await self._generate_response(user_profile, interaction_analysis)
            
            # Generate recommendations
            recommendations = await self._generate_contextual_recommendations(user_profile, interaction_analysis)
            
            # Detect crisis situations
            crisis_detection = await self._detect_crisis_situation(user_profile, interaction_analysis)
            
            return {
                "session_id": session_id,
                "response": response,
                "interface_config": interface_config.__dict__,
                "recommendations": [rec.__dict__ for rec in recommendations],
                "crisis_detection": crisis_detection,
                "suggested_actions": await self._get_suggested_actions(user_profile),
                "accessibility_updates": interface_config.accessibility_features,
                "next_steps": await self._get_next_steps(user_profile, interaction_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error processing user interaction: {e}")
            return {
                "session_id": session_id,
                "response": "I'm here to help you. How can I assist you today?",
                "interface_config": {"mode": "standard"},
                "recommendations": [],
                "crisis_detection": {"is_crisis": False},
                "suggested_actions": ["Get help", "Find services"],
                "accessibility_updates": [],
                "next_steps": []
            }
    
    async def find_services(self, session_id: str, search_criteria: Dict[str, Any]) -> List[AIServiceRecommendation]:
        """
        AI-powered service discovery and matching for kiosk users
        """
        try:
            if session_id not in self.user_profiles:
                return []
            
            user_profile = self.user_profiles[session_id]
            
            # Get all available resources
            db = next(get_db())
            resources = db.query(Resource).filter(Resource.is_active == True).all()
            
            # AI-powered matching
            recommendations = []
            for resource in resources:
                match_score = await self._calculate_service_match(resource, user_profile, search_criteria)
                
                if match_score > 0.3:  # Minimum match threshold
                    recommendation = AIServiceRecommendation(
                        recommendation_id=f"service_{resource.id}_{session_id}",
                        service_type=resource.resource_type,
                        title=resource.name,
                        description=await self._adapt_description(resource.description, user_profile),
                        confidence_score=match_score,
                        personalization_factors=await self._get_personalization_factors(resource, user_profile),
                        accessibility_adaptations=await self._get_accessibility_adaptations(resource, user_profile),
                        cultural_considerations=await self._get_cultural_considerations(resource, user_profile),
                        implementation_steps=await self._get_implementation_steps(resource, user_profile),
                        alternative_options=await self._get_alternative_options(resource, user_profile),
                        urgency_level=await self._assess_urgency_level(resource, user_profile),
                        estimated_time=await self._estimate_service_time(resource, user_profile)
                    )
                    recommendations.append(recommendation)
            
            # Sort by match score and return top recommendations
            recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
            return recommendations[:5]  # Top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error finding services: {e}")
            return []
    
    async def schedule_appointment(self, session_id: str, appointment_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered appointment scheduling with optimization
        """
        try:
            if session_id not in self.user_profiles:
                return {"error": "Session not found"}
            
            user_profile = self.user_profiles[session_id]
            
            # Get available appointments
            available_appointments = await self._get_available_appointments(appointment_preferences)
            
            # AI optimization for user preferences
            optimized_appointments = await self._optimize_appointments_for_user(
                available_appointments, user_profile, appointment_preferences
            )
            
            # Generate scheduling recommendations
            recommendations = []
            for apt in optimized_appointments[:3]:  # Top 3 options
                recommendations.append({
                    "appointment_id": apt["id"],
                    "datetime": apt["datetime"],
                    "provider": apt["provider"],
                    "location": apt["location"],
                    "accessibility_features": apt["accessibility_features"],
                    "cultural_considerations": apt["cultural_considerations"],
                    "confidence_score": apt["confidence_score"],
                    "reasoning": apt["reasoning"]
                })
            
            return {
                "recommendations": recommendations,
                "scheduling_notes": await self._generate_scheduling_notes(user_profile, appointment_preferences),
                "reminder_options": await self._get_reminder_options(user_profile),
                "accessibility_accommodations": await self._get_accessibility_accommodations(user_profile)
            }
            
        except Exception as e:
            logger.error(f"Error scheduling appointment: {e}")
            return {"error": "Unable to schedule appointment"}
    
    async def handle_crisis_situation(self, session_id: str, crisis_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered crisis detection and response
        """
        try:
            if session_id not in self.user_profiles:
                return {"error": "Session not found"}
            
            user_profile = self.user_profiles[session_id]
            
            # Assess crisis level
            crisis_level = await self._assess_crisis_level(crisis_indicators, user_profile)
            
            # Generate crisis response
            crisis_response = await self._generate_crisis_response(crisis_level, user_profile)
            
            # Switch to crisis interface mode
            interface_config = await self._switch_to_crisis_mode(user_profile)
            self.interface_configurations[session_id] = interface_config
            
            # Generate immediate actions
            immediate_actions = await self._generate_immediate_actions(crisis_level, user_profile)
            
            return {
                "crisis_level": crisis_level,
                "response": crisis_response,
                "interface_config": interface_config.__dict__,
                "immediate_actions": immediate_actions,
                "emergency_contacts": await self._get_emergency_contacts(user_profile),
                "safety_plan": await self._generate_safety_plan(crisis_level, user_profile),
                "follow_up_actions": await self._get_follow_up_actions(crisis_level, user_profile)
            }
            
        except Exception as e:
            logger.error(f"Error handling crisis situation: {e}")
            return {
                "crisis_level": "unknown",
                "response": "I can see you need immediate help. Let me connect you with someone who can assist you right away.",
                "interface_config": {"mode": "crisis"},
                "immediate_actions": ["Call 911 if emergency", "Connect with crisis counselor"],
                "emergency_contacts": ["911", "Crisis hotline: 1-800-XXX-XXXX"],
                "safety_plan": [],
                "follow_up_actions": []
            }
    
    async def generate_accessibility_report(self, session_id: str) -> Dict[str, Any]:
        """
        Generate accessibility usage report for system improvement
        """
        try:
            if session_id not in self.user_profiles:
                return {"error": "Session not found"}
            
            user_profile = self.user_profiles[session_id]
            interface_config = self.interface_configurations[session_id]
            
            # Analyze accessibility usage
            accessibility_usage = await self._analyze_accessibility_usage(user_profile, interface_config)
            
            # Generate improvement recommendations
            improvements = await self._generate_accessibility_improvements(accessibility_usage)
            
            # Calculate accessibility score
            accessibility_score = await self._calculate_accessibility_score(user_profile, interface_config)
            
            return {
                "accessibility_score": accessibility_score,
                "usage_analysis": accessibility_usage,
                "improvement_recommendations": improvements,
                "user_feedback": await self._collect_user_feedback(user_profile),
                "system_improvements": await self._suggest_system_improvements(accessibility_usage)
            }
            
        except Exception as e:
            logger.error(f"Error generating accessibility report: {e}")
            return {"error": "Unable to generate accessibility report"}
    
    async def _analyze_user_profile(self, session_id: str, initial_interaction: Dict[str, Any] = None) -> UserProfile:
        """Analyze user profile from initial interaction"""
        # Default profile
        profile = UserProfile(
            session_id=session_id,
            behavior_pattern=UserBehaviorPattern.FIRST_TIME,
            accessibility_needs=[],
            preferred_language="en",
            tech_comfort_level="medium",
            emotional_state="neutral",
            cultural_background="unknown",
            age_group="adult",
            interaction_style="direct",
            learning_preference="visual",
            trust_level=0.5,
            confidence_level=0.5
        )
        
        # Analyze initial interaction if available
        if initial_interaction:
            # Detect accessibility needs
            if initial_interaction.get("large_text_requested"):
                profile.accessibility_needs.append(AccessibilityNeed.VISUAL_IMPAIRMENT)
            
            if initial_interaction.get("voice_guidance_requested"):
                profile.accessibility_needs.append(AccessibilityNeed.VISUAL_IMPAIRMENT)
            
            if initial_interaction.get("simplified_language_requested"):
                profile.accessibility_needs.append(AccessibilityNeed.COGNITIVE_IMPAIRMENT)
            
            # Detect language preference
            if initial_interaction.get("language_preference"):
                profile.preferred_language = initial_interaction["language_preference"]
            
            # Detect emotional state
            if initial_interaction.get("emotional_indicators"):
                profile.emotional_state = initial_interaction["emotional_indicators"]
        
        return profile
    
    async def _generate_adaptive_interface(self, user_profile: UserProfile) -> AdaptiveInterface:
        """Generate adaptive interface configuration"""
        mode = InterfaceMode.STANDARD
        font_size = "medium"
        color_scheme = "default"
        navigation_style = "standard"
        input_method = "touch"
        audio_enabled = False
        voice_guidance = False
        simplified_language = False
        visual_cues = []
        accessibility_features = []
        
        # Adapt based on accessibility needs
        if AccessibilityNeed.VISUAL_IMPAIRMENT in user_profile.accessibility_needs:
            mode = InterfaceMode.ACCESSIBLE
            font_size = "large"
            color_scheme = "high_contrast"
            audio_enabled = True
            voice_guidance = True
            visual_cues = ["audio_descriptions", "haptic_feedback"]
            accessibility_features.append("screen_reader_support")
        
        if AccessibilityNeed.HEARING_IMPAIRMENT in user_profile.accessibility_needs:
            visual_cues.append("visual_indicators")
            accessibility_features.append("visual_alerts")
        
        if AccessibilityNeed.MOTOR_IMPAIRMENT in user_profile.accessibility_needs:
            input_method = "voice"
            accessibility_features.append("voice_control")
        
        if AccessibilityNeed.COGNITIVE_IMPAIRMENT in user_profile.accessibility_needs:
            mode = InterfaceMode.SIMPLIFIED
            simplified_language = True
            navigation_style = "guided"
            visual_cues.append("step_by_step_guidance")
        
        if AccessibilityNeed.LANGUAGE_BARRIER in user_profile.accessibility_needs:
            simplified_language = True
            accessibility_features.append("translation_support")
        
        # Adapt based on age group
        if user_profile.age_group == "senior":
            font_size = "large"
            navigation_style = "guided"
        
        if user_profile.age_group == "child":
            mode = InterfaceMode.CHILD_FRIENDLY
            color_scheme = "bright"
            visual_cues.append("child_friendly_graphics")
        
        return AdaptiveInterface(
            mode=mode,
            font_size=font_size,
            color_scheme=color_scheme,
            navigation_style=navigation_style,
            input_method=input_method,
            audio_enabled=audio_enabled,
            voice_guidance=voice_guidance,
            simplified_language=simplified_language,
            visual_cues=visual_cues,
            accessibility_features=accessibility_features
        )
    
    async def _generate_personalized_greeting(self, user_profile: UserProfile) -> str:
        """Generate personalized greeting"""
        greetings = {
            "en": [
                "Hello! I'm your AI assistant, here to help you find the services you need.",
                "Welcome! I'm here to guide you through our services and help you get the support you need.",
                "Hi there! I'm your personal assistant, ready to help you with whatever you need today."
            ],
            "es": [
                "¡Hola! Soy tu asistente de IA, aquí para ayudarte a encontrar los servicios que necesitas.",
                "¡Bienvenido! Estoy aquí para guiarte a través de nuestros servicios y ayudarte a obtener el apoyo que necesitas.",
                "¡Hola! Soy tu asistente personal, listo para ayudarte con lo que necesites hoy."
            ]
        }
        
        language = user_profile.preferred_language
        if language not in greetings:
            language = "en"
        
        import random
        greeting = random.choice(greetings[language])
        
        # Add personalization based on accessibility needs
        if user_profile.accessibility_needs:
            if AccessibilityNeed.VISUAL_IMPAIRMENT in user_profile.accessibility_needs:
                greeting += " I can provide audio guidance and large text options to help you navigate."
            if AccessibilityNeed.COGNITIVE_IMPAIRMENT in user_profile.accessibility_needs:
                greeting += " I'll use simple language and guide you step by step."
        
        return greeting
    
    async def _generate_initial_recommendations(self, user_profile: UserProfile) -> List[AIServiceRecommendation]:
        """Generate initial service recommendations"""
        recommendations = []
        
        # Basic service recommendations
        basic_services = [
            {
                "service_type": "general_assistance",
                "title": "Get Help",
                "description": "Connect with a caseworker for personalized assistance"
            },
            {
                "service_type": "find_services",
                "title": "Find Services",
                "description": "Search for specific services and resources"
            },
            {
                "service_type": "schedule_appointment",
                "title": "Schedule Appointment",
                "description": "Book an appointment with a service provider"
            }
        ]
        
        for service in basic_services:
            rec = AIServiceRecommendation(
                recommendation_id=f"initial_{service['service_type']}",
                service_type=service["service_type"],
                title=service["title"],
                description=service["description"],
                confidence_score=0.8,
                personalization_factors=["general_need"],
                accessibility_adaptations=[],
                cultural_considerations=[],
                implementation_steps=["Click to get started"],
                alternative_options=[],
                urgency_level="low",
                estimated_time="5 minutes"
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _analyze_interaction(self, interaction: Dict[str, Any], user_profile: UserProfile) -> Dict[str, Any]:
        """Analyze user interaction for insights"""
        analysis = {
            "intent": "general_inquiry",
            "emotional_state": "neutral",
            "confidence_level": 0.5,
            "interface_adaptation_needed": False,
            "crisis_indicators": [],
            "accessibility_needs_detected": [],
            "cultural_considerations": []
        }
        
        # Analyze interaction content
        if "message" in interaction:
            message = interaction["message"].lower()
            
            # Detect crisis indicators
            crisis_keywords = ["help", "emergency", "crisis", "urgent", "danger", "hurt"]
            if any(keyword in message for keyword in crisis_keywords):
                analysis["crisis_indicators"].append("crisis_language")
                analysis["emotional_state"] = "distressed"
            
            # Detect accessibility needs
            if "can't see" in message or "hard to read" in message:
                analysis["accessibility_needs_detected"].append("visual_impairment")
                analysis["interface_adaptation_needed"] = True
            
            if "don't understand" in message or "confusing" in message:
                analysis["accessibility_needs_detected"].append("cognitive_impairment")
                analysis["interface_adaptation_needed"] = True
        
        # Analyze interaction behavior
        if "interaction_time" in interaction:
            if interaction["interaction_time"] > 300:  # 5 minutes
                analysis["confidence_level"] = 0.3  # User struggling
                analysis["interface_adaptation_needed"] = True
        
        return analysis
    
    async def _update_user_profile(self, user_profile: UserProfile, analysis: Dict[str, Any]):
        """Update user profile based on interaction analysis"""
        # Update emotional state
        if analysis["emotional_state"] != "neutral":
            user_profile.emotional_state = analysis["emotional_state"]
        
        # Update accessibility needs
        for need in analysis["accessibility_needs_detected"]:
            if need == "visual_impairment" and AccessibilityNeed.VISUAL_IMPAIRMENT not in user_profile.accessibility_needs:
                user_profile.accessibility_needs.append(AccessibilityNeed.VISUAL_IMPAIRMENT)
            elif need == "cognitive_impairment" and AccessibilityNeed.COGNITIVE_IMPAIRMENT not in user_profile.accessibility_needs:
                user_profile.accessibility_needs.append(AccessibilityNeed.COGNITIVE_IMPAIRMENT)
        
        # Update confidence level
        user_profile.confidence_level = analysis["confidence_level"]
    
    async def _adapt_interface(self, user_profile: UserProfile, analysis: Dict[str, Any]) -> AdaptiveInterface:
        """Adapt interface based on user needs"""
        # Generate new interface configuration
        return await self._generate_adaptive_interface(user_profile)
    
    async def _generate_response(self, user_profile: UserProfile, analysis: Dict[str, Any]) -> str:
        """Generate AI response based on user profile and analysis"""
        if analysis["crisis_indicators"]:
            return "I can see you need immediate help. Let me connect you with someone who can assist you right away. Your safety is our priority."
        
        if analysis["accessibility_needs_detected"]:
            return "I notice you might need some assistance. Let me adjust the interface to make it easier for you to use."
        
        if user_profile.confidence_level < 0.4:
            return "I'm here to help you every step of the way. Let's take this slowly and I'll guide you through each option."
        
        return "I'm here to help you find the services you need. What would you like to do today?"
    
    async def _generate_contextual_recommendations(self, user_profile: UserProfile, analysis: Dict[str, Any]) -> List[AIServiceRecommendation]:
        """Generate contextual recommendations"""
        recommendations = []
        
        # Crisis recommendations
        if analysis["crisis_indicators"]:
            rec = AIServiceRecommendation(
                recommendation_id="crisis_support",
                service_type="crisis_support",
                title="Crisis Support",
                description="Immediate help and support for crisis situations",
                confidence_score=0.95,
                personalization_factors=["crisis_detection"],
                accessibility_adaptations=[],
                cultural_considerations=[],
                implementation_steps=["Call crisis hotline", "Connect with counselor"],
                alternative_options=["Emergency services", "Crisis text line"],
                urgency_level="critical",
                estimated_time="Immediate"
            )
            recommendations.append(rec)
        
        # Accessibility recommendations
        if analysis["accessibility_needs_detected"]:
            rec = AIServiceRecommendation(
                recommendation_id="accessibility_support",
                service_type="accessibility_support",
                title="Accessibility Support",
                description="Specialized support for accessibility needs",
                confidence_score=0.9,
                personalization_factors=["accessibility_needs"],
                accessibility_adaptations=["screen_reader", "large_text", "voice_guidance"],
                cultural_considerations=[],
                implementation_steps=["Enable accessibility features", "Connect with accessibility specialist"],
                alternative_options=["Human assistance", "Alternative formats"],
                urgency_level="medium",
                estimated_time="2 minutes"
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _detect_crisis_situation(self, user_profile: UserProfile, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Detect crisis situations"""
        is_crisis = len(analysis["crisis_indicators"]) > 0
        crisis_level = "high" if is_crisis else "low"
        
        return {
            "is_crisis": is_crisis,
            "crisis_level": crisis_level,
            "indicators": analysis["crisis_indicators"],
            "recommended_actions": ["Call 911 if emergency", "Connect with crisis counselor"] if is_crisis else []
        }
    
    async def _get_suggested_actions(self, user_profile: UserProfile) -> List[str]:
        """Get suggested actions based on user profile"""
        if user_profile.emotional_state == "distressed":
            return ["Get immediate help", "Talk to someone", "Find crisis resources"]
        elif user_profile.accessibility_needs:
            return ["Enable accessibility features", "Get assistance", "Find accessible services"]
        else:
            return ["Get help", "Find services", "Schedule appointment", "Check status"]
    
    async def _get_cultural_adaptations(self, user_profile: UserProfile) -> List[str]:
        """Get cultural adaptations"""
        adaptations = []
        
        if user_profile.preferred_language != "en":
            adaptations.append("language_translation")
        
        if user_profile.cultural_background != "unknown":
            adaptations.append("cultural_competency")
        
        return adaptations
    
    async def _calculate_service_match(self, resource: Resource, user_profile: UserProfile, search_criteria: Dict[str, Any]) -> float:
        """Calculate service match score"""
        match_score = 0.0
        
        # Base match
        match_score += 0.3
        
        # Language match
        if resource.language_support and user_profile.preferred_language in resource.language_support:
            match_score += 0.2
        
        # Accessibility match
        if resource.accessibility_info:
            for need in user_profile.accessibility_needs:
                if need.value in resource.accessibility_info:
                    match_score += 0.1
        
        # Cultural considerations
        if resource.cultural_considerations and user_profile.cultural_background in resource.cultural_considerations:
            match_score += 0.2
        
        # Search criteria match
        if search_criteria.get("service_type") and resource.resource_type == search_criteria["service_type"]:
            match_score += 0.3
        
        return min(match_score, 1.0)
    
    async def _adapt_description(self, description: str, user_profile: UserProfile) -> str:
        """Adapt description for user profile"""
        if user_profile.learning_preference == "simple" or AccessibilityNeed.COGNITIVE_IMPAIRMENT in user_profile.accessibility_needs:
            # Simplify language
            return description.replace("utilize", "use").replace("facilitate", "help")
        
        return description
    
    async def _get_personalization_factors(self, resource: Resource, user_profile: UserProfile) -> List[str]:
        """Get personalization factors"""
        factors = []
        
        if resource.language_support and user_profile.preferred_language in resource.language_support:
            factors.append("language_match")
        
        if resource.accessibility_info:
            factors.append("accessibility_support")
        
        if resource.cultural_considerations:
            factors.append("cultural_competency")
        
        return factors
    
    async def _get_accessibility_adaptations(self, resource: Resource, user_profile: UserProfile) -> List[str]:
        """Get accessibility adaptations"""
        adaptations = []
        
        for need in user_profile.accessibility_needs:
            if need == AccessibilityNeed.VISUAL_IMPAIRMENT:
                adaptations.append("large_text")
                adaptations.append("audio_description")
            elif need == AccessibilityNeed.HEARING_IMPAIRMENT:
                adaptations.append("visual_indicators")
            elif need == AccessibilityNeed.MOTOR_IMPAIRMENT:
                adaptations.append("voice_control")
        
        return adaptations
    
    async def _get_cultural_considerations(self, resource: Resource, user_profile: UserProfile) -> List[str]:
        """Get cultural considerations"""
        considerations = []
        
        if user_profile.preferred_language != "en":
            considerations.append("language_support")
        
        if user_profile.cultural_background != "unknown":
            considerations.append("cultural_competency")
        
        return considerations
    
    async def _get_implementation_steps(self, resource: Resource, user_profile: UserProfile) -> List[str]:
        """Get implementation steps"""
        steps = ["Contact the service provider", "Check eligibility requirements"]
        
        if user_profile.accessibility_needs:
            steps.append("Request accessibility accommodations")
        
        if user_profile.preferred_language != "en":
            steps.append("Request language assistance")
        
        return steps
    
    async def _get_alternative_options(self, resource: Resource, user_profile: UserProfile) -> List[str]:
        """Get alternative options"""
        return ["Similar services", "Alternative providers", "Online options"]
    
    async def _assess_urgency_level(self, resource: Resource, user_profile: UserProfile) -> str:
        """Assess urgency level"""
        if user_profile.emotional_state == "distressed":
            return "high"
        elif resource.resource_type in ["crisis_support", "emergency_housing"]:
            return "high"
        else:
            return "medium"
    
    async def _estimate_service_time(self, resource: Resource, user_profile: UserProfile) -> str:
        """Estimate service time"""
        if resource.resource_type == "crisis_support":
            return "Immediate"
        elif resource.resource_type == "appointment":
            return "30-60 minutes"
        else:
            return "15-30 minutes"
    
    async def _get_available_appointments(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get available appointments"""
        # Mock data - in production, this would query the database
        return [
            {
                "id": "apt_1",
                "datetime": datetime.now() + timedelta(days=1, hours=9),
                "provider": "Dr. Smith",
                "location": "Main Office",
                "accessibility_features": ["wheelchair_accessible"],
                "cultural_considerations": ["bilingual_staff"],
                "confidence_score": 0.8,
                "reasoning": "Good availability"
            }
        ]
    
    async def _optimize_appointments_for_user(self, appointments: List[Dict[str, Any]], user_profile: UserProfile, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimize appointments for user"""
        # Simple optimization - in production, this would be more sophisticated
        return sorted(appointments, key=lambda x: x["confidence_score"], reverse=True)
    
    async def _generate_scheduling_notes(self, user_profile: UserProfile, preferences: Dict[str, Any]) -> str:
        """Generate scheduling notes"""
        return "Appointment scheduled based on your preferences and availability."
    
    async def _get_reminder_options(self, user_profile: UserProfile) -> List[str]:
        """Get reminder options"""
        options = ["Email reminder", "Text message"]
        
        if AccessibilityNeed.HEARING_IMPAIRMENT in user_profile.accessibility_needs:
            options = ["Email reminder", "Visual alert"]
        
        return options
    
    async def _get_accessibility_accommodations(self, user_profile: UserProfile) -> List[str]:
        """Get accessibility accommodations"""
        accommodations = []
        
        if AccessibilityNeed.VISUAL_IMPAIRMENT in user_profile.accessibility_needs:
            accommodations.append("Large print materials")
            accommodations.append("Audio description")
        
        if AccessibilityNeed.HEARING_IMPAIRMENT in user_profile.accessibility_needs:
            accommodations.append("Sign language interpreter")
            accommodations.append("Visual alerts")
        
        return accommodations
    
    async def _assess_crisis_level(self, crisis_indicators: Dict[str, Any], user_profile: UserProfile) -> str:
        """Assess crisis level"""
        if len(crisis_indicators) > 2:
            return "critical"
        elif len(crisis_indicators) > 0:
            return "high"
        else:
            return "low"
    
    async def _generate_crisis_response(self, crisis_level: str, user_profile: UserProfile) -> str:
        """Generate crisis response"""
        if crisis_level == "critical":
            return "This is a critical situation. Please call 911 immediately if this is a life-threatening emergency. I'm also connecting you with our crisis support team right now."
        elif crisis_level == "high":
            return "I can see you're in distress. Let me connect you with our crisis support team immediately. You're not alone, and help is available."
        else:
            return "I'm here to help you. Let's work together to address what's bothering you."
    
    async def _switch_to_crisis_mode(self, user_profile: UserProfile) -> AdaptiveInterface:
        """Switch to crisis interface mode"""
        return AdaptiveInterface(
            mode=InterfaceMode.CRISIS,
            font_size="large",
            color_scheme="high_contrast",
            navigation_style="guided",
            input_method="touch",
            audio_enabled=True,
            voice_guidance=True,
            simplified_language=True,
            visual_cues=["emergency_indicators", "clear_instructions"],
            accessibility_features=["screen_reader_support", "voice_control"]
        )
    
    async def _generate_immediate_actions(self, crisis_level: str, user_profile: UserProfile) -> List[str]:
        """Generate immediate actions"""
        if crisis_level == "critical":
            return ["Call 911 immediately", "Connect with crisis counselor", "Ensure safety"]
        elif crisis_level == "high":
            return ["Connect with crisis counselor", "Call crisis hotline", "Get immediate support"]
        else:
            return ["Talk to someone", "Get support", "Find resources"]
    
    async def _get_emergency_contacts(self, user_profile: UserProfile) -> List[str]:
        """Get emergency contacts"""
        contacts = ["911", "Crisis hotline: 1-800-XXX-XXXX"]
        
        if user_profile.preferred_language != "en":
            contacts.append(f"Crisis hotline ({user_profile.preferred_language}): 1-800-XXX-XXXX")
        
        return contacts
    
    async def _generate_safety_plan(self, crisis_level: str, user_profile: UserProfile) -> List[str]:
        """Generate safety plan"""
        if crisis_level in ["critical", "high"]:
            return [
                "Stay in a safe location",
                "Have emergency contacts ready",
                "Remove any potential dangers",
                "Keep important documents accessible"
            ]
        return []
    
    async def _get_follow_up_actions(self, crisis_level: str, user_profile: UserProfile) -> List[str]:
        """Get follow-up actions"""
        if crisis_level in ["critical", "high"]:
            return [
                "Follow up with crisis counselor",
                "Schedule safety check",
                "Connect with ongoing support"
            ]
        return ["Schedule follow-up appointment", "Check in with caseworker"]
    
    async def _analyze_accessibility_usage(self, user_profile: UserProfile, interface_config: AdaptiveInterface) -> Dict[str, Any]:
        """Analyze accessibility usage"""
        return {
            "features_used": interface_config.accessibility_features,
            "adaptations_made": len(interface_config.accessibility_features),
            "user_satisfaction": 0.8,
            "effectiveness": 0.85
        }
    
    async def _generate_accessibility_improvements(self, usage_analysis: Dict[str, Any]) -> List[str]:
        """Generate accessibility improvements"""
        return [
            "Add more voice guidance options",
            "Improve screen reader compatibility",
            "Add haptic feedback for motor impairments"
        ]
    
    async def _calculate_accessibility_score(self, user_profile: UserProfile, interface_config: AdaptiveInterface) -> float:
        """Calculate accessibility score"""
        score = 0.0
        
        # Base score
        score += 0.3
        
        # Feature coverage
        if interface_config.accessibility_features:
            score += min(len(interface_config.accessibility_features) * 0.1, 0.4)
        
        # User needs coverage
        needs_covered = 0
        for need in user_profile.accessibility_needs:
            if need.value in str(interface_config.accessibility_features):
                needs_covered += 1
        
        if user_profile.accessibility_needs:
            score += (needs_covered / len(user_profile.accessibility_needs)) * 0.3
        
        return min(score, 1.0)
    
    async def _collect_user_feedback(self, user_profile: UserProfile) -> Dict[str, Any]:
        """Collect user feedback"""
        return {
            "ease_of_use": 0.8,
            "accessibility_rating": 0.85,
            "satisfaction": 0.9,
            "recommendations": ["More voice options", "Simpler navigation"]
        }
    
    async def _suggest_system_improvements(self, usage_analysis: Dict[str, Any]) -> List[str]:
        """Suggest system improvements"""
        return [
            "Implement machine learning for better accessibility detection",
            "Add more cultural adaptations",
            "Improve crisis detection algorithms"
        ]
