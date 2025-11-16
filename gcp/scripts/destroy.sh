#!/bin/bash
# Destroy all First Contact EIS infrastructure

set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
REGION="${GCP_REGION:-us-central1}"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}⚠️  WARNING: This will destroy ALL infrastructure!${NC}"
echo ""
echo "This will delete:"
echo "  • All Cloud Run services"
echo "  • Cloud SQL database (with all data)"
echo "  • Redis instance"
echo "  • All container images"
echo "  • All secrets"
echo "  • VPC and networking"
echo ""
read -p "Type 'DESTROY' to confirm: " confirm

if [ "$confirm" != "DESTROY" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo -e "${YELLOW}Destroying infrastructure with Terraform...${NC}"

cd "$(dirname "$0")/../../gcp/terraform"

terraform destroy -auto-approve

echo ""
echo -e "${RED}All infrastructure destroyed!${NC}"
echo ""
echo "To delete the entire project, run:"
echo "  gcloud projects delete $PROJECT_ID"
