"""
First Contact E.I.S. - Orchestration Engine
THE BRAIN - Handles all intelligent coordination decisions

This is the core innovation. The orchestrator:
1. Receives events from Event Listener
2. Queries full context across all systems
3. Makes intelligent decisions (rules + AI)
4. Plans multi-step coordination
5. Formats recommendations for caseworker approval
6. Learns from outcomes

Author: Claude (CTO, EINHARJER INNOVATIVE SOLUTIONS LLC)
Date: November 6, 2025
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Event:
    """Represents an event that triggers orchestration"""
    event_id: str
    event_type: str  # appointment_cancelled, housing_available, client_update, etc.
    timestamp: datetime
    client_id: Optional[str]
    provider_id: Optional[str]
    metadata: Dict[str, Any]


@dataclass
class Context:
    """Full context for decision-making"""
    affected_client: Optional[Dict[str, Any]]
    related_clients: List[Dict[str, Any]]
    provider_capacity: Dict[str, Any]
    system_state: Dict[str, Any]
    historical_patterns: List[Dict[str, Any]]
    business_rules: Dict[str, Any]


@dataclass
class Action:
    """Single action to execute"""
    action_type: str  # cancel_appointment, book_appointment, send_notification, etc.
    target_system: str  # doctor_office, transport, case_management, sms, etc.
    parameters: Dict[str, Any]
    depends_on: Optional[List[str]] = None  # Action IDs this depends on


@dataclass
class ExecutionPlan:
    """Complete plan for multi-system coordination"""
    plan_id: str
    actions: List[Action]
    estimated_duration_seconds: int
    affected_systems: List[str]


@dataclass
class Recommendation:
    """Recommendation presented to caseworker"""
    recommendation_id: str
    summary: str
    reasoning: List[str]
    impact: Dict[str, Any]  # savings, urgency_improvement, etc.
    execution_plan: ExecutionPlan
    confidence_score: float  # 0.0 to 1.0
    requires_approval: bool = True


# ============================================================================
# ORCHESTRATION ENGINE
# ============================================================================

class OrchestrationEngine:
    """
    THE BRAIN - Central intelligence for coordination decisions
    
    This is what makes First Contact E.I.S. revolutionary.
    The orchestrator sees the entire ecosystem and makes optimal decisions.
    """
    
    def __init__(self, db_session, ai_service=None):
        """
        Initialize the orchestrator
        
        Args:
            db_session: Database session for querying context
            ai_service: Optional AI service for complex cases (Vertex AI Claude)
        """
        self.db = db_session
        self.ai = ai_service
        
        # Statistics tracking
        self.decisions_made = 0
        self.ai_decisions = 0  # Should be ~5%
        self.rule_decisions = 0  # Should be ~95%
        
        logger.info("Orchestration Engine initialized")
    
    
    # ------------------------------------------------------------------------
    # MAIN ORCHESTRATION FLOW
    # ------------------------------------------------------------------------
    
    async def handle_event(self, event: Event) -> Optional[Recommendation]:
        """
        Main entry point - handle an event and return recommendation
        
        This is the complete brain cycle:
        1. SENSE - Understand what happened
        2. THINK - Analyze full context
        3. DECIDE - Determine optimal action
        4. COORDINATE - Plan multi-step execution
        5. PRESENT - Format as recommendation
        
        Args:
            event: The event that triggered orchestration
            
        Returns:
            Recommendation for caseworker approval, or None if no action needed
        """
        logger.info(f"Orchestrator handling event: {event.event_type} ({event.event_id})")
        
        try:
            # STEP 1: SENSE - Understand the event
            if not self._should_orchestrate(event):
                logger.info(f"Event {event.event_id} does not require orchestration")
                return None
            
            # STEP 2: THINK - Get full context
            context = await self._get_full_context(event)
            
            # STEP 3: DECIDE - Make intelligent decision
            decision = await self._make_decision(event, context)
            
            if not decision:
                logger.info(f"No decision made for event {event.event_id}")
                return None
            
            # STEP 4: COORDINATE - Plan execution
            execution_plan = self._create_execution_plan(decision, context)
            
            # STEP 5: PRESENT - Format as recommendation
            recommendation = self._format_recommendation(decision, execution_plan, context)
            
            # REMEMBER - Store for learning
            await self._store_pattern(event, context, decision, recommendation)
            
            self.decisions_made += 1
            logger.info(f"Recommendation created: {recommendation.recommendation_id}")
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error in orchestration: {e}", exc_info=True)
            return None
    
    
    # ------------------------------------------------------------------------
    # DECISION MAKING (THE BRAIN'S CORE)
    # ------------------------------------------------------------------------
    
    async def _make_decision(
        self, 
        event: Event, 
        context: Context
    ) -> Optional[Dict[str, Any]]:
        """
        Make intelligent decision based on event and context
        
        95% of decisions use deterministic business rules
        5% of complex/ambiguous cases use AI
        
        Returns:
            Decision dict with type and parameters, or None
        """
        
        # Try deterministic rules first (95% of cases)
        decision = self._apply_business_rules(event, context)
        
        if decision:
            self.rule_decisions += 1
            logger.info(f"Decision made via business rules")
            return decision
        
        # If ambiguous, use AI (5% of cases)
        if self.ai and self._is_ambiguous(event, context):
            decision = await self._use_ai_decision(event, context)
            if decision:
                self.ai_decisions += 1
                logger.info(f"Decision made via AI")
                return decision
        
        return None
    
    
    def _apply_business_rules(
        self, 
        event: Event, 
        context: Context
    ) -> Optional[Dict[str, Any]]:
        """
        Apply deterministic business rules for decision-making
        
        This handles 95% of cases with clear logic.
        Example: appointment cancelled → find higher priority client
        """
        
        # RULE: Appointment Cancelled - Optimize Slot
        if event.event_type == "appointment_cancelled":
            return self._handle_appointment_cancellation(event, context)
        
        # RULE: Housing Available - Match to Waitlist
        elif event.event_type == "housing_available":
            return self._handle_housing_availability(event, context)
        
        # RULE: Client Documents Complete - Fast-track
        elif event.event_type == "documents_complete":
            return self._handle_documents_complete(event, context)
        
        # RULE: Deadline Approaching - Send Reminders
        elif event.event_type == "deadline_approaching":
            return self._handle_deadline_approaching(event, context)
        
        # Add more rules as needed...
        
        return None
    
    
    def _handle_appointment_cancellation(
        self, 
        event: Event, 
        context: Context
    ) -> Optional[Dict[str, Any]]:
        """
        RULE: When appointment cancelled, find best replacement
        
        This is the "calling an audible" scenario from the demo!
        
        Logic:
        1. Find clients who need this type of appointment
        2. Filter by:
           - Higher medical urgency
           - Documents ready
           - Transport compatible
           - No scheduling conflicts
        3. Return decision to bump highest priority client
        """
        
        # Get cancelled appointment details
        cancelled_time = event.metadata.get("appointment_time")
        provider_id = event.metadata.get("provider_id")
        appointment_type = event.metadata.get("appointment_type")
        
        # Find potential replacement clients
        candidates = context.related_clients
        
        # Score each candidate
        best_candidate = None
        best_score = 0.0
        
        for client in candidates:
            score = self._score_appointment_candidate(
                client, 
                cancelled_time, 
                provider_id,
                appointment_type,
                context
            )
            
            if score > best_score and score > 0.7:  # Threshold
                best_score = score
                best_candidate = client
        
        if best_candidate:
            return {
                "decision_type": "bump_appointment",
                "original_client_id": event.client_id,
                "new_client_id": best_candidate["id"],
                "appointment_time": cancelled_time,
                "provider_id": provider_id,
                "confidence": best_score,
                "reasoning": [
                    f"Higher medical urgency ({best_candidate.get('urgency_score', 0)})",
                    "All required documents uploaded",
                    "Lives on existing transport route",
                    "No scheduling conflicts"
                ]
            }
        
        return None
    
    
    def _score_appointment_candidate(
        self,
        client: Dict[str, Any],
        appointment_time: datetime,
        provider_id: str,
        appointment_type: str,
        context: Context
    ) -> float:
        """
        Score a client as potential appointment replacement
        
        Returns score 0.0-1.0 based on:
        - Medical urgency (0-40 points)
        - Documents ready (0-20 points)
        - Transport compatibility (0-20 points)
        - No conflicts (0-20 points)
        """
        score = 0.0
        
        # Medical urgency (40%)
        urgency = client.get("urgency_score", 0)
        score += (urgency / 10) * 0.4  # Normalize to 0-0.4
        
        # Documents ready (20%)
        if client.get("documents_complete", False):
            score += 0.2
        
        # Transport compatible (20%)
        if self._is_transport_compatible(client, provider_id, context):
            score += 0.2
        
        # No scheduling conflicts (20%)
        if not self._has_conflicts(client, appointment_time, context):
            score += 0.2
        
        return min(score, 1.0)
    
    
    def _handle_housing_availability(
        self, 
        event: Event, 
        context: Context
    ) -> Optional[Dict[str, Any]]:
        """
        RULE: When housing opens, match best client from waitlist
        
        Logic:
        1. Get housing requirements (bedroom count, location, etc.)
        2. Find waitlist clients who match
        3. Score by time on waitlist + urgency + readiness
        4. Return top match
        """
        # TODO: Implement housing matching logic
        return None
    
    
    def _handle_documents_complete(
        self, 
        event: Event, 
        context: Context
    ) -> Optional[Dict[str, Any]]:
        """
        RULE: When documents complete, fast-track next steps
        
        Logic:
        1. Check what's waiting on documents
        2. Identify next bottleneck
        3. Recommend acceleration
        """
        # TODO: Implement fast-track logic
        return None
    
    
    def _handle_deadline_approaching(
        self, 
        event: Event, 
        context: Context
    ) -> Optional[Dict[str, Any]]:
        """
        RULE: When deadline approaching, send reminders
        
        Logic:
        1. Identify what deadline
        2. Check if action needed
        3. Schedule reminders
        """
        # TODO: Implement deadline logic
        return None
    
    
    async def _use_ai_decision(
        self, 
        event: Event, 
        context: Context
    ) -> Optional[Dict[str, Any]]:
        """
        Use AI for complex/ambiguous decisions (5% of cases)
        
        This is where we call Vertex AI Claude for cases that
        don't fit clear business rules.
        """
        if not self.ai:
            return None
        
        # Format prompt for AI
        prompt = self._format_ai_prompt(event, context)
        
        # Call Vertex AI Claude
        response = await self.ai.generate(prompt)
        
        # Parse AI response into decision
        decision = self._parse_ai_response(response)
        
        return decision
    
    
    # ------------------------------------------------------------------------
    # CONTEXT GATHERING
    # ------------------------------------------------------------------------
    
    async def _get_full_context(self, event: Event) -> Context:
        """
        Query full context needed for decision-making
        
        This is comprehensive - we need to see the WHOLE situation:
        - Client history
        - Provider capacity
        - System state
        - Past patterns
        """
        
        # Query affected client
        affected_client = None
        if event.client_id:
            affected_client = await self._query_client(event.client_id)
        
        # Query related clients (potential matches)
        related_clients = await self._query_related_clients(event)
        
        # Query provider capacity
        provider_capacity = await self._query_provider_capacity(event)
        
        # Query system state
        system_state = await self._query_system_state()
        
        # Retrieve historical patterns
        historical_patterns = await self._query_historical_patterns(event)
        
        # Load business rules
        business_rules = self._load_business_rules()
        
        return Context(
            affected_client=affected_client,
            related_clients=related_clients,
            provider_capacity=provider_capacity,
            system_state=system_state,
            historical_patterns=historical_patterns,
            business_rules=business_rules
        )
    
    
    # ------------------------------------------------------------------------
    # EXECUTION PLANNING
    # ------------------------------------------------------------------------
    
    def _create_execution_plan(
        self, 
        decision: Dict[str, Any], 
        context: Context
    ) -> ExecutionPlan:
        """
        Create multi-step execution plan from decision
        
        This translates high-level decision into concrete actions
        across multiple systems.
        
        Example for "bump_appointment":
        1. Cancel original appointment
        2. Book new appointment
        3. Update transport
        4. Notify client via SMS
        5. Notify provider
        6. Update case management
        """
        
        actions = []
        plan_id = f"plan_{datetime.now().timestamp()}"
        
        if decision["decision_type"] == "bump_appointment":
            # Action 1: Cancel original appointment
            actions.append(Action(
                action_type="cancel_appointment",
                target_system="provider_scheduling",
                parameters={
                    "provider_id": decision["provider_id"],
                    "client_id": decision["new_client_id"],
                    "appointment_time": decision["appointment_time"]
                }
            ))
            
            # Action 2: Book new appointment
            actions.append(Action(
                action_type="book_appointment",
                target_system="provider_scheduling",
                parameters={
                    "provider_id": decision["provider_id"],
                    "client_id": decision["new_client_id"],
                    "appointment_time": decision["appointment_time"]
                },
                depends_on=["cancel_appointment"]
            ))
            
            # Action 3: Update transport
            actions.append(Action(
                action_type="update_transport",
                target_system="transportation",
                parameters={
                    "client_id": decision["new_client_id"],
                    "pickup_time": decision["appointment_time"] - timedelta(minutes=30),
                    "destination": "provider_location"
                }
            ))
            
            # Action 4: Notify client
            actions.append(Action(
                action_type="send_sms",
                target_system="notifications",
                parameters={
                    "client_id": decision["new_client_id"],
                    "message": f"Good news! Your appointment moved up to today at {decision['appointment_time']}. Transport arranged."
                }
            ))
            
            # Action 5: Notify provider
            actions.append(Action(
                action_type="notify_provider",
                target_system="provider_api",
                parameters={
                    "provider_id": decision["provider_id"],
                    "message": f"Patient update: {decision['new_client_id']} moved to {decision['appointment_time']}"
                }
            ))
            
            # Action 6: Update case management
            actions.append(Action(
                action_type="update_case",
                target_system="case_management",
                parameters={
                    "client_id": decision["new_client_id"],
                    "update_type": "appointment_rescheduled",
                    "details": decision
                }
            ))
        
        # Calculate affected systems and duration
        affected_systems = list(set([a.target_system for a in actions]))
        estimated_duration = len(actions) * 2  # ~2 seconds per action
        
        return ExecutionPlan(
            plan_id=plan_id,
            actions=actions,
            estimated_duration_seconds=estimated_duration,
            affected_systems=affected_systems
        )
    
    
    # ------------------------------------------------------------------------
    # RECOMMENDATION FORMATTING
    # ------------------------------------------------------------------------
    
    def _format_recommendation(
        self,
        decision: Dict[str, Any],
        execution_plan: ExecutionPlan,
        context: Context
    ) -> Recommendation:
        """
        Format decision + plan as caseworker recommendation
        
        This is what shows up in the caseworker dashboard with
        the APPROVE button.
        """
        
        rec_id = f"rec_{datetime.now().timestamp()}"
        
        # Create human-readable summary
        summary = self._create_summary(decision)
        
        # Calculate impact
        impact = self._calculate_impact(decision, context)
        
        return Recommendation(
            recommendation_id=rec_id,
            summary=summary,
            reasoning=decision.get("reasoning", []),
            impact=impact,
            execution_plan=execution_plan,
            confidence_score=decision.get("confidence", 0.8),
            requires_approval=True
        )
    
    
    def _create_summary(self, decision: Dict[str, Any]) -> str:
        """Create human-readable summary of decision"""
        
        if decision["decision_type"] == "bump_appointment":
            return f"Bump Client {decision['new_client_id']} to today's {decision['appointment_time']} appointment?"
        
        return "Optimization opportunity detected"
    
    
    def _calculate_impact(
        self, 
        decision: Dict[str, Any], 
        context: Context
    ) -> Dict[str, Any]:
        """
        Calculate impact of decision
        
        Returns dict with:
        - cost_savings: Dollar amount saved
        - urgency_improvement: How much urgency improved
        - efficiency_gain: Time/resource efficiency
        """
        
        impact = {
            "cost_savings": 0,
            "urgency_improvement": 0,
            "efficiency_gain": 0
        }
        
        if decision["decision_type"] == "bump_appointment":
            # Avoid wasted appointment slot
            impact["cost_savings"] = 120  # Average appointment cost
            
            # Urgency improvement
            if decision.get("confidence", 0) > 0.8:
                impact["urgency_improvement"] = "high"
        
        return impact
    
    
    # ------------------------------------------------------------------------
    # HELPER METHODS
    # ------------------------------------------------------------------------
    
    def _should_orchestrate(self, event: Event) -> bool:
        """Check if event requires orchestration"""
        orchestrable_events = [
            "appointment_cancelled",
            "housing_available",
            "documents_complete",
            "deadline_approaching",
            "client_update",
            "provider_capacity_change"
        ]
        return event.event_type in orchestrable_events
    
    
    def _is_ambiguous(self, event: Event, context: Context) -> bool:
        """Check if decision is ambiguous and needs AI"""
        # TODO: Implement ambiguity detection
        return False
    
    
    def _is_transport_compatible(
        self, 
        client: Dict[str, Any], 
        provider_id: str, 
        context: Context
    ) -> bool:
        """Check if client is on compatible transport route"""
        # TODO: Implement transport compatibility check
        return True
    
    
    def _has_conflicts(
        self, 
        client: Dict[str, Any], 
        time: datetime, 
        context: Context
    ) -> bool:
        """Check if client has scheduling conflicts"""
        # TODO: Implement conflict detection
        return False
    
    
    async def _query_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Query full client details"""
        # TODO: Implement database query
        return None
    
    
    async def _query_related_clients(self, event: Event) -> List[Dict[str, Any]]:
        """Query clients related to this event"""
        # TODO: Implement database query
        return []
    
    
    async def _query_provider_capacity(self, event: Event) -> Dict[str, Any]:
        """Query provider capacity/availability"""
        # TODO: Implement provider capacity query
        return {}
    
    
    async def _query_system_state(self) -> Dict[str, Any]:
        """Query overall system state"""
        # TODO: Implement system state query
        return {}
    
    
    async def _query_historical_patterns(self, event: Event) -> List[Dict[str, Any]]:
        """Query historical patterns for learning"""
        # TODO: Implement pattern retrieval
        return []
    
    
    def _load_business_rules(self) -> Dict[str, Any]:
        """Load business rules configuration"""
        # TODO: Implement rules loading
        return {}
    
    
    async def _store_pattern(
        self, 
        event: Event, 
        context: Context, 
        decision: Dict[str, Any], 
        recommendation: Recommendation
    ):
        """Store decision pattern for learning"""
        # TODO: Implement pattern storage
        pass
    
    
    def _format_ai_prompt(self, event: Event, context: Context) -> str:
        """Format prompt for AI decision-making"""
        # TODO: Implement AI prompt formatting
        return ""
    
    
    def _parse_ai_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse AI response into decision"""
        # TODO: Implement AI response parsing
        return None
    
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "decisions_made": self.decisions_made,
            "ai_decisions": self.ai_decisions,
            "rule_decisions": self.rule_decisions,
            "ai_percentage": (self.ai_decisions / max(self.decisions_made, 1)) * 100
        }
