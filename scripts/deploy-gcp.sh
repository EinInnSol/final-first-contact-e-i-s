#!/bin/bash

# 🚀 First Contact EIS - GCP Deployment Script
# Automated deployment to Google Cloud Platform

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="einharjer-valhalla"
REGION="us-east5"  # Claude 4.5 Sonnet on Vertex AI is only available in us-east5 or europe-west4
REGISTRY="first-contact-eis"
REGISTRY_URL="us-east5-docker.pkg.dev/${PROJECT_ID}/${REGISTRY}"

echo -e "${BLUE}🚀 First Contact EIS - GCP Deployment${NC}"
echo -e "${BLUE}==========================================${NC}\n"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI not found. Please install Google Cloud SDK.${NC}"
    exit 1
fi

# Verify project
echo -e "${YELLOW}📋 Verifying GCP project...${NC}"
CURRENT_PROJECT=$(gcloud config get-value project)
if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo -e "${YELLOW}Switching to project: $PROJECT_ID${NC}"
    gcloud config set project $PROJECT_ID
fi
echo -e "${GREEN}✅ Project verified: $PROJECT_ID${NC}\n"

# Authenticate Docker
echo -e "${YELLOW}🔐 Authenticating Docker with Artifact Registry...${NC}"
gcloud auth configure-docker us-east5-docker.pkg.dev --quiet
echo -e "${GREEN}✅ Docker authenticated${NC}\n"

# Function to build and push image
build_and_push() {
    local SERVICE_NAME=$1
    local DOCKERFILE_PATH=$2
    local IMAGE_TAG="${REGISTRY_URL}/${SERVICE_NAME}:latest"
    
    echo -e "${YELLOW}🔨 Building $SERVICE_NAME...${NC}"
    docker build -t $IMAGE_TAG -f $DOCKERFILE_PATH $(dirname $DOCKERFILE_PATH)
    
    echo -e "${YELLOW}📤 Pushing $SERVICE_NAME to Artifact Registry...${NC}"
    docker push $IMAGE_TAG
    
    echo -e "${GREEN}✅ $SERVICE_NAME built and pushed${NC}\n"
}

# Build backend
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Backend API${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
build_and_push "backend" "./backend/Dockerfile"

# Deploy backend
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Deploying to Cloud Run${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "${YELLOW}🚀 Deploying backend API...${NC}"
gcloud run deploy backend-api \
    --image=${REGISTRY_URL}/backend:latest \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --port=8000 \
    --min-instances=1 \
    --max-instances=10 \
    --memory=2Gi \
    --cpu=2 \
    --set-env-vars="GCP_PROJECT_ID=${PROJECT_ID},GCP_REGION=${REGION},DEMO_MODE=false" \
    --quiet

BACKEND_URL=$(gcloud run services describe backend-api --region=$REGION --format="value(status.url)")
echo -e "${GREEN}✅ Backend deployed: $BACKEND_URL${NC}\n"

echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo -e "${YELLOW}Backend URL: $BACKEND_URL${NC}\n"
