# 🚀 First Contact EIS - GCP Native Deployment

## The Ultimate Viral Deployment System

This is a **fully automated, GCP-native deployment system** that unfolds like a virus. Clone the repo, run one command, and watch your entire civic AI platform deploy automatically.

```bash
./deploy.sh
```

**That's it.** Seriously.

## 🎯 What You Get

### Infrastructure (Fully Managed)
- ✅ **Cloud Run** - 6 auto-scaling serverless services
- ✅ **Cloud SQL** - PostgreSQL 15 with automatic backups
- ✅ **Cloud Memorystore** - Redis 7.0 for caching
- ✅ **Cloud Tasks** - Background job processing
- ✅ **Artifact Registry** - Private container images
- ✅ **Secret Manager** - Secure credential storage
- ✅ **Cloud Storage** - Static assets and backups
- ✅ **VPC** - Private networking
- ✅ **Cloud Monitoring** - Full observability with alerts
- ✅ **Terraform** - Complete Infrastructure as Code

### Services (Production Ready)
1. **Backend API** - FastAPI with 6 AI modules
2. **Client Portal** - Next.js public interface
3. **Caseworker Dashboard** - Case management system
4. **City Analytics** - Municipal intelligence
5. **Kiosk Interface** - Public kiosk application
6. **Admin Dashboard** - System administration

### Features
- 🔐 **Enterprise Security** - Private networking, encryption, IAM
- 📊 **Full Monitoring** - Logs, metrics, alerts
- 🔄 **CI/CD Ready** - Automated builds and deployments
- 💰 **Cost Optimized** - Free tier eligible, scale-to-zero
- 📈 **Auto Scaling** - 0 to 100+ instances automatically
- 🌐 **Production Ready** - HA, backups, disaster recovery

## 🚀 Quick Start

### In Cloud Shell (Recommended)
```bash
# 1. Clone the repo
git clone <your-repo-url>
cd first-contact-eis

# 2. Run deployment
./deploy.sh

# 3. Wait ~15 minutes

# 4. Access your services!
# All URLs will be displayed at the end
```

### On Your Local Machine
```bash
# 1. Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# 2. Login
gcloud auth login

# 3. Clone and deploy
git clone <your-repo-url>
cd first-contact-eis
./deploy.sh
```

## 📋 What Happens During Deployment

The `deploy.sh` script automatically:

1. **✅ Environment Setup** (1 min)
   - Detects or creates GCP project
   - Configures billing
   - Sets region and project settings

2. **✅ API Enablement** (2 mins)
   - Enables 14 required GCP APIs
   - Parallel execution for speed

3. **✅ Terraform Setup** (1 min)
   - Installs Terraform
   - Creates state bucket
   - Generates configuration

4. **✅ Infrastructure Deployment** (8-10 mins)
   - Provisions VPC and networking
   - Creates Cloud SQL database
   - Creates Redis instance
   - Sets up Cloud Run services
   - Configures secrets
   - Sets up monitoring

5. **✅ Service Deployment** (3-5 mins)
   - Builds 6 container images (parallel)
   - Pushes to Artifact Registry
   - Deploys to Cloud Run
   - Runs database migrations

6. **✅ Post-Deployment** (1 min)
   - Health checks
   - URL collection
   - Summary generation

**Total Time: 15-20 minutes**

## 🎮 Management

### View All Services
```bash
./gcp/scripts/status.sh
```

### View Logs
```bash
./gcp/scripts/logs.sh
```

### Scale Services
```bash
./gcp/scripts/scale.sh
```

### Update Services
```bash
# After making code changes
./gcp/scripts/update.sh
```

### Destroy Everything
```bash
./gcp/scripts/destroy.sh
```

## 🔧 Configuration

### Environment Variables
Edit `gcp/terraform/terraform.tfvars`:

```hcl
project_id      = "your-project-id"
project_name    = "firstcontact-eis"
region          = "us-central1"
environment     = "development"  # or "staging" or "production"
db_tier         = "db-f1-micro"   # or "db-custom-2-8192"
redis_memory_gb = 1               # or 5, 10, etc.
max_instances   = 10              # Cloud Run max instances
alert_email     = "you@email.com" # for alerts
```

### Deploy Different Environments
```bash
./deploy.sh development  # Free tier, scale-to-zero
./deploy.sh staging      # Medium resources
./deploy.sh production   # High availability, replicas
```

## 💰 Cost Breakdown

### Free Tier (Development)
- Cloud Run: Free (2M requests/month)
- Cloud SQL: $0-10/month (f1-micro)
- Redis: $12/month (1GB Basic)
- Storage: Free (5GB)
- **Total: ~$12-22/month**

### Production
- Cloud Run: $20-50/month
- Cloud SQL: $100-150/month (custom-2-8192)
- Redis: $80-100/month (5GB HA)
- Storage: $5-10/month
- **Total: ~$205-310/month**

