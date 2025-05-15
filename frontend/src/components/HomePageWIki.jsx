import { useState, useCallback, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import SearchBar from '../components/SearchBar';
import SearchResults from '../components/SearchResults';
import { searchArticles } from '../services/api';

function HomePageWiki() {
  const { t } = useTranslation();

  const [searchTerm, setSearchTerm] = useState(() => {
    return localStorage.getItem('lastSearchTerm') || '';
  });
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (searchTerm) {
      handleSearch(searchTerm);
    }
  }, []);

  const handleSearch = useCallback(async (term) => {
    if (!term || !term.trim()) {
      setResults(null);
      return;
    }

    localStorage.setItem('lastSearchTerm', term);
    setSearchTerm(term);
    setIsLoading(true);
    setError(null);

    try {
      const data = await searchArticles(term);
      setResults(data);
    } catch (err) {
      console.error('Search error:', err);
      setError(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>{t('heroSection.title')}</h1>
        <p className="subtitle">
          {t('heroSection.subtitle')}
        </p>
        <SearchBar onSearch={handleSearch} initialSearchTerm={searchTerm} />
      </div>

      {(isLoading || results || error) && (
        <div className="results-section">
          <SearchResults
            results={results}
            isLoading={isLoading}
            error={error}
          />
        </div>
      )}
    </div>
  );
}

export default HomePageWiki;