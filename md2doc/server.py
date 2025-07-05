"""MCP Server for Markdown to DOCX conversion."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

from .api_client import ConversionAPIClient
from .models import ConvertTextRequest, ConvertTextResponse, TemplatesResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("md2doc")

# Initialize API client
api_client = ConversionAPIClient()


@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="convert_markdown_to_docx",
                description="Convert markdown text to DOCX format and save to Downloads directory",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Markdown content to convert"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Output filename (without extension), defaults to 'document'"
                        },
                        "template_name": {
                            "type": "string",
                            "description": "Template name to use (optional)"
                        },
                        "language": {
                            "type": "string",
                            "description": "Language code (e.g., 'en', 'zh'), defaults to 'en'"
                        },
                        "convert_mermaid": {
                            "type": "boolean",
                            "description": "Whether to convert Mermaid diagrams, defaults to false"
                        }
                    },
                    "required": ["content"]
                }
            ),
            Tool(
                name="list_templates",
                description="Get available templates organized by language",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    )


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "convert_markdown_to_docx":
            return await handle_convert_markdown_to_docx(arguments)
        elif name == "list_templates":
            return await handle_list_templates()
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )
                ],
                isError=True
            )
    except Exception as e:
        logger.error(f"Error handling tool call {name}: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ],
            isError=True
        )


async def handle_convert_markdown_to_docx(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle markdown to DOCX conversion."""
    try:
        # Parse arguments
        content = arguments.get("content", "")
        filename = arguments.get("filename", "document")
        template_name = arguments.get("template_name")
        language = arguments.get("language", "en")
        convert_mermaid = arguments.get("convert_mermaid", False)
        
        if not content:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="Error: Content is required"
                    )
                ],
                isError=True
            )
        
        # Create request
        request = ConvertTextRequest(
            content=content,
            filename=filename,
            template_name=template_name,
            language=language,
            convert_mermaid=convert_mermaid
        )
        
        # Convert markdown to DOCX
        response = await api_client.convert_text(request)
        
        if response.success:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"✅ Successfully converted markdown to DOCX!\n\n📁 File saved to: {response.file_path}\n\nYou can now open the document in Microsoft Word or any compatible application."
                    )
                ]
            )
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"❌ Conversion failed: {response.error_message}"
                    )
                ],
                isError=True
            )
            
    except Exception as e:
        logger.error(f"Error converting markdown to DOCX: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ],
            isError=True
        )


async def handle_list_templates() -> CallToolResult:
    """Handle template listing."""
    try:
        response = await api_client.get_templates()
        
        if response.templates:
            # Format templates for display
            template_text = "📋 Available Templates:\n\n"
            
            for language, templates in response.templates.items():
                template_text += f"**{language.upper()}:**\n"
                for template in templates:
                    template_text += f"  • {template}\n"
                template_text += "\n"
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=template_text
                    )
                ]
            )
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="No templates available or unable to fetch templates."
                    )
                ]
            )
            
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error fetching templates: {str(e)}"
                )
            ],
            isError=True
        )


async def main():
    """Main entry point."""
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="md2doc",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main()) 