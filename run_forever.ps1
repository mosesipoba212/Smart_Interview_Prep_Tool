# 🚀 Smart Interview Prep Tool - PowerShell Forever Runner
# This PowerShell script keeps your app running FOREVER with auto-restart

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎯 SMART INTERVIEW PREP TOOL" -ForegroundColor Yellow
Write-Host "🚀 BULLETPROOF PRODUCTION SERVER" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set window title
$Host.UI.RawUI.WindowTitle = "Smart Interview Prep Tool - PRODUCTION SERVER"

# Change to script directory
Set-Location $PSScriptRoot

# Forever loop with auto-restart
while ($true) {
    try {
        Write-Host "🌟 Starting production server..." -ForegroundColor Green
        Write-Host "📅 $(Get-Date)" -ForegroundColor Gray
        Write-Host ""
        
        # Start the production server
        & python run_production.py
        
        # If we reach here, the server stopped
        Write-Host ""
        Write-Host "⚠️  Server stopped! Auto-restarting in 5 seconds..." -ForegroundColor Yellow
        Write-Host "📅 $(Get-Date)" -ForegroundColor Gray
        
        Start-Sleep -Seconds 5
        
        Write-Host "🔄 Restarting server..." -ForegroundColor Cyan
    }
    catch {
        Write-Host ""
        Write-Host "❌ Error occurred: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "🔄 Restarting in 10 seconds..." -ForegroundColor Yellow
        
        Start-Sleep -Seconds 10
    }
}

# This should never be reached, but just in case
Write-Host ""
Write-Host "👋 Server runner stopped" -ForegroundColor Yellow
Read-Host "Press Enter to exit"