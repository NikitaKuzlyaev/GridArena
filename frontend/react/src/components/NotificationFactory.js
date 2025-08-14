// NotificationFactory.js
// Фабрика для отправки уведомлений по всему приложению

let notify = null;

export function setNotify(fn) {
  notify = fn;
}

/**
 * Отправить уведомление
 * @param {Object} params
 * @param {string} params.level - уровень (INFO, DEBUG, ERROR и т.д.)
 * @param {string} params.content - текст уведомления
 * @param {string} params.color - цвет окна (CSS-цвет)
 * @param {Date|string} [params.date] - дата (по умолчанию сейчас)
 */
export function sendNotification({ level, content, color, date = new Date() }) {
  if (notify) {
    notify({ level, content, color, date: typeof date === 'string' ? new Date(date) : date });
  } else {
    console.warn('Notification system is not initialized');
  }
}
