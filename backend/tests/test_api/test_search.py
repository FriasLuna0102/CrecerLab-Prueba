from unittest.mock import patch
from app.schemas.article import WikiSearchResponse, WikiSearchResult


def test_search_endpoint(client):
    # Configura el mock para no hacer llamadas reales a la API de Wikipedia
    with patch("app.services.wiki_service.WikipediaService.search_articles") as mock_search:
        # Configura la respuesta simulada
        mock_response = WikiSearchResponse(
            results=[
                WikiSearchResult(
                    page_id=12345,
                    title="Test Article",
                    snippet="This is a test snippet",
                    url="https://en.wikipedia.org/wiki/Test_Article"
                )
            ],
            total=1
        )
        mock_search.return_value = mock_response

        # Realiza la solicitud de prueba
        response = client.get("/api/search/?q=test")

        # Verifica la respuesta
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Test Article"