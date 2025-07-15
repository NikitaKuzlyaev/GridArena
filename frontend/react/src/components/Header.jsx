import React from 'react';
import './Header.css';

function Header() {
  const isAuth = Boolean(localStorage.getItem('accessToken'));
  return (
    <header className="header">
      <div className="header-left">
        <a href="/" className="header-title">GridArena</a>
        {isAuth && (
          <a href="/my-contests" className="contests-btn">Мои контесты</a>
        )}
      </div>
      <div className="header-right">
        <a href="/login" className="login-btn">Войти</a>
      </div>
    </header>
  );
}

export default Header;
