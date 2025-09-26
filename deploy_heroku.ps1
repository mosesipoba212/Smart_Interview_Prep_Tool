# Deploy to Heroku PowerShell script

Write-Host "🚀 Deploying Smart Interview Prep Tool to Heroku..." -ForegroundColor Green

# Check if Heroku CLI is installed
try {
    heroku --version | Out-Null
    Write-Host "✅ Heroku CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Heroku CLI not found. Please install from https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Red
    exit 1
}

# Login to Heroku
Write-Host "🔑 Checking Heroku authentication..." -ForegroundColor Yellow
try {
    heroku auth:whoami | Out-Null
    Write-Host "✅ Already logged in to Heroku" -ForegroundColor Green
} catch {
    Write-Host "🔑 Please login to Heroku..." -ForegroundColor Yellow
    heroku login
}

# Create Heroku app
Write-Host "📱 Creating Heroku app..." -ForegroundColor Yellow
$APP_NAME = Read-Host "Enter your app name (or press enter for auto-generated)"

if ([string]::IsNullOrWhiteSpace($APP_NAME)) {
    heroku create
} else {
    heroku create $APP_NAME
}

# Set environment variables
Write-Host "🔐 Setting environment variables..." -ForegroundColor Yellow
$SECRET_KEY = "smart-interview-prep-production-$(Get-Date -Format 'yyyyMMddHHmmss')"
heroku config:set SECRET_KEY="$SECRET_KEY"

# Optional: Set Gemini API key
$GEMINI_KEY = Read-Host "Enter GEMINI_API_KEY (optional, press enter to skip)"
if (![string]::IsNullOrWhiteSpace($GEMINI_KEY)) {
    heroku config:set GEMINI_API_KEY="$GEMINI_KEY"
}

# Deploy to Heroku
Write-Host "🚀 Deploying to Heroku..." -ForegroundColor Green
git add .
git commit -m "Deploy to Heroku - Smart Interview Prep Tool"
git push heroku main

# Open the app
Write-Host "✅ Deployment complete!" -ForegroundColor Green
heroku open

Write-Host "🎉 Your Smart Interview Prep Tool is now live!" -ForegroundColor Green
Write-Host "📊 Note: Gmail sync will need OAuth configuration for production use" -ForegroundColor Yellow