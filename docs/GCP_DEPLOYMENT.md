# 🚀 GCP Deployment Guide - First Contact EIS

**Complete guide to deploying First Contact EIS on Google Cloud Platform**

---

## 📋 Prerequisites

- ✅ GCP Account with billing enabled
- ✅ Project: `einharjer-valhalla` (Project Number: 403538493221)
- ✅ Claude models enabled in Vertex AI (4.5, Opus 4.1, 3.7)
- ✅ Google Cloud SDK (`gcloud`) installed and configured
- ✅ Docker installed locally (for building images)

---

## 🏗️ Architecture Overview

```
einharjer.com
├── Cloud Load Balancer (HTTPS)
│   ├── SSL Certificate (Google-managed)
│   └── URL Maps
│
├── Cloud Run Services
│   ├── backend-api (port 8000)
│   ├── client-portal (port 3000)
│   ├── caseworker-dashboard (port 3001)
│   ├── city-analytics (port 3002)
│   └── admin-dashboard (port 3004)
│
├── Cloud SQL (PostgreSQL 15)
│   └── Instance: firstcontact-db
│
├── Cloud Memorystore (Redis)
│   └── Instance: firstcontact-cache
│
├── Vertex AI
│   ├── Claude Sonnet 4.5
│   ├── Claude Opus 4.1
│   └── Claude 3.7
│
└── Artifact Registry
    └── Docker images
```

---

## 🎯 Step-by-Step Deployment

### **Phase 1: Enable Required APIs**

```bash
# Ensure you're in the right project
gcloud config set project einharjer-valhalla

# Enable required APIs (some may already be enabled)
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    sqladmin.googleapis.com \
    redis.googleapis.com \
    compute.googleapis.com \
    vpcaccess.googleapis.com \
    aiplatform.googleapis.com
```

---

### **Phase 2: Create Artifact Registry**

```bash
# Create Docker repository
gcloud artifacts repositories create first-contact-eis \
    --repository-format=docker \
    --location=us-west1 \
    --description="First Contact EIS Docker images"

# Configure Docker to use Artifact Registry
gcloud auth configure-docker us-west1-docker.pkg.dev
```

---

### **Phase 3: Set Up Cloud SQL (PostgreSQL)**

```bash
# Create PostgreSQL instance (this takes ~10 minutes)
gcloud sql instances create firstcontact-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-west1 \
    --root-password=CHANGE_ME_SECURE_PASSWORD \
    --availability-type=zonal \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup \
    --backup-start-time=03:00

# Create database
gcloud sql databases create firstcontact_eis \
    --instance=firstcontact-db

# Create database user
gcloud sql users create firstcontact \
    --instance=firstcontact-db \
    --password=CHANGE_ME_DB_PASSWORD

# Get connection name (save this!)
gcloud sql instances describe firstcontact-db \
    --format="value(connectionName)"
# Output: einharjer-valhalla:us-west1:firstcontact-db
```

---

### **Phase 4: Set Up Cloud Memorystore (Redis)**

```bash
# Create Redis instance (this takes ~5 minutes)
gcloud redis instances create firstcontact-cache \
    --size=1 \
    --region=us-west1 \
    --redis-version=redis_7_0 \
    --tier=basic

# Get Redis host (save this!)
gcloud redis instances describe firstcontact-cache \
    --region=us-west1 \
    --format="value(host)"
```

---

### **Phase 5: Create VPC Connector (for Cloud Run to access Cloud SQL/Redis)**

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create firstcontact-connector \
    --region=us-west1 \
    --network=default \
    --range=10.8.0.0/28
```

---

### **Phase 6: Build and Push Docker Images**

#### **Backend API**

```bash
cd backend

# Build Docker image
docker build -t us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/backend:latest .

# Push to Artifact Registry
docker push us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/backend:latest

cd ..
```

#### **Frontend Applications**

```bash
# Client Portal
cd frontend/client
docker build -t us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/client:latest .
docker push us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/client:latest
cd ../..

