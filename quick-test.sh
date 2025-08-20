#!/bin/bash

echo "🧪 Quick Test - Patent Drafting Agent"
echo "====================================="

# Test backend
echo "Testing Backend (port 8000)..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend: RUNNING"
    curl -s http://localhost:8000/ | head -3
else
    echo "❌ Backend: NOT RUNNING"
fi

echo ""

# Test frontend
echo "Testing Frontend (port 3000)..."
if curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ Frontend: RUNNING"
    curl -s http://localhost:3000/ | head -3
else
    echo "❌ Frontend: NOT RUNNING"
fi

echo ""
echo "🎯 Quick Commands:"
echo "  Start all: ./start-all.sh"
echo "  Stop all:  ./stop-all.sh"
echo "  Status:    make status"
echo "  Logs:      make logs"
