# First Contact E.I.S. Architecture Blueprint
## 🔒 LOCKED TECHNICAL ARCHITECTURE - DO NOT DEVIATE

**Last Updated:** November 3, 2025  
**Demo Deadline:** November 15, 2025 (12 days)  
**Pilot Value:** $75,000 Long Beach Contract  

---

## Executive Context

This is NOT just a demo - this is a **$5M+ ARR opportunity** disguised as a pilot. The platform must demonstrate:
1. **IHSS Pairing Innovation** - 52% cost savings per pair ($48K → $23K)
2. **Multi-tenant SaaS** - Each CoC gets isolated data + branded experience
3. **Federal Compliance** - HIPAA, HMIS 2026 standards, SOC 2 path
4. **Real-time Coordination** - Live caseworker alerts, geospatial analytics
5. **Transparency** - City dashboards showing ROI and outcomes

**Market Size:** 400+ Continuums of Care nationwide × $1,200-1,500/month = $5.76M-7.2M ARR

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT ENTRY POINTS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  QR Code (Geographic) ──┐                                           │
│  Mobile Web URL ────────┼──→ Client Portal (Cloud Run)              │
│  Kiosk (Field) ─────────┘                                           │
│                                                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        BACKEND API (Cloud Run)                       │
│                    FastAPI + Vertex AI Claude 4.5                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Intake Agent    │  │ Mutual Support   │  │ Classification   │ │
│  │                  │  │ Agent (IHSS)     │  │ Agent            │ │
│  │ • Data validation│  │                  │  │                  │ │
│  │ • Anonymization │  │ • 10 indicators  │  │ • Urgency scoring│ │
│  │ • Geolocation   │  │ • 0.7 threshold  │  │ • Multi-domain   │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  Audit Agent     │  │ Care Plan Gen    │  │ Resource Matcher │ │
│  │                  │  │                  │  │                  │ │
│  │ • Compliance     │  │ • AI-generated   │  │ • Service finder │ │
│  │ • Privacy checks │  │ • Personalized   │  │ • Availability   │ │
│  │ • Data sanitize  │  │ • Multi-lingual  │  │ • Referrals      │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER (Firestore)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Collections:                                                        │
│  • clients/          - Client intake records (encrypted)             │
│  • cases/            - Active case management                        │
│  • alerts/           - Real-time caseworker notifications            │
│  • mutual_support/   - IHSS pairing flags                           │
│  • organizations/    - Multi-tenant CoC data                         │
│  • qr_codes/         - Geographic location tracking                  │
│  • analytics/        - Aggregated metrics (anonymized)               │
│                                                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND PORTALS (Cloud Run)                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐  │
│  │ Client Portal   │   │ Caseworker      │   │ City Analytics  │  │
│  │                 │   │ Portal          │   │ Dashboard       │  │
│  │ • Intake forms  │   │                 │   │                 │  │
│  │ • Care plans    │   │ • Real-time     │   │ • Heat maps     │  │
│  │ • Appointments  │   │   alerts        │   │ • ROI tracking  │  │
│  │ • Resources     │   │ • Case mgmt     │   │ • Outcome data  │  │
│  │ • Multi-lang    │   │ • Pair review   │   │ • Transparency  │  │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘  │
│                                                                       │
│  ┌─────────────────┐                                                 │
│  │ Admin Portal    │                                                 │
│  │                 │                                                 │
│  │ • User mgmt     │                                                 │
│  │ • Config        │                                                 │
│  │ • Compliance    │                                                 │
│  │ • System health │                                                 │
│  └─────────────────┘                                                 │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack (LOCKED)

### Infrastructure
- **Cloud Provider:** Google Cloud Platform (GCP)
- **Project:** `einharjer-valhalla`
- **Project Number:** 403538493221
- **Region:** `us-east5` (Claude on Vertex AI availability)
- **Deployment:** Cloud Run (serverless, auto-scaling)
- **Container Registry:** Artifact Registry (`us-west1`)

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **AI Model:** Claude Sonnet 4.5 via Vertex AI AnthropicVertex SDK
- **Database:** Firestore (NoSQL, real-time)
- **Authentication:** Firebase Auth + JWT
- **API Documentation:** Auto-generated OpenAPI/Swagger

### Frontend
- **Framework:** Next.js 14+ (React 18+, App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State:** React Query + Context API
- **Real-time:** WebSocket + Firestore listeners
- **Accessibility:** WCAG 2.1 AA compliant

### Key Libraries
- **Backend:**
  - `fastapi` - API framework
  - `anthropic[vertex]` - Claude AI via Vertex
  - `firebase-admin` - Firestore + Auth
  - `pydantic` - Data validation
  - `python-jose` - JWT handling
  
- **Frontend:**
  - `react` + `next` - UI framework
  - `@tanstack/react-query` - Data fetching
  - `framer-motion` - Animations
  - `react-hot-toast` - Notifications
  - `recharts` - Data visualization

---

## Data Flow (Critical Paths)

### Path 1: QR Code → Intake → Caseworker Alert

```
1. Client scans QR code (geographic location embedded)
   └─> Location: "Downtown LA - 5th & Spring"
   └─> QR Code ID: "LA-DT-001"

2. Client Portal loads → Intake form
   └─> API: POST /api/intake/start
   └─> Stores: qr_code_id, timestamp, geo_data

3. Client completes intake
   └─> API: POST /api/intake/submit
   └─> Triggers: Mutual Support Agent evaluation

4. Mutual Support Agent scores intake
   └─> Checks 10 indicators (shared_residence, daily_care, etc.)
   └─> Score ≥ 0.7? → Create alert

5. Real-time alert to caseworker
   └─> Firestore: alerts/{alert_id}
   └─> WebSocket push to caseworker dashboard
   └─> Notification: "Potential IHSS pair detected"

6. Caseworker reviews → Approves pair
   └─> API: POST /api/pairs/create
   └─> Updates: mutual_support collection
   └─> Generates: IHSS enrollment packet
```

### Path 2: City Analytics (Transparency)

```
1. City dashboard requests metrics
   └─> API: GET /api/analytics/overview?org_id={coc_id}

2. Backend aggregates anonymized data
   └─> Firestore query: analytics collection
   └─> Calculates:
       • Total intakes this month
       • IHSS pairs identified
       • Housing placements
       • Cost savings ($48K → $23K per pair)
       • Geographic hotspots (heat map data)

3. Dashboard renders visualizations
   └─> Heat map: QR code scan locations
   └─> Chart: Outcome trends over time
   └─> Card: "$144K saved this month (6 pairs)"
```

---

## Security & Compliance (MANDATORY)

### Data Encryption
- **At Rest:** Firestore automatic encryption
- **In Transit:** TLS 1.3 (Cloud Run default)
- **PII Fields:** AES-256 encryption before storage

### HIPAA Compliance
- ✅ Business Associate Agreement (BAA) with GCP
- ✅ Audit logging (Cloud Logging)
- ✅ Access controls (IAM roles)
- ✅ Data minimization (only necessary fields)
- ✅ Right to deletion (GDPR/CCPA compliant)

### HMIS 2026 Standards
- ✅ Universal Data Elements (UDE)
- ✅ Project Descriptor Data Elements (PDDE)
- ✅ Data Quality Framework
- ✅ CSV export format (HMIS compatible)

### Multi-Tenancy Isolation
- Each CoC has unique `organization_id`
- Firestore security rules enforce data isolation
- No cross-org data visibility (except aggregated public metrics)

---

## Deployment Architecture

### Cloud Run Services

| Service | Path | Purpose | Resources |
|---------|------|---------|-----------|
| **backend** | `/api/*` | Main API + AI agents | 2 CPU, 4GB RAM |
| **client-portal** | `/` | Client-facing intake | 1 CPU, 2GB RAM |
| **caseworker-portal** | `/caseworker` | Case management | 1 CPU, 2GB RAM |
| **city-dashboard** | `/city` | Analytics + transparency | 1 CPU, 2GB RAM |
| **admin-portal** | `/admin` | System administration | 1 CPU, 2GB RAM |

### DNS Routing (Future)
- `api.einharjer.com` → backend
- `app.einharjer.com` → client-portal
- `caseworker.einharjer.com` → caseworker-portal
- `analytics.einharjer.com` → city-dashboard
- `admin.einharjer.com` → admin-portal

**Current (Demo):** Cloud Run auto-generated URLs

---

## Mutual Support Agent (Core Innovation)

### Detection Logic (Deterministic)

```python
class MutualSupportAgent:
    """
    Detects existing mutual care relationships for IHSS pairing.
    DETERMINISTIC scoring - NOT AI inference.
    """
    
    INDICATORS = {
        'shared_residence': 0.15,        # Live together
        'daily_care_provided': 0.15,     # Daily care given
        'assists_with_ADLs': 0.12,       # Help with ADLs
        'financial_interdependence': 0.10, # Shared finances
        'emergency_contact': 0.08,       # Listed as emergency contact
        'transportation_support': 0.08,  # Provides transport
        'meal_preparation': 0.08,        # Prepares meals
        'medication_management': 0.08,   # Manages meds
        'emotional_support': 0.08,       # Emotional care
        'advocacy_support': 0.08         # Advocates for them
    }
    
    THRESHOLD = 0.7  # 70% confidence for alert
    
    def evaluate(self, intake_record):
        score = 0.0
        for indicator, weight in self.INDICATORS.items():
            if intake_record.get(indicator, False):
                score += weight
        
        if score >= self.THRESHOLD:
            return {
                'status': 'mutual_support_detected',
                'confidence': score,
                'recommended_action': 'notify_caseworker',
                'potential_savings': 48000  # $48K per pair
            }
        
        return {'status': 'no_alert', 'confidence': score}
```

### Why Deterministic vs AI?
- ✅ **Regulatory compliance** - Explainable decisions
- ✅ **Cost efficiency** - No AI inference costs
- ✅ **Auditability** - Clear scoring logic
- ✅ **Speed** - Instant evaluation (no API calls)
- ✅ **Accuracy** - Domain experts defined weights

### When AI IS Used (5% of Operations)
- Care plan generation (personalized narratives)
- Resource matching (semantic search)
- Language translation (multi-lingual support)
- Ambiguous case review (edge cases)

---

## QR Code System (Geospatial Tracking)

### QR Code Structure

```json
{
  "qr_code_id": "LA-DT-001",
  "location": {
    "name": "Downtown LA - 5th & Spring",
    "lat": 34.0522,
    "lng": -118.2437,
    "type": "street_corner"
  },
  "organization_id": "long-beach-coc",
  "created_at": "2025-11-01T00:00:00Z",
  "scan_count": 247,
  "url": "https://app.einharjer.com/intake?qr=LA-DT-001"
}
```

### Geographic Analytics
- **Heat Map:** Where clients are accessing services
- **Resource Allocation:** Deploy services to high-traffic areas
- **Trend Analysis:** Track usage patterns over time
- **Multi-Org Comparison:** Benchmark across CoCs

---

## API Endpoints (Core Routes)

### Public Endpoints
- `POST /api/intake/start` - Begin intake (captures QR code)
- `POST /api/intake/submit` - Complete intake (triggers agents)
- `GET /api/resources` - Find available services
- `POST /api/appointments/schedule` - Book appointments

### Caseworker Endpoints (Auth Required)
- `GET /api/alerts` - Real-time caseworker notifications
- `GET /api/cases` - Active caseload
- `POST /api/pairs/review` - Review IHSS pair suggestion
- `POST /api/pairs/create` - Formalize IHSS pairing
- `POST /api/care-plans/generate` - AI-generated care plan

### City Admin Endpoints (Auth Required)
- `GET /api/analytics/overview` - Dashboard metrics
- `GET /api/analytics/outcomes` - Outcome data
- `GET /api/analytics/geospatial` - Heat map data
- `GET /api/analytics/financial` - Cost savings

### System Admin Endpoints (Auth Required)
- `GET /api/admin/organizations` - Manage CoCs
- `POST /api/admin/users` - User management
- `GET /api/admin/compliance` - Audit logs
- `GET /api/admin/health` - System health

---

## Performance Targets

### Response Times
- **Intake submission:** < 2 seconds
- **Mutual Support Agent:** < 500ms (deterministic)
- **AI care plan generation:** < 5 seconds
- **Dashboard load:** < 3 seconds

### Availability
- **Uptime:** 99.9% (Cloud Run SLA)
- **Offline support:** Client portal works offline (service worker)

### Scale
- **Concurrent users:** 1,000+ (Cloud Run auto-scale)
- **Daily intakes:** 10,000+ capacity
- **Database:** Firestore handles 1M+ docs effortlessly

---

## UX/UI Design Philosophy

### Accessibility First
- WCAG 2.1 AA compliance
- Screen reader optimized
- High contrast mode
- Large text mode
- Reduced motion option
- Keyboard navigation

### Multi-Language Support
- English, Spanish (initial)
- Expandable to 12+ languages
- AI-powered translations
- Cultural sensitivity

### Mobile-First
- 80% of clients use mobile devices
- Touch-optimized UI
- Offline-capable
- Progressive Web App (PWA)

### Visual Design (TO BE DECIDED WITH JAMES)
- **Color palette:** TBD
- **Typography:** TBD
- **Component library:** TBD
- **Brand identity:** TBD

**🚫 DO NOT PROCEED WITH STYLING WITHOUT APPROVAL 🚫**

---

## Development Workflow

### Git Strategy
- **Main branch:** `main` (production-ready)
- **Dev branch:** `gcp-vertex-deployment` (active development)
- **Feature branches:** `feature/{name}`
- **Hotfix branches:** `hotfix/{issue}`

### Deployment Pipeline
1. Local development → Test
2. Commit to `gcp-vertex-deployment`
3. Push to GitHub
4. Manual Cloud Build trigger
5. Deploy to Cloud Run (staging)
6. Test staging environment
7. Merge to `main` → Production deploy

### Testing Strategy
- **Unit tests:** Backend agents (pytest)
- **Integration tests:** API endpoints
- **E2E tests:** Critical user flows
- **Manual QA:** Full system walkthrough

---

## Milestones to Demo (12 Days)

### Phase 1: Foundation (Days 1-3) ✅ CURRENT
- [x] Backend API architecture
- [x] Mutual Support Agent (deterministic)
- [x] Firestore schema design
- [x] Vertex AI integration
- [ ] Deploy backend to Cloud Run
- [ ] Test API endpoints

### Phase 2: Frontend Build (Days 4-7)
- [ ] Finalize UX/UI design with James
- [ ] Build client portal (intake flow)
- [ ] Build caseworker portal (alerts + cases)
- [ ] Build city dashboard (analytics)
- [ ] Build admin portal (system mgmt)
- [ ] Deploy frontends to Cloud Run

### Phase 3: Integration (Days 8-10)
- [ ] Connect frontends to backend
- [ ] Real-time WebSocket alerts
- [ ] QR code system (geographic tracking)
- [ ] Mutual Support Agent end-to-end test
- [ ] Geospatial heat map
- [ ] Multi-tenant isolation testing

### Phase 4: Polish (Days 11-12)
- [ ] Demo script + walkthrough
- [ ] Performance optimization
- [ ] Security audit
- [ ] Compliance checklist
- [ ] Presentation deck
- [ ] Live demo rehearsal

---

## Cost Estimate (Monthly - Pilot Phase)

| Resource | Usage | Cost |
|----------|-------|------|
| Cloud Run (5 services) | ~50 hours/month | $50 |
| Firestore | 100K reads, 50K writes | $25 |
| Vertex AI (Claude) | 500K tokens/month | $15 |
| Artifact Registry | 5GB storage | $0.50 |
| Cloud Build | 10 builds/month | $1 |
| **TOTAL** | | **~$91.50/month** |

**Pilot Budget:** $75,000 / 6 months = $12,500/month  
**Infrastructure:** ~$100/month (0.8% of budget)

---

## Success Metrics (Demo Goals)

### Functional Proof
- ✅ Client completes intake via QR code
- ✅ Mutual Support Agent detects pair (score ≥ 0.7)
- ✅ Caseworker receives real-time alert
- ✅ Care plan generated (AI-powered)
- ✅ City dashboard shows ROI ($48K savings)

### Differentiation
- ✅ IHSS pairing innovation (52% cost reduction)
- ✅ Real-time coordination (not batch processing)
- ✅ Geospatial analytics (QR code tracking)
- ✅ Multi-tenant SaaS (400+ CoC market)
- ✅ Transparency (city dashboard shows outcomes)

### Compliance
- ✅ HIPAA ready (BAA with GCP)
- ✅ HMIS 2026 standards
- ✅ SOC 2 path documented

---

## 🔒 CRITICAL: DO NOT DEVIATE

This architecture is **locked** for the demo timeline. Any changes require explicit approval from James.

**Questions? Check with James before proceeding.**

---

**Last Updated:** November 3, 2025  
**Next Review:** After demo (November 16, 2025)
