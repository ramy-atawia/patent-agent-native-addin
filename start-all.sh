#!/bin/bash

# Patent Drafting Agent - Complete Startup Script
# This script starts both backend and frontend servers

set -e  # Exit on any error

echo "🚀 Starting Patent Drafting Agent - Complete Setup"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $port is already in use. Stopping existing process...${NC}"
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# Function to wait for server to be ready
wait_for_server() {
    local port=$1
    local name=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${BLUE}⏳ Waiting for $name to be ready on port $port...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$port > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $name is ready on port $port${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "\n${RED}❌ $name failed to start on port $port${NC}"
    return 1
}

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Install backend dependencies if needed
echo -e "${BLUE}📦 Checking backend dependencies...${NC}"
if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installing backend dependencies...${NC}"
    pip3 install fastapi "uvicorn[standard]" pydantic python-dotenv httpx
fi

# Check and copy .env file if needed
if [ ! -f ".env" ]; then
    if [ -f "agentic_native_drafting/.env" ]; then
        echo -e "${BLUE}📋 Copying environment variables...${NC}"
        cp agentic_native_drafting/.env .
    else
        echo -e "${RED}❌ No .env file found. Please create one with your Azure OpenAI credentials.${NC}"
        exit 1
    fi
fi

# Check frontend dependencies
echo -e "${BLUE}📦 Checking frontend dependencies...${NC}"
if [ ! -d "word-addin-agent-ui/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Installing frontend dependencies...${NC}"
    cd word-addin-agent-ui
    npm install
    cd ..
fi

# Stop any existing servers
echo -e "${BLUE}🛑 Stopping any existing servers...${NC}"
check_port 8000
check_port 3000

# Start backend server
echo -e "${BLUE}🚀 Starting backend server on port 8000...${NC}"
python3 -m uvicorn agentic_native_drafting.src.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to be ready
if wait_for_server 8000 "Backend"; then
    echo -e "${GREEN}✅ Backend server started successfully!${NC}"
else
    echo -e "${RED}❌ Backend server failed to start. Check backend.log for details.${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start frontend server
echo -e "${BLUE}🚀 Starting frontend server on port 3000...${NC}"
cd word-addin-agent-ui
npm run dev-server > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to be ready
if wait_for_server 3000 "Frontend"; then
    echo -e "${GREEN}✅ Frontend server started successfully!${NC}"
else
    echo -e "${RED}❌ Frontend server failed to start. Check frontend.log for details.${NC}"
    kill $FRONTEND_PID 2>/dev/null || true
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Save PIDs for later cleanup
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo ""
echo -e "${GREEN}🎉 SUCCESS! Both servers are now running:${NC}"
echo -e "${BLUE}   Backend:  http://localhost:8000${NC}"
echo -e "${BLUE}   Frontend: http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}📝 Log files:${NC}"
echo -e "   Backend:  backend.log"
echo -e "   Frontend: frontend.log"
echo ""
echo -e "${YELLOW}🛑 To stop all servers, run: ./stop-all.sh${NC}"
echo -e "${YELLOW}🔄 To restart, run: ./restart-all.sh${NC}"
echo ""
echo -e "${GREEN}🚀 Patent Drafting Agent is ready for testing!${NC}"

# Keep script running and show logs
echo -e "${BLUE}📊 Showing real-time logs (Ctrl+C to stop)...${NC}"
echo "=================================================="
tail -f backend.log frontend.log
