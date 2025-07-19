import React, { useState } from 'react';
import config from '../config';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [domain, setDomain] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch(config.backendUrl + 'api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username,
          password,
          domain_number: domain,
        }),
        credentials: 'include',
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Ошибка авторизации');
        return;
      }
      const data = await response.json();
      if (data.accessToken && data.userType) {
        localStorage.setItem('access_token', data.accessToken);
        localStorage.setItem('user_type', data.userType);
        
        // Редирект на главную страницу с перезагрузкой
        window.location.href = '/';
      } else {
        setError('Токен не получен');
      }
    } catch (err) {
      setError('Ошибка сети');
    }
  };

  return (
    <div className="login-page">
      <h2>Авторизация</h2>
      <form className="login-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Домен"
          value={domain}
          onChange={e => setDomain(e.target.value)}
          name="domain"
          required
        />
        <div style={{ fontSize: '12px', color: '#888', marginBottom: '8px' }}>
          0 - для организаторов, для участников номер домена сообщается организаторами
        </div>
        <input
          type="text"
          placeholder="Логин"
          value={username}
          onChange={e => setUsername(e.target.value)}
          name="username"
          required
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={e => setPassword(e.target.value)}
          name="password"
          required
        />
        <button type="submit">Войти</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: '8px' }}>{error}</div>}
      <div style={{ marginTop: '16px' }}>
        <span>У вас нет аккаунта? </span>
        <a href="/register" style={{ color: '#21a1f3' }}>Зарегистрируйтесь.</a>
      </div>
    </div>
  );
}

export default Login;
