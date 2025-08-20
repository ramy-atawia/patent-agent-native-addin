#!/bin/bash

# Patent Drafting Agent - Stop All Servers Script

echo "🛑 Stopping Patent Drafting Agent Servers"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to stop processes on a port
stop_port() {
    local port=$1
    local name=$2
    
    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "${BLUE}🛑 Stopping $name on port $port...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        echo -e "${GREEN}✅ $name stopped${NC}"
    else
        echo -e "${YELLOW}ℹ️  $name not running on port $port${NC}"
    fi
}

# Stop backend server
stop_port 8000 "Backend"

# Stop frontend server
stop_port 3000 "Frontend"

# Remove PID files if they exist
if [ -f ".backend.pid" ]; then
    rm .backend.pid
    echo -e "${GREEN}✅ Backend PID file removed${NC}"
fi

if [ -f ".frontend.pid" ]; then
    rm .frontend.pid
    echo -e "${GREEN}✅ Frontend PID file removed${NC}"
fi

echo ""
echo -e "${GREEN}🎉 All servers stopped successfully!${NC}"
echo -e "${YELLOW}🚀 To start again, run: ./start-all.sh${NC}"
