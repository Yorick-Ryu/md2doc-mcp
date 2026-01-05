# md2doc - Markdown to DOCX MCP Server

[![PyPI version](https://badge.fury.io/py/md2doc.svg)](https://badge.fury.io/py/md2doc)
[![MCP Badge](https://lobehub.com/badge/mcp/yorick-ryu-md2doc-mcp)](https://lobehub.com/mcp/yorick-ryu-md2doc-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that converts Markdown text to DOCX format using an external conversion service.

<img src="https://raw.githubusercontent.com/Yorick-Ryu/md2doc-mcp/master/images/md2doc.png" alt="md2doc Demo" width="600" style="max-width: 100%; height: auto;">

## Features

- Convert Markdown text to DOCX format
- Support for custom templates
- Multi-language support (English, Chinese, etc.)
- Automatic file download to user's Downloads directory
- Template listing and management

## Usage

### Cherry Studio

1. Open Cherry Studio
2. Go to Settings → MCP
3. Add the server configuration:
   ```json
   {
     "mcpServers": {
       "md2doc": {
         "command": "uvx",
         "args": ["md2doc"],
         "env": {
           "DEEP_SHARE_API_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

### Claude Desktop

1. Open your Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the md2doc server:
   ```json
   {
     "mcpServers": {
       "md2doc": {
         "command": "uvx",
         "args": ["md2doc"],
         "env": {
           "DEEP_SHARE_API_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop

### Command Line (Quick Start)

For immediate use without any client setup:

```bash
# Install and run the server
uvx md2doc

# Or with environment variable
DEEP_SHARE_API_KEY="your-api-key-here" uvx md2doc
```

### Python Integration

You can also use md2doc directly in your Python projects:

```python
import asyncio
from md2doc.api_client import ConversionAPIClient
from md2doc.models import ConvertTextRequest

async def convert_markdown():
    client = ConversionAPIClient()
    
    request = ConvertTextRequest(
        content="# Hello World\n\nThis is **markdown** content.",
        filename="example",
        language="zh",
        template_name="templates",
        remove_hr=False,
        compat_mode=True
    )
    
    response = await client.convert_text(request)
    if response.success:
        print(f"File saved to: {response.file_path}")

# Run the conversion
asyncio.run(convert_markdown())
```

### Other MCP Clients

The server works with any MCP-compatible client. Configure it to run:
```bash
uvx md2doc
```

With environment variables:
```bash
DEEP_SHARE_API_KEY="your-api-key-here" uvx md2doc
```

### Cloud Deployment (Remote Server)

When deploying this MCP server on a cloud server (VPS/Docker), set `MCP_SAVE_REMOTE=true` to return a temporary download link instead of saving to a local directory:

```bash
# In your cloud environment
export DEEP_SHARE_API_KEY="your-api-key-here"
export MCP_SAVE_REMOTE=true

uvx md2doc
```

The server will provide a download link for the converted document.

## API Key

### Free Trial API Key
Use this key for testing:
```
f4e8fe6f-e39e-486f-b7e7-e037d2ec216f
```

### Purchase API Key - Super Low Price!

- [Purchase Link](https://www.deepshare.app/purchase-en.html)
- [中国大陆购买](https://www.deepshare.app/purchase.html)

## Available Tools

- `convert_markdown_to_docx`: Convert markdown text to DOCX
- `list_templates`: Get available templates by language

## License

MIT 
