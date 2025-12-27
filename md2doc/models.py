"""Pydantic models for the md2doc MCP server."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ConvertTextRequest(BaseModel):
    """Request model for markdown to DOCX conversion."""
    
    content: str = Field(..., description="Markdown content to convert")
    filename: Optional[str] = Field("output", description="Output filename (without extension)")
    template_name: Optional[str] = Field("templates", description="Template name to use")
    language: str = Field("zh", description="Language code (e.g., 'en', 'zh')")
    convert_mermaid: Optional[bool] = Field(False, description="Whether to convert Mermaid diagrams")
    remove_hr: Optional[bool] = Field(False, description="Whether to remove horizontal rules from the document")
    compat_mode: Optional[bool] = Field(True, description="Enable compatibility mode for older document formats")


class ConvertTextResponse(BaseModel):
    """Response model for markdown to DOCX conversion."""
    
    success: bool = Field(..., description="Whether the conversion was successful")
    file_path: Optional[str] = Field(None, description="Path to the downloaded DOCX file")
    error_message: Optional[str] = Field(None, description="Error message if conversion failed")


class TemplatesResponse(BaseModel):
    """Response model for available templates."""
    
    templates: Dict[str, List[str]] = Field(..., description="Templates organized by language code") 