# Caseworker Dashboard
cd frontend/caseworker
docker build -t us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/caseworker:latest .
docker push us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/caseworker:latest
cd ../..

# City Analytics
cd frontend/city
docker build -t us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/city:latest .
docker push us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/city:latest
cd ../..

# Admin Dashboard
cd frontend/admin
docker build -t us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/admin:latest .
docker push us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/admin:latest
cd ../..
```

---

### **Phase 7: Deploy to Cloud Run**

#### **Backend API**

```bash
gcloud run deploy backend-api \
    --image=us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/backend:latest \
    --region=us-west1 \
    --platform=managed \
    --allow-unauthenticated \
    --port=8000 \
    --min-instances=1 \
    --max-instances=10 \
    --memory=2Gi \
    --cpu=2 \
    --vpc-connector=firstcontact-connector \
    --set-env-vars="GCP_PROJECT_ID=einharjer-valhalla,GCP_REGION=us-west1,DEMO_MODE=false" \
    --set-secrets="DATABASE_URL=DATABASE_URL:latest,REDIS_URL=REDIS_URL:latest,SECRET_KEY=SECRET_KEY:latest" \
    --add-cloudsql-instances=einharjer-valhalla:us-west1:firstcontact-db

# Get backend URL (save this for frontend)
gcloud run services describe backend-api \
    --region=us-west1 \
    --format="value(status.url)"
```

#### **Frontend Services**

```bash
# Get the backend API URL from above
BACKEND_URL=$(gcloud run services describe backend-api --region=us-west1 --format="value(status.url)")

# Client Portal
gcloud run deploy client-portal \
    --image=us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/client:latest \
    --region=us-west1 \
    --platform=managed \
    --allow-unauthenticated \
    --port=3000 \
    --memory=512Mi \
    --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}"

# Caseworker Dashboard
gcloud run deploy caseworker-dashboard \
    --image=us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/caseworker:latest \
    --region=us-west1 \
    --platform=managed \
    --allow-unauthenticated \
    --port=3001 \
    --memory=512Mi \
    --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}"

# City Analytics
gcloud run deploy city-analytics \
    --image=us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/city:latest \
    --region=us-west1 \
    --platform=managed \
    --allow-unauthenticated \
    --port=3002 \
    --memory=512Mi \
    --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}"

# Admin Dashboard
gcloud run deploy admin-dashboard \
    --image=us-west1-docker.pkg.dev/einharjer-valhalla/first-contact-eis/admin:latest \
    --region=us-west1 \
    --platform=managed \
    --allow-unauthenticated \
    --port=3004 \
    --memory=512Mi \
    --set-env-vars="NEXT_PUBLIC_API_URL=${BACKEND_URL}"
```

---

### **Phase 8: Set Up Secrets Manager**

```bash
# Create secrets (replace with actual values)
echo -n "postgresql://firstcontact:PASSWORD@/firstcontact_eis?host=/cloudsql/einharjer-valhalla:us-west1:firstcontact-db" | \
    gcloud secrets create DATABASE_URL --data-file=-

echo -n "redis://REDIS_HOST:6379" | \
    gcloud secrets create REDIS_URL --data-file=-

echo -n "YOUR_SUPER_SECRET_JWT_KEY_HERE" | \
    gcloud secrets create SECRET_KEY --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding DATABASE_URL \
    --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding REDIS_URL \
    --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding SECRET_KEY \
    --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

---

### **Phase 9: Configure Domain (einharjer.com)**

#### **Option A: Cloud Load Balancer (Recommended for Production)**

```bash
# Reserve external IP
gcloud compute addresses create einharjer-lb-ip \
    --ip-version=IPV4 \
    --global

# Get the IP address (configure DNS)
gcloud compute addresses describe einharjer-lb-ip \
    --global \
    --format="value(address)"

# Create managed SSL certificate
gcloud compute ssl-certificates create einharjer-cert \
    --domains=einharjer.com,www.einharjer.com,api.einharjer.com

# Create backend services, URL maps, etc. (see full guide in GCP docs)
```

