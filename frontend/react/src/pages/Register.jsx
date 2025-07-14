import React, { useState } from 'react';
import config from '../config';
import './Register.css';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await fetch(config.backendUrl + 'api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
        }),
        credentials: 'include',
      });
      if (!response.ok) {
        const data = await response.json();
        setError(data.detail || 'Ошибка регистрации');
        return;
      }
      const data = await response.json();
      // TODO: обработка успешной регистрации
      alert('Регистрация успешна!');
    } catch (err) {
      setError('Ошибка сети');
    }
  };

  return (
    <div className="register-page">
      <h2>Регистрация</h2>
      <form className="register-form" onSubmit={handleSubmit}>
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
        <button type="submit">Зарегистрироваться</button>
      </form>
      {error && <div style={{ color: 'red', marginTop: '8px' }}>{error}</div>}
    </div>
  );
}

export default Register;
