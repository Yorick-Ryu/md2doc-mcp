"""Pydantic models for the md2doc MCP server."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ConvertTextRequest(BaseModel):
    """Request model for markdown to DOCX conversion."""
    
    content: str = Field(..., description="Markdown content to convert")
    filename: Optional[str] = Field("document", description="Output filename (without extension)")
    template_name: Optional[str] = Field(None, description="Template name to use")
    language: str = Field("en", description="Language code (e.g., 'en', 'zh')")
    convert_mermaid: Optional[bool] = Field(False, description="Whether to convert Mermaid diagrams")


class ConvertTextResponse(BaseModel):
    """Response model for markdown to DOCX conversion."""
    
    success: bool = Field(..., description="Whether the conversion was successful")
    file_path: Optional[str] = Field(None, description="Path to the downloaded DOCX file")
    error_message: Optional[str] = Field(None, description="Error message if conversion failed")


class TemplatesResponse(BaseModel):
    """Response model for available templates."""
    
    templates: Dict[str, List[str]] = Field(..., description="Templates organized by language code") 