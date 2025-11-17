# First Contact E.I.S. - Cleanup Demo Files
# Removes all demo-related branches, files, and documentation

Write-Host "🧹 CLEANING UP DEMO FILES..." -ForegroundColor Cyan
Write-Host ""

# Change to repo directory
Set-Location "C:\Users\james\Documents\final-first-contact-e-i-s"

Write-Host "📋 Step 1: Identifying demo-related files..." -ForegroundColor Yellow

$demoFiles = @(
    # Demo documentation
    "docs\SESSION_NOTES_NOV3.md",
    "docs\SESSION_NOTES_NOV7.md",
    "docs\SESSION_STATUS_NOV9.md",
    "docs\NEXT_CHAT_STARTER.md",
    "HANDOFF_TO_CLAUDE_CODE.md",
    "FINAL_SESSION_HANDOFF.md",
    "MIRACLE_PLAYBOOK_SUMMARY.md",
    "INTEGRATION_INSTRUCTIONS.md",
    "CLAUDE_CODE_HANDOFF",
    "CLAUDE_CODE_INSTRUCTIONS.md",
    "CLAUDE_CODE_DEPLOYMENT_PLAYBOOK.md",
    
    # Demo frontends
    "frontend\demo-landing",
    "frontend\kiosk",
    
    # Demo backend files
    "backend\Dockerfile.simple",
    "backend\main_simple.py",
    "backend\test_first_contact.db",
    
    # Deployment logs
    "deployment-log.txt",
    "deployment-urls.txt",
    
    # Old infrastructure
    "infrastructure",
    
    # Demo scripts
    "scripts\autonomous_builder.py",
    "scripts\gcp_build.py"
)

Write-Host ""
Write-Host "🗑️  Step 2: Removing demo files..." -ForegroundColor Yellow

$removed = 0
$notFound = 0

foreach ($file in $demoFiles) {
    $fullPath = Join-Path (Get-Location) $file
    
    if (Test-Path $fullPath) {
        Write-Host "  Removing: $file" -ForegroundColor Red
        Remove-Item -Path $fullPath -Recurse -Force
        $removed++
    } else {
        Write-Host "  Not found: $file" -ForegroundColor DarkGray
        $notFound++
    }
}

Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Removed: $removed files/folders" -ForegroundColor Green
Write-Host "  ⚠️  Not found: $notFound files/folders" -ForegroundColor Yellow

Write-Host ""
Write-Host "🌿 Step 3: Checking Git branches..." -ForegroundColor Yellow

# Get current branch
$currentBranch = git rev-parse --abbrev-ref HEAD
Write-Host "  Current branch: $currentBranch" -ForegroundColor Cyan

# Check if we should delete gcp-vertex-deployment branch
Write-Host ""
Write-Host "📌 Branch Status:" -ForegroundColor Cyan
Write-Host "  • main (keep - production)" -ForegroundColor Green
Write-Host "  • gcp-vertex-deployment (demo branch)" -ForegroundColor Yellow

Write-Host ""
$deleteGcpBranch = Read-Host "Delete gcp-vertex-deployment branch? (yes/no)"

if ($deleteGcpBranch -eq "yes") {
    # Switch to main if on gcp-vertex-deployment
    if ($currentBranch -eq "gcp-vertex-deployment") {
        Write-Host "  Switching to main branch..." -ForegroundColor Yellow
        git checkout main
    }
    
    Write-Host "  Deleting local gcp-vertex-deployment..." -ForegroundColor Red
    git branch -D gcp-vertex-deployment
    
    Write-Host "  Deleting remote gcp-vertex-deployment..." -ForegroundColor Red
    git push origin --delete gcp-vertex-deployment
    
    Write-Host "  ✅ Branch deleted" -ForegroundColor Green
} else {
    Write-Host "  ⏭️  Keeping gcp-vertex-deployment branch" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📝 Step 4: Git status..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "✅ CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review changes: git status"
Write-Host "  2. Commit deletions: git add -A && git commit -m `"cleanup: Remove demo files`""
Write-Host "  3. Push to main: git push origin main"
Write-Host ""
