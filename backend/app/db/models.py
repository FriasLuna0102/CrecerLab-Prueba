from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class SavedArticle(Base):
    """Modelo para artículos guardados por el usuario"""

    __tablename__ = "saved_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    wikipedia_id = Column(String(100), nullable=False)
    wikipedia_url = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)
    full_text = Column(Text, nullable=True)
    word_count = Column(Integer, nullable=True)
    frequent_words = Column(Text, nullable=True)
    personal_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user_id = Column(String(50), nullable=False, index=True)

    class Config:
        orm_mode = True