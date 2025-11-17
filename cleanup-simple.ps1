# Cleanup Demo Files - Simple Version
Write-Host "Cleaning up demo files..." -ForegroundColor Cyan

# Change to repo
cd C:\Users\james\Documents\final-first-contact-e-i-s

# Remove demo documentation
Remove-Item -Path "CLAUDE_CODE_HANDOFF" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "docs\SESSION_NOTES_NOV3.md" -ErrorAction SilentlyContinue
Remove-Item -Path "docs\SESSION_NOTES_NOV7.md" -ErrorAction SilentlyContinue
Remove-Item -Path "docs\SESSION_STATUS_NOV9.md" -ErrorAction SilentlyContinue
Remove-Item -Path "docs\NEXT_CHAT_STARTER.md" -ErrorAction SilentlyContinue
Remove-Item -Path "HANDOFF_TO_CLAUDE_CODE.md" -ErrorAction SilentlyContinue
Remove-Item -Path "FINAL_SESSION_HANDOFF.md" -ErrorAction SilentlyContinue
Remove-Item -Path "MIRACLE_PLAYBOOK_SUMMARY.md" -ErrorAction SilentlyContinue
Remove-Item -Path "INTEGRATION_INSTRUCTIONS.md" -ErrorAction SilentlyContinue
Remove-Item -Path "CLAUDE_CODE_INSTRUCTIONS.md" -ErrorAction SilentlyContinue
Remove-Item -Path "CLAUDE_CODE_DEPLOYMENT_PLAYBOOK.md" -ErrorAction SilentlyContinue

# Remove demo frontends
Remove-Item -Path "frontend\demo-landing" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "frontend\kiosk" -Recurse -Force -ErrorAction SilentlyContinue

# Remove demo backend files
Remove-Item -Path "backend\Dockerfile.simple" -ErrorAction SilentlyContinue
Remove-Item -Path "backend\main_simple.py" -ErrorAction SilentlyContinue
Remove-Item -Path "backend\test_first_contact.db" -ErrorAction SilentlyContinue

# Remove deployment logs
Remove-Item -Path "deployment-log.txt" -ErrorAction SilentlyContinue
Remove-Item -Path "deployment-urls.txt" -ErrorAction SilentlyContinue

# Remove old infrastructure
Remove-Item -Path "infrastructure" -Recurse -Force -ErrorAction SilentlyContinue

# Remove demo scripts
Remove-Item -Path "scripts\autonomous_builder.py" -ErrorAction SilentlyContinue
Remove-Item -Path "scripts\gcp_build.py" -ErrorAction SilentlyContinue

Write-Host "Demo files removed!" -ForegroundColor Green
Write-Host ""
Write-Host "Git status:" -ForegroundColor Yellow
git status
