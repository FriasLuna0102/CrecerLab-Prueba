import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { saveArticle } from '../services/api';
import PersonalNotesEditor from './PersonalNotesEditor';
import WordFrequencyChart from './WordFrequencyChart';

function ArticleDetail({ article, analysis, onSave, onUpdate }) {
  const { t } = useTranslation();
  const [isSaving, setIsSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);
  const [saved, setSaved] = useState(false);
  const [chartType, setChartType] = useState('bar');

  const handleSaveArticle = async () => {
    if (saved || article.id > 0) {
      return;
    }

    setIsSaving(true);
    setSaveError(null);

    try {
      const articleToSave = {
        title: article.title,
        wikipedia_id: article.wikipedia_id,
        wikipedia_url: article.wikipedia_url,
        summary: article.summary,
        word_count: analysis.word_count,
        frequent_words: analysis.frequent_words
      };

      await saveArticle(articleToSave);
      setSaved(true);
      if (onSave) onSave();
    } catch (error) {
      console.error('Error saving article:', error);
      setSaveError(error.response?.data?.detail || 'Could not save article');
    } finally {
      setIsSaving(false);
    }
  };

  const handleArticleUpdate = (updatedArticle) => {
    if (onUpdate) {
      onUpdate(updatedArticle);
    }
  };

  const handleChartTypeChange = (type) => {
    setChartType(type);
  };

  if (!article || !analysis) {
    return <div className="loading">{t('loading')}</div>;
  }

  return (
    <div className="article-detail">
      <h1 className="article-title">{article.title}</h1>

      <div className="article-actions">
        <a
          href={article.wikipedia_url}
          target="_blank"
          rel="noopener noreferrer"
          className="wiki-link"
        >
          {t('articleDetail.viewOnWikipedia')}
        </a>
        <button
          onClick={handleSaveArticle}
          disabled={isSaving || saved || article.id > 0}
          className={`save-button ${saved || article.id > 0 ? 'saved' : ''}`}
        >
          {isSaving
            ? t('articleDetail.saving')
            : saved || article.id > 0
              ? t('articleDetail.saved')
              : t('articleDetail.saveArticle')}
        </button>
      </div>

      {saveError && <div className="error">{saveError}</div>}

      <div className="article-meta">
        <div className="word-count">
          <strong>{t('articleDetail.wordCount')}:</strong> {analysis.word_count}
        </div>
      </div>

      <div className="article-section">
        <h2>{t('articleDetail.summary')}</h2>
        <div className="article-summary">
          {article.summary || t('articleDetail.noSummary')}
        </div>
      </div>

      {/* Add personal notes editor only if article is saved */}
      {article.id > 0 && (
        <div className="article-section">
          <PersonalNotesEditor
            article={article}
            onUpdate={handleArticleUpdate}
          />
        </div>
      )}

      <div className="article-section">
        <h2>{t('articleDetail.contentAnalysis')}</h2>

        {/* Add the new WordFrequencyChart component */}
        <div className="frequency-visualization">
          <WordFrequencyChart
            frequentWords={analysis.frequent_words}
            chartType={chartType}
            onChartTypeChange={handleChartTypeChange}
          />
        </div>

        <div className="frequent-words">
          <h3>{t('articleDetail.mostCommonWords')}</h3>
          <ul className="word-list">
            {analysis.frequent_words.map((item, index) => (
              <li key={index} className="word-item">
                <span className="word">{item.word}</span>
                <span className="count">{item.count}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Sentiment analysis section */}
        {analysis.sentiment && (
          <div className="sentiment-analysis">
            <h3>{t('articleDetail.sentimentAnalysis')}</h3>
            <div className="sentiment-score">
              <div className="sentiment-label">{t('articleDetail.overallSentiment')}:</div>
              <div className={`sentiment-value ${analysis.sentiment.label.toLowerCase()}`}>
                {analysis.sentiment.label}
              </div>
            </div>
            <div className="sentiment-chart">
              <div className="sentiment-bar-container">
                <div
                  className="sentiment-bar"
                  style={{ width: `${analysis.sentiment.positive * 100}%` }}
                >
                  <span className="sentiment-label">
                    {t('articleDetail.positive', { value: (analysis.sentiment.positive * 100).toFixed(1) })}
                  </span>
                </div>
              </div>
              <div className="sentiment-bar-container">
                <div
                  className="sentiment-bar negative"
                  style={{ width: `${analysis.sentiment.negative * 100}%` }}
                >
                  <span className="sentiment-label">
                    {t('articleDetail.negative', { value: (analysis.sentiment.negative * 100).toFixed(1) })}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Entity recognition section */}
        {analysis.entities && analysis.entities.length > 0 && (
          <div className="entity-recognition">
            <h3>{t('articleDetail.entityRecognition')}</h3>
            <ul className="entity-list">
              {analysis.entities.map((entity, index) => (
                <li key={index} className="entity-item">
                  <span className={`entity-type ${entity.type.toLowerCase()}`}>{entity.type}</span>
                  <span className="entity-name">{entity.text}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ArticleDetail;