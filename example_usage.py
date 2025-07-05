#!/usr/bin/env python3
"""
Example usage of the md2doc MCP server.

This script demonstrates how to use the md2doc server to convert markdown to DOCX.

To run this example:
1. Install dependencies: uv pip install -e .
2. Set your API key: export DEEP_SHARE_API_KEY='your-api-key-here'
3. Run: uv run python example_usage.py

Note: Make sure to set the DEEP_SHARE_API_KEY environment variable before running this script.
"""

import asyncio
import os
from md2doc.api_client import ConversionAPIClient
from md2doc.models import ConvertTextRequest


async def example_convert_markdown():
    """Example of converting markdown to DOCX."""
    
    # Get API key from environment variable
    api_key = os.getenv("DEEP_SHARE_API_KEY")
    if not api_key:
        print("❌ Error: DEEP_SHARE_API_KEY environment variable is not set.")
        print("   Please set it: export DEEP_SHARE_API_KEY='your-api-key-here'")
        return
    
    # Initialize the API client
    client = ConversionAPIClient()
    
    # Example markdown content
    markdown_content = """# Sample Document

This is a sample markdown document that will be converted to DOCX format.

## Features

- **Bold text** and *italic text*
- Lists with bullets
- Code blocks

```python
def hello_world():
    print("Hello, World!")
```

## Tables

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

## Conclusion

This document demonstrates the conversion capabilities of the md2doc server.
"""
    
    # Create conversion request
    request = ConvertTextRequest(
        content=markdown_content,
        filename="sample_document",
        language="en",
        template_name="thesis",  # Optional: use a specific template
        convert_mermaid=False
    )
    
    print("Converting markdown to DOCX...")
    
    # Convert markdown to DOCX
    response = await client.convert_text(request)
    
    if response.success:
        print(f"✅ Success! File saved to: {response.file_path}")
    else:
        print(f"❌ Error: {response.error_message}")


async def example_list_templates():
    """Example of listing available templates."""
    
    # Get API key from environment variable
    api_key = os.getenv("DEEP_SHARE_API_KEY")
    if not api_key:
        print("❌ Error: DEEP_SHARE_API_KEY environment variable is not set.")
        print("   Please set it: export DEEP_SHARE_API_KEY='your-api-key-here'")
        return
    
    # Initialize the API client
    client = ConversionAPIClient()
    
    print("Fetching available templates...")
    
    # Get available templates
    response = await client.get_templates()
    
    if response.templates:
        print("📋 Available Templates:")
        for language, templates in response.templates.items():
            print(f"\n{language.upper()}:")
            for template in templates:
                print(f"  • {template}")
    else:
        print("No templates available or unable to fetch templates.")


if __name__ == "__main__":
    print("md2doc Example Usage")
    print("=" * 50)
    
    # Run examples
    asyncio.run(example_list_templates())
    print("\n" + "=" * 50)
    asyncio.run(example_convert_markdown()) 