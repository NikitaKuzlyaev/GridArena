import React, { createContext, useContext, useState, useCallback } from 'react';
import { setNotify } from './NotificationFactory';

const NotificationContext = createContext();

export function useNotifications() {
  return useContext(NotificationContext);
}

export function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([]);

  // Добавить уведомление
  const addNotification = useCallback((notification) => {
    const id = Math.random().toString(36).slice(2);
    setNotifications((prev) => [
      ...prev,
      { ...notification, id, isClosing: false }
    ]);
    // Через 5 секунд начинаем плавное закрытие
    setTimeout(() => {
      setNotifications((prev) => prev.map(n => n.id === id ? { ...n, isClosing: true } : n));
      // Через 2 секунды удаляем окончательно
      setTimeout(() => {
        setNotifications((prev) => prev.filter((n) => n.id !== id));
      }, 2000);
    }, 5000);
  }, []);

  // Удалить уведомление (по кнопке)
  const removeNotification = useCallback((id) => {
    setNotifications((prev) => prev.map(n => n.id === id ? { ...n, isClosing: true } : n));
    setTimeout(() => {
      setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, 2000);
  }, []);

  // Инициализация фабрики
  React.useEffect(() => {
    setNotify(addNotification);
  }, [addNotification]);

  return (
    <NotificationContext.Provider value={{ notifications, addNotification, removeNotification }}>
      {children}
    </NotificationContext.Provider>
  );
}
