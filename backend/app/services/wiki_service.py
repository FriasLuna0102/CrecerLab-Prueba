import requests
from typing import Dict, Any, Optional
from app.core.config import settings
from app.schemas.article import WikiSearchResult, WikiSearchResponse
import logging

logger = logging.getLogger(__name__)


class WikipediaService:
    def __init__(self, api_url: Optional[str] = None):
        self.api_url = api_url or settings.WIKIPEDIA_API_URL

    def search_articles(self, query: str, limit: int = 10) -> WikiSearchResponse:
        logger.info(f"Buscando artículos con término: {query}")

        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
            "srinfo": "totalhits",
            "srprop": "snippet"
        }

        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()

            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            total_hits = data.get("query", {}).get("searchinfo", {}).get("totalhits", 0)

            results = []
            for item in search_results:
                page_id = item.get("pageid")
                title = item.get("title")
                article_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

                result = WikiSearchResult(
                    page_id=page_id,
                    title=title,
                    snippet=item.get("snippet", ""),
                    url=article_url
                )
                results.append(result)

            return WikiSearchResponse(results=results, total=total_hits)

        except requests.RequestException as e:
            logger.error(f"Error en la solicitud a Wikipedia API: {str(e)}")
            raise Exception(f"Error al conectar con Wikipedia: {str(e)}")
        except Exception as e:
            logger.error(f"Error al procesar resultados de Wikipedia: {str(e)}")
            raise

    def get_article_content(self, page_id: int) -> Dict[str, Any]:
        """
        Obtiene el contenido completo de un artículo de Wikipedia
        """
        logger.info(f"Obteniendo contenido completo del artículo con ID: {page_id}")

        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "pageids": page_id,
            "inprop": "url",
            "explaintext": True,
            "exintro": False
        }

        try:
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
        except requests.RequestException as e:
            logger.error(f"Error en la solicitud a Wikipedia API: {str(e)}")
            raise Exception(f"Error al conectar con Wikipedia: {str(e)}")
        except Exception as e:
            logger.error(f"Error al procesar contenido de Wikipedia: {str(e)}")
            raise

    def get_article_summary(self, page_id: int) -> Dict[str, Any]:
        """
        Obtiene solo el resumen (introducción) de un artículo de Wikipedia
        """
        logger.info(f"Obteniendo resumen del artículo con ID: {page_id}")

        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|info",
            "pageids": page_id,
            "inprop": "url",
            "explaintext": True,
            "exintro": True
        }

        try:
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
        except requests.RequestException as e:
            logger.error(f"Error en la solicitud a Wikipedia API: {str(e)}")
            raise Exception(f"Error al conectar con Wikipedia: {str(e)}")
        except Exception as e:
            logger.error(f"Error al procesar resumen de Wikipedia: {str(e)}")
            raise