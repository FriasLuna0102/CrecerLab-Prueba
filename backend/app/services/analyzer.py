from typing import List, Dict, Tuple, Optional
import re
import nltk
from collections import Counter
from app.schemas.article import WordFrequency, ArticleAnalysis, SentimentAnalysis, Entity
from textblob import TextBlob
import spacy

# Descargar recursos necesarios de NLTK
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords

# Cargar modelo de spaCy para reconocimiento de entidades
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess

    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


class TextAnalyzer:
    """Servicio para analizar textos"""

    def __init__(self, language: str = "english"):
        """
        Inicializa el analizador de texto

        Args:
            language: Idioma para las stop words
        """
        self.stop_words = set(stopwords.words(language))

    def count_words(self, text: str) -> int:
        """
        Cuenta el número de palabras en un texto

        Args:
            text: Texto a analizar

        Returns:
            int: Número de palabras
        """
        # Eliminar caracteres especiales y contar palabras
        words = re.findall(r'\b\w+\b', text.lower())
        return len(words)

    def get_frequent_words(self, text: str, top_n: int = 10) -> List[WordFrequency]:
        """
        Obtiene las palabras más frecuentes en un texto, excluyendo stop words

        Args:
            text: Texto a analizar
            top_n: Número de palabras frecuentes a devolver

        Returns:
            List[WordFrequency]: Lista de palabras más frecuentes con sus conteos
        """
        # Limpiar y tokenizar el texto
        words = re.findall(r'\b\w+\b', text.lower())

        # Filtrar stop words
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]

        # Contar frecuencias
        word_counts = Counter(filtered_words)

        # Obtener las más frecuentes
        most_common = word_counts.most_common(top_n)

        # Convertir a lista de WordFrequency
        return [WordFrequency(word=word, count=count) for word, count in most_common]

    def analyze_sentiment(self, text: str) -> SentimentAnalysis:
        """
        Realiza análisis de sentimiento sobre el texto

        Args:
            text: Texto a analizar

        Returns:
            SentimentAnalysis: Análisis de sentimiento del texto
        """
        # Usar TextBlob para análisis de sentimiento
        blob = TextBlob(text)

        # La polaridad va de -1 (muy negativo) a 1 (muy positivo)
        polarity = blob.sentiment.polarity

        # Convertir polaridad a etiquetas
        if polarity > 0.1:
            label = "Positive"
            positive = 0.5 + polarity / 2  # Convertir a rango 0.5-1.0
            negative = 0.5 - polarity / 2  # Convertir a rango 0-0.5
            neutral = 0.5 - abs(polarity) / 2
        elif polarity < -0.1:
            label = "Negative"
            positive = 0.5 + polarity / 2  # Convertir a rango 0-0.5
            negative = 0.5 - polarity / 2  # Convertir a rango 0.5-1.0
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
        """
        Extrae entidades nombradas del texto

        Args:
            text: Texto a analizar
            max_entities: Número máximo de entidades a devolver

        Returns:
            List[Entity]: Lista de entidades encontradas
        """
        # Usar spaCy para reconocimiento de entidades
        doc = nlp(text[:50000])  # Limitar a 50k caracteres para rendimiento

        # Extraer entidades
        entities = []
        for ent in doc.ents:
            entity = Entity(
                text=ent.text,
                type=ent.label_,
                start=ent.start_char,
                end=ent.end_char
            )
            entities.append(entity)

        # Limitar número de entidades y devolver
        return entities[:max_entities]

    def analyze_text(self, text: str, top_n: int = 10) -> ArticleAnalysis:
        """
        Realiza un análisis completo del texto

        Args:
            text: Texto a analizar
            top_n: Número de palabras frecuentes a devolver

        Returns:
            ArticleAnalysis: Análisis completo del texto
        """
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