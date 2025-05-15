from typing import List
import re
import nltk
from collections import Counter
from app.schemas.article import WordFrequency, ArticleAnalysis, SentimentAnalysis, Entity
from textblob import TextBlob
import spacy

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords

try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess

    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


class TextAnalyzer:
    """Servicio para analizar textos"""

    def __init__(self, language: str = "english"):
        self.stop_words = set(stopwords.words(language))

    def count_words(self, text: str) -> int:
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)

    def get_frequent_words(self, text: str, top_n: int = 10) -> List[WordFrequency]:
        words = re.findall(r'\b\w+\b', text.lower())

        # Filtrar stop words
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]

        word_counts = Counter(filtered_words)

        most_common = word_counts.most_common(top_n)

        return [WordFrequency(word=word, count=count) for word, count in most_common]

    def analyze_sentiment(self, text: str) -> SentimentAnalysis:
        blob = TextBlob(text)

        polarity = blob.sentiment.polarity

        # Convertir polaridad a etiquetas
        if polarity > 0.1:
            label = "Positive"
            positive = 0.5 + polarity / 2
            negative = 0.5 - polarity / 2
            neutral = 0.5 - abs(polarity) / 2
        elif polarity < -0.1:
            label = "Negative"
            positive = 0.5 + polarity / 2
            negative = 0.5 - polarity / 2
            neutral = 0.5 - abs(polarity) / 2
        else:
            label = "Neutral"
            positive = 0.5 + polarity
            negative = 0.5 - polarity
            neutral = 0.8

        return SentimentAnalysis(
            label=label,
            positive=positive,
            negative=negative,
            neutral=neutral
        )

    def extract_entities(self, text: str, max_entities: int = 20) -> List[Entity]:
        # Limitar a 50k caracteres para rendimiento
        doc = nlp(text[:50000])

        entities = []
        for ent in doc.ents:
            entity = Entity(
                text=ent.text,
                type=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            )
            entities.append(entity)

        return entities[:max_entities]

    def analyze_text(self, text: str, top_n: int = 10) -> ArticleAnalysis:
        word_count = self.count_words(text)
        frequent_words = self.get_frequent_words(text, top_n)
        sentiment = self.analyze_sentiment(text)
        entities = self.extract_entities(text)

        return ArticleAnalysis(
            word_count=word_count,
            frequent_words=frequent_words,
            sentiment=sentiment,
            entities=entities
        )