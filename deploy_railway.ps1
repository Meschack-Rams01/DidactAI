# DidactAI Quick Deployment to Railway
# Run this script in PowerShell to deploy to Railway

Write-Host "ðŸš€ DidactAI Railway Deployment Script" -ForegroundColor Green
Write-Host "=" * 50

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✓œ… Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✓Œ Node.js not found. Please install Node.js first." -ForegroundColor Red
    Write-Host "   Download from: https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

# Install Railway CLI
Write-Host "ðŸ“¦ Installing Railway CLI..." -ForegroundColor Yellow
try {
    npm install -g @railway/cli
    Write-Host "✓œ… Railway CLI installed" -ForegroundColor Green
} catch {
    Write-Host "✓Œ Failed to install Railway CLI" -ForegroundColor Red
    exit 1
}

# Check if user is logged in to Railway
Write-Host "ðŸ” Checking Railway authentication..." -ForegroundColor Yellow
$loginCheck = railway whoami 2>&1
if ($loginCheck -like "*not logged in*" -or $LASTEXITCODE -ne 0) {
    Write-Host "ðŸ”‘ Please login to Railway..." -ForegroundColor Yellow
    railway login
    
    # Wait for login completion
    Write-Host "✓³ Waiting for login completion..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}

# Get current directory name for project naming
$projectName = Split-Path -Leaf $PWD
$projectName = $projectName.ToLower() -replace '[^a-z0-9-]', '-'

Write-Host "ðŸ“‹ Project Details:" -ForegroundColor Cyan
Write-Host "   Name: $projectName"
Write-Host "   Directory: $PWD"
Write-Host ""

# Confirm deployment
$confirmation = Read-Host "ðŸ¤” Do you want to deploy '$projectName' to Railway? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "✓Œ Deployment cancelled" -ForegroundColor Red
    exit 0
}

# Create new Railway project
Write-Host "ðŸ—ï¸ Creating Railway project..." -ForegroundColor Yellow
try {
    railway new $projectName
    Write-Host "✓œ… Railway project created" -ForegroundColor Green
} catch {
    Write-Host "✓š ï¸ Project might already exist, continuing..." -ForegroundColor Yellow
}

# Add PostgreSQL database
Write-Host "ðŸ—„ï¸ Adding PostgreSQL database..." -ForegroundColor Yellow
try {
    railway add postgresql
    Write-Host "✓œ… PostgreSQL database added" -ForegroundColor Green
} catch {
    Write-Host "✓š ï¸ Database might already exist, continuing..." -ForegroundColor Yellow
}

# Set essential environment variables
Write-Host "✓š™ï¸ Setting environment variables..." -ForegroundColor Yellow

# Generate a secure SECRET_KEY
$secretKey = [System.Web.Security.Membership]::GeneratePassword(50, 10)

railway variables set SECRET_KEY="$secretKey"
railway variables set DEBUG="False"
railway variables set DJANGO_SETTINGS_MODULE="DidactAI_project.production_settings"

# Prompt for Gemini API Key
Write-Host ""
Write-Host "ðŸ¤– Gemini API Configuration" -ForegroundColor Cyan
Write-Host "   Your current Gemini API key from .env will be used."
$geminiKey = (Get-Content .env | Select-String "GEMINI_API_KEY=(.+)" | ForEach-Object { $_.Matches.Groups[1].Value })
if ($geminiKey) {
    railway variables set GEMINI_API_KEY="$geminiKey"
    Write-Host "✓œ… Gemini API key configured" -ForegroundColor Green
} else {
    Write-Host "✓š ï¸ No Gemini API key found in .env file" -ForegroundColor Yellow
    $manualGeminiKey = Read-Host "Enter your Gemini API key (or press Enter to skip)"
    if ($manualGeminiKey) {
        railway variables set GEMINI_API_KEY="$manualGeminiKey"
        Write-Host "✓œ… Gemini API key configured" -ForegroundColor Green
    }
}

# Prompt for domain
Write-Host ""
Write-Host "ðŸŒ Domain Configuration" -ForegroundColor Cyan
$domain = Read-Host "Enter your domain (e.g., myschool-DidactAI.com) or press Enter for Railway domain"
if ($domain) {
    railway variables set ALLOWED_HOSTS="$domain,www.$domain"
    Write-Host "✓œ… Domain configured: $domain" -ForegroundColor Green
} else {
    Write-Host "✓œ… Using Railway's provided domain" -ForegroundColor Green
}

# Deploy the application
Write-Host ""
Write-Host "ðŸš€ Deploying to Railway..." -ForegroundColor Yellow
Write-Host "   This may take a few minutes..." -ForegroundColor Gray

try {
    railway up --detach
    Write-Host "✓œ… Deployment initiated successfully!" -ForegroundColor Green
} catch {
    Write-Host "✓Œ Deployment failed" -ForegroundColor Red
    Write-Host "   Check the Railway dashboard for details" -ForegroundColor Yellow
    exit 1
}

# Get project URL
Write-Host ""
Write-Host "ðŸŽ‰ Deployment Summary" -ForegroundColor Green
Write-Host "=" * 30

$projectUrl = railway status --json | ConvertFrom-Json | Select-Object -ExpandProperty url
if ($projectUrl) {
    Write-Host "ðŸŒ Your DidactAI platform: $projectUrl" -ForegroundColor Cyan
} else {
    Write-Host "ðŸŒ Check Railway dashboard for your app URL" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "ðŸ“‹ Next Steps:" -ForegroundColor Yellow
Write-Host "1. Visit your Railway dashboard to monitor deployment"
Write-Host "2. Once deployed, visit your app URL"
Write-Host "3. Create your admin account"
Write-Host "4. Test AI quiz generation"
Write-Host "5. Configure email settings if needed"
Write-Host ""
Write-Host "ðŸŽŠ Congratulations! Your AI-powered educational platform is deploying!" -ForegroundColor Green
Write-Host "   Visit https://railway.app/dashboard to monitor progress" -ForegroundColor Cyan

# Open Railway dashboard
$openDashboard = Read-Host "Open Railway dashboard in browser? (y/N)"
if ($openDashboard -eq 'y' -or $openDashboard -eq 'Y') {
    Start-Process "https://railway.app/dashboard"
}
