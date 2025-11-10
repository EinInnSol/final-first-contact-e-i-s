# Domain Transfer & DNS Setup for einharjer.com
## Wix → Google Cloud Platform

**Date:** November 9, 2025  
**Domain:** einharjer.com  
**Transfer Code:** nEpx&;SJh|4L
**Target:** Google Cloud Platform

---

## IMMEDIATE ACTION: Transfer Domain to Google Cloud

### Step 1: Enable Cloud Domains API

```bash
gcloud config set project einharjer-valhalla

gcloud services enable domains.googleapis.com
```

### Step 2: Initiate Domain Transfer

```bash
# Transfer domain to Google Cloud
gcloud domains registrations transfer einharjer.com \
  --authorization-code="nEpx&;SJh|4L" \
  --contact-data-from-file=domain-contact.yaml \
  --contact-privacy=private-contact-data \
  --yearly-price=12.00USD \
  --quiet

# This will:
# - Start transfer process with Wix
# - Cost: $12/year (includes renewal)
# - Transfer typically takes 5-7 days
# - Domain remains functional during transfer
```

### Step 3: Create Contact Data File

Create `domain-contact.yaml`:

```yaml
# domain-contact.yaml
allContacts:
  email: james@einharjer.com
  phoneNumber: "+1.YOUR_PHONE_NUMBER"
  postalAddress:
    recipients:
    - "James Faernstrom"
    organization: "EINHARJER INNOVATIVE SOLUTIONS LLC"
    addressLines:
    - "YOUR_ADDRESS_LINE_1"
    locality: "YOUR_CITY"
    regionCode: "US"
    postalCode: "YOUR_ZIP"
```

---

## STEP 4: Configure DNS for Cloud Run (DO THIS NOW)

While transfer is processing, set up DNS to point to GCP:

### A) Get Cloud Run Service URLs

```bash
# List your Cloud Run services
gcloud run services list --region=us-east5

# Get URLs for:
# - Backend API
# - Caseworker frontend  
# - City dashboard
# - Client portal
```

### B) Create Cloud Load Balancer (for custom domain)

```bash
# Reserve static IP
gcloud compute addresses create first-contact-ip \
  --global \
  --ip-version IPV4

# Get the IP address
gcloud compute addresses describe first-contact-ip \
  --global \
  --format="value(address)"
```

### C) Set up DNS Records in Wix (IMMEDIATE - Before Transfer)

Go to Wix DNS settings and add these records:

```
Type: A
Host: @
Points to: [YOUR_STATIC_IP_FROM_ABOVE]
TTL: 3600

Type: A  
Host: www
Points to: [YOUR_STATIC_IP_FROM_ABOVE]
TTL: 3600

Type: CNAME
Host: api
Points to: ghs.googlehosted.com
TTL: 3600

Type: CNAME
Host: app
Points to: ghs.googlehosted.com
TTL: 3600

Type: CNAME
Host: city
Points to: ghs.googlehosted.com  
TTL: 3600
```

This gives you:
- https://einharjer.com → Main landing page
- https://api.einharjer.com → Backend API
- https://app.einharjer.com → Caseworker portal
- https://city.einharjer.com → City dashboard

---

## STEP 5: Map Custom Domains to Cloud Run Services

```bash
# Map api.einharjer.com to backend
gcloud run services update first-contact-backend \
  --region=us-east5 \
  --add-cloudsql-instances=einharjer-valhalla:us-east5:first-contact-db

gcloud beta run domain-mappings create \
  --service=first-contact-backend \
  --domain=api.einharjer.com \
  --region=us-east5

# Map app.einharjer.com to caseworker frontend
gcloud beta run domain-mappings create \
  --service=caseworker-frontend \
  --domain=app.einharjer.com \
  --region=us-east5

# Map city.einharjer.com to city dashboard
gcloud beta run domain-mappings create \
  --service=city-dashboard \
  --domain=city.einharjer.com \
  --region=us-east5
```

---

## STEP 6: Enable SSL Certificates (Automatic)

Google Cloud automatically provisions SSL certificates for mapped domains.

Verify:
```bash
gcloud beta run domain-mappings describe \
  --domain=api.einharjer.com \
  --region=us-east5
```

Status should show "ACTIVE" with SSL certificate provisioned.

---

## VERIFICATION CHECKLIST

After DNS propagates (15-30 minutes):

- [ ] https://einharjer.com - loads
- [ ] https://api.einharjer.com/health - returns 200 OK
- [ ] https://app.einharjer.com - caseworker dashboard loads
- [ ] https://city.einharjer.com - city dashboard loads
- [ ] SSL certificates valid (green lock in browser)

---

## TIMELINE

- **Now:** Update DNS in Wix (takes effect in 15-30 min)
- **Day 1:** Initiate domain transfer with gcloud command
- **Days 2-7:** Transfer processes (domain stays functional)
- **Day 7:** Transfer complete, domain fully on GCP
- **Nov 15:** Demo uses api.einharjer.com URLs

---

## COMMANDS TO RUN RIGHT NOW

```bash
# 1. Set project
gcloud config set project einharjer-valhalla

# 2. Enable APIs
gcloud services enable domains.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable compute.googleapis.com

# 3. Reserve IP
gcloud compute addresses create first-contact-ip --global

# 4. Get the IP (copy this for Wix DNS)
gcloud compute addresses describe first-contact-ip --global --format="value(address)"

# 5. Start transfer (create domain-contact.yaml first)
gcloud domains registrations transfer einharjer.com \
  --authorization-code="nEpx&;SJh|4L" \
  --contact-data-from-file=domain-contact.yaml \
  --yearly-price=12.00USD
```

---

## NOTES

- Transfer fee: $12 (includes 1 year renewal)
- No downtime during transfer
- DNS changes take 15-30 minutes to propagate
- SSL certificates auto-provision in 15 minutes
- Domain privacy included free

**Transfer code:** nEpx&;SJh|4L (valid for 30 days from Wix)
