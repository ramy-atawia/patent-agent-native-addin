#!/bin/bash

# Patent Drafting Agent - Restart All Servers Script

echo "🔄 Restarting Patent Drafting Agent Servers"
echo "==========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🛑 Stopping existing servers...${NC}"
./stop-all.sh

echo ""
echo -e "${YELLOW}⏳ Waiting 3 seconds before restarting...${NC}"
sleep 3

echo ""
echo -e "${YELLOW}🚀 Starting servers...${NC}"
./start-all.sh
