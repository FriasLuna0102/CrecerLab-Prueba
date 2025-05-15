import requests
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.schemas.article import WikiSearchResult, WikiSearchResponse


class WikipediaService:
    """Servicio para interactuar con la API de Wikipedia"""

    def __init__(self, api_url: str = None):
        self.api_url = api_url or settings.WIKIPEDIA_API_URL

    def search_articles(self, query: str, limit: int = 10) -> WikiSearchResponse:
        """
        Busca artículos en Wikipedia basados en el término de búsqueda

        Args:
            query: Término de búsqueda
            limit: Número máximo de resultados a devolver

        Returns:
            WikiSearchResponse: Los resultados de la búsqueda
        """
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "srinfo": "totalhits",
            "srprop": "snippet"
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()  # Lanza excepción si hay error HTTP

        data = response.json()
        search_results = data.get("query", {}).get("search", [])
        total_hits = data.get("query", {}).get("searchinfo", {}).get("totalhits", 0)

        results = []
        for item in search_results:
            page_id = item.get("pageid")
            title = item.get("title")

            # Construir URL del artículo
            article_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

            result = WikiSearchResult(
                page_id=page_id,
                title=title,
                snippet=item.get("snippet", ""),
                url=article_url
            )
            results.append(result)

        return WikiSearchResponse(results=results, total=total_hits)

    def get_article_content(self, page_id: int) -> Dict[str, Any]:
        """
        Obtiene el contenido completo de un artículo de Wikipedia

        Args:
            page_id: ID de la página en Wikipedia

        Returns:
            Dict con la información del artículo
        """
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "pageids": page_id,
            "inprop": "url",
            "explaintext": True,  # Obtener texto plano
            "exintro": False  # Obtener el artículo completo
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()

        data = response.json()
        page_data = data.get("query", {}).get("pages", {}).get(str(page_id), {})

        return {
            "page_id": page_id,
            "title": page_data.get("title", ""),
            "content": page_data.get("extract", ""),
            "url": page_data.get("fullurl", f"https://en.wikipedia.org/?curid={page_id}")
        }

    def get_article_summary(self, page_id: int) -> Dict[str, Any]:
        """
        Obtiene solo el resumen (introducción) de un artículo de Wikipedia

        Args:
            page_id: ID de la página en Wikipedia

        Returns:
            Dict con el resumen del artículo
        """
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "pageids": page_id,
            "inprop": "url",
            "explaintext": True,  # Obtener texto plano
            "exintro": True  # Solo obtener la introducción
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()

        data = response.json()
        page_data = data.get("query", {}).get("pages", {}).get(str(page_id), {})

        return {
            "page_id": page_id,
            "title": page_data.get("title", ""),
            "summary": page_data.get("extract", ""),
            "url": page_data.get("fullurl", f"https://en.wikipedia.org/?curid={page_id}")
        }