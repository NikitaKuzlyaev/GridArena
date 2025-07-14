import React from 'react';
import './Header.css';

function Header() {
  const isAuth = Boolean(localStorage.getItem('accessToken'));
  return (
    <header className="header">
      <h3>Quiz App</h3>
      {isAuth ? (
        <a href="/my-contests" className="login-btn">Мои контесты</a>
      ) : (
        undefined
      )}
      <a href="/login" className="login-btn">Войти</a>
    </header>
  );
}

export default Header;
