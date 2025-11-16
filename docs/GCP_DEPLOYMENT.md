# 🚀 First Contact EIS - GCP Native Deployment Guide

## Overview

This guide covers the **fully automated, viral GCP deployment system** for First Contact EIS. The system is designed to unfold like a virus - clone the repo, run one command, and watch your entire infrastructure provision and deploy automatically.

## 🎯 What Gets Deployed

### Infrastructure (via Terraform)
- **Cloud Run**: 6 serverless services (backend + 5 frontends)
- **Cloud SQL**: Managed PostgreSQL database with automatic backups
- **Cloud Memorystore**: Managed Redis for caching
- **Cloud Tasks**: Background job processing
- **Artifact Registry**: Private container image repository
- **Secret Manager**: Secure secrets storage
- **Cloud Storage**: Static assets and backups
- **VPC**: Private networking for secure communication
- **Cloud Monitoring**: Full observability with alerts
- **Cloud Scheduler**: Automated maintenance tasks

### Services
1. **Backend API** - FastAPI with all AI modules
2. **Client Portal** - Public-facing client interface
3. **Caseworker Dashboard** - Case management system
4. **City Analytics** - Municipal intelligence dashboard
5. **Kiosk Interface** - Public kiosk application
6. **Admin Dashboard** - System administration

## 🔥 Viral Deployment (One Command)

### Prerequisites
- GCP account with billing enabled
- Cloud Shell or local machine with gcloud CLI

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd first-contact-eis
```

### Step 2: Run Viral Deployment
```bash
./deploy.sh
```

That's it! The script will:
1. ✅ Detect or create GCP project
2. ✅ Enable all required APIs
3. ✅ Configure billing (with prompts)
4. ✅ Install Terraform
5. ✅ Provision all infrastructure
6. ✅ Build all container images
7. ✅ Deploy all services
8. ✅ Run database migrations
9. ✅ Display all service URLs

**Total deployment time: ~15-20 minutes**

## 📋 Deployment Environments

### Development (Default)
```bash
./deploy.sh development
```
- Minimal resources (free tier eligible)
- Scale-to-zero enabled
- db-f1-micro database
- 1GB Redis

### Staging
```bash
./deploy.sh staging
```
- Medium resources
- Min 1 instance per service
- db-g1-small database
- 2GB Redis

### Production
```bash
./deploy.sh production
```
- High availability
- Regional database with replicas
- db-custom-4-16384 database
- 5GB Redis with HA
- Alert notifications enabled

## 🛠️ Management Scripts

All management scripts are in `gcp/scripts/`:

### View Logs
```bash
./gcp/scripts/logs.sh
```
Interactive menu to view logs from any service.

### Check Status
```bash
./gcp/scripts/status.sh
```
Complete status report of all infrastructure.

### Scale Services
```bash
./gcp/scripts/scale.sh
```
Interactive scaling for any service.

### Update Services
```bash
./gcp/scripts/update.sh
```
Rebuild and redeploy all services with latest code.

### Destroy Everything
```bash
./gcp/scripts/destroy.sh
```
Complete infrastructure teardown.

## 🔧 Manual Operations

### View Service URLs
```bash
gcloud run services list --region=us-central1
```

### View Logs for Specific Service
```bash
gcloud run services logs read firstcontact-eis-backend --region=us-central1
```

### Update Single Service
```bash
# Build new image
gcloud builds submit --tag=us-central1-docker.pkg.dev/$PROJECT_ID/firstcontact-eis-images/backend:latest ./backend

# Deploy
gcloud run deploy firstcontact-eis-backend \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/firstcontact-eis-images/backend:latest \
  --region=us-central1
```

### Connect to Database
```bash
# Get Cloud SQL proxy
gcloud sql connect firstcontact-eis-db --user=firstcontact
```

### View Secrets
```bash
gcloud secrets list
gcloud secrets versions access latest --secret=jwt-secret
```

## 📊 Infrastructure Management

### Terraform Commands
```bash
cd gcp/terraform

# View current state
terraform show

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy everything
terraform destroy
```

### Update Infrastructure
1. Edit `gcp/terraform/terraform.tfvars`
2. Run `terraform plan` to preview changes
3. Run `terraform apply` to apply changes

### Common Infrastructure Updates

#### Upgrade Database
```hcl
# In terraform.tfvars
db_tier = "db-custom-2-8192"  # 2 vCPU, 8GB RAM
```

#### Increase Redis Memory
```hcl
# In terraform.tfvars
redis_memory_gb = 5
```

#### Scale Cloud Run
```hcl
# In terraform.tfvars
max_instances = 100
```

## 🔐 Security Best Practices

### Secrets Management
- All secrets stored in Secret Manager
- Automatic rotation recommended
- Never commit secrets to git

### Database Security
- Private networking only (no public IP)
- SSL required for all connections
- Automatic backups enabled
- Point-in-time recovery available

### Network Security
- VPC for private communication
- Cloud Run uses managed SSL
- IAM for fine-grained access control

### Update Secrets
```bash
# Update database password
gcloud secrets versions add db-password --data-file=-
# Enter new password, then Ctrl+D

