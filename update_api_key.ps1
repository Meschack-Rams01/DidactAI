# PowerShell script to update Gemini API key in DidactIA
# Run this script after getting a new API key

param(
    [Parameter(Mandatory=$false)]
    [string]$ApiKey
)

Write-Host "🤖 DidactIA API Key Updater" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found in current directory" -ForegroundColor Red
    Write-Host "💡 Please run this script from your DidactIA project root" -ForegroundColor Yellow
    exit 1
}

# If no API key provided, prompt for it
if (-not $ApiKey) {
    Write-Host "🔑 Please enter your new Gemini API key:" -ForegroundColor Yellow
    Write-Host "   (Get one from: https://aistudio.google.com/)" -ForegroundColor Gray
    $ApiKey = Read-Host "API Key"
}

# Validate API key format
if (-not $ApiKey -or -not $ApiKey.StartsWith("AIzaSy")) {
    Write-Host "❌ Invalid API key format. Should start with 'AIzaSy'" -ForegroundColor Red
    exit 1
}

# Read current .env file
$envContent = Get-Content ".env" -Raw

# Check if GEMINI_API_KEY line exists
if ($envContent -match "GEMINI_API_KEY=.*") {
    # Replace existing key
    $newContent = $envContent -replace "GEMINI_API_KEY=.*", "GEMINI_API_KEY=$ApiKey"
    Write-Host "✅ Found existing GEMINI_API_KEY, updating..." -ForegroundColor Green
} else {
    # Add new key
    $newContent = $envContent + "`nGEMINI_API_KEY=$ApiKey"
    Write-Host "✅ Adding new GEMINI_API_KEY..." -ForegroundColor Green
}

# Write updated content back to .env
Set-Content ".env" -Value $newContent -NoNewline

Write-Host "✅ API key updated successfully!" -ForegroundColor Green
Write-Host "🔑 New key: $($ApiKey.Substring(0,20))..." -ForegroundColor Gray

# Test if Django is running and suggest restart
$djangoProcess = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*manage.py*runserver*"}
if ($djangoProcess) {
    Write-Host "⚠️  Django server is running. Please restart it:" -ForegroundColor Yellow
    Write-Host "   1. Press Ctrl+C in the server window" -ForegroundColor Gray
    Write-Host "   2. Run: python manage.py runserver" -ForegroundColor Gray
} else {
    Write-Host "💡 You can now start your Django server:" -ForegroundColor Yellow
    Write-Host "   python manage.py runserver" -ForegroundColor Gray
}

Write-Host "🧪 To test AI functionality, run:" -ForegroundColor Yellow
Write-Host "   python test_ai_refresh.py" -ForegroundColor Gray

Write-Host "`n🎉 AI refresh complete!" -ForegroundColor Green