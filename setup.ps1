# ========================================
# Quick Start Script for Antigravity
# ========================================
# This script sets up your environment automatically

Write-Host "🛸 Antigravity Ultimate Research Team - Quick Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Step 1: Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.(1[01]|[0-9])") {
    Write-Host "⚠️  Warning: Python 3.10+ required. Found: $pythonVersion" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Python version OK: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Step 2: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Step 3: Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Step 4: Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip -q
pip install -r requirements.txt -q
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check for .env file
Write-Host "Step 5: Checking environment configuration..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "🔑 IMPORTANT: You must edit .env and add your API keys!" -ForegroundColor Red
    Write-Host "   1. Open .env in any text editor" -ForegroundColor Yellow
    Write-Host "   2. Get API keys from:" -ForegroundColor Yellow
    Write-Host "      - Google Gemini: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
    Write-Host "      - Tavily Search: https://tavily.com" -ForegroundColor Cyan
    Write-Host "   3. Replace placeholder values in .env" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press Enter after you've configured .env..." -ForegroundColor Yellow
    Read-Host
} else {
    Write-Host "✅ .env file found" -ForegroundColor Green
}
Write-Host ""

# Verify setup
Write-Host "Step 6: Verifying installation..." -ForegroundColor Yellow
python verify_v11_1.py
Write-Host ""

# Done
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "🚀 Setup Complete! Ready to launch." -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Yellow
Write-Host "  streamlit run app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "For CLI simulation:" -ForegroundColor Yellow
Write-Host "  python simulate_interaction.py" -ForegroundColor Cyan
Write-Host ""
