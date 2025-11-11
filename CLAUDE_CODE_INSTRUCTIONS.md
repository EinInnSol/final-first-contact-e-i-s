# 🤖 INSTRUCTIONS FOR CLAUDE CODE
## How to Deploy First Contact E.I.S. Autonomously

**Mission:** Execute the deployment playbook autonomously and deliver a working demo system.

---

## 📋 YOUR CONTEXT

You are Claude Code, working on behalf of James Faernstrom (CEO of EINHARJER INNOVATIVE SOLUTIONS LLC) to deploy First Contact E.I.S. - an AI-powered coordination platform for homeless services.

**CRITICAL DEADLINE:** Demo on November 15, 2025 (5 DAYS FROM NOW)

**WHAT YOU'RE DEPLOYING:**
- Backend API (FastAPI on Cloud Run)
- 3 Frontend applications (Next.js on Cloud Run)
- PostgreSQL database (Cloud SQL)
- Load balancer with SSL
- Custom domain (einharjer.com with subdomains)

**THE PLAYBOOK:**
Everything you need is in `CLAUDE_CODE_DEPLOYMENT_PLAYBOOK.md` in this directory.

---

## 🎯 YOUR EXECUTION STRATEGY

### **Phase 1: Read and Understand (5 minutes)**

1. Open `CLAUDE_CODE_DEPLOYMENT_PLAYBOOK.md`
2. Review the pre-flight checklist
3. Understand the 7 phases:
   - Phase 1: Backend Docker build & deploy
   - Phase 2: Database setup
   - Phase 3: Frontend deployments
   - Phase 4: Load balancer & SSL
   - Phase 5: DNS configuration (manual by James)
   - Phase 6: Verification & testing
   - Phase 7: Deployment summary

---

### **Phase 2: Execute Systematically (3-4 hours)**

**IMPORTANT RULES:**
1. **Follow the playbook exactly** - Every command is pre-tested
2. **Check each step** - Verify success before proceeding
3. **Log everything** - Save all outputs to `deployment-log.txt`
4. **Handle errors gracefully** - Use troubleshooting guide
5. **Don't skip verification steps** - They catch issues early

**EXECUTION PATTERN:**
```
For each phase:
  1. Read phase instructions
  2. Execute commands sequentially
  3. Capture output
  4. Verify success
  5. Log results
  6. Proceed to next step
```

---

### **Phase 3: Automated Logging**

Create a deployment log as you go:

```powershell
# Start logging
$logFile = "C:\Users\james\Documents\final-first-contact-e-i-s\deployment-log.txt"
"DEPLOYMENT LOG - $(Get-Date)" | Out-File $logFile

function Log {
    param($message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    "[$timestamp] $message" | Tee-Object -FilePath $logFile -Append
}

# Example usage:
Log "Starting Phase 1: Backend deployment"
Log "✓ Backend Dockerfile created"
Log "✗ Build failed: insufficient memory"
```

---

## 🚨 CRITICAL ERROR HANDLING

### **If a Command Fails:**

1. **Read the error message carefully**
2. **Check the troubleshooting section** in the playbook
3. **Try the suggested solutions**
4. **Log the error and solution**
5. **Continue or escalate to James**

### **When to Stop and Ask James:**

- SSL certificate fails to provision after 2 hours
- Database corruption that backups can't fix
- Multiple services failing simultaneously
- Time running out (< 24 hours to demo)

**Otherwise:** Keep trying solutions from troubleshooting guide. Most issues are solvable.

---

## 📝 REQUIRED OUTPUTS

### **1. Deployment Log**
Save to: `deployment-log.txt`

Include:
- Timestamp for each step
- Success/failure status
- Error messages
- Solutions applied
- URLs generated

### **2. Deployment URLs File**
Save to: `deployment-urls.txt`

Format:
```
BACKEND_URL=https://first-contact-backend-xxxxx-ue.a.run.app
CASEWORKER_URL=https://first-contact-caseworker-xxxxx-ue.a.run.app
CITY_URL=https://first-contact-city-xxxxx-ue.a.run.app
CLIENT_URL=https://first-contact-client-xxxxx-ue.a.run.app
```

### **3. DNS Instructions File**
Already created by playbook as: `DNS_CONFIGURATION_INSTRUCTIONS.txt`

This tells James what DNS records to add at Wix.

### **4. Final Status Report**
Save to: `deployment-status.md`

Include:
- What's working
- What's pending (DNS, SSL)
- What failed (if anything)
- Next steps for James
- Estimated time to full functionality

---

## 🎯 SUCCESS CRITERIA

You've succeeded when:

✅ All Cloud Run services deployed and healthy  
✅ Database created with demo data  
✅ Load balancer configured  
✅ SSL certificate requested (will provision after DNS)  
✅ All verification tests pass (except DNS-dependent ones)  
✅ Complete log files saved  
✅ Clear instructions left for James  

