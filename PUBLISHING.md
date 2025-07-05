# Publishing Guide for md2doc

This guide explains how to publish the md2doc package to PyPI.

## Prerequisites

1. **PyPI Account**: Create an account on [PyPI](https://pypi.org/account/register/)
2. **TestPyPI Account**: Create an account on [TestPyPI](https://test.pypi.org/account/register/) for testing
3. **API Token**: Generate an API token from your PyPI account settings

## Setup

### 1. Install Publishing Tools

```bash
# Install build tools
uv pip install build twine

# Or install globally
pip install build twine
```

### 2. Configure PyPI Credentials

You have several options for authentication with `uv publish`:

#### Option A: Environment Variables (Recommended)

Set environment variables for authentication:

```bash
# For PyPI
export UV_PUBLISH_TOKEN="your-pypi-token-here"
export UV_PUBLISH_URL="https://upload.pypi.org/legacy/"

# For TestPyPI
export UV_PUBLISH_TOKEN="your-testpypi-token-here"
export UV_PUBLISH_URL="https://test.pypi.org/legacy/"
```

#### Option B: Command Line Arguments

Pass credentials directly in the command:

```bash
# For PyPI
uv publish -t "your-pypi-token-here" --publish-url "https://upload.pypi.org/legacy/"

# For TestPyPI
uv publish -t "your-testpypi-token-here" --publish-url "https://test.pypi.org/legacy/"
```

#### Option C: Traditional ~/.pypirc (for twine)

If you prefer using twine, create a `~/.pypirc` file:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = your-pypi-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = your-testpypi-token-here
```

## Publishing Process

### Option 1: Using the Automated Script

```bash
# Make script executable (if not already)
chmod +x publish.sh

# Run the publish script
./publish.sh
```

### Option 2: Manual Publishing

#### Step 1: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
uv build
```

#### Step 2: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI using environment variables
export UV_PUBLISH_TOKEN="your-testpypi-token-here"
export UV_PUBLISH_URL="https://test.pypi.org/legacy/"
uv publish

# Or using command line arguments
uv publish -t "your-testpypi-token-here" --publish-url "https://test.pypi.org/legacy/"

# Test installation
uvx md2doc --index-url https://test.pypi.org/simple/
```

#### Step 3: Publish to PyPI

```bash
# Upload to PyPI using environment variables
export UV_PUBLISH_TOKEN="your-pypi-token-here"
export UV_PUBLISH_URL="https://upload.pypi.org/legacy/"
uv publish

# Or using command line arguments
uv publish -t "your-pypi-token-here" --publish-url "https://upload.pypi.org/legacy/"
```

## Version Management

To update the version:

1. Edit `pyproject.toml`:
   ```toml
   [project]
   version = "0.1.1"  # Increment version
   ```

2. Update `md2doc/__init__.py`:
   ```python
   __version__ = "0.1.1"
   ```

3. Build and publish:
   ```bash
   ./publish.sh
   ```

## Verification

After publishing, verify the installation:

```bash
# Test installation
uvx md2doc

# Or install and test
uv pip install md2doc
python -c "import md2doc; print(md2doc.__version__)"
```

## Troubleshooting

### Common Issues

1. **Authentication Error**: Check your `~/.pypirc` file and API tokens
2. **Version Already Exists**: Increment the version number in `pyproject.toml`
3. **Build Errors**: Ensure all dependencies are correctly specified

### Testing Locally

```bash
# Test the package locally before publishing
uv pip install -e .
python test_package.py
```

## Package Information

- **Package Name**: md2doc
- **PyPI URL**: https://pypi.org/project/md2doc/
- **Install Command**: `uvx md2doc`
- **Entry Point**: `md2doc.server:main`

## Support

If you encounter issues during publishing:

1. Check the [PyPI documentation](https://packaging.python.org/tutorials/packaging-projects/)
2. Verify your package structure with `python -m build --sdist --wheel`
3. Test with TestPyPI first 