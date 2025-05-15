import pytest
from unittest.mock import patch, MagicMock
import requests
from app.services.wiki_service import WikipediaService


@pytest.fixture
def wiki_service():
    return WikipediaService()


def test_search_articles(wiki_service):
    # Simula una respuesta JSON de la API de Wikipedia
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "query": {
            "search": [
                {
                    "pageid": 12345,
                    "title": "Test Article",
                    "snippet": "This is a test snippet"
                }
            ],
            "searchinfo": {
                "totalhits": 1
            }
        }
    }

    with patch.object(requests, "get", return_value=mock_response):
        result = wiki_service.search_articles("test")

        assert result.total == 1
        assert len(result.results) == 1
        assert result.results[0].page_id == 12345
        assert result.results[0].title == "Test Article"


def test_get_article_content(wiki_service):
    # Simula una respuesta JSON de la API de Wikipedia
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "query": {
            "pages": {
                "12345": {
                    "title": "Test Article",
                    "extract": "This is test content",
                    "fullurl": "https://en.wikipedia.org/wiki/Test_Article"
                }
            }
        }
    }

    with patch.object(requests, "get", return_value=mock_response):
        result = wiki_service.get_article_content(12345)

        assert result["page_id"] == 12345
        assert result["title"] == "Test Article"
        assert result["content"] == "This is test content"