#!/bin/bash

# Example publishing script for md2doc
# This script shows how to publish using environment variables

echo "🚀 md2doc Publishing Example"
echo "=========================="

# Build the package first
echo "📦 Building package..."
uv build

if [ ! -d "dist" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# Example 1: Publish to TestPyPI
echo ""
echo "📤 Publishing to TestPyPI..."
echo "Set your TestPyPI token:"
echo "export UV_PUBLISH_TOKEN=\"your-testpypi-token-here\""
echo "export UV_PUBLISH_URL=\"https://test.pypi.org/legacy/\""
echo ""
echo "Then run: uv publish"
echo ""

# Example 2: Publish to PyPI
echo "📤 Publishing to PyPI..."
echo "Set your PyPI token:"
echo "export UV_PUBLISH_TOKEN=\"your-pypi-token-here\""
echo "export UV_PUBLISH_URL=\"https://upload.pypi.org/legacy/\""
echo ""
echo "Then run: uv publish"
echo ""

# Example 3: Using command line arguments
echo "📤 Alternative: Using command line arguments..."
echo "For TestPyPI:"
echo "uv publish -t \"your-testpypi-token-here\" --publish-url \"https://test.pypi.org/legacy/\""
echo ""
echo "For PyPI:"
echo "uv publish -t \"your-pypi-token-here\" --publish-url \"https://upload.pypi.org/legacy/\""
echo ""

echo "🎉 After publishing, users can install with: uvx md2doc" 