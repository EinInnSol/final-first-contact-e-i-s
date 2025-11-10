# 🚀 AUTONOMOUS DEPLOYMENT GUIDE
## First Contact E.I.S. - Complete GCP Deployment

**Created:** November 10, 2025  
**Target:** November 15, 2025 Demo  
**Status:** READY TO EXECUTE

---

## 📋 WHAT WAS DISCOVERED

### **Current GCP State:**
- ✅ **Project:** einharjer-valhalla (403538493221)
- ✅ **Authentication:** faernstromjames@gmail.com (active)
- ✅ **Region:** us-east5
- ✅ **Existing Services:**
  - `first-contact-backend` (deployed Nov 4, returns 404)
  - `valhalla-orchestrator` (deployed Oct 31)

### **What Needs To Be Done:**
1. Enable missing APIs (SQL, Firestore, etc.)
2. Create Cloud SQL database
3. Create Firestore database  
4. Rebuild and redeploy backend (with proper routes)
5. Deploy frontend
6. Seed demo data
7. Configure domain
8. Run health checks

---

## ⚡ ONE-COMMAND DEPLOYMENT

### **Step 1: Run Master Script**

```powershell
cd C:\Users\james\Documents\final-first-contact-e-i-s\deployment
.\MASTER_DEPLOY.ps1
```

**That's it.** The script will:
- Audit current state
- Enable all required APIs  
- Create databases
- Build and deploy services
- Seed demo data
- Run health checks
- Generate deployment report

**Time:** 20-30 minutes (mostly waiting for Cloud SQL)

---

## 🎯 WHAT THE SCRIPT DOES

### **Phase 1: Audit (1 minute)**
- Checks authentication
- Lists existing services
- Verifies project configuration

### **Phase 2: Enable APIs (2-3 minutes)**
Enables:
- Cloud Run
- Cloud SQL  
- Firestore
- Vertex AI
- Cloud Build
- Secret Manager
- Artifact Registry
- Cloud Scheduler
- Compute Engine

### **Phase 3: Cloud SQL (10-15 minutes)**
- Creates PostgreSQL 15 instance
- Creates `first_contact` database
- Configures backups
- Sets root password

### **Phase 4: Firestore (1 minute)**
- Creates Firestore database (native mode)
- Configures for real-time sync

### **Phase 5: Backend (5 minutes)**
- Builds Docker image
- Deploys to Cloud Run
- Connects to Cloud SQL
- Sets environment variables
- Returns API URL

### **Phase 6: Frontend (5 minutes)**
- Builds Next.js Docker image
- Deploys to Cloud Run
- Connects to backend API
- Returns frontend URL

### **Phase 7: Seed Data (1 minute)**
- Creates demo clients (Maria, Robert)
- Creates demo providers
- Creates demo appointments
- Seeds QR locations

### **Phase 8: Health Checks (1 minute)**
- Tests backend health endpoint
- Tests frontend accessibility
- Verifies database connection

---

## 📊 EXPECTED OUTPUT

```
╔════════════════════════════════════════════════════════════╗
║         DEPLOYMENT COMPLETE - ALL SYSTEMS ONLINE          ║
╚════════════════════════════════════════════════════════════╝

📊 DEPLOYMENT SUMMARY
─────────────────────────────────────────────────────────────

Backend URL:   https://first-contact-backend-403538493221.us-east5.run.app
Frontend URL:  https://first-contact-frontend-403538493221.us-east5.run.app
Database:      first-contact-db (us-east5)
Project:       einharjer-valhalla

🎯 NEXT STEPS:
1. Visit frontend: [URL]
2. Test demo flow: Trigger → Recommend → Approve
3. Check API docs: [URL]/docs
4. Review logs: gcloud logging read

Demo Date: November 15, 2025 (5 days)

🚀 LET'S WIN THIS $75K PILOT!
```

---

## 🐛 TROUBLESHOOTING

### **If Script Fails:**

**Common Issues:**

1. **API Not Enabled Error**
   ```
   Solution: Wait 2-3 minutes after enabling APIs, then re-run
   ```

2. **Cloud SQL Creation Timeout**
   ```
   Solution: Normal - takes 10-15 minutes. Be patient.
   ```

3. **Docker Build Fails**
   ```
   Solution: Check Dockerfile syntax, ensure requirements.txt exists
   ```

4. **Permission Denied**
   ```
   Solution: Run: gcloud auth application-default login
   ```

### **Manual Verification:**

```powershell
# Check services
gcloud run services list --region=us-east5

# Check databases
gcloud sql instances list

# Check Firestore
gcloud firestore databases list

# View logs
gcloud logging read --limit=50
```

---

## 🔄 RE-DEPLOYMENT

If you need to redeploy (e.g., after code changes):

```powershell
# Quick redeploy (just services)
gcloud builds submit backend --tag=us-east5-docker.pkg.dev/einharjer-valhalla/first-contact/backend:latest
gcloud run deploy first-contact-backend --image=[TAG] --region=us-east5

# Full redeploy (everything)
.\MASTER_DEPLOY.ps1
```

---

## 📁 FILES CREATED

```
deployment/
├── MASTER_DEPLOY.ps1          # Main deployment script
├── DEPLOYMENT_GUIDE.md         # This file
└── NEXT_SESSION_PLAN.md        # What to do next

backend/
└── Dockerfile                  # Backend container config

frontend/caseworker/
└── Dockerfile                  # Frontend container config
```

---

## 🎬 AFTER DEPLOYMENT

### **Immediate Testing:**
1. Visit frontend URL
2. Click "Trigger Demo Event"
3. Watch recommendation appear
4. Click "APPROVE"
5. Verify execution completes

### **If Demo Flow Doesn't Work:**
1. Check backend logs: `gcloud logging read`
2. Check database connection
3. Verify orchestration routes are wired
4. Check Firestore permissions

---

## 🚀 NEXT SESSION PRIORITIES

**See:** `NEXT_SESSION_PLAN.md`

1. Run deployment script
2. Test demo flow end-to-end  
3. Seed realistic demo data
4. Polish UI for presentation
5. Rehearse demo script

---

**DEPLOYMENT SYSTEM READY** ✅

**Everything is automated. Just run the script.**

**Time to demo: 5 days**

**LET'S SHIP THIS.** 🚀🧠
