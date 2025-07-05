"""Tests for the API client."""

import os
import pytest
from unittest.mock import AsyncMock, patch, Mock
from md2doc.api_client import ConversionAPIClient
from md2doc.models import ConvertTextRequest, TemplatesResponse


class TestConversionAPIClient:
    """Test cases for ConversionAPIClient."""
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch.dict(os.environ, {"DEEP_SHARE_API_KEY": "test-key"}):
            client = ConversionAPIClient()
            assert client.api_key == "test-key"
            assert client.base_url == "https://api.deepshare.app"
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="DEEP_SHARE_API_KEY environment variable is required"):
                ConversionAPIClient()
    
    def test_init_with_custom_base_url(self):
        """Test initialization with custom base URL."""
        with patch.dict(os.environ, {"DEEP_SHARE_API_KEY": "test-key"}):
            client = ConversionAPIClient("https://custom-api.com")
            assert client.base_url == "https://custom-api.com"
    
    @pytest.mark.asyncio
    async def test_convert_text_success(self):
        """Test successful text conversion."""
        with patch.dict(os.environ, {"DEEP_SHARE_API_KEY": "test-key"}):
            client = ConversionAPIClient()
            
            # Mock the Downloads directory
            with patch.object(client, '_get_downloads_directory', return_value="/tmp/downloads"):
                with patch.object(client, '_ensure_unique_filename', return_value="/tmp/downloads/test.docx"):
                    with patch('builtins.open', create=True) as mock_open:
                        mock_file = AsyncMock()
                        mock_open.return_value.__enter__.return_value = mock_file
                        
                        # Mock httpx client
                        mock_response = AsyncMock()
                        mock_response.status_code = 200
                        mock_response.content = b"fake-docx-content"
                        mock_response.text = "OK"
                        
                        mock_client = AsyncMock()
                        mock_client.__aenter__.return_value = mock_client
                        mock_client.__aexit__.return_value = None
                        mock_client.post.return_value = mock_response
                        
                        with patch('httpx.AsyncClient', return_value=mock_client):
                            request = ConvertTextRequest(
                                content="# Test\n\nThis is a test.",
                                filename="test",
                                language="en"
                            )
                            
                            response = await client.convert_text(request)
                            
                            assert response.success is True
                            assert response.file_path == "/tmp/downloads/test.docx"
                            assert response.error_message is None
    
    @pytest.mark.asyncio
    async def test_convert_text_api_error(self):
        """Test text conversion with API error."""
        with patch.dict(os.environ, {"DEEP_SHARE_API_KEY": "test-key"}):
            client = ConversionAPIClient()
            
            # Mock httpx client
            mock_response = AsyncMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.post.return_value = mock_response
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                request = ConvertTextRequest(
                    content="# Test\n\nThis is a test.",
                    filename="test",
                    language="en"
                )
                
                response = await client.convert_text(request)
                
                assert response.success is False
                assert "API request failed with status 400" in response.error_message
    
    @pytest.mark.asyncio
    async def test_get_templates_success(self):
        """Test successful template retrieval."""
        with patch.dict(os.environ, {"DEEP_SHARE_API_KEY": "test-key"}):
            client = ConversionAPIClient()
            
            # Mock httpx client
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json = Mock(return_value={
                "en": ["thesis", "article"],
                "zh": ["论文", "模板"]
            })
            
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.get.return_value = mock_response
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                response = await client.get_templates()
                
                assert isinstance(response, TemplatesResponse)
                assert response.templates["en"] == ["thesis", "article"]
                assert response.templates["zh"] == ["论文", "模板"]
    
    @pytest.mark.asyncio
    async def test_get_templates_api_error(self):
        """Test template retrieval with API error."""
        with patch.dict(os.environ, {"DEEP_SHARE_API_KEY": "test-key"}):
            client = ConversionAPIClient()
            
            # Mock httpx client
            mock_response = AsyncMock()
            mock_response.status_code = 500
            
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client.get.return_value = mock_response
            
            with patch('httpx.AsyncClient', return_value=mock_client):
                response = await client.get_templates()
                
                assert isinstance(response, TemplatesResponse)
                assert response.templates == {}
    
    def test_ensure_unique_filename(self):
        """Test unique filename generation."""
        with patch.dict(os.environ, {"DEEP_SHARE_API_KEY": "test-key"}):
            client = ConversionAPIClient()
            
            # Test when file doesn't exist
            with patch('os.path.exists', return_value=False):
                result = client._ensure_unique_filename("/tmp/test.docx")
                assert result == "/tmp/test.docx"
            
            # Test when file exists
            with patch('os.path.exists', side_effect=[True, False]):
                result = client._ensure_unique_filename("/tmp/test.docx")
                assert result == "/tmp/test_1.docx"
            
            # Test when multiple files exist
            with patch('os.path.exists', side_effect=[True, True, False]):
                result = client._ensure_unique_filename("/tmp/test.docx")
                assert result == "/tmp/test_2.docx" 