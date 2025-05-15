from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import ConfigDict

T = TypeVar('T')

class ArticleBase(BaseModel):
    title: str
    wikipedia_id: str
    wikipedia_url: str
    summary: Optional[str] = None

class SavedArticleCreate(ArticleBase):
    full_text: Optional[str] = None
    word_count: Optional[int] = None
    frequent_words: Optional[List[dict]] = None
    user_id: str = "default_user"

class SavedArticleUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    personal_notes: Optional[str] = None

class SavedArticleInDB(ArticleBase):
    id: int
    word_count: Optional[int] = None
    frequent_words: Optional[List[dict]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    personal_notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WordFrequency(BaseModel):
    word: str
    count: int

class SentimentAnalysis(BaseModel):
    label: str
    positive: float
    negative: float
    neutral: float

class Entity(BaseModel):
    text: str
    type: str
    start: int
    end: int

class ArticleAnalysis(BaseModel):
    word_count: int
    frequent_words: List[WordFrequency] = Field(..., max_length=10)
    sentiment: Optional[SentimentAnalysis] = None
    entities: Optional[List[Entity]] = None

class WikiSearchResult(BaseModel):
    page_id: int
    title: str
    snippet: Optional[str] = None
    url: Optional[str] = None

class WikiSearchResponse(BaseModel):
    results: List[WikiSearchResult]
    total: int

class ArticleDetailResponse(BaseModel):
    article: SavedArticleInDB
    analysis: ArticleAnalysis

class PaginatedResponse(Generic[T]):
    items: List[T]
    total: int