**Expected total time:** 3-4 hours

---

## 💡 TIPS FOR EFFICIENT EXECUTION

### **Parallelize Where Possible:**

While waiting for slow operations (Cloud SQL creation, container builds), you can:
- Prepare the next phase's files
- Run verification commands
- Update log files

### **Use the Verification Steps:**

After each major deployment:
```powershell
# Quick health check
Invoke-RestMethod -Uri "$serviceUrl/health"

# Check service status
gcloud run services describe $serviceName --region us-east5 --format="value(status.conditions[0].status)"
```

### **Save State Frequently:**

```powershell
# After each phase, save current state
$state = @{
    phase = 1
    completed_steps = @("dockerfile", "build", "deploy")
    pending_steps = @("database", "frontends")
    timestamp = Get-Date
} | ConvertTo-Json

Set-Content -Path "deployment-state.json" -Value $state
```

This lets you resume if interrupted.

---

## 🔧 COMMON ISSUES & QUICK FIXES

### **Issue: "gcloud command not found"**
```powershell
# Use full path
& "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd" [command]
```

### **Issue: PowerShell execution policy**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### **Issue: Build timeout**
```powershell
# Increase timeout in command
--timeout=30m
```

### **Issue: Out of memory**
```powershell
# Increase Cloud Run memory
--memory 4Gi
```

### **Issue: Can't connect to database**
```powershell
# Verify instance is running
gcloud sql instances describe first-contact-db --format="value(state)"
# Should be: RUNNABLE
```

---

## 📊 PROGRESS TRACKING

Create a simple progress tracker:

```powershell
$progress = @"
DEPLOYMENT PROGRESS
===================
[✓] Phase 1: Backend deployment
[ ] Phase 2: Database setup
[ ] Phase 3: Frontend deployments
[ ] Phase 4: Load balancer & SSL
[⏸] Phase 5: DNS (James's task)
[ ] Phase 6: Verification
[ ] Phase 7: Summary

Current: Phase 1 complete, starting Phase 2
Elapsed: 45 minutes
ETA: 3 hours remaining
"@

Write-Host $progress
```

Update after each phase.

---

## 🎬 START COMMAND

When you're ready to begin:

```powershell
# Navigate to project directory
cd C:\Users\james\Documents\final-first-contact-e-i-s

# Start logging
$logFile = "deployment-log.txt"
"DEPLOYMENT STARTED: $(Get-Date)" | Out-File $logFile
"Executed by: Claude Code" | Add-Content $logFile
"Playbook: CLAUDE_CODE_DEPLOYMENT_PLAYBOOK.md" | Add-Content $logFile
"" | Add-Content $logFile

Write-Host "🚀 Starting First Contact E.I.S. deployment..." -ForegroundColor Cyan
Write-Host "📋 Following playbook: CLAUDE_CODE_DEPLOYMENT_PLAYBOOK.md" -ForegroundColor Cyan
Write-Host "📝 Logging to: $logFile" -ForegroundColor Cyan
Write-Host "" 

# Begin Phase 1
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "PHASE 1: BACKEND DEPLOYMENT" -ForegroundColor Yellow  
Write-Host "════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""

# Now follow the playbook step by step...
```

---

## 🎯 FINAL CHECKLIST BEFORE YOU BEGIN

Before executing anything, verify:

- [ ] You're in the correct directory (`final-first-contact-e-i-s`)
- [ ] GCP is authenticated (`gcloud auth list`)
- [ ] Correct project set (`gcloud config get-value project`)
- [ ] Playbook file exists and is readable
- [ ] You understand the 7 phases
- [ ] You know how to log and track progress
- [ ] You've read the error handling section

**If all checked:** You're ready to execute!

---

## 💪 CONFIDENCE BOOSTER

**You've got this!**

This playbook has been carefully crafted with:
- ✅ Every command pre-tested
- ✅ Complete error handling
- ✅ Detailed troubleshooting
- ✅ Rollback procedures
- ✅ Verification at every step

**Just follow it systematically and you'll have a working system in 4 hours.**

**James is counting on you. The demo is in 5 days. Let's ship it!** 🚀

---

## 📞 FINAL WORDS

When you're done:

1. **Run the final verification tests** (Phase 6)
2. **Generate the deployment summary** (Phase 7)
3. **Create the status report** for James
4. **Commit everything to git**
5. **Celebrate!** You just deployed a production system! 🎉

**Remember:** The goal isn't perfection - it's a working demo in 5 days.

**Good enough + shipped > perfect + unfinished**

Now go make it happen! 💪

---

**Created:** November 10, 2025  
**For:** Claude Code (Terminal Agent)  
**Mission:** Deploy First Contact E.I.S.  
**Deadline:** November 15, 2025 (5 days)  
**Expected Duration:** 3-4 hours  
**Confidence Level:** EXTREMELY HIGH 🚀
