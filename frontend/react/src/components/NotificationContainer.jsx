import React from 'react';
import { useNotifications } from './NotificationContext';

const levelToIcon = {
  INFO: 'ℹ️',
  DEBUG: '🐞',
  ERROR: '❌',
  WARNING: '⚠️',
  SUCCESS: '✅',
};

export default function NotificationContainer() {
  const { notifications, removeNotification } = useNotifications();

  return (
    <div style={{
      position: 'fixed',
      right: 12,
      bottom: 12,
      zIndex: 9999,
      display: 'flex',
      flexDirection: 'column',
      gap: 4,
      alignItems: 'flex-start',
      pointerEvents: 'none',
    }}>
      {notifications.map(({ id, level, content, color, date, isClosing }) => (
        <div
          key={id}
          style={{
            minWidth: 240,
            maxWidth: 240,
            background: color || '#222',
            color: '#fff',
            borderRadius: 2,
            boxShadow: '0 4px 24px rgba(0,0,0,0.15)',
            padding: '16px 20px 14px 20px',
            fontSize: 15,
            display: 'flex',
            alignItems: 'flex-start',
            gap: 12,
            pointerEvents: 'auto',
            animation: isClosing ? 'fadeOut 2s forwards' : 'fadeInUp 0.4s',
            position: 'relative',
            transition: 'opacity 2s',
            opacity: isClosing ? 0 : 1,
          }}
        >
          <span style={{ fontSize: 12, marginRight: 2 }}>
            {levelToIcon[level] || '🔔'}
          </span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600, marginBottom: 2, textAlign: 'left', }}>{level}</div>
            <div>{content}</div>
            <div style={{ fontSize: 10, opacity: 0.6, marginTop: 6 }}>
              {new Date(date).toLocaleString('ru-RU')}
            </div>
          </div>
          <button
            onClick={() => removeNotification(id)}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#fff',
              fontSize: 18,
              cursor: 'pointer',
              marginLeft: 8,
              opacity: 0.7,
              position: 'absolute',
              top: 8,
              right: 8,
              padding: 0,
            }}
            aria-label="Закрыть уведомление"
          >
            ×
          </button>
        </div>
      ))}
      <style>{`
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(40px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeOut {
          from { opacity: 1; }
          to { opacity: 0; }
        }
      `}</style>
    </div>
  );
}
