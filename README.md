# md2doc - Markdown to DOCX MCP Server

A Model Context Protocol (MCP) server that converts Markdown text to DOCX format using an external conversion service.

## Features

- Convert Markdown text to DOCX format
- Support for custom templates
- Multi-language support (English, Chinese, etc.)
- Automatic file download to user's Downloads directory
- Template listing and management

## Installation

### Prerequisites

1. Install [uv](https://github.com/astral-sh/uv) (recommended):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```

   Or install via Homebrew:
   ```bash
   brew install uv
   ```

### Install Dependencies

1. Clone this repository
2. Install dependencies using uv (recommended):
   ```bash
   uv pip install -e .
   ```

   Or using traditional pip:
   ```bash
   pip install -e .
   ```

## Environment Variables

Set the following environment variable:
- `DEEP_SHARE_API_KEY`: Your API key for the conversion service

## Usage

### As an MCP Server

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "md2doc": {
      "command": "python",
      "args": ["-m", "md2doc.server"],
      "env": {
        "DEEP_SHARE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Available Tools

- `convert_markdown_to_docx`: Convert markdown text to DOCX
- `list_templates`: Get available templates by language

## API Reference

The server uses the following external API endpoints:

- `POST /convert-text`: Convert markdown to DOCX
- `GET /templates`: Get available templates

## License

MIT 