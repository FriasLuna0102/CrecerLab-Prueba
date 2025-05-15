import { Link } from 'react-router-dom';
import React from 'react';
import { useTranslation } from 'react-i18next';

function SearchResults({ results, isLoading, error }) {
  const { t } = useTranslation();

  if (isLoading) {
    return <div className="loading">{t('searching')}</div>;
  }

  if (error) {
    return <div className="error">{t('error', { message: error.message })}</div>;
  }

  if (!results || results.length === 0) {
    return <div className="no-results">{t('noResults')}</div>;
  }

  const cleanHtml = (html) => {
    const doc = new DOMParser().parseFromString(html, 'text/html');
    return doc.body.textContent || "";
  };

  return (
    <div className="search-results">
      <h2>{t('searchResults')}</h2>
      <div className="results-count">{t('foundArticles', { count: results.total })}</div>
      <ul className="results-list">
        {results.results.map((article) => (
          <li key={article.page_id} className="result-item">
            <Link to={`/article/${article.page_id}`} className="result-link">
              <h3 className="result-title">{article.title}</h3>
              <p className="result-snippet">
                {cleanHtml(article.snippet || t('articleDetail.noSummary'))}...
              </p>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchResults;