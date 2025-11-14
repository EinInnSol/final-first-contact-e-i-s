# First Contact EIS - Demo Guide

## 🎯 Demo Workflow Overview

This guide walks you through the complete demo workflow for First Contact EIS in less than 48 hours.

### Demo Flow
1. **Print QR Code** → Scan with phone
2. **Complete HUD 40 Form** → Submit intake
3. **Amber Gets SMS** → "New client assigned"
4. **Caseworker Dashboard** → AI action plan appears
5. **Click APPROVE** → Compliance notification
6. **Show City Dashboard** → Vendor tracking & impact metrics

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Twilio account (optional - works in demo mode without)

### Step 1: Environment Setup

```bash
# Copy environment file
cp env.example .env

# Edit .env and set:
DEMO_MODE=true  # This enables demo mode without real API keys
MOCK_AI_RESPONSES=true

# Optional: Add Twilio credentials for SMS
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+15555551234
```

### Step 2: Start Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Services will be available at:
# - Backend API: http://localhost:8000
# - Client Portal: http://localhost:3001
# - Caseworker Dashboard: http://localhost:3000
# - City Analytics: http://localhost:3002
# - Admin/QR Generator: http://localhost:3004
```

### Step 3: Install Dependencies (if running without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (run each in separate terminal)
cd frontend/client && npm install && npm run dev
cd frontend/caseworker && npm install && npm run dev
cd frontend/city && npm install && npm run dev
cd frontend/admin && npm install && npm run dev
```

---

## 📱 Demo Execution Steps

### Part 1: Generate QR Code (2 minutes)

1. **Open QR Generator**
   - Navigate to: `http://localhost:3004/qr-generator`
   - Click "Generate Demo QR Codes"
   - Click "Print" on any QR code (or "Print All")

2. **What You'll See:**
   - 5 QR codes for Long Beach locations
   - Each links to intake form with metadata
   - Printable format with instructions

### Part 2: Client Intake (5 minutes)

1. **Scan QR Code with Phone**
   - Scan the printed QR code
   - Opens: `http://[your-url]/intake?loc=downtown_library&area=90802`

2. **Complete Intake Form**
   - **Personal Info:** Enter demo data
     - First Name: Maria
     - Last Name: Rodriguez
     - DOB: 01/15/1985
     - Phone: (562) 555-0123

   - **HUD 40 Assessment:** Progress through sections
     - Section 1: Personal Information
     - Section 2: Household Composition
     - Section 3: Safety and Health
     - Section 4-7: Continue through remaining sections

3. **Submit Form**
   - Click "Submit Assessment"
   - **Result Screen Shows:**
     ```
     ✅ Thank You for Completing Your Assessment

     You have been assigned:
     AMBER SCHMUTZ
     Phone: 562-681-1431
     Expect a call at: 2:30 PM today

     Case Number: FC-20241114-A3F2B1
     Crisis Level: High
     ```

4. **SMS Notification Sent** (if Twilio configured)
   - Amber receives: "🔔 New client assigned: Maria Rodriguez"

### Part 3: Caseworker Dashboard (3 minutes)

1. **Open Caseworker Demo Dashboard**
   - Navigate to: `http://localhost:3000/demo`
   - **Alternative:** If using deployed version, use your deployed URL

2. **What You'll See:**
   - **Real-time Events Feed** with new client notification
   - **AI Optimization Opportunity Card:**
     ```
     ⚡ NEW OPTIMIZATION OPPORTUNITY

     New Client Assigned: Maria Rodriguez
     Case #FC-20241114-A3F2B1
     Crisis Level: HIGH (78% score)

     📋 Reason:
     Client has higher medical urgency, all documents uploaded,
     lives on existing transport route, no conflicts.

     💡 Impact:
     Avoid $320 wasted appointment, better care for urgent case

     🔧 Actions (6 steps across 4 systems):
     1. Schedule emergency housing assessment within 24 hours
     2. Connect with childcare services immediately
     3. Initiate domestic violence safety planning
     4. Coordinate with legal aid for protection order
     5. Arrange transportation for appointments
     6. Update HMIS database

     ⏱️ Estimated time: 12 seconds
     🎯 Confidence: 94%
     ```

3. **Click [APPROVE] Button**
   - Actions execute in background
   - Card changes to "✓ APPROVED - Actions executing..."

