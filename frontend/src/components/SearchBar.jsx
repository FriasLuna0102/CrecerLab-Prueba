import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import useDebounce from '../hooks/useDebounce';

function SearchBar({ onSearch, initialSearchTerm = '' }) {
  const { t } = useTranslation();
  const [searchTerm, setSearchTerm] = useState(initialSearchTerm);

  // Usar debounce para no hacer búsquedas con cada pulsación de tecla
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(() => {
    if (debouncedSearchTerm && debouncedSearchTerm.trim() !== '') {
      onSearch(debouncedSearchTerm);
    }
  }, [debouncedSearchTerm, onSearch]);

  useEffect(() => {
    if (initialSearchTerm !== searchTerm) {
      setSearchTerm(initialSearchTerm);
    }
  }, [initialSearchTerm]);

  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm);
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="search-input"
        placeholder={t('searchWikipedia')}
        value={searchTerm}
        onChange={handleInputChange}
      />
      <button type="submit" className="search-button">
        {t('search')}
      </button>
    </form>
  );
}

export default SearchBar;