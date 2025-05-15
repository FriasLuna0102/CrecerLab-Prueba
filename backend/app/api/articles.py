from fastapi import APIRouter, Depends, HTTPException, Path, Query, Body
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.wiki_service import WikipediaService
from app.services.analyzer import TextAnalyzer
from app.schemas.article import (
    SavedArticleCreate,
    SavedArticleInDB,
    SavedArticleUpdate,
    ArticleDetailResponse,
    ArticleAnalysis
)
from app.db.models import SavedArticle
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime as dt


router = APIRouter()

DEFAULT_USER_ID = "default_user"


@router.get("/detail/{page_id}", response_model=ArticleDetailResponse)
async def get_article_detail(
        page_id: int = Path(..., description="ID de la página en Wikipedia"),
        db: Session = Depends(get_db)
):
    """
    Obtiene los detalles y análisis de un artículo de Wikipedia
    """
    try:
        wiki_service = WikipediaService()
        text_analyzer = TextAnalyzer()

        article_data = wiki_service.get_article_content(page_id)

        content = article_data.get("content", "")
        analysis = text_analyzer.analyze_text(content)

        db_article = db.query(SavedArticle).filter(
            SavedArticle.wikipedia_id == str(page_id),
            SavedArticle.user_id == DEFAULT_USER_ID
        ).first()

        if db_article:
            article = SavedArticleInDB(
                id=db_article.id,
                title=db_article.title,
                wikipedia_id=db_article.wikipedia_id,
                wikipedia_url=db_article.wikipedia_url,
                summary=db_article.summary,
                personal_notes=db_article.personal_notes,
                word_count=db_article.word_count,
                frequent_words=eval(db_article.frequent_words) if db_article.frequent_words else None,
                created_at=db_article.created_at,
                updated_at=db_article.updated_at
            )
        else:
            summary_data = wiki_service.get_article_summary(page_id)

            article = SavedArticleInDB(
                id=-1,
                title=article_data.get("title", ""),
                wikipedia_id=str(page_id),
                wikipedia_url=article_data.get("url", ""),
                summary=summary_data.get("summary", ""),
                word_count=analysis.word_count,
                frequent_words=[{"word": wf.word, "count": wf.count} for wf in analysis.frequent_words],
                created_at=dt.now(),
                updated_at=dt.now()
            )

        return ArticleDetailResponse(article=article, analysis=analysis)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalles del artículo: {str(e)}")


@router.post("/", response_model=SavedArticleInDB)
async def save_article(
        article: SavedArticleCreate = Body(...),
        db: Session = Depends(get_db)
):
    """
    Guarda un artículo en la base de datos
    """
    try:
        db_article = db.query(SavedArticle).filter(
            SavedArticle.wikipedia_id == article.wikipedia_id,
            SavedArticle.user_id == article.user_id
        ).first()

        if db_article:
            raise HTTPException(status_code=400, detail="El artículo ya está guardado")

        frequent_words_str = str(
            [{"word": wf.word, "count": wf.count} for wf in article.frequent_words]) if article.frequent_words else None

        db_article = SavedArticle(
            title=article.title,
            wikipedia_id=article.wikipedia_id,
            wikipedia_url=article.wikipedia_url,
            summary=article.summary,
            full_text=article.full_text,
            word_count=article.word_count,
            frequent_words=frequent_words_str,
            user_id=article.user_id
        )

        db.add(db_article)
        db.commit()
        db.refresh(db_article)

        frequent_words = eval(db_article.frequent_words) if db_article.frequent_words else None

        return SavedArticleInDB(
            id=db_article.id,
            title=db_article.title,
            wikipedia_id=db_article.wikipedia_id,
            wikipedia_url=db_article.wikipedia_url,
            summary=db_article.summary,
            word_count=db_article.word_count,
            frequent_words=frequent_words,
            created_at=db_article.created_at,
            updated_at=db_article.updated_at
        )

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el artículo: {str(e)}")


@router.get("/", response_model=Dict[str, Any])
async def get_saved_articles(
        skip: int = Query(0, ge=0, description="Número de artículos para saltar (paginación)"),
        limit: int = Query(100, ge=1, le=100, description="Número máximo de artículos a devolver"),
        db: Session = Depends(get_db)
):
    """
    Obtiene la lista de artículos guardados con el conteo total
    """
    try:
        total_count = db.query(SavedArticle).filter(
            SavedArticle.user_id == DEFAULT_USER_ID
        ).count()

        db_articles = db.query(SavedArticle).filter(
            SavedArticle.user_id == DEFAULT_USER_ID
        ).offset(skip).limit(limit).all()

        articles = []
        for db_article in db_articles:
            frequent_words = eval(db_article.frequent_words) if db_article.frequent_words else None

            article = SavedArticleInDB(
                id=db_article.id,
                title=db_article.title,
                wikipedia_id=db_article.wikipedia_id,
                wikipedia_url=db_article.wikipedia_url,
                summary=db_article.summary,
                personal_notes=db_article.personal_notes,
                word_count=db_article.word_count,
                frequent_words=frequent_words,
                created_at=db_article.created_at,
                updated_at=db_article.updated_at
            )
            articles.append(article)

        return {
            "items": articles,
            "total": total_count
        }

    except Exception as e:
        import traceback
        print(f"Error al obtener artículos guardados: {str(e)}")
        print(traceback.format_exc())

        raise HTTPException(status_code=500, detail=f"Error al obtener artículos guardados: {str(e)}")

@router.patch("/{article_id}", response_model=SavedArticleInDB)
async def update_article(
        article_id: int = Path(..., description="ID del artículo guardado"),
        article_update: SavedArticleUpdate = Body(...),
        db: Session = Depends(get_db)
):
    """
    Actualiza un artículo guardado (título, resumen o notas personales)
    """
    try:
        db_article = db.query(SavedArticle).filter(
            SavedArticle.id == article_id,
            SavedArticle.user_id == DEFAULT_USER_ID
        ).first()

        if not db_article:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")

        if article_update.title is not None:
            db_article.title = article_update.title

        if article_update.summary is not None:
            db_article.summary = article_update.summary

        if article_update.personal_notes is not None:
            db_article.personal_notes = article_update.personal_notes

        db.commit()
        db.refresh(db_article)

        frequent_words = eval(db_article.frequent_words) if db_article.frequent_words else None

        return SavedArticleInDB(
            id=db_article.id,
            title=db_article.title,
            wikipedia_id=db_article.wikipedia_id,
            wikipedia_url=db_article.wikipedia_url,
            summary=db_article.summary,
            personal_notes=db_article.personal_notes,
            word_count=db_article.word_count,
            frequent_words=frequent_words,
            created_at=db_article.created_at,
            updated_at=db_article.updated_at
        )

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el artículo: {str(e)}")


@router.delete("/{article_id}", response_model=dict)
async def delete_article(
        article_id: int = Path(..., description="ID del artículo guardado"),
        db: Session = Depends(get_db)
):
    """
    Elimina un artículo guardado
    """
    try:
        db_article = db.query(SavedArticle).filter(
            SavedArticle.id == article_id,
            SavedArticle.user_id == DEFAULT_USER_ID
        ).first()

        if not db_article:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")

        db.delete(db_article)
        db.commit()

        return {"message": "Artículo eliminado correctamente"}

    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el artículo: {str(e)}")