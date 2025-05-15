import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import ArticleDetail from '../components/ArticleDetail';
import { getArticleDetails } from '../services/api';

function DetailPageWiki() {
  const { t } = useTranslation();
  const { pageId } = useParams();
  const navigate = useNavigate();
  const [articleData, setArticleData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArticleDetails = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const data = await getArticleDetails(pageId);
        setArticleData(data);
      } catch (err) {
        console.error('Error fetching article details:', err);
        setError(err.response?.data?.detail || 'Failed to load article details');
      } finally {
        setIsLoading(false);
      }
    };

    if (pageId) {
      fetchArticleDetails();
    }
  }, [pageId]);

  const handleArticleUpdate = (updatedArticle) => {
    console.log("Article updated in DetailPage:", updatedArticle);

    setArticleData(prevData => {
      console.log("Updating state from:", prevData);
      const newData = {
        ...prevData,
        article: updatedArticle
      };
      console.log("New state will be:", newData);
      return newData;
    });
  };

  const handleSaveSuccess = () => {
  };

  const handleBackClick = () => {
    navigate(-1);
  };

  if (isLoading) {
    return <div className="loading">{t('loading')}</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error">{t('error', { message: error })}</div>
        <button onClick={handleBackClick} className="back-button">
          {t('navigation.back')}
        </button>
      </div>
    );
  }

  return (
    <div className="detail-page">
      <button onClick={handleBackClick} className="back-button">
        &larr; {t('navigation.back')}
      </button>

      {articleData && (
        <ArticleDetail
          article={articleData.article}
          analysis={articleData.analysis}
          onSave={handleSaveSuccess}
          onUpdate={handleArticleUpdate}
        />
      )}
    </div>
  );
}

export default DetailPageWiki;