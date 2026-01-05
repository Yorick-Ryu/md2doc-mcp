"""MCP Server for Markdown to DOCX conversion."""

import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

from .api_client import ConversionAPIClient
from .models import ConvertTextRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastMCP server
mcp = FastMCP("md2doc")

# Initialize API client lazily
_api_client = None


def get_api_client() -> ConversionAPIClient:
    """Get or create the API client."""
    global _api_client
    if _api_client is None:
        _api_client = ConversionAPIClient()
    return _api_client


@mcp.tool()
async def convert_markdown_to_docx(
    content: str,
    filename: str = "output",
    template_name: str = "templates",
    language: str = "zh",
    convert_mermaid: bool = False,
    remove_hr: bool = False,
    compat_mode: Optional[bool] = True
) -> str:
    """Convert markdown text to DOCX format and save to Downloads directory.
    
    Args:
        content: Markdown content to convert
        filename: Output filename (without extension), defaults to 'output'
        template_name: Template name to use, defaults to 'templates'
        language: Language code (e.g., 'en', 'zh'), defaults to 'zh'
        convert_mermaid: Whether to convert Mermaid diagrams, defaults to false
        remove_hr: Whether to remove horizontal rules, defaults to false
        compat_mode: Enable compatibility mode for older document formats (optional)
    
    Returns:
        Success message with file path or error message
    """
    if not content:
        return "Error: Content is required"
    
    try:
        # Create request
        request = ConvertTextRequest(
            content=content,
            filename=filename,
            template_name=template_name,
            language=language,
            convert_mermaid=convert_mermaid,
            remove_hr=remove_hr,
            compat_mode=compat_mode
        )
        
        # Get API client and convert markdown to DOCX
        api_client = get_api_client()
        response = await api_client.convert_text(request)
        
        if response.success:
            if response.file_path.startswith("http"):
                return f"✅ Successfully converted markdown to DOCX!\n\n🔗 Download Link: {response.file_path}\n\n*Note: This link is temporary. Please download it to your local machine.*"
            else:
                return f"✅ Successfully converted markdown to DOCX!\n\n📁 File saved to: {response.file_path}\n\nYou can now open the document in Microsoft Word or any compatible application."
        else:
            return f"❌ Conversion failed: {response.error_message}"
            
    except Exception as e:
        logger.error(f"Error converting markdown to DOCX: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
async def list_templates() -> str:
    """Get available templates organized by language.
    
    Returns:
        List of available templates or error message
    """
    try:
        api_client = get_api_client()
        response = await api_client.get_templates()
        
        if response.templates:
            # Format templates for display
            template_text = "📋 Available Templates:\n\n"
            
            for language, templates in response.templates.items():
                template_text += f"**{language.upper()}:**\n"
                for template in templates:
                    template_text += f"  • {template}\n"
                template_text += "\n"
            
            return template_text
        else:
            return "No templates available or unable to fetch templates."
            
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        return f"Error fetching templates: {str(e)}"


def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main() 