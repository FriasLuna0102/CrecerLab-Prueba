import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { updateArticle } from '../services/api';

function PersonalNotesEditor({ article, onUpdate }) {
  const { t } = useTranslation();
  const [notes, setNotes] = useState(article.personal_notes || '');
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);

  console.log("Article in editor:", article); // Debug log
  console.log("Personal notes in editor:", article.personal_notes); // Debug log

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setNotes(article.personal_notes || '');
    setIsEditing(false);
    setError(null);
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      setError(null);

      console.log("Saving notes:", notes);

      const updatedArticle = await updateArticle(article.id, {
        personal_notes: notes
      });

      console.log("Received updated article:", updatedArticle);

      if (onUpdate) {
        console.log("Calling onUpdate with:", updatedArticle);
        onUpdate(updatedArticle);
      }

      setIsEditing(false);
    } catch (err) {
      setError(t('error', { message: 'Failed to save notes. Please try again.' }));
      console.error('Error saving notes:', err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="personal-notes">
      <h3 className="notes-title">{t('notes.personalNotes')}</h3>

      {isEditing ? (
        <div className="notes-editor">
          <textarea
            className="notes-textarea"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder={t('notes.addNotes')}
            rows={5}
          />

          {error && <div className="error">{error}</div>}

          <div className="notes-actions">
            <button
              className="cancel-button"
              onClick={handleCancel}
              disabled={isSaving}
            >
              {t('notes.cancel')}
            </button>
            <button
              className="save-button"
              onClick={handleSave}
              disabled={isSaving}
            >
              {isSaving ? t('notes.savingNotes') : t('notes.saveNotes')}
            </button>
          </div>
        </div>
      ) : (
        <div className="notes-display">
          {article.personal_notes ? (
            <div className="notes-content">
              {article.personal_notes.split('\n').map((line, i) => (
                <p key={i}>{line || ' '}</p>
              ))}
            </div>
          ) : (
            <p className="no-notes">{t('notes.noNotes')}</p>
          )}

          <button
            className="edit-button"
            onClick={handleEditClick}
          >
            {article.personal_notes ? t('notes.editNotes') : t('notes.addNotes')}
          </button>
        </div>
      )}
    </div>
  );
}

export default PersonalNotesEditor;