4. **Compliance Notification Appears** (after 1 second)
   - Modal pops up:
     ```
     📋 Compliance Report Ready
     Case #FC-20241114-A3F2B1

     HUD/HMIS compliance report is ready for upload.
     Should we proceed?

     [Yes, Upload Report]  [Review First]
     ```

5. **Click "Yes, Upload Report"**
   - Report uploads to HMIS
   - Demo complete for caseworker flow

### Part 4: City Command Center (5 minutes)

1. **Open City Dashboard**
   - Navigate to: `http://localhost:3002/command-center`

2. **Key Features to Highlight:**

   **A. Key Metrics (Top Row)**
   - Total Clients Served: 1,247 (↑ 12%)
   - Active Cases: 342
   - Housing Placements: 89 (↑ 18%)
   - Avg Time to Placement: 23 days (↓ 3 days)

   **B. Vendor Performance Overview**
   - Shows 4 vendors with contract values
   - Success rates: 84-92%
   - Clients served, avg time to housing
   - Compliance scores
   - Cost per client
   - Performance bars

   **C. Geographic Distribution**
   - 5 Long Beach areas (Downtown, Cambodia Town, etc.)
   - QR scan counts
   - Intake completion rates
   - Crisis level averages
   - Top needs by area

   **D. Real-Time Activity Feed**
   - Live updates of:
     - New intakes
     - Housing placements
     - Compliance reports
     - Crisis interventions
   - Shows vendor and location

   **E. AI Insights Panel**
   - Resource optimization suggestions
   - Geographic trend warnings
   - Cost efficiency recommendations

3. **The "Wow" Moment:**
   - "This dashboard lets the city monitor EVERY vendor awarded a contract"
   - "See which areas need more resources based on QR code scans"
   - "Track vendor performance in real-time"
   - "AI suggests budget reallocation for better outcomes"

---

## 🎤 Demo Script

### Opening (30 seconds)
> "Let me show you how First Contact EIS transforms homeless services using AI and human oversight. We'll go through a complete workflow in under 2 minutes."

### Step 1: QR Code (15 seconds)
> "We place QR codes at strategic locations around the city. Each code is tagged with location and vendor metadata for tracking."
>
> *Scan QR code with phone*

### Step 2: Intake Form (30 seconds)
> "The client scans the code and gets the HUD standardized 40-question assessment, pre-filled with location data. Let me quickly submit this..."
>
> *Scroll through form, click submit*
>
> "Upon submission, the client immediately knows their assigned caseworker..."

### Step 3: Result Screen (15 seconds)
> *Show result screen*
>
> "Maria is assigned to caseworker Amber Schmutz, who will call at 2:30 PM. Amber also receives an SMS notification on her phone."

### Step 4: Caseworker Dashboard (45 seconds)
> *Switch to caseworker dashboard*
>
> "This is Amber's dashboard. She sees a real-time notification with an AI-powered action plan."
>
> "The AI analyzed the assessment and suggests 6 actions across 4 different systems - housing, childcare, legal aid, transportation."
>
> "It shows the reason, impact ($320 saved), estimated execution time (12 seconds), and 94% confidence."
>
> "Amber reviews and clicks APPROVE..."
>
> *Click approve*
>
> "Immediately, a compliance notification appears - the HUD/HMIS report is ready for upload. She clicks yes..."
>
> *Click yes*

### Step 5: City Dashboard (60 seconds)
> *Switch to city command center*
>
> "But here's the real game-changer - the City Command Center."
>
> "This dashboard shows the progress and impact of EVERY vendor awarded a contract for homeless services."
>
> "See these 4 vendors? We can track:
> - How many clients they've served
> - Their success rates (87-92%)
> - Average time to housing
> - Cost per client
> - Compliance scores"
>
> "Here's the geographic view - we see QR code scans and intake completions by area. Downtown has 234 scans, 187 intakes. Cambodia Town shows elevated crisis levels - the AI suggests deploying more resources there."
>
> "And look at the AI insights - it's recommending we reallocate 15% of budget from underperforming vendors to Pacific Housing Solutions, which has a 92% success rate. That could save $125K."
>
> "Every QR code scan is tracked to a specific location and vendor. The city has complete visibility into program effectiveness."

