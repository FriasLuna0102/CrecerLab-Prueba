from unittest.mock import patch
from app.schemas.article import ArticleDetailResponse, SavedArticleInDB, ArticleAnalysis
from app.db.models import SavedArticle


def test_get_article_detail(client):
    # Mock para los servicios de Wikipedia y analizador
    with patch("app.services.wiki_service.WikipediaService.get_article_content") as mock_content, \
            patch("app.services.wiki_service.WikipediaService.get_article_summary") as mock_summary, \
            patch("app.services.analyzer.TextAnalyzer.analyze_text") as mock_analyze:
        # Configura las respuestas simuladas
        mock_content.return_value = {
            "page_id": 12345,
            "title": "Test Article",
            "content": "This is test content",
            "url": "https://en.wikipedia.org/wiki/Test_Article"
        }

        mock_summary.return_value = {
            "page_id": 12345,
            "title": "Test Article",
            "summary": "This is a test summary",
            "url": "https://en.wikipedia.org/wiki/Test_Article"
        }

        mock_analyze.return_value = ArticleAnalysis(
            word_count=4,
            frequent_words=[],
            sentiment=None,
            entities=None
        )

        # Realiza la solicitud de prueba
        response = client.get("/api/articles/detail/12345")

        # Verifica la respuesta
        assert response.status_code == 200
        data = response.json()
        assert data["article"]["title"] == "Test Article"
        assert data["analysis"]["word_count"] == 4


def test_save_article(client, test_db):
    # Datos de prueba
    article_data = {
        "title": "Test Article",
        "wikipedia_id": "12345",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Test_Article",
        "summary": "This is a test summary",
        "word_count": 4,
        "frequent_words": [{"word": "test", "count": 2}]
    }

    # Realiza la solicitud de prueba
    response = client.post("/api/articles/", json=article_data)

    # Verifica la respuesta
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Article"
    assert data["wikipedia_id"] == "12345"

    # Verifica que el artículo se guardó en la base de datos
    db_article = test_db.query(SavedArticle).filter(
        SavedArticle.wikipedia_id == "12345"
    ).first()
    assert db_article is not None
    assert db_article.title == "Test Article"