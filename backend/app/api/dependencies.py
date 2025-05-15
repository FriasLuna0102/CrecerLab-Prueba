from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import SavedArticle

async def get_article_or_404(
        article_id: int,
        db: Session = Depends(get_db),
        user_id: str = "default_user"
) -> SavedArticle:
    db_article = db.query(SavedArticle).filter(
        SavedArticle.id == article_id,
        SavedArticle.user_id == user_id
    ).first()

    if db_article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artículo no encontrado"
        )

    return db_article