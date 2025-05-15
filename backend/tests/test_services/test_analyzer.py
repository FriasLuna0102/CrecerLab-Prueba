import pytest
from app.services.analyzer import TextAnalyzer
from app.schemas.article import WordFrequency, SentimentAnalysis, Entity


@pytest.fixture
def analyzer():
    return TextAnalyzer()


def test_analyze_text(analyzer):
    """Prueba el análisis completo de texto"""
    sample_text = """
    Python is a programming language. Python is widely used for web development, 
    data analysis, artificial intelligence, and scientific computing. 
    Many developers love Python because of its simplicity and readability.
    """

    analysis = analyzer.analyze_text(sample_text)

    assert analysis.word_count > 20, "El conteo de palabras debe ser mayor que 20"

    assert len(analysis.frequent_words) > 0, "Debe haber palabras frecuentes identificadas"
    python_found = any(wf.word.lower() == "python" for wf in analysis.frequent_words)
    assert python_found, "Python debería estar entre las palabras frecuentes"

    for word_freq in analysis.frequent_words:
        assert isinstance(word_freq, WordFrequency)
        assert word_freq.word is not None
        assert word_freq.count > 0


def test_count_words(analyzer):
    """Prueba el conteo de palabras"""
    text = "Esto es una prueba de conteo de palabras."
    count = analyzer.count_words(text)
    assert count == 8, f"Esperaba 8 palabras, pero obtuve {count}"

def test_get_frequent_words(analyzer):
    """Prueba la extracción de palabras frecuentes"""
    text = """
    Python python PYTHON Python. 
    Test test testing tests.
    Word word words wording.
    """

    frequent_words = analyzer.get_frequent_words(text, top_n=3)

    assert len(frequent_words) <= 3, f"Debería devolver como máximo 3 palabras, devolvió {len(frequent_words)}"
    assert all(isinstance(wf, WordFrequency) for wf in
               frequent_words), "Todos los elementos deben ser instancias de WordFrequency"

    assert frequent_words[
               0].word.lower() == "python", f"La palabra más frecuente debería ser 'python', fue '{frequent_words[0].word}'"
    assert frequent_words[0].count == 4, f"La frecuencia de 'python' debería ser 4, fue {frequent_words[0].count}"


def test_analyze_sentiment(analyzer):
    """Prueba el análisis de sentimiento"""
    positive_text = "I love this product! It's amazing and wonderful."
    positive_sentiment = analyzer.analyze_sentiment(positive_text)

    assert isinstance(positive_sentiment, SentimentAnalysis)
    assert positive_sentiment.label == "Positive", f"El texto positivo fue clasificado como {positive_sentiment.label}"
    assert positive_sentiment.positive > 0.5, f"La puntuación positiva debería ser > 0.5, fue {positive_sentiment.positive}"

    negative_text = "I hate this product. It's terrible and disappointing."
    negative_sentiment = analyzer.analyze_sentiment(negative_text)

    assert isinstance(negative_sentiment, SentimentAnalysis)
    assert negative_sentiment.label == "Negative", f"El texto negativo fue clasificado como {negative_sentiment.label}"
    assert negative_sentiment.negative > 0.5, f"La puntuación negativa debería ser > 0.5, fue {negative_sentiment.negative}"


def test_extract_entities(analyzer):
    """Prueba la extracción de entidades"""
    text = "Barack Obama was the president of the United States. He visited New York in January 2015."
    entities = analyzer.extract_entities(text)

    assert len(entities) > 0, "Deberían identificarse entidades"

    for entity in entities:
        assert isinstance(entity, Entity)
        assert entity.text is not None
        assert entity.type is not None
        assert entity.start >= 0
        assert entity.end > entity.start

    person_found = any(entity.type in ["PERSON", "PER"] for entity in entities)
    assert person_found, "Debería detectarse al menos una persona"

    location_found = any(entity.type in ["GPE", "LOC", "LOCATION"] for entity in entities)
    assert location_found, "Debería detectarse al menos una ubicación"

    date_found = any(entity.type in ["DATE", "TIME"] for entity in entities)
    assert date_found, "Debería detectarse al menos una fecha"