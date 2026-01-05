"""API client for the external markdown to DOCX conversion service."""

import os
import httpx
from .models import ConvertTextRequest, ConvertTextResponse, TemplatesResponse


class ConversionAPIClient:
    """Client for the external markdown to DOCX conversion API."""
    
    def __init__(self, base_url: str = "https://api.deepshare.app"):
        """Initialize the API client.
        
        Args:
            base_url: Base URL for the conversion API
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = os.getenv("DEEP_SHARE_API_KEY")
        
        if not self.api_key:
            raise ValueError("DEEP_SHARE_API_KEY environment variable is required")
    
    async def convert_text(self, request: ConvertTextRequest) -> ConvertTextResponse:
        """Convert markdown text to DOCX.
        
        Args:
            request: Conversion request parameters
            
        Returns:
            Response with conversion result
        """
        async with httpx.AsyncClient() as client:
            headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "content": request.content,
                "filename": request.filename,
                "template_name": request.template_name,
                "language": request.language,
                "convert_mermaid": request.convert_mermaid,
                "remove_hr": request.remove_hr,
                "compat_mode": request.compat_mode
            }
            
            try:
                # Decide which endpoint to use
                is_remote = os.getenv("MCP_SAVE_REMOTE", "false").lower() == "true"
                endpoint = "/convert-text-to-url" if is_remote else "/convert-text"
                
                response = await client.post(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    data = response.json() if is_remote else response.content
                    
                    if is_remote:
                        # Backend returned a JSON with {"url": "..."}
                        return ConvertTextResponse(
                            success=True,
                            file_path=data.get("url")
                        )
                    else:
                        # Backend returned binary DOCX
                        downloads_dir = self._get_downloads_directory()
                        filename = f"{request.filename}.docx"
                        file_path = os.path.join(downloads_dir, filename)
                        file_path = self._ensure_unique_filename(file_path)
                        
                        with open(file_path, "wb") as f:
                            f.write(data)
                        
                        return ConvertTextResponse(
                            success=True,
                            file_path=file_path
                        )
                else:
                    return ConvertTextResponse(
                        success=False,
                        error_message=f"API request failed with status {response.status_code}: {response.text}"
                    )
                    
            except httpx.RequestError as e:
                return ConvertTextResponse(
                    success=False,
                    error_message=f"Network error: {str(e)}"
                )
            except Exception as e:
                return ConvertTextResponse(
                    success=False,
                    error_message=f"Unexpected error: {str(e)}"
                )
    
    async def get_templates(self) -> TemplatesResponse:
        """Get available templates from the API.
        
        Returns:
            Response with available templates organized by language
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/templates",
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    templates_data = response.json()
                    return TemplatesResponse(templates=templates_data)
                else:
                    # Return empty templates if API fails
                    return TemplatesResponse(templates={})
                    
            except Exception as e:
                # Return empty templates on error
                return TemplatesResponse(templates={})
    
    def _get_downloads_directory(self) -> str:
        """Get the user's Downloads directory.
        
        Returns:
            Path to the Downloads directory
        """
        home_dir = os.path.expanduser("~")
        downloads_dir = os.path.join(home_dir, "Downloads")
        
        # Create Downloads directory if it doesn't exist
        os.makedirs(downloads_dir, exist_ok=True)
        
        return downloads_dir
    
    def _ensure_unique_filename(self, file_path: str) -> str:
        """Ensure the filename is unique by adding a number if needed.
        
        Args:
            file_path: Original file path
            
        Returns:
            Unique file path
        """
        if not os.path.exists(file_path):
            return file_path
        
        base_name, ext = os.path.splitext(file_path)
        counter = 1
        
        while True:
            new_path = f"{base_name}_{counter}{ext}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1 