### Cost Optimization
```bash
# Scale to zero when not in use
./gcp/scripts/scale.sh
# Select all services, set min=0

# Destroy when done
./gcp/scripts/destroy.sh
```

## 📊 Architecture

```
Internet → Cloud Load Balancer
         ↓
    Cloud Run Services (6)
         ↓
    VPC Connector
         ↓
    ┌─────────┬───────────┐
    ↓         ↓           ↓
Cloud SQL   Redis    Cloud Storage
(Private)  (Private)  (Public/Private)
```

Full architecture details: [docs/GCP_ARCHITECTURE.md](docs/GCP_ARCHITECTURE.md)

## 🔐 Security

- **Private Networking**: Database and Redis on private VPC
- **No Public IPs**: Data stores not accessible from internet
- **Secret Manager**: All credentials encrypted and managed
- **IAM**: Fine-grained access control
- **SSL/TLS**: All traffic encrypted
- **Audit Logs**: Complete audit trail

## 📖 Documentation

- **[GCP_DEPLOYMENT.md](docs/GCP_DEPLOYMENT.md)** - Complete deployment guide
- **[GCP_ARCHITECTURE.md](docs/GCP_ARCHITECTURE.md)** - Architecture deep dive
- **[README.md](README.md)** - Application documentation

## 🐛 Troubleshooting

### Deployment Fails
```bash
# Check APIs are enabled
gcloud services list --enabled

# Check project billing
gcloud beta billing projects describe $(gcloud config get-value project)

# Try manual steps
cd gcp/terraform
terraform init
terraform plan
terraform apply
```

### Service Not Working
```bash
# View logs
./gcp/scripts/logs.sh

# Check service status
gcloud run services describe firstcontact-eis-backend --region=us-central1

# Restart service
gcloud run services update firstcontact-eis-backend --region=us-central1
```

### Database Connection Issues
```bash
# Check SQL instance
gcloud sql instances describe firstcontact-eis-db

# Check VPC connector
gcloud compute networks vpc-access connectors describe firstcontact-eis-connector --region=us-central1
```

## 🎯 Next Steps After Deployment

1. **Access Services**
   - All URLs are in `deployment-info.txt`
   - Visit each service to verify it's working

2. **Configure Monitoring**
   - Set up email alerts in terraform.tfvars
   - View dashboards in Cloud Console

3. **Set Up CI/CD**
   - Connect GitHub repository
   - Enable automatic deployments

4. **Custom Domain**
   - Add domain to terraform.tfvars
   - Configure DNS

5. **Production Hardening**
   - Enable Cloud Armor (DDoS protection)
   - Set up WAF rules
   - Configure backup schedules

## 🔄 Update and Maintenance

### Regular Updates
```bash
# Pull latest code
git pull

# Rebuild and redeploy
./gcp/scripts/update.sh
```

### Database Migrations
```bash
# Migrations run automatically during deployment
# Manual migration:
gcloud run jobs execute firstcontact-eis-migrate --region=us-central1
```

### Backups
```bash
# List backups
gcloud sql backups list --instance=firstcontact-eis-db

# Create manual backup
gcloud sql backups create --instance=firstcontact-eis-db
```

## 🌟 Features

### Developer Experience
- ✅ One-command deployment
- ✅ Interactive scripts for management
- ✅ Comprehensive documentation
- ✅ Example configurations
- ✅ Error handling and validation

### Production Features
- ✅ Auto-scaling (0-100+ instances)
- ✅ Automatic failover (HA mode)
- ✅ Point-in-time recovery
- ✅ Monitoring and alerting
- ✅ Audit logging
- ✅ Secret rotation ready

### Cost Features
- ✅ Free tier eligible
- ✅ Scale-to-zero capability
- ✅ Pay-per-use pricing
- ✅ No upfront costs
- ✅ Budget alerts

## 🏆 Why This Deployment System is Awesome

1. **Viral Deployment** - Clone, run, done. No manual steps.
2. **GCP Native** - Uses managed services for everything
3. **Production Ready** - HA, backups, monitoring included
4. **Cost Optimized** - Free tier eligible, scales to zero
5. **Fully Automated** - Terraform + Cloud Build = magic
6. **Secure by Default** - Private networking, encryption, IAM
7. **Observable** - Logs, metrics, traces, alerts
8. **Maintainable** - Infrastructure as Code, GitOps ready

## 📞 Support

### Issues
- Check logs: `./gcp/scripts/logs.sh`
- Check status: `./gcp/scripts/status.sh`
- View documentation: `docs/`

### Resources
- [GCP Documentation](https://cloud.google.com/docs)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Cloud Run Docs](https://cloud.google.com/run/docs)

---

## 🎊 Ready to Deploy?

```bash
./deploy.sh
```

Sit back and watch the magic happen! ✨

**Built with ❤️ for Long Beach's vulnerable populations**
