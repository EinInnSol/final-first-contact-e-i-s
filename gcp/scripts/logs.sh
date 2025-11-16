#!/bin/bash
# View logs for First Contact EIS services

set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
REGION="${GCP_REGION:-us-central1}"
PROJECT_NAME="firstcontact-eis"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}First Contact EIS - Log Viewer${NC}"
echo ""

# Menu
echo "Select service to view logs:"
echo "1) Backend API"
echo "2) Client Portal"
echo "3) Caseworker Dashboard"
echo "4) City Analytics"
echo "5) Kiosk Interface"
echo "6) Admin Dashboard"
echo "7) All services"
echo ""
read -p "Enter choice [1-7]: " choice

case $choice in
    1) SERVICE="${PROJECT_NAME}-backend" ;;
    2) SERVICE="${PROJECT_NAME}-client" ;;
    3) SERVICE="${PROJECT_NAME}-caseworker" ;;
    4) SERVICE="${PROJECT_NAME}-city" ;;
    5) SERVICE="${PROJECT_NAME}-kiosk" ;;
    6) SERVICE="${PROJECT_NAME}-admin" ;;
    7) SERVICE="" ;;
    *) echo "Invalid choice"; exit 1 ;;
esac

if [ -z "$SERVICE" ]; then
    echo -e "${GREEN}Streaming logs from all services...${NC}"
    gcloud logging read "resource.type=cloud_run_revision AND resource.labels.project_id=$PROJECT_ID" \
        --limit=100 \
        --format="table(timestamp,resource.labels.service_name,severity,textPayload)" \
        --project="$PROJECT_ID"
else
    echo -e "${GREEN}Streaming logs from $SERVICE...${NC}"
    gcloud run services logs read "$SERVICE" \
        --region="$REGION" \
        --project="$PROJECT_ID" \
        --limit=100
fi
