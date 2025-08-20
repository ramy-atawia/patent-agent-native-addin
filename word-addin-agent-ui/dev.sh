#!/bin/bash

echo "🚀 Starting Patent Drafting Agent Word Add-in Development Environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "✅ .env file created. Please update REACT_APP_API_URL if needed."
fi

# Check if backend is running
echo "🔍 Checking backend connection..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "⚠️  Backend not responding at http://localhost:8000"
    echo "   Please start the backend first:"
    echo "   cd ../agentic_native_drafting && python -m uvicorn src.main:app --reload"
    echo ""
fi

# Start development server
echo "🌐 Starting development server..."
echo "   The add-in will be available at: https://localhost:3000"
echo "   Press Ctrl+C to stop the server"
echo ""

npm run dev-server
