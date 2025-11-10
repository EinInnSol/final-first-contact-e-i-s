# Domain Setup for First Contact E.I.S.
# Configures einharjer.com with Cloud DNS and maps to Cloud Run services

$PROJECT_ID = "einharjer-valhalla"
$DOMAIN = "einharjer.com"
$REGION = "us-east5"
$GCLOUD = "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"

Write-Host "🌐 Configuring Domain: $DOMAIN" -ForegroundColor Cyan

# Create Cloud DNS managed zone
Write-Host "Creating DNS zone..." -ForegroundColor Yellow
& $GCLOUD dns managed-zones create first-contact-zone `
    --description="First Contact E.I.S. DNS Zone" `
    --dns-name="$DOMAIN." `
    --project=$PROJECT_ID

# Get Cloud Run service IPs
$backend_url = & $GCLOUD run services describe first-contact-backend `
    --region=$REGION --project=$PROJECT_ID --format="value(status.url)"
$frontend_url = & $GCLOUD run services describe first-contact-frontend `
    --region=$REGION --project=$PROJECT_ID --format="value(status.url)"

Write-Host "Backend: $backend_url" -ForegroundColor Gray
Write-Host "Frontend: $frontend_url" -ForegroundColor Gray

# Create DNS records
Write-Host "Creating DNS records..." -ForegroundColor Yellow

# Root domain -> Frontend
& $GCLOUD dns record-sets create "$DOMAIN." `
    --zone=first-contact-zone `
    --type=CNAME `
    --ttl=300 `
    --rrdatas="$frontend_url" `
    --project=$PROJECT_ID

# api subdomain -> Backend
& $GCLOUD dns record-sets create "api.$DOMAIN." `
    --zone=first-contact-zone `
    --type=CNAME `
    --ttl=300 `
    --rrdatas="$backend_url" `
    --project=$PROJECT_ID

Write-Host "✓ DNS configured" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANT: Update domain registrar nameservers to:" -ForegroundColor Yellow
& $GCLOUD dns managed-zones describe first-contact-zone `
    --project=$PROJECT_ID --format="value(nameServers)"
