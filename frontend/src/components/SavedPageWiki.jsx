import { useTranslation } from 'react-i18next';
import SavedArticles from '../components/SavedArticles';

function SavedPageWiki() {
  const { t } = useTranslation();

  return (
    <div className="saved-page">
      <h1>{t('savedPage.mySavedArticles')}</h1>
      <SavedArticles />
    </div>
  );
}

export default SavedPageWiki;