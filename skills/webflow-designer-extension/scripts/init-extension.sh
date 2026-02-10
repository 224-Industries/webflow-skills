#!/bin/bash
# Initialize a new Webflow Designer Extension project
# Usage: ./init-extension.sh <project-name> [template]

set -e

PROJECT_NAME="${1:-my-webflow-extension}"
TEMPLATE="${2:-react}"

echo "🚀 Creating Webflow Designer Extension: $PROJECT_NAME"
echo "   Template: $TEMPLATE"
echo ""

# Check for required tools
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed."
    exit 1
fi

# Check for Webflow CLI
if ! command -v webflow &> /dev/null; then
    echo "📦 Installing Webflow CLI..."
    npm install -g @webflow/webflow-cli
fi

# Initialize project
echo "📁 Initializing project..."
webflow extension init "$PROJECT_NAME" "$TEMPLATE"

# Navigate to project
cd "$PROJECT_NAME"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install type definitions
echo "📦 Installing type definitions..."
npm install --save-dev @webflow/designer-extension-typings

echo ""
echo "✅ Project '$PROJECT_NAME' created successfully!"
echo ""
echo "📋 Next steps:"
echo "   cd $PROJECT_NAME"
echo "   npm run dev"
echo ""
echo "📌 Then in Webflow:"
echo "   1. Go to Workspace Settings > Apps & Integrations > Develop"
echo "   2. Install your app on a test site"
echo "   3. Open the Designer and press 'E' for the app panel"
echo "   4. Launch your development app"
echo ""
