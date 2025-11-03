# 🚀 First Contact EIS - GCP Deployment Script (PowerShell)
# Automated deployment to Google Cloud Platform

$ErrorActionPreference = "Stop"

# Configuration
$PROJECT_ID = "einharjer-valhalla"
$REGION = "us-west1"
$REGISTRY = "first-contact-eis"
$REGISTRY_URL = "us-west1-docker.pkg.dev/$PROJECT_ID/$REGISTRY"

Write-Host "🚀 First Contact EIS - GCP Deployment" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Blue
Write-Host ""

# Check if gcloud is installed
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "❌ gcloud CLI not found. Please install Google Cloud SDK." -ForegroundColor Red
    exit 1
}

# Verify project
Write-Host "📋 Verifying GCP project..." -ForegroundColor Yellow
$CURRENT_PROJECT = gcloud config get-value project 2>$null
if ($CURRENT_PROJECT -ne $PROJECT_ID) {
    Write-Host "Switching to project: $PROJECT_ID" -ForegroundColor Yellow
    gcloud config set project $PROJECT_ID
}
Write-Host "✅ Project verified: $PROJECT_ID" -ForegroundColor Green
Write-Host ""

# Authenticate Docker
Write-Host "🔐 Authenticating Docker with Artifact Registry..." -ForegroundColor Yellow
gcloud auth configure-docker us-west1-docker.pkg.dev --quiet
Write-Host "✅ Docker authenticated" -ForegroundColor Green
Write-Host ""

# Build backend
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "Backend API" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue

$BACKEND_IMAGE = "$REGISTRY_URL/backend:latest"

Write-Host "🔨 Building backend..." -ForegroundColor Yellow
docker build -t $BACKEND_IMAGE -f .\backend\Dockerfile .\backend

Write-Host "📤 Pushing backend to Artifact Registry..." -ForegroundColor Yellow
docker push $BACKEND_IMAGE

Write-Host "✅ Backend built and pushed" -ForegroundColor Green
Write-Host ""

# Deploy to Cloud Run
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "Deploying to Cloud Run" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue

Write-Host "🚀 Deploying backend API..." -ForegroundColor Yellow
gcloud run deploy backend-api `
    --image=$BACKEND_IMAGE `
    --region=$REGION `
    --platform=managed `
    --allow-unauthenticated `
    --port=8000 `
    --min-instances=1 `
    --max-instances=10 `
    --memory=2Gi `
    --cpu=2 `
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID,GCP_REGION=$REGION,DEMO_MODE=false" `
    --quiet

$BACKEND_URL = gcloud run services describe backend-api --region=$REGION --format="value(status.url)"
Write-Host "✅ Backend deployed: $BACKEND_URL" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 Deployment complete!" -ForegroundColor Green
Write-Host "Backend URL: $BACKEND_URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Test the backend: $BACKEND_URL/health" -ForegroundColor White
Write-Host "   2. Test Vertex AI: $BACKEND_URL/api/ai/health" -ForegroundColor White
Write-Host "   3. Build and deploy frontends (optional)" -ForegroundColor White
Write-Host "   4. Configure domain (einharjer.com)" -ForegroundColor White
Write-Host ""
