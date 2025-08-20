#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "🚀 Starting Agentic Native Drafting Service..."

# Load local env if present (for development only)
if [ -f "$ROOT_DIR/.env" ]; then
  echo "📄 Loading environment variables from .env"
  set -a
  . "$ROOT_DIR/.env"
  set +a
else
  echo "⚠️  No .env file found - make sure environment variables are set"
fi

# Check if virtual environment exists
if [ -d "$ROOT_DIR/.venv" ]; then
  echo "🐍 Activating virtual environment"
  source "$ROOT_DIR/.venv/bin/activate"
else
  echo "⚠️  No virtual environment found at $ROOT_DIR/.venv"
fi

# Ensure src has __init__.py
if [ ! -f "$ROOT_DIR/src/__init__.py" ]; then
  echo "📝 Creating __init__.py in src directory"
  touch "$ROOT_DIR/src/__init__.py"
fi

echo "📁 Working from root directory: $ROOT_DIR"
cd "$ROOT_DIR"

echo "🌐 Starting FastAPI server on http://127.0.0.1:8000"
echo "📊 API docs will be available at http://127.0.0.1:8000/docs"
echo ""

# Run uvicorn with module syntax
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000