# Update JWT secret
gcloud secrets versions add jwt-secret --data-file=-
# Enter new secret, then Ctrl+D
```

## 💰 Cost Optimization

### Free Tier Resources
- Cloud Run: 2M requests/month free
- Cloud SQL: f1-micro free (with limits)
- Cloud Storage: 5GB free
- Secret Manager: 6 secrets free

### Development Tips
1. Use scale-to-zero for all services
2. Use db-f1-micro database
3. Use 1GB Redis
4. Delete when not in use: `./gcp/scripts/destroy.sh`

### Production Costs (Estimated)
- Cloud Run (6 services): ~$20-50/month
- Cloud SQL (db-custom-2-8192): ~$100/month
- Redis (5GB HA): ~$80/month
- Storage & Networking: ~$10/month
- **Total: ~$210-250/month**

### Cost Reduction
```bash
# Stop database (keeps data)
gcloud sql instances patch firstcontact-eis-db --activation-policy=NEVER

# Restart database
gcloud sql instances patch firstcontact-eis-db --activation-policy=ALWAYS

# Scale down all services
./gcp/scripts/scale.sh
# Set min=0, max=1 for all
```

## 📈 Monitoring & Alerts

### View Metrics
```bash
# Open Cloud Console Monitoring
gcloud monitoring dashboards list
```

### Configure Alerts
Edit `gcp/terraform/main.tf` to add more alert policies:
```hcl
resource "google_monitoring_alert_policy" "custom_alert" {
  display_name = "Custom Alert"
  # ... configuration
}
```

### Log Analysis
```bash
# View error logs
gcloud logging read "severity>=ERROR" --limit=50

# View specific service logs
gcloud logging read "resource.labels.service_name=firstcontact-eis-backend" --limit=100

# Export logs to BigQuery
gcloud logging sinks create my-sink \
  bigquery.googleapis.com/projects/$PROJECT_ID/datasets/logs_dataset \
  --log-filter='resource.type="cloud_run_revision"'
```

## 🔄 CI/CD Integration

### GitHub Actions
The system includes Cloud Build integration. To set up automatic deployments:

1. Enable Cloud Build GitHub App
```bash
gcloud beta builds connections create github \
  --region=us-central1 \
  github-connection
```

2. Create trigger
```bash
gcloud builds triggers create github \
  --name=deploy-on-push \
  --repo-name=first-contact-eis \
  --repo-owner=your-org \
  --branch-pattern=^main$ \
  --build-config=cloudbuild.yaml
```

### Manual Trigger
```bash
gcloud builds submit --config=cloudbuild.yaml
```

## 🐛 Troubleshooting

### Deployment Fails
```bash
# Check APIs are enabled
gcloud services list --enabled

# Check IAM permissions
gcloud projects get-iam-policy $PROJECT_ID

# Check quotas
gcloud compute project-info describe --project=$PROJECT_ID
```

### Service Not Starting
```bash
# View service logs
gcloud run services logs read <service-name> --region=us-central1

# Describe service
gcloud run services describe <service-name> --region=us-central1

# Check revisions
gcloud run revisions list --service=<service-name> --region=us-central1
```

### Database Connection Issues
```bash
# Check Cloud SQL status
gcloud sql instances describe firstcontact-eis-db

# Test connection
gcloud sql connect firstcontact-eis-db --user=firstcontact

# View database logs
gcloud sql operations list --instance=firstcontact-eis-db
```

### Performance Issues
```bash
# Check service metrics
gcloud run services describe <service-name> --region=us-central1 --format="value(status.url)"

# Increase resources
gcloud run services update <service-name> \
  --memory=1Gi \
  --cpu=2 \
  --region=us-central1
```

## 🚨 Emergency Operations

### Rollback Deployment
```bash
# List revisions
gcloud run revisions list --service=firstcontact-eis-backend --region=us-central1

# Rollback to specific revision
gcloud run services update-traffic firstcontact-eis-backend \
  --to-revisions=<revision-name>=100 \
  --region=us-central1
```

### Database Restore
```bash
# List backups
gcloud sql backups list --instance=firstcontact-eis-db

# Restore from backup
gcloud sql backups restore <backup-id> \
  --backup-instance=firstcontact-eis-db \
  --backup-id=<backup-id>
```

### Service Emergency Stop
```bash
# Scale to zero
gcloud run services update <service-name> \
  --max-instances=0 \
  --region=us-central1
```

## 📞 Support

For issues or questions:
1. Check logs: `./gcp/scripts/logs.sh`
2. Check status: `./gcp/scripts/status.sh`
3. Review Terraform state: `cd gcp/terraform && terraform show`
4. Contact GCP Support (if critical)

## 🎓 Additional Resources

- [GCP Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud SQL Best Practices](https://cloud.google.com/sql/docs/postgres/best-practices)

---

**Built with ❤️ for Long Beach's vulnerable populations**
