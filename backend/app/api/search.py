from fastapi import APIRouter, HTTPException, Query
from app.services.wiki_service import WikipediaService
from app.schemas.article import WikiSearchResponse
import logging

router = APIRouter(
    prefix="/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}}
)

logger = logging.getLogger(__name__)

@router.get("/", response_model=WikiSearchResponse)
async def search_wikipedia(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados")
):
    """
    Busca artículos en Wikipedia basados en el término de búsqueda
    """
    try:
        wiki_service = WikipediaService()
        search_response = wiki_service.search_articles(query=q, limit=limit)
        return search_response
    except Exception as e:
        logger.error(f"Error al buscar en Wikipedia: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al buscar en Wikipedia: {str(e)}")