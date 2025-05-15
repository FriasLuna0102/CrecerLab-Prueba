import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

function LanguageSwitcher() {
  const { i18n } = useTranslation();
  const [selectedLanguage, setSelectedLanguage] = useState(i18n.language);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Español' },
    // Add more languages as needed
  ];

  useEffect(() => {
    setSelectedLanguage(i18n.language);
  }, [i18n.language]);

  const changeLanguage = (event) => {
    const langCode = event.target.value;
    i18n.changeLanguage(langCode);
    setSelectedLanguage(langCode);
  };

  return (
    <select
      value={selectedLanguage}
      onChange={changeLanguage}
      className="language-selector"
      aria-label="Language selector"
    >
      {languages.map((lang) => (
        <option key={lang.code} value={lang.code}>
          {lang.name}
        </option>
      ))}
    </select>
  );
}

export default LanguageSwitcher;