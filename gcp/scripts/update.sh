#!/bin/bash
# Update and redeploy First Contact EIS services

set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
REGION="${GCP_REGION:-us-central1}"
PROJECT_NAME="firstcontact-eis"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}First Contact EIS - Service Updater${NC}"
echo ""

# Get backend URL for frontend builds
BACKEND_URL=$(gcloud run services describe "${PROJECT_NAME}-backend" --region="$REGION" --format="value(status.url)" 2>/dev/null || echo "")

echo -e "${GREEN}Rebuilding and redeploying all services...${NC}"
echo ""

# Submit Cloud Build
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions="_REGION=$REGION,_PROJECT_NAME=$PROJECT_NAME,_BACKEND_URL=$BACKEND_URL" \
    --timeout=3600s \
    .

echo ""
echo -e "${GREEN}All services updated and redeployed!${NC}"
echo ""
echo "View new deployment:"
gcloud run services list --region="$REGION"
