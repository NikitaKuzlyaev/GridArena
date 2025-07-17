import React from 'react';
import './Header.css';
import config from '../config';

function deleteCookie(name) {
  document.cookie = name + '=; Max-Age=0; path=/;';
}

function Header() {
  const isAuth = Boolean(localStorage.getItem('access_token'));

  const handleLogout = async () => {
    console.log('Нажата кнопка Выйти');
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = (() => {
      const match = document.cookie.match(/(?:^|; )refresh_token=([^;]*)/);
      return match ? decodeURIComponent(match[1]) : null;
    })();
    if (!accessToken) return;
    try {
      const response = await fetch(`${config.backendUrl}api/v1/auth/block-my-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
      console.log('Ответ сервера:', response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (e) {
      console.error('Ошибка при блокировке токена:', e);
      // Можно обработать ошибку, если нужно
    }
    localStorage.removeItem('access_token');
    deleteCookie('refresh_token');
    console.log('access_token:', localStorage.getItem('access_token'));
    console.log('refresh_token cookie:', document.cookie);
    window.location.href = '/login';
  };

  return (
    <header className="header">
      <div className="header-left">
        <a href="/" className="header-title">GridArena</a>
        {isAuth && (
          <a href="/my-contests" className="contests-btn">Мои контесты</a>
        )}
      </div>
      <div className="header-right">
        {!isAuth ? (
          <a href="/login" className="login-btn">Войти</a>
        ) : (
          <button className="login-btn" onClick={handleLogout}>Выйти</button>
        )}
      </div>
    </header>
  );
}

export default Header;
