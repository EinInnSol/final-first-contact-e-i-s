"""
Tests for AI service functionality
"""

import pytest
import json
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from main import app
from app.ai_service import DemoModeService, AIService
from app.models import User, UserRole

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def demo_service():
    """Demo mode service fixture"""
    return DemoModeService()

@pytest.fixture
def ai_service():
    """AI service fixture"""
    return AIService()

class TestDemoModeService:
    """Test demo mode service"""
    
    def test_is_demo_mode(self, demo_service):
        """Test demo mode detection"""
        with patch.dict('os.environ', {'DEMO_MODE': 'true', 'OPENAI_API_KEY': ''}):
            assert demo_service.is_demo_mode() is True
        
        with patch.dict('os.environ', {'DEMO_MODE': 'false', 'OPENAI_API_KEY': 'test-key'}):
            assert demo_service.is_demo_mode() is False

    def test_get_mock_ai_response_crisis(self, demo_service):
        """Test mock AI response for crisis queries"""
        response = demo_service.get_mock_ai_response("I'm in crisis and need help")
        assert "crisis" in response.lower()
        assert "immediate" in response.lower()
        assert "emergency" in response.lower()

    def test_get_mock_ai_response_triage(self, demo_service):
        """Test mock AI response for triage queries"""
        response = demo_service.get_mock_ai_response("I need a triage assessment")
        assert "triage" in response.lower()
        assert "assessment" in response.lower()
        assert "crisis score" in response.lower()

    def test_get_mock_ai_response_care_plan(self, demo_service):
        """Test mock AI response for care plan queries"""
        response = demo_service.get_mock_ai_response("Generate a care plan for me")
        assert "care plan" in response.lower()
        assert "phase" in response.lower()
        assert "goals" in response.lower()

    def test_get_mock_ai_response_general(self, demo_service):
        """Test mock AI response for general queries"""
        query = "I need help with housing"
        response = demo_service.get_mock_ai_response(query)
        assert query.lower() in response.lower()
        assert "housing" in response.lower()
        assert "services" in response.lower()

    def test_get_mock_triage_response(self, demo_service):
        """Test mock triage response generation"""
        responses = {
            "housing_status": "homeless",
            "safety_concerns": "yes",
            "children": "yes"
        }
        result = demo_service.get_mock_triage_response(responses)
        
        assert "crisis_level" in result
        assert "crisis_score" in result
        assert "crisis_indicators" in result
        assert "recommended_services" in result
        assert "immediate_actions" in result
        assert "care_plan" in result
        
        # Check that crisis indicators are detected
        assert "homelessness" in result["crisis_indicators"]
        assert "children_at_risk" in result["crisis_indicators"]
        
        # Check crisis score is calculated
        assert result["crisis_score"] > 0
        assert result["crisis_score"] <= 100

class TestAIService:
    """Test AI service"""
    
    def test_init(self, ai_service):
        """Test AI service initialization"""
        assert ai_service.timeout == 30
        assert ai_service.max_retries == 3

    @pytest.mark.asyncio
    async def test_get_ai_response_demo_mode(self, ai_service):
        """Test AI response in demo mode"""
        with patch.dict('os.environ', {'DEMO_MODE': 'true', 'OPENAI_API_KEY': ''}):
            response = await ai_service.get_ai_response("Test query")
            assert isinstance(response, str)
            assert len(response) > 0

    @pytest.mark.asyncio
    async def test_get_ai_response_openai(self, ai_service):
        """Test AI response with OpenAI"""
        mock_response = {
            "choices": [{"message": {"content": "Test AI response"}}]
        }
        
        with patch.dict('os.environ', {'DEMO_MODE': 'false', 'OPENAI_API_KEY': 'test-key'}):
            with patch('httpx.AsyncClient.post') as mock_post:
                mock_post.return_value.json.return_value = mock_response
                mock_post.return_value.raise_for_status.return_value = None
                
                response = await ai_service.get_ai_response("Test query")
                assert response == "Test AI response"

    @pytest.mark.asyncio
    async def test_get_ai_response_anthropic(self, ai_service):
        """Test AI response with Anthropic"""
        mock_response = {
            "content": [{"text": "Test Anthropic response"}]
        }
        
        with patch.dict('os.environ', {'DEMO_MODE': 'false', 'OPENAI_API_KEY': '', 'ANTHROPIC_API_KEY': 'test-key'}):
            with patch('httpx.AsyncClient.post') as mock_post:
                mock_post.return_value.json.return_value = mock_response
                mock_post.return_value.raise_for_status.return_value = None
                
                response = await ai_service.get_ai_response("Test query")
                assert response == "Test Anthropic response"

    @pytest.mark.asyncio
    async def test_get_ai_response_fallback(self, ai_service):
        """Test AI response fallback to demo mode"""
        with patch.dict('os.environ', {'DEMO_MODE': 'false', 'OPENAI_API_KEY': 'test-key'}):
            with patch('httpx.AsyncClient.post') as mock_post:
                mock_post.side_effect = Exception("API Error")
                
                response = await ai_service.get_ai_response("Test query")
                assert isinstance(response, str)
                assert len(response) > 0

