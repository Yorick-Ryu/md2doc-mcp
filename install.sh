#!/bin/bash

# md2doc MCP Server Installation Script

echo "🚀 Installing md2doc MCP Server..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   source \$HOME/.local/bin/env"
    exit 1
fi

echo "✅ uv is installed."

# Install the package in development mode
echo "📦 Installing md2doc package..."
uv pip install -e .

if [ $? -eq 0 ]; then
    echo "✅ md2doc package installed successfully!"
else
    echo "❌ Failed to install md2doc package."
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
echo "🎉 Installation complete!"
echo ""
echo "To use the md2doc MCP server:"
echo "1. Set your API key: export DEEP_SHARE_API_KEY='your-api-key-here'"
echo "2. Add the server to your MCP client configuration:"
echo "   See mcp-config.json for an example"
echo ""
echo "Available tools:"
echo "- convert_markdown_to_docx: Convert markdown to DOCX"
echo "- list_templates: Get available templates"
echo ""
echo "For more information, see README.md" 