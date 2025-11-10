# ============================================================================
# REPOSITORY CLEANUP & FINALIZATION SCRIPT
# Prepares repo for production deployment
# ============================================================================

$ErrorActionPreference = "Stop"

Write-Host "🧹 CLEANING AND FINALIZING REPOSITORY..." -ForegroundColor Cyan
Write-Host ""

$repo_root = "C:\Users\james\Documents\final-first-contact-e-i-s"
cd $repo_root

# Files to DELETE (deprecated/unnecessary)
$files_to_delete = @(
    "backend\app\ai_case_manager.py",           # Old AI approach
    "backend\app\ai_client_concierge.py",       # Old AI approach
    "backend\app\ai_cross_system_learning.py",  # Old AI approach
    "backend\app\ai_kiosk_intelligence.py",     # Old AI approach
    "backend\app\ai_municipal_intelligence.py", # Old AI approach
    "backend\app\ai_system_management.py",      # Old AI approach
    "backend\app\agents",                       # Old multi-agent folder
    "railway.toml",                             # Not using Railway
    "docker-compose.yml",                       # Using GCP not Docker Compose
    "docker-compose.prod.yml",                  # Using GCP not Docker Compose
    "backend\test_first_contact.db",            # Test database
    "backend\logs\app.log",                     # Old logs
    "backend\logs\error.log"                    # Old logs
)

Write-Host "Removing deprecated files..." -ForegroundColor Yellow
foreach ($file in $files_to_delete) {
    $full_path = Join-Path $repo_root $file
    if (Test-Path $full_path) {
        Remove-Item -Path $full_path -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "✓ Deleted: $file" -ForegroundColor Gray
    }
}

# Create .gitignore additions
Write-Host ""
Write-Host "Updating .gitignore..." -ForegroundColor Yellow

$gitignore_additions = @"

# Deployment
deployment/*.log
*.db
*.sqlite

# Logs
logs/
*.log

# Environment
.env.local
.env.production

# GCP
gcp-key.json
service-account.json

# IDE
.vscode/
.idea/

"@

Add-Content -Path ".gitignore" -Value $gitignore_additions
Write-Host "✓ .gitignore updated" -ForegroundColor Green

# Create deployment .gitkeep files
Write-Host ""
Write-Host "Creating directory structure..." -ForegroundColor Yellow
New-Item -Path "backend\logs\.gitkeep" -ItemType File -Force | Out-Null
Write-Host "✓ Directory structure created" -ForegroundColor Green

Write-Host ""
Write-Host "✅ CLEANUP COMPLETE" -ForegroundColor Green
Write-Host ""
