#!/bin/bash
# Check status of all First Contact EIS resources

set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
REGION="${GCP_REGION:-us-central1}"
PROJECT_NAME="firstcontact-eis"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   First Contact EIS - Infrastructure Status Report${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}🚀 Cloud Run Services:${NC}"
gcloud run services list --region="$REGION" --format="table(SERVICE,REGION,URL,LAST_DEPLOYED)" || echo "No services found"
echo ""

echo -e "${YELLOW}💾 Cloud SQL Instances:${NC}"
gcloud sql instances list --format="table(name,region,tier,status,ipAddress)" || echo "No SQL instances found"
echo ""

echo -e "${YELLOW}🔴 Redis Instances:${NC}"
gcloud redis instances list --region="$REGION" --format="table(name,region,tier,memorySizeGb,status)" || echo "No Redis instances found"
echo ""

echo -e "${YELLOW}📦 Artifact Registry Repositories:${NC}"
gcloud artifacts repositories list --location="$REGION" --format="table(name,format,createTime)" || echo "No repositories found"
echo ""

echo -e "${YELLOW}🔐 Secrets:${NC}"
gcloud secrets list --format="table(name,created)" || echo "No secrets found"
echo ""

echo -e "${YELLOW}📊 Recent Cloud Build Jobs:${NC}"
gcloud builds list --limit=5 --format="table(id,createTime,duration,status)" || echo "No builds found"
echo ""

echo -e "${YELLOW}💰 Estimated Monthly Cost:${NC}"
echo "Note: Run 'gcloud billing projects describe $PROJECT_ID' for billing details"
echo ""

echo -e "${GREEN}Status check complete!${NC}"