class TestAIEndpoints:
    """Test AI service endpoints"""
    
    def test_ai_chat_endpoint(self, client):
        """Test AI chat endpoint"""
        # Mock authentication
        with patch('app.auth.get_current_active_user') as mock_auth:
            mock_user = User(
                id="test-id",
                username="testuser",
                email="test@example.com",
                role=UserRole.CASEWORKER,
                is_active=True
            )
            mock_auth.return_value = mock_user
            
            # Test AI chat
            chat_data = {
                "query": "I need help with housing",
                "context": {"client_id": "test-client"}
            }
            response = client.post("/api/v1/ai/chat", json=chat_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "response" in data
            assert "confidence" in data
            assert "suggestions" in data

    def test_crisis_detection_endpoint(self, client):
        """Test crisis detection endpoint"""
        # Mock authentication
        with patch('app.auth.get_current_active_user') as mock_auth:
            mock_user = User(
                id="test-id",
                username="testuser",
                email="test@example.com",
                role=UserRole.CASEWORKER,
                is_active=True
            )
            mock_auth.return_value = mock_user
            
            # Test crisis detection
            crisis_data = {
                "text": "I want to hurt myself",
                "context": {"client_id": "test-client"}
            }
            response = client.post("/api/v1/ai/crisis-detection", json=crisis_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "risk_level" in data
            assert "confidence" in data
            assert "triggers" in data
            assert "recommended_actions" in data
            assert "escalation_required" in data

    def test_triage_endpoint(self, client):
        """Test triage assessment endpoint"""
        # Mock authentication
        with patch('app.auth.get_current_active_user') as mock_auth:
            mock_user = User(
                id="test-id",
                username="testuser",
                email="test@example.com",
                role=UserRole.CASEWORKER,
                is_active=True
            )
            mock_auth.return_value = mock_user
            
            # Mock database session
            with patch('app.database.get_db') as mock_db:
                mock_session = AsyncMock()
                mock_db.return_value = mock_session
                
                # Test triage assessment
                triage_data = {
                    "client_id": "test-client-id",
                    "responses": {
                        "housing_status": "homeless",
                        "safety_concerns": "yes"
                    },
                    "language": "en"
                }
                response = client.post("/api/v1/ai/triage", json=triage_data)
                assert response.status_code == 200
                
                data = response.json()
                assert "crisis_level" in data
                assert "crisis_score" in data
                assert "crisis_indicators" in data
                assert "recommended_services" in data
                assert "immediate_actions" in data
                assert "care_plan" in data

    def test_care_plan_endpoint(self, client):
        """Test care plan generation endpoint"""
        # Mock authentication
        with patch('app.auth.get_current_active_user') as mock_auth:
            mock_user = User(
                id="test-id",
                username="testuser",
                email="test@example.com",
                role=UserRole.CASEWORKER,
                is_active=True
            )
            mock_auth.return_value = mock_user
            
            # Test care plan generation
            care_plan_data = {
                "case_id": "test-case-id",
                "client_profile": {
                    "age": 30,
                    "situation": "homeless with children"
                },
                "services_needed": ["housing", "childcare"],
                "crisis_level": "high"
            }
            response = client.post("/api/v1/ai/care-plan", json=care_plan_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "care_plan" in data
            assert "timeline" in data
            assert "resources" in data
            assert "success_metrics" in data

    def test_ai_health_check(self, client):
        """Test AI service health check"""
        response = client.get("/api/v1/ai/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "demo_mode" in data
        assert "services" in data

class TestCrisisDetection:
    """Test crisis detection functionality"""
    
    def test_crisis_keywords_detection(self, client):
        """Test crisis keyword detection"""
        crisis_texts = [
            "I want to kill myself",
            "I'm being abused by my partner",
            "I have no home and my children are hungry",
            "I'm scared and don't know what to do"
        ]
        
        for text in crisis_texts:
            with patch('app.auth.get_current_active_user') as mock_auth:
                mock_user = User(
                    id="test-id",
                    username="testuser",
                    email="test@example.com",
                    role=UserRole.CASEWORKER,
                    is_active=True
                )
                mock_auth.return_value = mock_user
                
                crisis_data = {
                    "text": text,
                    "context": {"client_id": "test-client"}
                }
                response = client.post("/api/v1/ai/crisis-detection", json=crisis_data)
                assert response.status_code == 200
                
                data = response.json()
                assert data["risk_level"] in ["medium", "high", "critical"]
                assert len(data["triggers"]) > 0
                assert data["escalation_required"] is True

    def test_low_risk_detection(self, client):
        """Test low risk detection"""
        low_risk_text = "I'm looking for job training opportunities"
        
        with patch('app.auth.get_current_active_user') as mock_auth:
            mock_user = User(
                id="test-id",
                username="testuser",
                email="test@example.com",
                role=UserRole.CASEWORKER,
                is_active=True
            )
            mock_auth.return_value = mock_user
            
            crisis_data = {
                "text": low_risk_text,
                "context": {"client_id": "test-client"}
            }
            response = client.post("/api/v1/ai/crisis-detection", json=crisis_data)
            assert response.status_code == 200
            
            data = response.json()
            assert data["risk_level"] == "low"
            assert data["escalation_required"] is False

@pytest.mark.asyncio
async def test_ai_service_error_handling():
    """Test AI service error handling"""
    ai_service = AIService()
    
    # Test with invalid API key
    with patch.dict('os.environ', {'DEMO_MODE': 'false', 'OPENAI_API_KEY': 'invalid-key'}):
        with patch('httpx.AsyncClient.post') as mock_post:
            mock_post.side_effect = Exception("API Error")
            
            response = await ai_service.get_ai_response("Test query")
            # Should fallback to demo mode
            assert isinstance(response, str)
            assert len(response) > 0