#### **Option B: Cloud Run Domain Mapping (Simpler)**

```bash
# Map domain to each service
gcloud beta run domain-mappings create \
    --service=client-portal \
    --domain=einharjer.com \
    --region=us-west1

gcloud beta run domain-mappings create \
    --service=backend-api \
    --domain=api.einharjer.com \
    --region=us-west1

gcloud beta run domain-mappings create \
    --service=caseworker-dashboard \
    --domain=staff.einharjer.com \
    --region=us-west1

# Update DNS records as instructed by the output
```

---

### **Phase 10: Run Database Migrations**

```bash
# Connect to Cloud SQL via proxy
cloud_sql_proxy -instances=einharjer-valhalla:us-west1:firstcontact-db=tcp:5432 &

# Run Alembic migrations
cd backend
export DATABASE_URL="postgresql://firstcontact:PASSWORD@localhost:5432/firstcontact_eis"
alembic upgrade head
cd ..
```

---

## 🧪 Testing Deployment

```bash
# Get service URLs
echo "Backend API:"
gcloud run services describe backend-api --region=us-west1 --format="value(status.url)"

echo "Client Portal:"
gcloud run services describe client-portal --region=us-west1 --format="value(status.url)"

echo "Caseworker Dashboard:"
gcloud run services describe caseworker-dashboard --region=us-west1 --format="value(status.url)"

echo "City Analytics:"
gcloud run services describe city-analytics --region=us-west1 --format="value(status.url)"

echo "Admin Dashboard:"
gcloud run services describe admin-dashboard --region=us-west1 --format="value(status.url)"

# Test backend health
BACKEND_URL=$(gcloud run services describe backend-api --region=us-west1 --format="value(status.url)")
curl ${BACKEND_URL}/health
curl ${BACKEND_URL}/api/ai/health
```

---

## 📊 Monitoring & Logs

```bash
# View logs
gcloud run services logs read backend-api --region=us-west1
gcloud run services logs read client-portal --region=us-west1

# Open Cloud Console monitoring
echo "Monitoring: https://console.cloud.google.com/monitoring"
echo "Logs: https://console.cloud.google.com/logs"
echo "Cloud Run: https://console.cloud.google.com/run"
```

---

## 💰 Cost Estimate (Monthly)

| Service | Configuration | Estimated Cost |
|---------|--------------|----------------|
| Cloud SQL | db-f1-micro, 10GB | ~$10 |
| Cloud Memorystore | 1GB Redis | ~$30 |
| Cloud Run | 5 services, light traffic | ~$20 |
| Vertex AI | Claude API calls | Pay-per-use (~$50-100) |
| Load Balancer | Optional | ~$20 |
| **Total** | | **~$130-180/month** |

---

## 🚨 Important Notes

1. **Secrets**: Change all placeholder passwords before deploying
2. **Firewall**: Cloud Run services are publicly accessible by default
3. **Backups**: Cloud SQL backups are enabled (daily at 3 AM)
4. **Vertex AI**: Authentication uses Application Default Credentials (ADC)
5. **Scaling**: Cloud Run auto-scales (1-10 instances per service)
6. **Kiosk**: Removed from deployment (as requested)

---

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Domain Mapping Guide](https://cloud.google.com/run/docs/mapping-custom-domains)

---

**Deployment Checklist:**

- [ ] Phase 1: Enable APIs
- [ ] Phase 2: Create Artifact Registry
- [ ] Phase 3: Set up Cloud SQL
- [ ] Phase 4: Set up Redis
- [ ] Phase 5: Create VPC Connector
- [ ] Phase 6: Build and push Docker images
- [ ] Phase 7: Deploy to Cloud Run
- [ ] Phase 8: Configure secrets
- [ ] Phase 9: Configure domain
- [ ] Phase 10: Run migrations
- [ ] Test all services
- [ ] Monitor and optimize

---

**Built with ❤️ for Long Beach's vulnerable populations**
