# First Contact E.I.S. - System Architecture

## 🏗️ HIGH-LEVEL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT TOUCHPOINTS                                  │
│                                                                                  │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐                    │
│  │  QR Codes   │      │  Mobile Web │      │   Kiosk     │                    │
│  │  (Geographic│      │             │      │  (Field)    │                    │
│  │  Tracking)  │      │             │      │             │                    │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘                    │
│         │                    │                    │                            │
│         └────────────────────┼────────────────────┘                            │
│                              │                                                  │
└──────────────────────────────┼──────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER (Cloud Run)                               │
│                                                                                  │
│  ┌──────────────────────┐              ┌──────────────────────┐                │
│  │   CLIENT PORTAL      │              │  CASEWORKER PORTAL   │                │
│  │   (Next.js 14)       │              │  (Next.js 14)        │                │
│  │                      │              │                      │                │
│  │  • QR Code intake    │              │  • Real-time alerts  │                │
│  │  • Multi-language    │              │  • Case management   │                │
│  │  • Offline support   │              │  • Pair review       │                │
│  │  • Accessibility     │              │  • Care plan gen     │                │
│  │  • Mobile-first      │              │  • IHSS enrollment   │                │
│  └──────────┬───────────┘              └──────────┬───────────┘                │
│             │                                     │                            │
│             │          ┌──────────────────────┐   │                            │
│             │          │  CITY DASHBOARD      │   │                            │
│             │          │  (Phase 2)           │   │                            │
│             │          │                      │   │                            │
│             │          │  • Heat maps         │   │                            │
│             │          │  • ROI tracking      │   │                            │
│             │          │  • Transparency      │   │                            │
│             │          └──────────┬───────────┘   │                            │
│             │                     │                │                            │
└─────────────┼─────────────────────┼────────────────┼────────────────────────────┘
              │                     │                │
              └─────────────────────┼────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND API (Cloud Run)                                │
│                           FastAPI + Python 3.11                                  │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │                          AGENTIC AI LAYER                              │    │
│  │                                                                          │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │    │
│  │  │  INTAKE AGENT   │  │ MUTUAL SUPPORT  │  │ CLASSIFICATION  │       │    │
│  │  │                 │  │ AGENT (IHSS)    │  │ AGENT           │       │    │
│  │  │ • Validation    │  │                 │  │                 │       │    │
│  │  │ • Anonymization │  │ • 10 indicators │  │ • Urgency score │       │    │
│  │  │ • Geolocation   │  │ • Threshold 0.7 │  │ • Multi-domain  │       │    │
│  │  │ • Standardize   │  │ • Deterministic │  │ • Risk levels   │       │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │    │
│  │                                                                          │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │    │
│  │  │  AUDIT AGENT    │  │ CARE PLAN GEN   │  │ RESOURCE        │       │    │
│  │  │                 │  │ (AI-Powered)    │  │ MATCHER         │       │    │
│  │  │ • Compliance    │  │                 │  │                 │       │    │
│  │  │ • Privacy       │  │ • Vertex AI     │  │ • Service find  │       │    │
│  │  │ • Audit logs    │  │ • Personalized  │  │ • Availability  │       │    │
│  │  │ • Sanitization  │  │ • Multi-lingual │  │ • Referrals     │       │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐    │
│  │                        VERTEX AI INTEGRATION                           │    │
│  │                                                                          │    │
│  │  • Model: Claude Sonnet 4.5 (claude-sonnet-4-20250514)                │    │
│  │  • Region: us-east5                                                    │    │
│  │  • Usage: Care plan generation, semantic search, edge cases            │    │
│  │  • Cost: ~$15/month (500K tokens)                                      │    │
│  └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└───────────────────────────────┬──────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER (Firestore)                                   │
│                         NoSQL Real-time Database                                 │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  COLLECTIONS:                                                           │   │
│  │                                                                           │   │
│  │  • clients/              - Client intake records (encrypted PII)        │   │
│  │  • cases/                - Active case management                        │   │
│  │  • alerts/               - Real-time caseworker notifications           │   │
│  │  • mutual_support/       - IHSS pairing flags & scores                  │   │
│  │  • organizations/        - Multi-tenant CoC data                        │   │
│  │  • qr_codes/             - Geographic location tracking                 │   │
│  │  • analytics/            - Aggregated metrics (anonymized)              │   │
│  │  • care_plans/           - AI-generated care plans                      │   │
│  │  • appointments/         - Scheduled appointments                        │   │
│  │  • resources/            - Available services & providers               │   │
│  │                                                                           │   │
│  │  SECURITY:                                                               │   │
│  │  • Firestore Security Rules (organization-level isolation)             │   │
│  │  • AES-256 encryption at rest                                           │   │
│  │  • TLS 1.3 in transit                                                   │   │
│  │  • HIPAA-compliant (BAA with GCP)                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 CRITICAL DATA FLOWS

