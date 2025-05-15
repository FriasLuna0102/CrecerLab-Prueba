from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.wiki_service import WikipediaService
from app.schemas.article import WikiSearchResponse

router = APIRouter()

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
        raise HTTPException(status_code=500, detail=f"Error al buscar en Wikipedia: {str(e)}")