#!/bin/bash

echo "🚀 Deploying Patent Drafting Agent Word Add-in..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the word-addin-agent-ui directory"
    exit 1
fi

# Build the project
echo "📦 Building project..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build completed successfully"

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "❌ dist directory not found. Build may have failed."
    exit 1
fi

# Copy manifest to dist
echo "📋 Copying manifest..."
cp manifest.xml dist/

# Copy assets to dist
echo "🖼️  Copying assets..."
cp -r assets dist/ 2>/dev/null || echo "⚠️  No assets directory found"

echo ""
echo "🎉 Deployment package ready in dist/ directory!"
echo ""
echo "Next steps:"
echo "1. Update manifest.xml with production URLs"
echo "2. Upload dist/ contents to your web server"
echo "3. Update Office Add-in manifest in Word"
echo ""
echo "For production deployment:"
echo "- Update REACT_APP_API_URL in .env"
echo "- Ensure HTTPS is enabled"
echo "- Test the add-in thoroughly"
echo ""
echo "Files in dist/:"
ls -la dist/
