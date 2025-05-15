import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import ArticleCard from './ArticleCard';
import { getSavedArticles } from '../services/api';

function SavedArticles() {
  const { t } = useTranslation();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1); // Comenzar en página 1 (más intuitivo para usuarios)
  const [totalArticles, setTotalArticles] = useState(0);
  const articlesPerPage = 6;

  const totalPages = Math.ceil(totalArticles / articlesPerPage);

  const loadArticles = async (page = 1) => {
    try {
      setLoading(true);
      setError(null);

      const skip = (page - 1) * articlesPerPage;

      const response = await getSavedArticles(skip, articlesPerPage);

      setArticles(response.items);
      setTotalArticles(response.total);

    } catch (err) {
      setError(t('error', { message: 'Failed to load saved articles' }));
      console.error('API error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadArticles(currentPage);
  }, [currentPage]);

  const handleDeleteArticle = (deletedId) => {
    setArticles(prev => prev.filter(article => article.id !== deletedId));

    if (articles.length === 1 && currentPage > 1) {
      setCurrentPage(prev => prev - 1);
    } else {
      loadArticles(currentPage);
    }
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);

      window.scrollTo({ top: document.querySelector('.saved-articles').offsetTop - 80, behavior: 'smooth' });
    }
  };

  const getPageNumbers = () => {
    let pages = [];

    pages.push(1);

    for (let i = Math.max(2, currentPage - 1); i <= Math.min(totalPages - 1, currentPage + 1); i++) {
      if (i === 2 && currentPage > 3) {
        pages.push('...');
      } else if (i === totalPages - 1 && currentPage < totalPages - 2) {
        pages.push('...');
      } else {
        pages.push(i);
      }
    }

    if (totalPages > 1) {
      pages.push(totalPages);
    }

    return [...new Set(pages)];
  };

  if (loading && articles.length === 0) {
    return <div className="loading">{t('loading')}</div>;
  }

  if (error && articles.length === 0) {
    return (
      <div className="error-container">
        <div className="error">{error}</div>
        <button onClick={() => loadArticles(currentPage)} className="retry-button">
          {t('tryAgain')}
        </button>
      </div>
    );
  }

  if (articles.length === 0 && !loading) {
    return (
      <div className="no-saved-articles">
        <h2>{t('savedPage.noSavedArticles')}</h2>
        <p>{t('savedPage.noSavedArticlesDesc')}</p>
      </div>
    );
  }

  return (
    <div className="saved-articles">
      <h2>{t('savedArticles')}</h2>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => loadArticles(currentPage)} className="retry-button">
            {t('reload')}
          </button>
        </div>
      )}

      <div className="articles-grid">
        {articles.map(article => (
          <ArticleCard
            key={article.id}
            article={article}
            onDelete={handleDeleteArticle}
          />
        ))}
      </div>

      {/* Paginación numérica */}
      {totalPages > 1 && (
        <div className="pagination">
          <button
            className="pagination-button prev"
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1 || loading}
            aria-label={t('savedPage.prev')}
          >
            &laquo; {t('savedPage.prev')}
          </button>

          <div className="page-numbers">
            {getPageNumbers().map((page, index) => (
              page === '...' ? (
                <span key={`ellipsis-${index}`} className="ellipsis">...</span>
              ) : (
                <button
                  key={`page-${page}`}
                  className={`page-number ${currentPage === page ? 'active' : ''}`}
                  onClick={() => handlePageChange(page)}
                  disabled={loading}
                >
                  {page}
                </button>
              )
            ))}
          </div>

          <button
            className="pagination-button next"
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages || loading}
            aria-label={t('savedPage.next')}
          >
            {t('savedPage.next')} &raquo;
          </button>
        </div>
      )}

      {/* Información de paginación */}
      <div className="pagination-info">
        {loading ? (
          <span>{t('loading')}</span>
        ) : (
          <span>
            {t('savedPage.showing', { shown: articles.length, total: totalArticles })}
            {totalPages > 1 ? ` (${t('savedPage.page', { current: currentPage, total: totalPages })})` : ''}
          </span>
        )}
      </div>
    </div>
  );
}

export default SavedArticles;