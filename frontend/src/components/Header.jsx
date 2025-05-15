import { Link } from 'react-router-dom';
import LanguageSwitcher from './LanguageSwitcher';
import { useTranslation } from 'react-i18next';

function Header() {
  const { t } = useTranslation();

  return (
    <header className="header">
      <div className="container header-content">
        <Link to="/" className="logo">
          {t('appName')}
        </Link>
        <nav className="nav">
          <ul className="nav-list">
            <li className="nav-item">
              <Link to="/" className="nav-link">{t('home')}</Link>
            </li>
            <li className="nav-item">
              <Link to="/saved" className="nav-link">{t('savedArticles')}</Link>
            </li>
            <li className="nav-item">
              <LanguageSwitcher />
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;