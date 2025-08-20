.PHONY: help start stop restart status logs clean build docker-up docker-down docker-build test

# Default target
help:
	@echo "Patent Drafting Agent - Management Commands"
	@echo "==========================================="
	@echo ""
	@echo "Local Development:"
	@echo "  start        - Start both backend and frontend servers"
	@echo "  stop         - Stop both servers"
	@echo "  restart      - Restart both servers"
	@echo "  status       - Show status of both servers"
	@echo "  logs         - Show real-time logs from both servers"
	@echo "  clean        - Clean up log files and PID files"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up    - Start services with Docker Compose"
	@echo "  docker-down  - Stop Docker services"
	@echo "  docker-build - Build Docker images"
	@echo ""
	@echo "Build & Test:"
	@echo "  build        - Build frontend for production"
	@echo "  test         - Run tests"
	@echo ""
	@echo "Setup:"
	@echo "  setup        - Initial setup (install dependencies, create venv)"
	@echo "  install      - Install dependencies for both services"

# Local development commands
start:
	@echo "🚀 Starting Patent Drafting Agent..."
	@./start-all.sh

stop:
	@echo "🛑 Stopping Patent Drafting Agent..."
	@./stop-all.sh

restart:
	@echo "🔄 Restarting Patent Drafting Agent..."
	@./restart-all.sh

status:
	@echo "📊 Server Status:"
	@echo "Backend (8000):"
	@lsof -i :8000 2>/dev/null || echo "  ❌ Not running"
	@echo "Frontend (3000):"
	@lsof -i :3000 2>/dev/null || echo "  ❌ Not running"

logs:
	@echo "📝 Showing logs (Ctrl+C to stop)..."
	@tail -f backend.log frontend.log 2>/dev/null || echo "No log files found. Start servers first."

clean:
	@echo "🧹 Cleaning up..."
	@rm -f .backend.pid .frontend.pid
	@rm -f backend.log frontend.log
	@echo "✅ Cleanup complete"

# Docker commands
docker-up:
	@echo "🐳 Starting services with Docker Compose..."
	@docker-compose up -d

docker-down:
	@echo "🐳 Stopping Docker services..."
	@docker-compose down

docker-build:
	@echo "🔨 Building Docker images..."
	@docker-compose build

# Build and test
build:
	@echo "🔨 Building frontend..."
	@cd word-addin-agent-ui && npm run build

test:
	@echo "🧪 Running tests..."
	@cd word-addin-agent-ui && npm test

# Setup commands
setup: install
	@echo "🔧 Setting up virtual environment..."
	@python3 -m venv .venv
	@echo "✅ Setup complete! Run 'source .venv/bin/activate' to activate"

install:
	@echo "📦 Installing dependencies..."
	@echo "Installing backend dependencies..."
	@source .venv/bin/activate && pip install -r agentic_native_drafting/requirements.txt
	@echo "Installing frontend dependencies..."
	@cd word-addin-agent-ui && npm install
	@echo "✅ Dependencies installed"

# Quick start for development
dev: start
	@echo "🚀 Development environment started!"
	@echo "Backend:  http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop all servers"
