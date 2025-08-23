#!/bin/bash
"""
Start Backend and Run Prior Art Tests
This script starts the backend server and runs both test suites.
"""

set -e  # Exit on any error

echo "🚀 Starting Prior Art Search Test Suite"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "src/main.py" ]; then
    echo "❌ Error: Must be run from the agentic_native_drafting directory"
    echo "💡 Please cd to: /Users/Mariam/agentic-native-drafting/agentic_native_drafting"
    exit 1
fi

# Check if environment file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "💡 Please ensure .env file exists with required API keys"
    exit 1
fi

echo "✅ Environment check passed"

# Function to check if backend is running
check_backend() {
    curl -s http://localhost:8000/ > /dev/null 2>&1
    return $?
}

# Start backend if not running
if check_backend; then
    echo "✅ Backend already running"
else
    echo "🔄 Starting backend server..."
    python -m uvicorn src.main:app --reload --port 8000 &
    BACKEND_PID=$!
    echo "📝 Backend PID: $BACKEND_PID"
    
    # Wait for backend to start
    echo "⏳ Waiting for backend to start..."
    for i in {1..30}; do
        if check_backend; then
            echo "✅ Backend is ready!"
            break
        fi
        echo "   Attempt $i/30..."
        sleep 2
    done
    
    if ! check_backend; then
        echo "❌ Backend failed to start after 60 seconds"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
fi

# Function to cleanup
cleanup() {
    echo ""
    echo "🧹 Cleaning up..."
    if [ ! -z "$BACKEND_PID" ]; then
        echo "🛑 Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
    fi
}

# Set trap for cleanup
trap cleanup EXIT INT TERM

echo ""
echo "🧪 Running Direct API Tests..."
echo "=============================="
python3 test_direct_prior_art_api.py

echo ""
echo "🤖 Running Agent Integration Tests..."
echo "===================================="
python3 test_agent_prior_art.py

echo ""
echo "🎉 All tests completed!"
echo "📁 Check the test_reports/ directory for detailed results"
