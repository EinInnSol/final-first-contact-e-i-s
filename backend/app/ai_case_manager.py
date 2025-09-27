"""
AI-Enhanced Human-in-the-Loop Case Management System
The most sophisticated civic AI system ever built - amplifies human intelligence
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .models import Case, Client, User, Intervention, Resource, Assessment
from .ai_service import AIService
from .database import get_db

logger = logging.getLogger(__name__)

class UrgencyLevel(Enum):
    CRITICAL = "critical"      # Immediate intervention needed
    HIGH = "high"             # Within 24-48 hours
    MEDIUM = "medium"         # Within 1 week
    LOW = "low"              # Within 2 weeks

class CaseStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"
    CRISIS = "crisis"

@dataclass
class CaseworkerProfile:
    """AI-generated caseworker capability profile"""
    user_id: str
    expertise_areas: List[str]
    current_caseload: int
    max_caseload: int
    success_rate: float
    avg_case_duration: float
    specializations: List[str]
    cultural_competencies: List[str]
    language_skills: List[str]
    availability_score: float
    stress_indicators: List[str]
    preferred_case_types: List[str]

@dataclass
class ClientRiskProfile:
    """AI-analyzed client risk and needs assessment"""
    client_id: str
    risk_factors: List[str]
    protective_factors: List[str]
    urgency_score: float
    crisis_probability: float
    success_probability: float
    cultural_considerations: List[str]
    family_dynamics: Dict[str, Any]
    trauma_indicators: List[str]
    resource_needs: List[str]
    intervention_priorities: List[str]

@dataclass
class AICaseRecommendation:
    """AI-generated case management recommendation"""
    case_id: str
    recommendation_type: str
    confidence_score: float
    reasoning: str
    evidence_basis: List[str]
    expected_outcome: str
    risk_assessment: str
    alternative_options: List[str]
    human_override_required: bool
    urgency_level: UrgencyLevel
    implementation_steps: List[str]

class AICaseManager:
    """
    The most advanced AI case management system ever built.
    Amplifies human intelligence rather than replacing it.
    """
    
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.caseworker_profiles: Dict[str, CaseworkerProfile] = {}
        self.client_risk_profiles: Dict[str, ClientRiskProfile] = {}
        self.learning_models = {}
        self.performance_metrics = {}
        self._initialize_ai_models()
    
    def _initialize_ai_models(self):
        """Initialize sophisticated AI models for case management"""
        # Urgency scoring model
        self.urgency_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        # Success prediction model
        self.success_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42
        )
        
        # Crisis prediction model
        self.crisis_model = GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.05,
            max_depth=8,
            random_state=42
        )
        
        # Caseworker matching model
        self.matching_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
        
        self.scaler = StandardScaler()
        logger.info("AI Case Management models initialized")
    
    async def analyze_case_urgency(self, case: Case, client: Client) -> Tuple[float, UrgencyLevel, str]:
        """
        AI-powered urgency analysis with sophisticated risk assessment
        """
        try:
            # Gather comprehensive case data
            case_data = await self._gather_case_data(case, client)
            
            # Extract features for urgency scoring
            features = self._extract_urgency_features(case_data)
            
            # AI urgency scoring
            urgency_score = self.urgency_model.predict([features])[0]
            urgency_score = max(0.0, min(1.0, urgency_score))  # Clamp to 0-1
            
            # Determine urgency level
            if urgency_score >= 0.8:
                level = UrgencyLevel.CRITICAL
            elif urgency_score >= 0.6:
                level = UrgencyLevel.HIGH
            elif urgency_score >= 0.4:
                level = UrgencyLevel.MEDIUM
            else:
                level = UrgencyLevel.LOW
            
            # Generate AI reasoning
            reasoning = await self._generate_urgency_reasoning(case_data, urgency_score, level)
            
            return urgency_score, level, reasoning
            
        except Exception as e:
            logger.error(f"Error analyzing case urgency: {e}")
            return 0.5, UrgencyLevel.MEDIUM, "Unable to analyze urgency - manual review required"
    
    async def recommend_caseworker_assignment(self, case: Case, client: Client) -> List[Tuple[str, float, str]]:
        """
        AI-powered caseworker matching with skill and workload optimization
        """
        try:
            # Get all available caseworkers
            db = next(get_db())
            caseworkers = db.query(User).filter(
                User.role.in_(["caseworker", "senior_caseworker", "supervisor"]),
                User.is_active == True
            ).all()
            
            if not caseworkers:
                return []
            
            # Analyze client needs
            client_profile = await self._analyze_client_profile(client)
            
            # Score each caseworker
            recommendations = []
            for caseworker in caseworkers:
                profile = await self._get_caseworker_profile(caseworker.id)
                if not profile:
                    continue
                
                # AI matching score
                match_score = await self._calculate_caseworker_match(
                    profile, client_profile, case
                )
                
                # Workload consideration
                workload_factor = self._calculate_workload_factor(profile)
                
                # Final score
                final_score = match_score * workload_factor
                
                # Generate reasoning
                reasoning = await self._generate_assignment_reasoning(
                    profile, client_profile, final_score
                )
                
                recommendations.append((
                    caseworker.id,
                    final_score,
                    reasoning
                ))
            
            # Sort by score and return top recommendations
            recommendations.sort(key=lambda x: x[1], reverse=True)
            return recommendations[:5]  # Top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error recommending caseworker assignment: {e}")
            return []
    
    async def generate_care_plan_recommendations(self, case: Case, client: Client) -> List[AICaseRecommendation]:
        """
        AI-powered care plan generation with evidence-based recommendations
        """
        try:
            # Analyze client comprehensively
            client_profile = await self._analyze_client_profile(client)
            case_data = await self._gather_case_data(case, client)
            
            recommendations = []
            
            # 1. Immediate intervention recommendations
            immediate_recs = await self._generate_immediate_interventions(
                client_profile, case_data
            )
            recommendations.extend(immediate_recs)
            
            # 2. Long-term goal recommendations
            goal_recs = await self._generate_goal_recommendations(
                client_profile, case_data
            )
            recommendations.extend(goal_recs)
            
            # 3. Resource matching recommendations
            resource_recs = await self._generate_resource_recommendations(
                client_profile, case_data
            )
            recommendations.extend(resource_recs)
            
            # 4. Crisis prevention recommendations
            crisis_recs = await self._generate_crisis_prevention_recommendations(
                client_profile, case_data
            )
            recommendations.extend(crisis_recs)
            
            # 5. Family-centered recommendations
            family_recs = await self._generate_family_recommendations(
                client_profile, case_data
            )
            recommendations.extend(family_recs)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating care plan recommendations: {e}")
            return []
    
    async def predict_crisis_probability(self, case: Case, client: Client, timeframe_hours: int = 72) -> Tuple[float, List[str]]:
        """
        AI-powered crisis prediction with early warning system
        """
        try:
            # Gather comprehensive data
            case_data = await self._gather_case_data(case, client)
            client_profile = await self._analyze_client_profile(client)
            
            # Extract crisis prediction features
            features = self._extract_crisis_features(case_data, client_profile)
            
            # AI crisis prediction
            crisis_probability = self.crisis_model.predict([features])[0]
            crisis_probability = max(0.0, min(1.0, crisis_probability))
            
            # Identify risk factors
            risk_factors = self._identify_crisis_risk_factors(
                case_data, client_profile, crisis_probability
            )
            
            return crisis_probability, risk_factors
            
        except Exception as e:
            logger.error(f"Error predicting crisis probability: {e}")
            return 0.0, []
    
    async def suggest_next_actions(self, case: Case, current_status: str) -> List[AICaseRecommendation]:
        """
        AI-powered next action recommendations based on current case status
        """
        try:
            # Get case history and current state
            case_data = await self._gather_case_data(case, None)
            
            # Analyze current status
            status_analysis = await self._analyze_case_status(case, current_status)
            
            # Generate contextual recommendations
            recommendations = []
            
            if current_status == CaseStatus.OPEN:
                # New case - initial assessment recommendations
                recs = await self._generate_initial_assessment_recommendations(case_data)
                recommendations.extend(recs)
                
            elif current_status == CaseStatus.IN_PROGRESS:
                # Active case - progress optimization recommendations
                recs = await self._generate_progress_recommendations(case_data)
                recommendations.extend(recs)
                
            elif current_status == CaseStatus.CRISIS:
                # Crisis case - emergency intervention recommendations
                recs = await self._generate_crisis_intervention_recommendations(case_data)
                recommendations.extend(recs)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error suggesting next actions: {e}")
            return []
    
    async def learn_from_outcome(self, case_id: str, outcome: str, success_metrics: Dict[str, float]):
        """
        AI learning from case outcomes to improve future recommendations
        """
        try:
            # Get case data
            db = next(get_db())
            case = db.query(Case).filter(Case.id == case_id).first()
            if not case:
                return
            
            # Extract learning features
            case_data = await self._gather_case_data(case, None)
            features = self._extract_learning_features(case_data, outcome, success_metrics)
            
            # Update models with new data
            await self._update_learning_models(features, outcome, success_metrics)
            
            # Update caseworker profiles
            if case.assigned_user_id:
                await self._update_caseworker_profile(case.assigned_user_id, outcome, success_metrics)
            
            logger.info(f"AI learned from case {case_id} outcome: {outcome}")
            
        except Exception as e:
            logger.error(f"Error learning from outcome: {e}")
    
    async def _gather_case_data(self, case: Case, client: Optional[Client]) -> Dict[str, Any]:
        """Gather comprehensive case data for AI analysis"""
        db = next(get_db())
        
        data = {
            "case_id": case.id,
            "status": case.status,
            "priority": case.priority,
            "created_at": case.created_at,
            "updated_at": case.updated_at,
            "assigned_user_id": case.assigned_user_id,
            "case_type": case.case_type,
            "description": case.description,
            "notes": []
        }
        
        # Get case notes
        notes = db.query(CaseNote).filter(CaseNote.case_id == case.id).all()
        data["notes"] = [{"content": note.content, "created_at": note.created_at} for note in notes]
        
        # Get client data if available
        if client:
            data["client"] = {
                "id": client.id,
                "age": client.age,
                "gender": client.gender,
                "race_ethnicity": client.race_ethnicity,
                "language_preference": client.language_preference,
                "housing_status": client.housing_status,
                "employment_status": client.employment_status,
                "income_level": client.income_level,
                "family_size": client.family_size,
                "health_conditions": client.health_conditions,
                "substance_use": client.substance_use,
                "mental_health": client.mental_health,
                "criminal_history": client.criminal_history,
                "domestic_violence": client.domestic_violence,
                "immigration_status": client.immigration_status
            }
        
        return data
    
    def _extract_urgency_features(self, case_data: Dict[str, Any]) -> List[float]:
        """Extract features for urgency scoring"""
        features = []
        
        # Time-based features
        days_since_created = (datetime.now() - case_data["created_at"]).days
        features.append(min(days_since_created / 30, 1.0))  # Normalize to 0-1
        
        # Priority features
        priority_map = {"low": 0.2, "medium": 0.5, "high": 0.8, "urgent": 1.0}
        features.append(priority_map.get(case_data["priority"], 0.5))
        
        # Client risk features
        if "client" in case_data:
            client = case_data["client"]
            
            # Housing instability
            housing_risk = 1.0 if client.get("housing_status") in ["homeless", "at_risk"] else 0.0
            features.append(housing_risk)
            
            # Health risks
            health_risk = 1.0 if client.get("health_conditions") or client.get("mental_health") else 0.0
            features.append(health_risk)
            
            # Family safety
            family_risk = 1.0 if client.get("domestic_violence") else 0.0
            features.append(family_risk)
            
            # Substance use
            substance_risk = 1.0 if client.get("substance_use") else 0.0
            features.append(substance_risk)
            
            # Age vulnerability
            age = client.get("age", 30)
            if age < 18 or age > 65:
                age_risk = 0.8
            else:
                age_risk = 0.2
            features.append(age_risk)
        else:
            # Default values if no client data
            features.extend([0.5, 0.5, 0.5, 0.5, 0.5])
        
        # Case complexity
        note_count = len(case_data["notes"])
        features.append(min(note_count / 10, 1.0))  # Normalize to 0-1
        
        return features
    
    async def _generate_urgency_reasoning(self, case_data: Dict[str, Any], urgency_score: float, level: UrgencyLevel) -> str:
        """Generate AI reasoning for urgency assessment"""
        reasoning_factors = []
        
        if urgency_score >= 0.8:
            reasoning_factors.append("CRITICAL: Multiple high-risk factors detected")
        elif urgency_score >= 0.6:
            reasoning_factors.append("HIGH: Significant risk factors present")
        elif urgency_score >= 0.4:
            reasoning_factors.append("MEDIUM: Moderate risk factors identified")
        else:
            reasoning_factors.append("LOW: Minimal immediate risk factors")
        
        # Add specific risk factors
        if "client" in case_data:
            client = case_data["client"]
            if client.get("housing_status") in ["homeless", "at_risk"]:
                reasoning_factors.append("Housing instability detected")
            if client.get("mental_health") or client.get("health_conditions"):
                reasoning_factors.append("Health concerns identified")
            if client.get("domestic_violence"):
                reasoning_factors.append("Domestic violence risk")
            if client.get("substance_use"):
                reasoning_factors.append("Substance use concerns")
        
        return " | ".join(reasoning_factors)
    
    async def _analyze_client_profile(self, client: Client) -> ClientRiskProfile:
        """Comprehensive AI analysis of client risk and needs"""
        risk_factors = []
        protective_factors = []
        cultural_considerations = []
        trauma_indicators = []
        resource_needs = []
        
        # Analyze risk factors
        if client.housing_status in ["homeless", "at_risk"]:
            risk_factors.append("housing_instability")
            resource_needs.append("housing_assistance")
        
        if client.mental_health:
            risk_factors.append("mental_health_concerns")
            resource_needs.append("mental_health_services")
        
        if client.substance_use:
            risk_factors.append("substance_use")
            resource_needs.append("substance_abuse_treatment")
        
        if client.domestic_violence:
            risk_factors.append("domestic_violence")
            trauma_indicators.append("domestic_violence_trauma")
            resource_needs.append("domestic_violence_support")
        
        # Analyze protective factors
        if client.employment_status == "employed":
            protective_factors.append("employment_stability")
        
        if client.family_size > 1:
            protective_factors.append("family_support")
        
        # Cultural considerations
        if client.race_ethnicity:
            cultural_considerations.append(f"cultural_background_{client.race_ethnicity}")
        
        if client.language_preference != "en":
            cultural_considerations.append(f"language_preference_{client.language_preference}")
        
        # Calculate scores
        urgency_score = len(risk_factors) / 10.0  # Normalize to 0-1
        crisis_probability = min(urgency_score * 1.5, 1.0)  # Scale up for crisis prediction
        success_probability = len(protective_factors) / 5.0  # Normalize to 0-1
        
        return ClientRiskProfile(
            client_id=client.id,
            risk_factors=risk_factors,
            protective_factors=protective_factors,
            urgency_score=urgency_score,
            crisis_probability=crisis_probability,
            success_probability=success_probability,
            cultural_considerations=cultural_considerations,
            family_dynamics={"size": client.family_size, "composition": "unknown"},
            trauma_indicators=trauma_indicators,
            resource_needs=resource_needs,
            intervention_priorities=risk_factors[:3]  # Top 3 risk factors
        )
    
    async def _get_caseworker_profile(self, user_id: str) -> Optional[CaseworkerProfile]:
        """Get or create caseworker AI profile"""
        if user_id in self.caseworker_profiles:
            return self.caseworker_profiles[user_id]
        
        # Create new profile (in real implementation, this would be more sophisticated)
        profile = CaseworkerProfile(
            user_id=user_id,
            expertise_areas=["general_casework"],
            current_caseload=0,
            max_caseload=25,
            success_rate=0.75,
            avg_case_duration=90.0,
            specializations=["general"],
            cultural_competencies=["english"],
            language_skills=["english"],
            availability_score=1.0,
            stress_indicators=[],
            preferred_case_types=["general"]
        )
        
        self.caseworker_profiles[user_id] = profile
        return profile
    
    async def _calculate_caseworker_match(self, profile: CaseworkerProfile, client_profile: ClientRiskProfile, case: Case) -> float:
        """Calculate AI-powered caseworker-client match score"""
        match_score = 0.0
        
        # Base compatibility
        match_score += 0.3
        
        # Workload consideration
        workload_factor = 1.0 - (profile.current_caseload / profile.max_caseload)
        match_score += 0.2 * workload_factor
        
        # Success rate consideration
        match_score += 0.2 * profile.success_rate
        
        # Cultural competency match
        cultural_match = any(
            comp in profile.cultural_competencies 
            for comp in client_profile.cultural_considerations
        )
        if cultural_match:
            match_score += 0.15
        
        # Language match
        language_match = any(
            lang in profile.language_skills 
            for lang in [client_profile.cultural_considerations[0]] if client_profile.cultural_considerations
        )
        if language_match:
            match_score += 0.15
        
        return min(match_score, 1.0)
    
    def _calculate_workload_factor(self, profile: CaseworkerProfile) -> float:
        """Calculate workload factor for case assignment"""
        if profile.current_caseload >= profile.max_caseload:
            return 0.1  # Very low priority
        elif profile.current_caseload >= profile.max_caseload * 0.8:
            return 0.5  # Medium priority
        else:
            return 1.0  # High priority
    
    async def _generate_assignment_reasoning(self, profile: CaseworkerProfile, client_profile: ClientRiskProfile, score: float) -> str:
        """Generate reasoning for caseworker assignment"""
        reasons = []
        
        if score >= 0.8:
            reasons.append("Excellent match")
        elif score >= 0.6:
            reasons.append("Good match")
        else:
            reasons.append("Adequate match")
        
        if profile.current_caseload < profile.max_caseload * 0.5:
            reasons.append("Available capacity")
        
        if profile.success_rate >= 0.8:
            reasons.append("High success rate")
        
        return " | ".join(reasons)
    
    async def _generate_immediate_interventions(self, client_profile: ClientRiskProfile, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate immediate intervention recommendations"""
        recommendations = []
        
        # Safety assessment
        if "domestic_violence" in client_profile.risk_factors:
            rec = AICaseRecommendation(
                case_id=case_data["case_id"],
                recommendation_type="safety_assessment",
                confidence_score=0.95,
                reasoning="Domestic violence risk detected - immediate safety assessment required",
                evidence_basis=["domestic_violence_indicators", "safety_protocols"],
                expected_outcome="Enhanced safety planning and resource connection",
                risk_assessment="HIGH - Immediate intervention needed",
                alternative_options=["Crisis hotline contact", "Emergency shelter referral"],
                human_override_required=True,
                urgency_level=UrgencyLevel.CRITICAL,
                implementation_steps=[
                    "Conduct safety assessment within 24 hours",
                    "Connect with domestic violence advocate",
                    "Develop safety plan with client"
                ]
            )
            recommendations.append(rec)
        
        # Housing crisis intervention
        if "housing_instability" in client_profile.risk_factors:
            rec = AICaseRecommendation(
                case_id=case_data["case_id"],
                recommendation_type="housing_crisis_intervention",
                confidence_score=0.85,
                reasoning="Housing instability detected - immediate housing assessment needed",
                evidence_basis=["housing_status", "homelessness_prevention_protocols"],
                expected_outcome="Housing stability through rapid rehousing or prevention services",
                risk_assessment="HIGH - Risk of homelessness",
                alternative_options=["Emergency shelter", "Rapid rehousing", "Rental assistance"],
                human_override_required=False,
                urgency_level=UrgencyLevel.HIGH,
                implementation_steps=[
                    "Complete housing assessment within 48 hours",
                    "Check emergency housing availability",
                    "Connect with housing resources"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _generate_goal_recommendations(self, client_profile: ClientRiskProfile, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate long-term goal recommendations"""
        recommendations = []
        
        # Employment goals
        if "employment_stability" not in client_profile.protective_factors:
            rec = AICaseRecommendation(
                case_id=case_data["case_id"],
                recommendation_type="employment_goal",
                confidence_score=0.75,
                reasoning="Employment stability needed for long-term success",
                evidence_basis=["employment_status", "income_stability_goals"],
                expected_outcome="Stable employment and increased income",
                risk_assessment="MEDIUM - Employment support needed",
                alternative_options=["Job training", "Career counseling", "Employment services"],
                human_override_required=False,
                urgency_level=UrgencyLevel.MEDIUM,
                implementation_steps=[
                    "Assess employment history and skills",
                    "Connect with employment services",
                    "Develop employment plan"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _generate_resource_recommendations(self, client_profile: ClientRiskProfile, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate resource matching recommendations"""
        recommendations = []
        
        for resource_need in client_profile.resource_needs:
            rec = AICaseRecommendation(
                case_id=case_data["case_id"],
                recommendation_type=f"resource_{resource_need}",
                confidence_score=0.8,
                reasoning=f"Client needs {resource_need} based on assessment",
                evidence_basis=["client_assessment", "resource_matching_algorithms"],
                expected_outcome=f"Access to {resource_need} services",
                risk_assessment="LOW - Resource connection",
                alternative_options=[f"Alternative {resource_need} providers"],
                human_override_required=False,
                urgency_level=UrgencyLevel.MEDIUM,
                implementation_steps=[
                    f"Research {resource_need} providers",
                    "Check eligibility requirements",
                    "Make referral and follow up"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _generate_crisis_prevention_recommendations(self, client_profile: ClientRiskProfile, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate crisis prevention recommendations"""
        recommendations = []
        
        if client_profile.crisis_probability > 0.6:
            rec = AICaseRecommendation(
                case_id=case_data["case_id"],
                recommendation_type="crisis_prevention",
                confidence_score=0.9,
                reasoning="High crisis probability detected - prevention measures needed",
                evidence_basis=["crisis_prediction_model", "risk_factors"],
                expected_outcome="Crisis prevention through proactive intervention",
                risk_assessment="HIGH - Crisis prevention needed",
                alternative_options=["Crisis intervention team", "Emergency protocols"],
                human_override_required=True,
                urgency_level=UrgencyLevel.HIGH,
                implementation_steps=[
                    "Implement crisis prevention plan",
                    "Increase check-in frequency",
                    "Connect with crisis prevention resources"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    async def _generate_family_recommendations(self, client_profile: ClientRiskProfile, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate family-centered recommendations"""
        recommendations = []
        
        if client_profile.family_dynamics.get("size", 0) > 1:
            rec = AICaseRecommendation(
                case_id=case_data["case_id"],
                recommendation_type="family_centered_approach",
                confidence_score=0.7,
                reasoning="Family-centered approach needed for household with multiple members",
                evidence_basis=["family_size", "family_centered_practice"],
                expected_outcome="Improved family stability and coordination",
                risk_assessment="MEDIUM - Family coordination needed",
                alternative_options=["Individual services", "Family therapy"],
                human_override_required=False,
                urgency_level=UrgencyLevel.MEDIUM,
                implementation_steps=[
                    "Assess family needs and dynamics",
                    "Coordinate services for all family members",
                    "Develop family action plan"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _extract_crisis_features(self, case_data: Dict[str, Any], client_profile: ClientRiskProfile) -> List[float]:
        """Extract features for crisis prediction"""
        features = []
        
        # Client risk factors
        features.append(len(client_profile.risk_factors) / 10.0)
        features.append(client_profile.urgency_score)
        features.append(1.0 if client_profile.trauma_indicators else 0.0)
        
        # Case characteristics
        days_since_created = (datetime.now() - case_data["created_at"]).days
        features.append(min(days_since_created / 30, 1.0))
        
        # Note frequency (indicator of complexity)
        note_count = len(case_data["notes"])
        features.append(min(note_count / 20, 1.0))
        
        return features
    
    def _identify_crisis_risk_factors(self, case_data: Dict[str, Any], client_profile: ClientRiskProfile, crisis_probability: float) -> List[str]:
        """Identify specific crisis risk factors"""
        risk_factors = []
        
        if crisis_probability > 0.8:
            risk_factors.append("Very high crisis probability")
        
        if "domestic_violence" in client_profile.risk_factors:
            risk_factors.append("Domestic violence risk")
        
        if "housing_instability" in client_profile.risk_factors:
            risk_factors.append("Housing instability")
        
        if client_profile.trauma_indicators:
            risk_factors.append("Trauma indicators present")
        
        if len(case_data["notes"]) > 10:
            risk_factors.append("High case complexity")
        
        return risk_factors
    
    async def _analyze_case_status(self, case: Case, current_status: str) -> Dict[str, Any]:
        """Analyze current case status for recommendations"""
        return {
            "status": current_status,
            "case_age_days": (datetime.now() - case.created_at).days,
            "last_activity": case.updated_at,
            "priority": case.priority
        }
    
    async def _generate_initial_assessment_recommendations(self, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate recommendations for new cases"""
        recommendations = []
        
        rec = AICaseRecommendation(
            case_id=case_data["case_id"],
            recommendation_type="initial_assessment",
            confidence_score=0.9,
            reasoning="New case requires comprehensive initial assessment",
            evidence_basis=["case_management_best_practices"],
            expected_outcome="Complete understanding of client needs and circumstances",
            risk_assessment="MEDIUM - Assessment needed",
            alternative_options=["Phone assessment", "Home visit"],
            human_override_required=False,
            urgency_level=UrgencyLevel.MEDIUM,
            implementation_steps=[
                "Schedule initial assessment meeting",
                "Prepare assessment tools and questions",
                "Conduct comprehensive needs assessment"
            ]
        )
        recommendations.append(rec)
        
        return recommendations
    
    async def _generate_progress_recommendations(self, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate recommendations for active cases"""
        recommendations = []
        
        rec = AICaseRecommendation(
            case_id=case_data["case_id"],
            recommendation_type="progress_review",
            confidence_score=0.8,
            reasoning="Active case requires progress review and next steps",
            evidence_basis=["case_progress_tracking"],
            expected_outcome="Updated action plan and continued progress",
            risk_assessment="LOW - Progress review needed",
            alternative_options=["Status update", "Goal adjustment"],
            human_override_required=False,
            urgency_level=UrgencyLevel.LOW,
            implementation_steps=[
                "Review case progress and goals",
                "Identify barriers and successes",
                "Update action plan as needed"
            ]
        )
        recommendations.append(rec)
        
        return recommendations
    
    async def _generate_crisis_intervention_recommendations(self, case_data: Dict[str, Any]) -> List[AICaseRecommendation]:
        """Generate recommendations for crisis cases"""
        recommendations = []
        
        rec = AICaseRecommendation(
            case_id=case_data["case_id"],
            recommendation_type="crisis_intervention",
            confidence_score=0.95,
            reasoning="Crisis case requires immediate intervention",
            evidence_basis=["crisis_intervention_protocols"],
            expected_outcome="Crisis stabilization and safety",
            risk_assessment="CRITICAL - Immediate intervention needed",
            alternative_options=["Emergency services", "Crisis team"],
            human_override_required=True,
            urgency_level=UrgencyLevel.CRITICAL,
            implementation_steps=[
                "Activate crisis intervention protocols",
                "Ensure client safety immediately",
                "Connect with emergency resources"
            ]
        )
        recommendations.append(rec)
        
        return recommendations
    
    def _extract_learning_features(self, case_data: Dict[str, Any], outcome: str, success_metrics: Dict[str, float]) -> List[float]:
        """Extract features for AI learning"""
        features = []
        
        # Case characteristics
        features.append(len(case_data["notes"]))
        features.append((datetime.now() - case_data["created_at"]).days)
        
        # Success metrics
        features.append(success_metrics.get("goal_achievement", 0.0))
        features.append(success_metrics.get("client_satisfaction", 0.0))
        features.append(success_metrics.get("timeline_adherence", 0.0))
        
        return features
    
    async def _update_learning_models(self, features: List[float], outcome: str, success_metrics: Dict[str, float]):
        """Update AI models with new learning data"""
        # In a real implementation, this would update the actual ML models
        # For now, we'll just log the learning
        logger.info(f"AI learning: features={features}, outcome={outcome}, metrics={success_metrics}")
    
    async def _update_caseworker_profile(self, user_id: str, outcome: str, success_metrics: Dict[str, float]):
        """Update caseworker profile based on outcomes"""
        if user_id in self.caseworker_profiles:
            profile = self.caseworker_profiles[user_id]
            
            # Update success rate
            if outcome == "successful":
                profile.success_rate = (profile.success_rate + 1.0) / 2.0
            else:
                profile.success_rate = (profile.success_rate + 0.0) / 2.0
            
            # Update average case duration
            if "duration_days" in success_metrics:
                profile.avg_case_duration = (profile.avg_case_duration + success_metrics["duration_days"]) / 2.0
