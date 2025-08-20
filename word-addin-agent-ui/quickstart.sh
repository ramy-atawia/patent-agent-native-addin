#!/bin/bash

echo "🚀 Quick Start: Patent Drafting Agent Word Add-in"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the word-addin-agent-ui directory"
    exit 1
fi

echo "📋 Prerequisites Check:"
echo "   - Node.js 16+ installed"
echo "   - Backend API running on port 8000"
echo "   - Microsoft Word available"
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+ first."
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ required. Current: $(node -v)"
    exit 1
fi

echo "✅ Node.js: $(node -v)"

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "✅ Dependencies already installed"
fi

# Check backend
echo "🔍 Checking backend connection..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "⚠️  Backend not responding on port 8000"
    echo "   Please start the backend first:"
    echo "   cd ../agentic_native_drafting && python -m uvicorn src.main:app --reload"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to stop..."
fi

# Create .env if needed
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file..."
    cp env.example .env
    echo "✅ .env file created"
fi

echo ""
echo "🎯 Starting Development Environment..."
echo ""

# Start development server
echo "🌐 Starting development server..."
echo "   URL: https://localhost:3000"
echo "   Press Ctrl+C to stop"
echo ""

# Start the dev server
npm run dev-server
