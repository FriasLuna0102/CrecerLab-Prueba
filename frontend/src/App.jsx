import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './components/HomePageWIki.jsx';
import DetailPage from './components/DetailPageWiki';
import SavedPage from './components/SavedPageWiki';
import './App.css';

function App() {
  return (
      <div className="app">
        <Header />
        <main className="container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/article/:pageId" element={<DetailPage />} />
            <Route path="/saved" element={<SavedPage />} />
          </Routes>
        </main>
      </div>
  );
}

export default App;