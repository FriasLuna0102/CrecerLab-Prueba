import React from 'react';
import { useTranslation } from 'react-i18next';

function ConfirmDialog({ isOpen, title, message, onConfirm, onCancel, confirmText, cancelText }) {
  const { t } = useTranslation();

  if (!isOpen) return null;

  return (
    <div className="confirm-dialog-overlay">
      <div className="confirm-dialog">
        <div className="confirm-dialog-header">
          <h3>{title}</h3>
          <button className="close-button" onClick={onCancel} aria-label={t('notes.cancel')}>
            &times;
          </button>
        </div>

        <div className="confirm-dialog-content">
          <p>{message}</p>
        </div>

        <div className="confirm-dialog-actions">
          <button
            className="cancel-button"
            onClick={onCancel}
          >
            {cancelText || t('notes.cancel')}
          </button>
          <button
            className="confirm-button"
            onClick={onConfirm}
          >
            {confirmText || t('confirmDialog.delete')}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDialog;