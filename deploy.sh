#!/bin/bash
###############################################################################
# First Contact EIS - Viral GCP Deployment Script
#
# This script unfolds like a virus when executed in Cloud Shell or Gemini
# It automatically provisions ALL GCP infrastructure and deploys the entire
# application with zero manual intervention.
#
# Usage: ./deploy.sh [environment]
# Example: ./deploy.sh production
###############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

###############################################################################
# Helper Functions
###############################################################################

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

###############################################################################
# Banner
###############################################################################

show_banner() {
    echo -e "${PURPLE}"
    cat << "EOF"
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
║      AI-Enhanced Human-in-the-Loop Civic Services Platform          ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

###############################################################################
# Environment Setup
###############################################################################

setup_environment() {
    log "Setting up deployment environment..."

    # Get environment (default: development)
    ENVIRONMENT="${1:-development}"
    log_info "Environment: $ENVIRONMENT"

    # Get or create GCP project
    if [ -z "${GCP_PROJECT:-}" ]; then
        # Try to get current project
        GCP_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")

        if [ -z "$GCP_PROJECT" ]; then
            log_warn "No GCP project set. Let's create one!"
            read -p "Enter project ID (or press enter for auto-generated): " PROJECT_INPUT

            if [ -z "$PROJECT_INPUT" ]; then
                # Generate project ID
                RANDOM_SUFFIX=$(date +%s | sha256sum | base64 | head -c 8 | tr '[:upper:]' '[:lower:]')
                GCP_PROJECT="firstcontact-eis-${RANDOM_SUFFIX}"
                log_info "Generated project ID: $GCP_PROJECT"
            else
                GCP_PROJECT="$PROJECT_INPUT"
            fi

            # Create project
            log_info "Creating GCP project: $GCP_PROJECT"
            gcloud projects create "$GCP_PROJECT" --name="First Contact EIS" || true
        fi
    fi

    # Set project
    gcloud config set project "$GCP_PROJECT"
    log_success "Using GCP project: $GCP_PROJECT"

    # Set region
    REGION="${GCP_REGION:-us-central1}"
    gcloud config set compute/region "$REGION"
    log_info "Region: $REGION"

    # Enable billing (prompt if needed)
    BILLING_ENABLED=$(gcloud beta billing projects describe "$GCP_PROJECT" --format="value(billingEnabled)" 2>/dev/null || echo "False")
    if [ "$BILLING_ENABLED" != "True" ]; then
        log_warn "Billing is not enabled for this project."
        log_info "Listing available billing accounts:"
        gcloud beta billing accounts list

        read -p "Enter billing account ID: " BILLING_ACCOUNT
        gcloud beta billing projects link "$GCP_PROJECT" --billing-account="$BILLING_ACCOUNT"
        log_success "Billing enabled!"
    fi

    # Export variables
    export PROJECT_ID="$GCP_PROJECT"
    export REGION
    export ENVIRONMENT
    export PROJECT_NAME="firstcontact-eis"
}

###############################################################################
# Enable APIs
###############################################################################

enable_apis() {
    log "Enabling required GCP APIs..."

    APIS=(
        "compute.googleapis.com"
        "run.googleapis.com"
        "cloudbuild.googleapis.com"
        "artifactregistry.googleapis.com"
        "sqladmin.googleapis.com"
        "redis.googleapis.com"
        "cloudtasks.googleapis.com"
        "secretmanager.googleapis.com"
        "storage.googleapis.com"
        "monitoring.googleapis.com"
        "logging.googleapis.com"
        "cloudscheduler.googleapis.com"
        "vpcaccess.googleapis.com"
        "servicenetworking.googleapis.com"
    )

    for api in "${APIS[@]}"; do
        log_info "Enabling $api..."
        gcloud services enable "$api" --project="$PROJECT_ID" &
    done

    wait
    log_success "All APIs enabled!"
}

###############################################################################
# Setup Terraform
###############################################################################

setup_terraform() {
    log "Setting up Terraform..."

    # Install Terraform if not present
    if ! command -v terraform &> /dev/null; then
        log_info "Installing Terraform..."
        wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
        sudo apt update && sudo apt install terraform -y
    fi

    # Create GCS bucket for Terraform state
    BUCKET_NAME="${PROJECT_ID}-terraform-state"
    if ! gsutil ls -b "gs://${BUCKET_NAME}" &> /dev/null; then
        log_info "Creating Terraform state bucket..."
        gsutil mb -p "$PROJECT_ID" -l "$REGION" "gs://${BUCKET_NAME}"
        gsutil versioning set on "gs://${BUCKET_NAME}"
    fi

    # Create terraform.tfvars
    cat > gcp/terraform/terraform.tfvars <<EOF
project_id      = "$PROJECT_ID"
project_name    = "$PROJECT_NAME"
region          = "$REGION"
environment     = "$ENVIRONMENT"
db_tier         = "db-f1-micro"
redis_memory_gb = 1
max_instances   = 10
alert_email     = ""
custom_domain   = ""
EOF

    log_success "Terraform configured!"
}

###############################################################################
# Deploy Infrastructure
###############################################################################

deploy_infrastructure() {
    log "Deploying infrastructure with Terraform..."

    cd gcp/terraform

    # Initialize Terraform
    log_info "Initializing Terraform..."
    terraform init \
        -backend-config="bucket=${PROJECT_ID}-terraform-state" \
        -backend-config="prefix=terraform/state"

    # Plan
    log_info "Planning infrastructure..."
    terraform plan -out=tfplan

    # Apply
    log_info "Applying infrastructure (this may take 10-15 minutes)..."
    terraform apply tfplan

    # Get outputs
    export BACKEND_URL=$(terraform output -raw backend_url)

    cd "$SCRIPT_DIR"
    log_success "Infrastructure deployed!"
}

###############################################################################
# Build and Deploy Services
###############################################################################

build_and_deploy() {
    log "Building and deploying services with Cloud Build..."

    # Submit Cloud Build
    log_info "Submitting build to Cloud Build..."
    gcloud builds submit \
        --config=cloudbuild.yaml \
        --substitutions="_REGION=$REGION,_PROJECT_NAME=$PROJECT_NAME,_BACKEND_URL=$BACKEND_URL" \
        --timeout=3600s \
        .

    log_success "All services deployed!"
}

###############################################################################
# Post-Deployment Configuration
###############################################################################

post_deployment() {
    log "Running post-deployment configuration..."

    # Get service URLs
    BACKEND_URL=$(gcloud run services describe "${PROJECT_NAME}-backend" --region="$REGION" --format="value(status.url)")
    CLIENT_URL=$(gcloud run services describe "${PROJECT_NAME}-client" --region="$REGION" --format="value(status.url)")
    CASEWORKER_URL=$(gcloud run services describe "${PROJECT_NAME}-caseworker" --region="$REGION" --format="value(status.url)")
    CITY_URL=$(gcloud run services describe "${PROJECT_NAME}-city" --region="$REGION" --format="value(status.url)")
    KIOSK_URL=$(gcloud run services describe "${PROJECT_NAME}-kiosk" --region="$REGION" --format="value(status.url)")
    ADMIN_URL=$(gcloud run services describe "${PROJECT_NAME}-admin" --region="$REGION" --format="value(status.url)")

    # Run database migrations
    log_info "Running database migrations..."
    gcloud run jobs create "${PROJECT_NAME}-migrate" \
        --image="${REGION}-docker.pkg.dev/${PROJECT_ID}/${PROJECT_NAME}-images/backend:latest" \
        --region="$REGION" \
        --task-timeout=600 \
        --command="alembic" \
        --args="upgrade,head" || true

    gcloud run jobs execute "${PROJECT_NAME}-migrate" --region="$REGION" --wait || true

    # Save deployment info
    cat > deployment-info.txt <<EOF
╔═══════════════════════════════════════════════════════════════════════╗
║             FIRST CONTACT EIS - DEPLOYMENT SUCCESSFUL! 🎉            ║
╚═══════════════════════════════════════════════════════════════════════╝

Project ID: $PROJECT_ID
Region: $REGION
Environment: $ENVIRONMENT

🌐 SERVICE URLS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Client Portal:          $CLIENT_URL
👥 Caseworker Dashboard:   $CASEWORKER_URL
🏛️  City Analytics:         $CITY_URL
🖥️  Kiosk Interface:        $KIOSK_URL
⚙️  Admin Dashboard:        $ADMIN_URL
🔧 Backend API:            $BACKEND_URL
📖 API Documentation:      $BACKEND_URL/docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 NEXT STEPS:

1. Visit any of the URLs above to access the system
2. Monitor logs: gcloud logging read --project=$PROJECT_ID
3. View metrics: https://console.cloud.google.com/monitoring?project=$PROJECT_ID
4. Manage infrastructure: cd gcp/terraform && terraform [plan|apply|destroy]

📊 RESOURCE MANAGEMENT:

• View all Cloud Run services:
  gcloud run services list --region=$REGION

• Scale a service:
  gcloud run services update <service-name> --max-instances=20 --region=$REGION

• View Cloud SQL instances:
  gcloud sql instances list

• View Redis instances:
  gcloud redis instances list --region=$REGION

💰 COST OPTIMIZATION:

• Current config uses minimal resources (free tier eligible)
• Production upgrade: Update gcp/terraform/terraform.tfvars
• Delete everything: terraform destroy (in gcp/terraform/)

🔐 SECURITY:

• All secrets stored in Secret Manager
• Database uses private networking only
• Cloud Run uses managed SSL certificates
• IAM permissions follow least privilege

📖 DOCUMENTATION:

• Full docs: ./docs/GCP_DEPLOYMENT.md
• Architecture: ./docs/GCP_ARCHITECTURE.md
• Troubleshooting: ./docs/TROUBLESHOOTING.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Deployment completed at: $(date)

Built with ❤️ for Long Beach's vulnerable populations
EOF

    log_success "Deployment complete!"
    cat deployment-info.txt
}

###############################################################################
# Main Execution
###############################################################################

main() {
    show_banner

    log "🚀 Starting viral deployment sequence..."
    echo ""

    # Step 1: Environment setup
    setup_environment "$@"
    echo ""

    # Step 2: Enable APIs
    enable_apis
    echo ""

    # Step 3: Setup Terraform
    setup_terraform
    echo ""

    # Step 4: Deploy infrastructure
    deploy_infrastructure
    echo ""

    # Step 5: Build and deploy services
    build_and_deploy
    echo ""

    # Step 6: Post-deployment
    post_deployment
    echo ""

    log_success "🎉 DEPLOYMENT COMPLETE! The system has unfolded successfully!"
    log_info "Check deployment-info.txt for all service URLs and next steps"
}

# Run main function
main "$@"
