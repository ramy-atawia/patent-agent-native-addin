#!/bin/bash

echo "🚀 Setting up Patent Drafting Agent Word Add-in..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ npm version: $(npm -v)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cat > .env << EOF
# Backend API Configuration
REACT_APP_API_URL=http://localhost:8000

# Development Configuration
NODE_ENV=development
EOF
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

# Copy icons from myword-addin if available
if [ -d "../myword-addin/assets" ]; then
    echo "📁 Copying icons from myword-addin..."
    cp -r ../myword-addin/assets/* assets/ 2>/dev/null || echo "⚠️  Some icons could not be copied"
    echo "✅ Icons copied"
else
    echo "⚠️  myword-addin/assets directory not found. Please copy icons manually."
fi

# Install Office Add-in development tools
echo "🔧 Installing Office Add-in development tools..."
npm install -g office-addin-dev-certs office-addin-debugging office-addin-manifest

if [ $? -ne 0 ]; then
    echo "⚠️  Failed to install Office Add-in tools globally. You may need to run with sudo."
    echo "   Try: sudo npm install -g office-addin-dev-certs office-addin-debugging office-addin-manifest"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Start the backend API (see agentic-native-drafting folder)"
echo "2. Run: npm run dev-server"
echo "3. In another terminal, run: npm start"
echo ""
echo "The add-in will be available in Word under the Home tab."
echo ""
echo "For more information, see README.md"
