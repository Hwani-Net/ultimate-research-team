#!/bin/bash
# ========================================
# Quick Start Script for Antigravity
# (macOS/Linux)
# ========================================

echo "🛸 Antigravity Ultimate Research Team - Quick Setup"
echo "================================================="
echo ""

# Check Python version
echo "Step 1: Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ ! $python_version =~ Python\ 3\.(1[0-9]|[0-9]) ]]; then
    echo "⚠️  Warning: Python 3.10+ required. Found: $python_version"
    echo "Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python version OK: $python_version"
echo ""

# Create virtual environment
echo "Step 2: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Step 3: Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Step 4: Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Check for .env file
echo "Step 5: Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "🔑 IMPORTANT: You must edit .env and add your API keys!"
    echo "   1. Open .env in any text editor"
    echo "   2. Get API keys from:"
    echo "      - Google Gemini: https://makersuite.google.com/app/apikey"
    echo "      - Tavily Search: https://tavily.com"
    echo "   3. Replace placeholder values in .env"
    echo ""
    echo "Press Enter after you've configured .env..."
    read
else
    echo "✅ .env file found"
fi
echo ""

# Verify setup
echo "Step 6: Verifying installation..."
python verify_v11_1.py
echo ""

# Done
echo "================================================="
echo "🚀 Setup Complete! Ready to launch."
echo ""
echo "To start the application:"
echo "  streamlit run app.py"
echo ""
echo "For CLI simulation:"
echo "  python simulate_interaction.py"
echo ""
