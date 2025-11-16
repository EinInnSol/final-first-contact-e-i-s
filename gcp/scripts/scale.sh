#!/bin/bash
# Scale Cloud Run services

set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
REGION="${GCP_REGION:-us-central1}"
PROJECT_NAME="firstcontact-eis"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}First Contact EIS - Service Scaler${NC}"
echo ""

# Get current service stats
echo "Current service configuration:"
echo ""
gcloud run services list --region="$REGION" --format="table(SERVICE,REGION,URL,LAST_DEPLOYED)"
echo ""

# Select service
echo "Select service to scale:"
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
    1) SERVICES=("${PROJECT_NAME}-backend") ;;
    2) SERVICES=("${PROJECT_NAME}-client") ;;
    3) SERVICES=("${PROJECT_NAME}-caseworker") ;;
    4) SERVICES=("${PROJECT_NAME}-city") ;;
    5) SERVICES=("${PROJECT_NAME}-kiosk") ;;
    6) SERVICES=("${PROJECT_NAME}-admin") ;;
    7) SERVICES=(
        "${PROJECT_NAME}-backend"
        "${PROJECT_NAME}-client"
        "${PROJECT_NAME}-caseworker"
        "${PROJECT_NAME}-city"
        "${PROJECT_NAME}-kiosk"
        "${PROJECT_NAME}-admin"
    ) ;;
    *) echo "Invalid choice"; exit 1 ;;
esac

echo ""
read -p "Minimum instances (0 for scale to zero): " MIN_INSTANCES
read -p "Maximum instances: " MAX_INSTANCES

for service in "${SERVICES[@]}"; do
    echo -e "${GREEN}Scaling $service...${NC}"
    gcloud run services update "$service" \
        --region="$REGION" \
        --min-instances="$MIN_INSTANCES" \
        --max-instances="$MAX_INSTANCES" \
        --project="$PROJECT_ID"
done

echo ""
echo -e "${GREEN}Scaling complete!${NC}"
