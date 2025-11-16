# ⚡ First Contact EIS - Quick Start Guide

## 🚀 Fastest Way to Deploy

### For Cloud Shell Users (RECOMMENDED)

1. **Open Cloud Shell**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Click the Cloud Shell icon (top right)

2. **Clone and Deploy**
   ```bash
   git clone <your-repo-url>
   cd first-contact-eis
   ./deploy.sh
   ```

3. **Wait 15-20 minutes** ☕

4. **Access your system!**
   - All URLs will be displayed
   - Services are live and ready to use

That's it! You're done! 🎉

---

## 📱 What You'll See

During deployment, you'll see:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║    ███████╗██╗██████╗ ███████╗████████╗     ██████╗ ██████╗ ███╗   ██║
║    ██╔════╝██║██╔══██╗██╔════╝╚══██╔══╝    ██╔════╝██╔═══██╗████╗  ██║
║    █████╗  ██║██████╔╝███████╗   ██║       ██║     ██║   ██║██╔██╗ ██║
║    ██╔══╝  ██║██╔══██╗╚════██║   ██║       ██║     ██║   ██║██║╚██╗██║
║    ██║     ██║██║  ██║███████║   ██║       ╚██████╗╚██████╔╝██║ ╚████║
║    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
║                                                                       ║
║              🚀 GCP Native Viral Deployment System 🚀                ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

[INFO] Environment: development
[SUCCESS] Using GCP project: your-project-id
[INFO] Enabling required APIs...
[SUCCESS] All APIs enabled!
[INFO] Setting up Terraform...
[SUCCESS] Terraform configured!
[INFO] Deploying infrastructure...
[SUCCESS] Infrastructure deployed!
[INFO] Building services...
[SUCCESS] All services deployed!
```

At the end, you'll get:

```
╔═══════════════════════════════════════════════════════════════════════╗
║             FIRST CONTACT EIS - DEPLOYMENT SUCCESSFUL! 🎉            ║
╚═══════════════════════════════════════════════════════════════════════╝

🌐 SERVICE URLS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Client Portal:          https://firstcontact-eis-client-xxx.run.app
👥 Caseworker Dashboard:   https://firstcontact-eis-caseworker-xxx.run.app
🏛️  City Analytics:         https://firstcontact-eis-city-xxx.run.app
🖥️  Kiosk Interface:        https://firstcontact-eis-kiosk-xxx.run.app
⚙️  Admin Dashboard:        https://firstcontact-eis-admin-xxx.run.app
🔧 Backend API:            https://firstcontact-eis-backend-xxx.run.app
📖 API Documentation:      https://firstcontact-eis-backend-xxx.run.app/docs
```

---

## 🎮 What to Do Next

### 1. Test Your Services

Visit each URL to verify everything works:

- **Backend API Docs**: `/docs` endpoint shows all API routes
- **Client Portal**: Public-facing interface
- **Caseworker Dashboard**: Login and case management
- **City Analytics**: Municipal intelligence dashboard
- **Kiosk Interface**: Public kiosk simulation
- **Admin Dashboard**: System administration

### 2. View Infrastructure

```bash
./gcp/scripts/status.sh
```

This shows:
- All Cloud Run services
- Database status
- Redis status
- Container images
- Recent builds

### 3. Monitor Logs

```bash
./gcp/scripts/logs.sh
```

Interactive menu to view logs from any service.

### 4. Scale Services (Optional)

```bash
./gcp/scripts/scale.sh
```

Adjust min/max instances for each service.

---

## 💰 Cost Estimate

### Development (What you just deployed)
- **Cloud Run**: FREE (under 2M requests/month)
- **Cloud SQL**: $0-10/month (f1-micro)
- **Redis**: $12/month (1GB)
- **Storage**: FREE (under 5GB)
- **Networking**: FREE (under limits)

**Total: ~$12-22/month**

### How to Keep Costs Low

1. **Use scale-to-zero** (already configured)
   - Services shut down when not in use
   - No charges for idle time

2. **Delete when done testing**
   ```bash
   ./gcp/scripts/destroy.sh
   ```

3. **Monitor budget**
   - Set up budget alerts in GCP Console
   - Get notified before spending too much

---

## 🔧 Common Tasks

### Update Code and Redeploy
```bash
# Make code changes
git pull  # or edit files

# Redeploy everything
./gcp/scripts/update.sh
```

### View Specific Service Logs
```bash
gcloud run services logs read firstcontact-eis-backend \
  --region=us-central1 \
  --limit=100
```

### Connect to Database
```bash
gcloud sql connect firstcontact-eis-db --user=firstcontact
```

### Destroy Everything
```bash
./gcp/scripts/destroy.sh
```

---

## 🐛 Troubleshooting

### "Billing not enabled"
```bash
# List billing accounts
gcloud beta billing accounts list

# Link billing
gcloud beta billing projects link YOUR-PROJECT-ID \
  --billing-account=BILLING-ACCOUNT-ID
```

### "API not enabled"
```bash
# Enable specific API
gcloud services enable run.googleapis.com

# Or let deploy.sh handle it
./deploy.sh
```

### "Permission denied"
```bash
# Make deploy script executable
chmod +x deploy.sh

# Run again
./deploy.sh
```

### Service not responding
```bash
# Check logs
./gcp/scripts/logs.sh

# Check status
gcloud run services describe firstcontact-eis-backend \
  --region=us-central1

# Redeploy if needed
./gcp/scripts/update.sh
```

---

## 📚 Full Documentation

- **[GCP_README.md](GCP_README.md)** - Complete GCP deployment overview
- **[docs/GCP_DEPLOYMENT.md](docs/GCP_DEPLOYMENT.md)** - Detailed deployment guide
- **[docs/GCP_ARCHITECTURE.md](docs/GCP_ARCHITECTURE.md)** - Architecture deep dive
- **[README.md](README.md)** - Application documentation

---

## 🎯 Advanced Options

### Deploy to Different Environment
```bash
./deploy.sh production  # High availability, replicas
./deploy.sh staging     # Medium resources
./deploy.sh development # Free tier (default)
```

### Use Different Region
```bash
export GCP_REGION=us-west1
./deploy.sh
```

### Use Existing Project
```bash
export GCP_PROJECT=my-existing-project
./deploy.sh
```

---

## 🌟 What Makes This Special?

✅ **One Command** - Entire system deploys automatically
✅ **GCP Native** - Uses all managed services
✅ **Production Ready** - HA, backups, monitoring included
✅ **Cost Optimized** - Free tier eligible
✅ **Secure** - Private networking, encryption, IAM
✅ **Observable** - Logs, metrics, alerts built-in
✅ **Scalable** - 0 to 100+ instances automatically
✅ **Maintainable** - Infrastructure as Code

---

## 💡 Pro Tips

1. **Use Cloud Shell** - Already has all tools installed
2. **Enable billing first** - Prevents deployment errors
3. **Start with development** - Test before production
4. **Monitor costs** - Set up budget alerts
5. **Use destroy script** - Clean up when testing

---

## 🚨 Need Help?

1. **Check logs**: `./gcp/scripts/logs.sh`
2. **Check status**: `./gcp/scripts/status.sh`
3. **Read docs**: See documentation links above
4. **GCP Console**: [console.cloud.google.com](https://console.cloud.google.com)

---

## 🎊 Ready?

```bash
./deploy.sh
```

**That's all you need!** The system unfolds automatically. ✨

---

**Built with ❤️ for Long Beach's vulnerable populations**
