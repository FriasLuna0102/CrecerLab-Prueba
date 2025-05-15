import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { deleteArticle } from '../services/api';
import ConfirmDialog from './ConfirmDialog';

function ArticleCard({ article, onDelete }) {
  const { t, i18n } = useTranslation();
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState(null);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);

  const handleDeleteClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setShowConfirmDialog(true);
  };

  const handleConfirmDelete = async () => {
    setIsDeleting(true);
    setError(null);

    try {
      await deleteArticle(article.id);
      if (onDelete) onDelete(article.id);
    } catch (err) {
      setError('Failed to delete article');
      console.error('Delete error:', err);
    } finally {
      setIsDeleting(false);
      setShowConfirmDialog(false);
    }
  };

  const handleCancelDelete = () => {
    setShowConfirmDialog(false);
  };

  // Formato de fecha para mejor visualización
  const formatDate = (dateString) => {
    if (!dateString) return t('unknown');
    const date = new Date(dateString);
    return date.toLocaleDateString(i18n.language);
  };

  return (
    <>
      <div className="article-card">
        <div className="card-header">
          <h3 className="card-title">
            <Link to={`/article/${article.wikipedia_id}`}>
              {article.title}
            </Link>
          </h3>
          <button
            onClick={handleDeleteClick}
            disabled={isDeleting}
            className="delete-button"
            aria-label={t('savedPage.delete')}
          >
            {isDeleting ? t('savedPage.deleting') : t('savedPage.delete')}
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        <div className="card-meta">
          <span className="word-count">{t('savedPage.words', { count: article.word_count || 'N/A' })}</span>
          <span className="saved-date">{t('savedPage.saved', { date: formatDate(article.created_at) })}</span>
        </div>

        <p className="card-summary">
          {article.summary
            ? (article.summary.length > 150
                ? `${article.summary.substring(0, 150)}...`
                : article.summary)
            : t('articleDetail.noSummary')}
        </p>

        <div className="card-footer">
          <Link to={`/article/${article.wikipedia_id}`} className="view-link">
            {t('savedPage.viewDetails')}
          </Link>
          <a
            href={article.wikipedia_url}
            target="_blank"
            rel="noopener noreferrer"
            className="wiki-link"
          >
            Wikipedia
          </a>
        </div>
      </div>

      {/* Diálogo de confirmación */}
      <ConfirmDialog
        isOpen={showConfirmDialog}
        title={t('confirmDialog.confirmDeletion')}
        message={t('confirmDialog.areYouSureDelete', { title: article.title })}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        confirmText={t('confirmDialog.delete')}
        cancelText={t('confirmDialog.cancel')}
      />
    </>
  );
}

export default ArticleCard;