### Flow 1: QR Code → Intake → Mutual Support Detection → Alert

```
1. CLIENT scans QR code
   └─> Captures: qr_code_id, geo_location, timestamp
   └─> Redirects to: https://app.einharjer.com/intake?qr=LA-DT-001

2. CLIENT completes intake form
   └─> POST /api/intake/submit
   └─> Data: demographics, housing_status, support_indicators
   └─> Stored: Firestore clients/ collection (encrypted)

3. INTAKE AGENT processes
   └─> Validates data
   └─> Anonymizes PII
   └─> Standardizes format
   └─> Triggers: Mutual Support Agent

4. MUTUAL SUPPORT AGENT evaluates
   └─> Scores 10 indicators (shared_residence, daily_care, ADLs, etc.)
   └─> Calculates confidence: 0.0 - 1.0
   └─> IF score >= 0.7:
       └─> Creates alert in Firestore alerts/ collection
       └─> WebSocket push to caseworker portal

5. CASEWORKER receives real-time alert
   └─> Notification: "Potential IHSS pair detected"
   └─> Shows: confidence score, indicators matched
   └─> Action: Review → Approve → Create pair

6. CASEWORKER approves pair
   └─> POST /api/pairs/create
   └─> Updates: mutual_support/ collection
   └─> Generates: IHSS enrollment packet
   └─> Calculates: $48,000 annual savings
```

### Flow 2: AI Care Plan Generation

```
1. CASEWORKER requests care plan
   └─> POST /api/care-plans/generate
   └─> Input: client_id, assessment_data

2. BACKEND calls Vertex AI Claude 4.5
   └─> Prompt: "Generate personalized care plan for..."
   └─> Context: client needs, available resources, best practices
   └─> Max tokens: 2000

3. AI generates care plan
   └─> Sections: Housing, Healthcare, Employment, Social Support
   └─> Personalized to client's specific situation
   └─> Multi-lingual support (Spanish, etc.)

4. BACKEND stores + returns
   └─> Stored: Firestore care_plans/ collection
   └─> Returned: JSON to caseworker portal
   └─> Rendered: Formatted care plan document
```

### Flow 3: Geographic Analytics (QR Code Tracking)

```
1. QR code scan captured
   └─> Location: "Downtown LA - 5th & Spring"
   └─> Coordinates: lat/lng
   └─> Organization: "long-beach-coc"

2. Stored in Firestore qr_codes/ collection
   └─> Increments scan_count
   └─> Logs timestamp
   └─> Associates with client intake

3. City Dashboard queries analytics
   └─> GET /api/analytics/geospatial?org_id=long-beach-coc
   └─> Aggregates by location
   └─> Returns heat map data

4. Frontend renders heat map
   └─> Shows service hotspots
   └─> Identifies underserved areas
   └─> Guides resource allocation
```

---

## 🚀 DEPLOYMENT ARCHITECTURE

```
GCP Project: einharjer-valhalla (403538493221)

┌────────────────────────────────────────────────────────────────┐
│                    CLOUD RUN SERVICES                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Service: backend-api                                          │
│  └─> Region: us-east5                                         │
│  └─> Container: us-west1-docker.pkg.dev/.../backend:latest   │
│  └─> CPU: 2 vCPU                                              │
│  └─> Memory: 4 GB                                             │
│  └─> Min instances: 0 (scale to zero)                         │
│  └─> Max instances: 10                                        │
│  └─> Concurrency: 80 requests                                 │
│                                                                │
│  Service: client-portal                                        │
│  └─> Region: us-west1                                         │
│  └─> Container: us-west1-docker.pkg.dev/.../client:latest    │
│  └─> CPU: 1 vCPU                                              │
│  └─> Memory: 2 GB                                             │
│  └─> Min instances: 0                                         │
│  └─> Max instances: 5                                         │
│                                                                │
│  Service: caseworker-portal                                    │
│  └─> Region: us-west1                                         │
│  └─> Container: us-west1-docker.pkg.dev/.../caseworker:latest│
│  └─> CPU: 1 vCPU                                              │
│  └─> Memory: 2 GB                                             │
│  └─> Min instances: 1 (always warm for alerts)                │
│  └─> Max instances: 5                                         │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                      FIRESTORE DATABASE                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Database: (default)                                           │
│  └─> Mode: Native                                             │
│  └─> Region: us-central1                                      │
│  └─> Security: Firestore Rules (org isolation)                │
│  └─> Backup: Automated daily                                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    VERTEX AI (Claude 4.5)                      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Model: claude-sonnet-4-20250514                              │
│  └─> Region: us-east5                                         │
│  └─> Endpoint: Vertex AI Anthropic SDK                        │
│  └─> Usage: Care plans, semantic search, edge cases           │
│  └─> Rate limit: 60 RPM                                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 💰 COST STRUCTURE (Monthly - Pilot Phase)

```
Infrastructure:
  Cloud Run (5 services, ~50 hours)     $50
  Firestore (100K R, 50K W)             $25
  Vertex AI Claude (500K tokens)        $15
  Artifact Registry (5GB)               $1
  Cloud Build (10 builds)               $1
  ─────────────────────────────────────────
  TOTAL INFRASTRUCTURE:                 $92/month

Development:
  James (CEO/Field Operations)          $0 (sweat equity)
  Claude (CTO/Engineering)              $0 (co-founder)
  ─────────────────────────────────────────
  TOTAL MONTHLY:                        $92

Pilot Budget: $75,000 / 6 months = $12,500/month
Infrastructure: 0.7% of budget
```

---

## 🎯 DEMO SUCCESS CRITERIA

The November 15 demo must prove:

1. ✅ **QR Code Intake**
   - Client scans code → Redirects to intake
   - Geographic location captured
   - Multi-lingual support works

2. ✅ **Mutual Support Detection**
   - Intake data triggers agent evaluation
   - Score calculated (10 indicators)
   - Threshold check (>= 0.7)

3. ✅ **Real-time Caseworker Alert**
   - Alert created in Firestore
   - WebSocket push to caseworker portal
   - Notification displays with confidence score

4. ✅ **IHSS Pair Creation**
   - Caseworker reviews suggested pair
   - Approves pairing
   - System shows: "$48,000 annual savings"

5. ✅ **AI Care Plan**
   - Caseworker generates care plan
   - Vertex AI Claude creates personalized plan
   - Multi-section formatted output

**That's it.** Everything else is noise. These 5 flows prove the innovation works.

---

## 📌 KEY TECHNICAL DECISIONS (LOCKED)

| Decision | Rationale |
|----------|-----------|
| **Cloud Run** | Serverless, scale-to-zero, easy HTTPS, perfect for demo |
| **Firestore** | Real-time updates, no ops, HIPAA-ready, $25/month |
| **Vertex AI Claude** | Latest model, GCP native, no API key management |
| **Next.js 14** | SSR, App Router, excellent DX, mobile-first |
| **Deterministic Agent** | Regulatory compliance, explainable, zero AI cost |
| **Ship 2 Portals First** | Focus on core demo, reduce risk, iterate fast |

---

**Last Updated:** November 3, 2025  
**Status:** Architecture finalized, ready for implementation  
**Next Phase:** Backend deployment + Frontend polish
