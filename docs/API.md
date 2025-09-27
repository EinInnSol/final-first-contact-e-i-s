# First Contact EIS API Documentation

## Overview

The First Contact EIS API provides comprehensive endpoints for managing civic services, AI-powered assistance, case management, and compliance reporting. The API is built with FastAPI and follows RESTful principles.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.firstcontact-eis.org`

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your-token>
```

## Endpoints

### Health Check

#### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "database": {
      "status": "healthy",
      "response_time_ms": 5.2
    },
    "redis": {
      "status": "healthy",
      "response_time_ms": 2.1
    },
    "ai_service": {
      "status": "healthy",
      "response_time_ms": 15.8
    }
  }
}
```

### Authentication

#### POST /api/v1/auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "client"
}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "role": "client",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### POST /api/v1/auth/token
Login and get access token.

**Request Body:**
```json
{
  "username": "username",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### GET /api/v1/auth/me
Get current user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "role": "client",
  "is_active": true,
  "is_verified": true,
  "last_login": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### AI Services

#### POST /api/v1/ai/chat
Chat with AI assistant.

**Request Body:**
```json
{
  "query": "I need help with housing",
  "context": {
    "client_id": "uuid",
    "language": "en"
  }
}
```

**Response:**
```json
{
  "response": "I can help you with housing assistance. Let me connect you with local resources...",
  "confidence": 0.85,
  "suggestions": [
    "Would you like to schedule an appointment?",
    "Do you need help with employment?",
    "Are you looking for healthcare services?"
  ],
  "crisis_indicators": [],
  "recommended_actions": [
    "Schedule intake appointment",
    "Connect with caseworker"
  ]
}
```

#### POST /api/v1/ai/triage
Perform AI-powered triage assessment.

**Request Body:**
```json
{
  "client_id": "uuid",
  "responses": {
    "housing_status": "homeless",
    "safety_concerns": "yes",
    "children": "yes"
  },
  "language": "en"
}
```

**Response:**
```json
{
  "crisis_level": "high",
  "crisis_score": 85.0,
  "crisis_indicators": ["homelessness", "children_at_risk"],
  "recommended_services": ["housing", "childcare", "mental_health"],
  "immediate_actions": [
    "Contact emergency shelter services",
    "Initiate safety planning protocol",
    "Connect with domestic violence resources"
  ],
  "care_plan": {
    "immediate_needs": ["safety", "housing", "basic_needs"],
    "short_term_goals": ["stabilization", "service_connection"],
    "long_term_goals": ["self_sufficiency", "independence"]
  }
}
```

#### POST /api/v1/ai/crisis-detection
Detect crisis indicators in text.

**Request Body:**
```json
{
  "text": "I want to hurt myself",
  "context": {
    "client_id": "uuid"
  }
}
```

**Response:**
```json
{
  "risk_level": "critical",
  "confidence": 0.95,
  "triggers": ["suicidal_ideation"],
  "recommended_actions": [
    "Contact emergency services immediately",
    "Schedule crisis intervention appointment",
    "Connect with mental health services"
  ],
  "escalation_required": true,
  "emergency_contacts": [
    {
      "name": "National Suicide Prevention Lifeline",
      "phone": "988"
    }
  ]
}
```

### Case Management

#### GET /api/v1/cases
Get cases for a client.

**Query Parameters:**
- `client_id`: Client ID (required)
- `status`: Case status filter
- `priority`: Priority level filter
- `page`: Page number (default: 1)
- `size`: Page size (default: 10)

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "client_id": "uuid",
      "case_number": "FC-2024-001",
      "title": "Housing Crisis - Family with Children",
      "description": "Family of 3 experiencing homelessness...",
      "status": "open",
      "priority": "high",
      "crisis_indicators": ["homeless", "children"],
      "services_needed": ["housing", "childcare"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1,
  "has_next": false,
  "has_prev": false
}
```

#### POST /api/v1/cases
Create a new case.

**Request Body:**
```json
{
  "client_id": "uuid",
  "title": "Case Title",
  "description": "Case description",
  "priority": "medium",
  "crisis_indicators": ["homeless"],
  "services_needed": ["housing", "employment"]
}
```

### Resources

#### GET /api/v1/resources
Get available resources.

**Query Parameters:**
- `service_type`: Filter by service type
- `city`: Filter by city
- `language`: Filter by supported language
- `page`: Page number
- `size`: Page size

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Long Beach Housing Authority",
      "description": "Provides affordable housing and rental assistance",
      "service_type": "housing",
      "provider_name": "City of Long Beach",
      "contact_phone": "(562) 570-6944",
      "contact_email": "housing@longbeach.gov",
      "website": "https://www.longbeach.gov/housing",
      "address": "1800 E Wardlow Rd",
      "city": "Long Beach",
      "state": "CA",
      "zip_code": "90807",
      "eligibility_requirements": ["low_income", "citizen_or_eligible_immigrant"],
      "hours_of_operation": {
        "monday": "8:00-17:00",
        "tuesday": "8:00-17:00"
      },
      "languages_supported": ["en", "es"],
      "is_active": true
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10
}
```

### Compliance

#### POST /api/v1/compliance/hud-report
Generate HUD compliance report.

**Request Body:**
```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "include_clients": true,
  "include_services": true
}
```

**Response:**
```json
{
  "report_data": {
    "universal_data_elements": {
      "client_count": 150,
      "services_provided": 300,
      "outcomes_achieved": 85
    },
    "demographics": {
      "age_groups": {...},
      "ethnicity": {...},
      "gender": {...}
    }
  },
  "export_url": "/api/v1/compliance/hud-report/download/uuid",
  "record_count": 150
}
```

## Error Handling

The API uses standard HTTP status codes and returns error details in the response body:

```json
{
  "error": "Validation Error",
  "detail": "Invalid email format",
  "type": "validation_error",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Common Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

- **General endpoints**: 100 requests per minute
- **AI endpoints**: 10 requests per minute
- **Authentication endpoints**: 5 requests per minute

## WebSocket Events

The API supports real-time updates via WebSocket:

### Connection
```javascript
const socket = io('ws://localhost:8000');
```

### Events

#### crisis_alert
```json
{
  "type": "crisis_alert",
  "data": {
    "client_id": "uuid",
    "risk_level": "critical",
    "message": "Crisis situation detected"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### notification
```json
{
  "type": "notification",
  "data": {
    "user_id": "uuid",
    "title": "New Case Assignment",
    "message": "You have been assigned to case FC-2024-001",
    "type": "case_assignment"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### case_update
```json
{
  "type": "case_update",
  "data": {
    "case_id": "uuid",
    "status": "in_progress",
    "updated_by": "uuid"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## SDKs and Libraries

### JavaScript/TypeScript
```bash
npm install @firstcontact-eis/sdk
```

### Python
```bash
pip install firstcontact-eis-sdk
```

## Support

For API support and questions:
- **Email**: api-support@firstcontact-eis.org
- **Documentation**: https://docs.firstcontact-eis.org
- **Status Page**: https://status.firstcontact-eis.org
