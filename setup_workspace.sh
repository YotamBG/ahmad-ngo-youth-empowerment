#!/bin/bash

# GOOGLE WORKSPACE AUTOMATION SETUP SCRIPT
# Ahmad NGO Youth Empowerment Project
# Based on Matrix Dance implementation

set -e

echo "🚀 GOOGLE WORKSPACE AUTOMATION SETUP"
echo "====================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "📦 Please install Python 3.8 or higher"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if Google Cloud CLI is installed
if ! command -v gcloud &> /dev/null; then
    echo "⚠️  Google Cloud CLI not found"
    echo "📦 Installing Google Cloud CLI..."
    
    # Install gcloud CLI (Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz | tar -xz
        ./google-cloud-sdk/install.sh --quiet
        source ./google-cloud-sdk/path.bash.inc
    else
        echo "📋 Please install Google Cloud CLI manually:"
        echo "   https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
fi

echo "✅ Google Cloud CLI found: $(gcloud version --format='value(Google Cloud SDK)')"

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create default configuration if it doesn't exist
if [ ! -f "workspace_config.json" ]; then
    echo "📝 Creating default configuration..."
    python3 -c "
from google_workspace_automation import GoogleWorkspaceAutomator
automator = GoogleWorkspaceAutomator()
print('✅ Configuration file created: workspace_config.json')
"
fi

# Check environment variables
echo "🔍 Checking environment variables..."

if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "⚠️  GOOGLE_APPLICATION_CREDENTIALS not set"
    echo "💡 This will be set automatically during service account creation"
fi

if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "⚠️  CLOUDFLARE_API_TOKEN not set"
    echo "🔑 Please set this if using Cloudflare for DNS management:"
    echo "   export CLOUDFLARE_API_TOKEN='your-token-here'"
fi

echo ""
echo "✅ SETUP COMPLETE!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Update workspace_config.json with your domain and details"
echo "2. Set required environment variables:"
echo "   export CLOUDFLARE_API_TOKEN='your-token-here'"
echo "3. Run the automation script:"
echo "   source venv/bin/activate"
echo "   python3 google_workspace_automation.py"
echo ""
echo "📚 For detailed instructions, see the script documentation"
echo "🔗 Reference: Matrix Dance project implementation" 