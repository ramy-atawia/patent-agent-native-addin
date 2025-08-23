#!/bin/bash

# Prior Art Search LLM Performance Test Runner
# This script runs the comprehensive prior art search evaluation

echo "🚀 Starting Prior Art Search LLM Performance Evaluation"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "test_prior_art_llm_performance.py" ]; then
    echo "❌ Error: test_prior_art_llm_performance.py not found"
    echo "Please run this script from the agentic_native_drafting directory"
    exit 1
fi

# Check if Python virtual environment exists
if [ -d ".venv" ]; then
    echo "🐍 Activating Python virtual environment..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "🐍 Activating Python virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found, using system Python"
fi

# Check environment variables
echo "🔍 Checking environment variables..."
if [ -z "$AZURE_OPENAI_ENDPOINT" ] || [ -z "$AZURE_OPENAI_API_KEY" ] || [ -z "$AZURE_OPENAI_DEPLOYMENT_NAME" ]; then
    echo "❌ Missing required environment variables:"
    echo "   AZURE_OPENAI_ENDPOINT: $AZURE_OPENAI_ENDPOINT"
    echo "   AZURE_OPENAI_API_KEY: [SET]"
    echo "   AZURE_OPENAI_DEPLOYMENT_NAME: $AZURE_OPENAI_DEPLOYMENT_NAME"
    echo ""
    echo "Please set these variables before running the tests:"
    echo "export AZURE_OPENAI_ENDPOINT='your-endpoint'"
    echo "export AZURE_OPENAI_API_KEY='your-api-key'"
    echo "export AZURE_OPENAI_DEPLOYMENT_NAME='your-deployment'"
    exit 1
fi

echo "✅ Environment variables configured"

# Install dependencies if needed
echo "📦 Checking dependencies..."
python -c "import httpx, pydantic" 2>/dev/null || {
    echo "📦 Installing required dependencies..."
    pip install httpx pydantic python-dotenv
}

# Run the tests
echo "🧪 Running Prior Art Search LLM Performance Tests..."
echo "=================================================="

python test_prior_art_llm_performance.py

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Tests completed successfully!"
    echo "📊 Check the generated results files for detailed analysis"
else
    echo ""
    echo "❌ Tests failed with exit code $?"
    echo "Check the error messages above for details"
fi