### Closing (15 seconds)
> "That's First Contact EIS - AI-enhanced, human-controlled civic services. From intake to placement to city-wide impact tracking, all in one integrated platform."

---

## 🔧 Troubleshooting

### Backend not starting?
```bash
# Check if ports are available
lsof -i :8000

# View logs
docker-compose logs backend
```

### Frontend not loading?
```bash
# Check if Node modules are installed
cd frontend/client && npm install

# Check port availability
lsof -i :3001
```

### QR codes not generating?
```bash
# Install qrcode library
pip install qrcode[pil]

# Check backend logs
docker-compose logs backend | grep qr
```

### SMS not sending?
- Check TWILIO_* environment variables
- Verify Twilio account has funds
- Check phone number format: +15555551234
- **Note:** Demo mode works without Twilio - SMS messages are logged instead

---

## 📊 Demo Data

### Pre-configured Locations
1. Martin Luther King Jr. Park (90805)
2. Long Beach Main Library (90802)
3. Multi-Service Center (90813)
4. Long Beach Health Center (90806)
5. Houghton Park Community Center (90815)

### Pre-configured Vendors
1. Coastal Homeless Services - $1.2M contract
2. Pacific Housing Solutions - $850K contract
3. Community Care Network - $650K contract
4. Long Beach Family Services - $550K contract

### Demo Caseworker
- Name: Amber Schmutz
- Phone: 562-681-1431
- Email: amber@firstcontact-eis.org
- Role: Caseworker

---

## 🌐 GCP Deployment (Production)

### Already Deployed
According to your architecture diagram, you have:
- **Project:** einharjer-valhalla
- **Region:** us-east5
- **Cloud Run** services configured
- **Cloud SQL** (PostgreSQL 15)
- **Firestore** for real-time events
- **BigQuery** for analytics

### Deploy Updates

```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/einharjer-valhalla/firstcontact-backend ./backend
gcloud run deploy firstcontact-backend \
  --image gcr.io/einharjer-valhalla/firstcontact-backend \
  --region us-east5 \
  --platform managed

# Build and deploy frontends
cd frontend/client
gcloud builds submit --tag gcr.io/einharjer-valhalla/firstcontact-client .
gcloud run deploy firstcontact-client --image gcr.io/einharjer-valhalla/firstcontact-client --region us-east5

# Repeat for caseworker, city, admin frontends
```

### Environment Variables (Cloud Run)
Set these in Cloud Run console or via command:
```bash
gcloud run services update firstcontact-backend \
  --update-env-vars DEMO_MODE=false,\
DATABASE_URL=postgresql://user:pass@/cloudsql/project:region:instance,\
TWILIO_ACCOUNT_SID=your_sid,\
TWILIO_AUTH_TOKEN=your_token
```

---

## ✅ Pre-Demo Checklist

- [ ] All services running (check `docker-compose ps`)
- [ ] QR code printed and ready
- [ ] Phone/tablet for scanning QR code
- [ ] Browser tabs open:
  - [ ] QR Generator (localhost:3004/qr-generator)
  - [ ] Client Intake (will open via QR scan)
  - [ ] Caseworker Dashboard (localhost:3000/demo)
  - [ ] City Command Center (localhost:3002/command-center)
- [ ] Demo script reviewed
- [ ] Screen sharing/projector tested
- [ ] Backup demo data prepared (in case of issues)

---

## 🎯 Key Selling Points

1. **AI + Human in the Loop**
   - AI suggests, humans approve
   - 95% AI work, 5% human oversight
   - 60 seconds vs 2-4 hours traditional process

2. **Vendor Accountability**
   - Real-time tracking of all contractors
   - Performance metrics visible to city
   - Data-driven contract renewals

3. **Geographic Intelligence**
   - QR codes track where clients enter system
   - Heatmaps show high-need areas
   - Deploy resources where needed most

4. **Compliance Automation**
   - HUD/HMIS reports generated automatically
   - Reduce reporting time by 90%
   - Maintain 98%+ compliance

5. **Cost Efficiency**
   - $47K average cost per placement
   - AI identifies $125K+ in savings opportunities
   - Better outcomes for same budget

---

## 📞 Support

For demo assistance:
- Check logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`
- Full reset: `docker-compose down -v && docker-compose up -d`

---

**Good luck with your demo! You've got this! 🚀**
