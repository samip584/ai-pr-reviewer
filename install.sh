#!/bin/bash
set -e

echo "🤖 Installing rwgpt - AI-Powered Code Review CLI"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Install the package
echo ""
echo "📦 Installing rwgpt..."
pip install -e .

# Verify installation
echo ""
echo "🔍 Verifying installation..."
if command -v rwgpt &> /dev/null; then
    echo "✓ rwgpt installed successfully!"
    rwgpt --help | head -3
else
    echo "⚠️  rwgpt command not found in PATH"
    echo "You can still use: python3 -m rwgpt"
fi

# Check for API key
echo ""
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY is not set"
    echo ""
    echo "To set your API key, run:"
    echo "  export OPENAI_API_KEY='sk-your-api-key-here'"
    echo ""
    echo "For permanent setup, add to your ~/.zshrc or ~/.bashrc:"
    echo "  echo 'export OPENAI_API_KEY=\"sk-your-api-key-here\"' >> ~/.zshrc"
else
    echo "✓ OPENAI_API_KEY is set"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Try it out:"
echo "  cd /path/to/your/git/repo"
echo "  rwgpt --input \"\$(git diff)\""
