#!/bin/bash

# md2doc Development Setup Script (using uv)

echo "🚀 Setting up md2doc development environment with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
fi

echo "✅ uv is available."

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
uv pip install -e ".[dev]"

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies."
    exit 1
fi

# Check if API key is set
if [ -z "$DEEP_SHARE_API_KEY" ]; then
    echo "⚠️  Warning: DEEP_SHARE_API_KEY environment variable is not set."
    echo "   Please set it before using the server:"
    echo "   export DEEP_SHARE_API_KEY='your-api-key-here'"
else
    echo "✅ DEEP_SHARE_API_KEY is set."
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Available commands:"
echo "- uv run python -m md2doc.server    # Run the MCP server"
echo "- uv run python example_usage.py     # Run the example script"
echo "- uv run pytest tests/               # Run tests"
echo "- uv run black .                     # Format code"
echo "- uv run isort .                     # Sort imports"
echo ""
echo "To use the md2doc MCP server:"
echo "1. Set your API key: export DEEP_SHARE_API_KEY='your-api-key-here'"
echo "2. Add the server to your MCP client configuration (see mcp-config.json)"
echo ""
echo "For more information, see README.md" 