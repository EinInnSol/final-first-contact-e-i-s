"""
Mutual Support Agent - Core Innovation of First Contact E.I.S.

Detects pre-existing mutual support relationships between clients and enables:
1. IHSS pairing (formalizing informal care relationships)
2. Consolidated case management (reducing overhead by 50%+)
3. Improved housing retention (75-85% vs 30-40%)
4. Cost savings ($42K vs $90K per pair)

Author: James & Claude (Co-Founders)
Date: November 2, 2025
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class SupportIndicator:
    """Individual signal of mutual support between clients"""
    indicator_type: str
    confidence: float
    evidence: Dict[str, any]
    detected_at: datetime


@dataclass
class MutualSupportPair:
    """Detected pairing opportunity between two clients"""
    client_a_id: str
    client_b_id: str
    confidence_score: float
    support_indicators: List[SupportIndicator]
    recommended_actions: List[str]
    ihss_eligible: bool
    consolidation_benefits: Dict[str, any]


class MutualSupportAgent:
    """
    Detects and formalizes mutual support relationships between clients.
    
    This is the core innovation that differentiates First Contact E.I.S. from
    traditional Coordinated Entry Systems. By identifying existing care relationships,
    we can:
    
    - Create income through IHSS formalization
    - Reduce case management overhead by 50%+
    - Improve housing retention from 30-40% to 75-85%
    - Lower cost per person from $45K to $21K
    
    Real-world usage: James and his wife will use this as caseworkers during
    the 6-month LA pilot to identify pairing opportunities in their caseload.
    """
    
    def __init__(self, threshold: float = 0.7):
        """
        Initialize the Mutual Support Agent.
        
        Args:
            threshold: Minimum confidence score to trigger caseworker alert (default: 0.7)
        """
        self.threshold = threshold
        
        # Support indicators from whitepaper + expanded based on IHSS eligibility
        self.support_indicators = {
            'daily_care_provided': {
                'weight': 1.0,
                'description': 'One person provides daily care/check-ins',
                'ihss_relevant': True
            },
            'shared_residence': {
                'weight': 0.9,
                'description': 'Living together or in close proximity',
                'ihss_relevant': True
            },
            'assists_with_ADLs': {
                'weight': 1.0,
                'description': 'Help with Activities of Daily Living (bathing, dressing, eating)',
                'ihss_relevant': True
            },
            'community_support': {
                'weight': 0.7,
                'description': 'Participate in community support activities together',
                'ihss_relevant': False
            },
            'shared_resources': {
                'weight': 0.8,
                'description': 'Pool money, share food, coordinate benefits',
                'ihss_relevant': False
            },
            'mutual_assistance': {
                'weight': 0.8,
                'description': 'Help each other with appointments, transportation, etc.',
                'ihss_relevant': False
            },
            'medication_management': {
                'weight': 0.9,
                'description': 'One person helps the other manage medications',
                'ihss_relevant': True
            },
            'mobility_assistance': {
                'weight': 0.9,
                'description': 'Help with walking, wheelchair, or mobility devices',
                'ihss_relevant': True
            },
            'transportation_support': {
                'weight': 0.6,
                'description': 'One person helps the other get to appointments',
                'ihss_relevant': True
            },
            'meal_preparation': {
                'weight': 0.8,
                'description': 'One person cooks or helps with meals',
                'ihss_relevant': True
            }
        }
        
        logger.info(f"Mutual Support Agent initialized with threshold: {self.threshold}")
    
    def evaluate_client_pair(self, client_a: Dict, client_b: Dict) -> Optional[MutualSupportPair]:
        """
        Evaluate two clients for mutual support relationship.
        
        Args:
            client_a: First client data
            client_b: Second client data
            
        Returns:
            MutualSupportPair if confidence >= threshold, else None
        """
        indicators_found = []
        total_weight = 0.0
        max_possible_weight = sum(ind['weight'] for ind in self.support_indicators.values())
        
        # Check each indicator
        for indicator_key, indicator_config in self.support_indicators.items():
            if self._check_indicator(client_a, client_b, indicator_key):
                indicators_found.append(
                    SupportIndicator(
                        indicator_type=indicator_key,
                        confidence=indicator_config['weight'],
                        evidence={
                            'client_a': client_a.get(indicator_key),
                            'client_b': client_b.get(indicator_key),
                            'description': indicator_config['description']
                        },
                        detected_at=datetime.now()
                    )
                )
                total_weight += indicator_config['weight']
        
        # Calculate confidence score
        confidence = total_weight / max_possible_weight
        
        logger.info(
            f"Evaluated pair {client_a.get('id')} + {client_b.get('id')}: "
            f"{len(indicators_found)} indicators, confidence: {confidence:.2f}"
        )
        
        # If confidence meets threshold, create pairing recommendation
        if confidence >= self.threshold:
            ihss_eligible = self._check_ihss_eligibility(indicators_found)
            benefits = self._calculate_consolidation_benefits(client_a, client_b, indicators_found)
            actions = self._generate_recommended_actions(ihss_eligible, indicators_found)
            
            pair = MutualSupportPair(
                client_a_id=client_a.get('id'),
                client_b_id=client_b.get('id'),
                confidence_score=confidence,
                support_indicators=indicators_found,
                recommended_actions=actions,
                ihss_eligible=ihss_eligible,
                consolidation_benefits=benefits
            )
            
            logger.info(f"🎯 MUTUAL SUPPORT PAIR DETECTED: {pair.client_a_id} + {pair.client_b_id}")
            return pair
        
        return None
    
    def scan_caseload_for_pairs(self, clients: List[Dict]) -> List[MutualSupportPair]:
        """
        Scan entire caseload for pairing opportunities.
        
        This is what James and his wife will run regularly to identify
        consolidation opportunities in their caseload.
        
        Args:
            clients: List of all clients in caseload
            
        Returns:
            List of detected pairing opportunities, sorted by confidence
        """
        pairs = []
        
        # Check every combination (avoiding duplicates)
        for i, client_a in enumerate(clients):
            for client_b in clients[i+1:]:
                pair = self.evaluate_client_pair(client_a, client_b)
                if pair:
                    pairs.append(pair)
        
        # Sort by confidence score (highest first)
        pairs.sort(key=lambda p: p.confidence_score, reverse=True)
        
        logger.info(f"Scanned {len(clients)} clients, found {len(pairs)} potential pairs")
        return pairs
    
    def _check_indicator(self, client_a: Dict, client_b: Dict, indicator: str) -> bool:
        """Check if a specific indicator is present between two clients"""
        # Look for indicator in client data
        a_has = client_a.get(indicator, False)
        b_has = client_b.get(indicator, False)
        
        # For mutual support, one or both should show the indicator
        return a_has or b_has
    
    def _check_ihss_eligibility(self, indicators: List[SupportIndicator]) -> bool:
        """
        Determine if pair is eligible for IHSS formalization.
        
        IHSS requires care activities that meet specific criteria.
        At least 2 IHSS-relevant indicators needed.
        """
        ihss_relevant = [
            ind for ind in indicators 
            if self.support_indicators[ind.indicator_type]['ihss_relevant']
        ]
        return len(ihss_relevant) >= 2
    
    def _calculate_consolidation_benefits(
        self, 
        client_a: Dict, 
        client_b: Dict, 
        indicators: List[SupportIndicator]
    ) -> Dict[str, any]:
        """
        Calculate the benefits of consolidating these two cases.
        
        Returns concrete numbers for cost savings, appointment reduction, etc.
        """
        # Estimate current separate costs
        separate_appointments = client_a.get('pending_appointments', 15) + client_b.get('pending_appointments', 15)
        separate_transportation_cost = separate_appointments * 75  # $75 per trip
        separate_caseworker_hours = separate_appointments * 2  # 2 hours per appointment
        
        # Estimate consolidated costs (50% reduction)
        consolidated_appointments = int(separate_appointments * 0.5)
        consolidated_transportation_cost = consolidated_appointments * 75
        consolidated_caseworker_hours = consolidated_appointments * 2
        
        # IHSS income potential
        ihss_monthly_income = 1800 if self._check_ihss_eligibility(indicators) else 0
        
        return {
            'appointment_reduction': separate_appointments - consolidated_appointments,
            'transportation_savings': separate_transportation_cost - consolidated_transportation_cost,
            'caseworker_hours_saved': separate_caseworker_hours - consolidated_caseworker_hours,
            'ihss_monthly_income_potential': ihss_monthly_income,
            'estimated_cost_savings': {
                'per_month': ihss_monthly_income + (separated_appointments - consolidated_appointments) * 200,
                'over_6_months': (ihss_monthly_income * 6) + ((separate_appointments - consolidated_appointments) * 200 * 6)
            },
            'retention_probability_boost': '+45%' if ihss_monthly_income > 0 else '+25%'
        }
    
    def _generate_recommended_actions(
        self, 
        ihss_eligible: bool, 
        indicators: List[SupportIndicator]
    ) -> List[str]:
        """Generate action items for caseworker"""
        actions = [
            "Review relationship with both clients",
            "Validate support indicators in person",
            "Consolidate appointment schedules"
        ]
        
        if ihss_eligible:
            actions.extend([
                "🎯 PRIORITY: Initiate IHSS application process",
                "Determine provider/recipient roles",
                "Schedule IHSS assessment appointment",
                "Explain income benefits to potential provider"
            ])
        
        actions.extend([
            "Request co-located temporary housing placement",
            "Coordinate shared transportation",
            "Begin shared housing search (2BR units)",
            "Schedule monthly retention check-ins after housing"
        ])
        
        return actions
    
    def generate_caseworker_alert(self, pair: MutualSupportPair) -> Dict:
        """
        Generate alert for caseworker dashboard.
        
        This is what James and his wife will see when a pair is detected.
        """
        return {
            'alert_type': 'MUTUAL_SUPPORT_DETECTED',
            'priority': 'HIGH' if pair.ihss_eligible else 'MEDIUM',
            'clients': [pair.client_a_id, pair.client_b_id],
            'confidence': f"{pair.confidence_score:.0%}",
            'ihss_eligible': pair.ihss_eligible,
            'indicators_found': [
                {
                    'type': ind.indicator_type,
                    'description': ind.evidence['description']
                }
                for ind in pair.support_indicators
            ],
            'estimated_savings': pair.consolidation_benefits['estimated_cost_savings'],
            'next_steps': pair.recommended_actions,
            'message': self._generate_alert_message(pair)
        }
    
    def _generate_alert_message(self, pair: MutualSupportPair) -> str:
        """Generate human-readable alert message"""
        if pair.ihss_eligible:
            return (
                f"🎯 HIGH PRIORITY: Potential IHSS pairing detected with {pair.confidence_score:.0%} confidence. "
                f"These clients show {len(pair.support_indicators)} support indicators including ADL assistance. "
                f"Formalizing this relationship could generate ${pair.consolidation_benefits['ihss_monthly_income_potential']}/month "
                f"in IHSS income while reducing case management costs by "
                f"${pair.consolidation_benefits['estimated_cost_savings']['over_6_months']:,} over 6 months."
            )
        else:
            return (
                f"Mutual support relationship detected with {pair.confidence_score:.0%} confidence. "
                f"Consolidating these cases could save {pair.consolidation_benefits['appointment_reduction']} appointments "
                f"and ${pair.consolidation_benefits['estimated_cost_savings']['over_6_months']:,} over 6 months while "
                f"improving retention probability by {pair.consolidation_benefits['retention_probability_boost']}."
            )


# Demo/Testing functions
def create_demo_clients() -> List[Dict]:
    """Create demo client data for testing"""
    return [
        {
            'id': 'client_001',
            'name': 'Maria G.',
            'daily_care_provided': True,
            'assists_with_ADLs': True,
            'shared_residence': True,
            'meal_preparation': True,
            'pending_appointments': 18
        },
        {
            'id': 'client_002',
            'name': 'Robert K.',
            'daily_care_provided': False,
            'shared_residence': True,
            'community_support': True,
            'transportation_support': True,
            'pending_appointments': 16
        },
        {
            'id': 'client_003',
            'name': 'Sarah L.',
            'assists_with_ADLs': True,
            'medication_management': True,
            'shared_resources': True,
            'pending_appointments': 20
        }
    ]


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)
    
    agent = MutualSupportAgent(threshold=0.7)
    clients = create_demo_clients()
    
    # Scan for pairs
    pairs = agent.scan_caseload_for_pairs(clients)
    
    print(f"\n{'='*60}")
    print(f"MUTUAL SUPPORT AGENT - DEMO RESULTS")
    print(f"{'='*60}\n")
    print(f"Scanned {len(clients)} clients")
    print(f"Found {len(pairs)} potential pairs\n")
    
    for i, pair in enumerate(pairs, 1):
        print(f"--- PAIR #{i} ---")
        alert = agent.generate_caseworker_alert(pair)
        print(f"Clients: {pair.client_a_id} + {pair.client_b_id}")
        print(f"Confidence: {alert['confidence']}")
        print(f"IHSS Eligible: {alert['ihss_eligible']}")
        print(f"Priority: {alert['priority']}")
        print(f"\nMessage: {alert['message']}\n")
    
    async def evaluate_intake(self, intake_record: Dict, db) -> Dict:
        """
        Evaluate a new intake for potential mutual support relationships.
        
        This is the async method called by the intake router.
        It searches the database for other clients in the same organization
        who might have an existing support relationship with this person.
        
        Args:
            intake_record: New intake data
            db: AsyncSession for database queries
            
        Returns:
            Dict with pairs_detected count and detected_pairs list
        """
        from sqlalchemy import select, and_
        from app.models import Client, Intake as IntakeModel
        
        detected_pairs = []
        organization_id = intake_record.get('organization_id')
        
        if not organization_id:
            logger.warning("No organization_id in intake record, cannot evaluate")
            return {'pairs_detected': 0, 'detected_pairs': []}
        
        # Get all other clients in the same organization
        query = select(Client).where(
            and_(
                Client.organization_id == organization_id,
                Client.id != intake_record.get('client_id')
            )
        )
        
        result = await db.execute(query)
        potential_matches = result.scalars().all()
        
        logger.info(f"Evaluating intake {intake_record.get('id')} against {len(potential_matches)} potential matches")
        
        # Check each potential match
        for client_b in potential_matches:
            # Get most recent intake for client B
            intake_query = select(IntakeModel).where(
                IntakeModel.client_id == client_b.id
            ).order_by(IntakeModel.created_at.desc()).limit(1)
            
            intake_result = await db.execute(intake_query)
            client_b_intake = intake_result.scalar_one_or_none()
            
            if not client_b_intake:
                continue
            
            # Convert to dict format for evaluation
            client_b_record = {
                'id': str(client_b.id),
                'first_name': client_b.first_name,
                'last_name': client_b.last_name,
                'housing_status': client_b_intake.housing_status,
                'support_network': client_b_intake.support_network or {},
                'medical_conditions': client_b_intake.medical_conditions or [],
            }
            
            # Evaluate pair
            pair = self.evaluate_client_pair(intake_record, client_b_record)
            
            if pair:
                # Calculate financial benefits
                ihss_monthly = 1800.0 if pair.ihss_eligible else 0.0
                annual_savings = pair.consolidation_benefits.get('estimated_cost_savings', {}).get('over_6_months', 0) * 2
                
                detected_pairs.append({
                    'client_b_id': str(client_b.id),
                    'client_b_name': f"{client_b.first_name} {client_b.last_name}",
                    'confidence_score': pair.confidence_score,
                    'ihss_eligible': pair.ihss_eligible,
                    'indicators': [ind.indicator_type for ind in pair.support_indicators],
                    'estimated_monthly_benefit': ihss_monthly,
                    'estimated_annual_savings': annual_savings
                })
                
                logger.info(
                    f"🎯 PAIR DETECTED: {intake_record.get('first_name')} + {client_b.first_name} "
                    f"(confidence: {pair.confidence_score:.0%})"
                )
        
        return {
            'pairs_detected': len(detected_pairs),
            'detected_pairs': detected_pairs
        }
