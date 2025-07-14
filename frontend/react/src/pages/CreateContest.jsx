import React, { useState } from 'react';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';

function CreateContest() {
  const [form, setForm] = useState({
    name: '',
    started_at: '',
    closed_at: '',
    start_points: '',
    number_of_slots_for_problems: '',
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(config.backendUrl + 'api/v1/contest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify({
          name: form.name,
          started_at: form.started_at,
          closed_at: form.closed_at,
          start_points: Number(form.start_points),
          number_of_slots_for_problems: Number(form.number_of_slots_for_problems),
        }),
        credentials: 'include',
      });
      const data = await response.json();
      setLoading(false);
      if (!response.ok) {
        setError({ code: response.status, message: data.detail || response.statusText });
        return;
      }
      if (data.body && data.body.contest_id) {
        window.location.href = '/my-contests';
      } else {
        setError({ code: 'unknown', message: 'Некорректный ответ сервера' });
      }
    } catch (err) {
      setLoading(false);
      setError({ code: 'network', message: 'Ошибка сети' });
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      <h2 style={{ textAlign: 'center' }}>Создать контест</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" type="text" placeholder="Название" maxLength={256} required value={form.name} onChange={handleChange} style={{ width: '100%', margin: '8px 0', padding: '8px' }} />
        <input name="started_at" type="datetime-local" required value={form.started_at} onChange={handleChange} style={{ width: '100%', margin: '8px 0', padding: '8px' }} />
        <input name="closed_at" type="datetime-local" required value={form.closed_at} onChange={handleChange} style={{ width: '100%', margin: '8px 0', padding: '8px' }} />
        <input name="start_points" type="number" min={0} max={10000} required placeholder="Стартовый баланс" value={form.start_points} onChange={handleChange} style={{ width: '100%', margin: '8px 0', padding: '8px' }} />
        <input name="number_of_slots_for_problems" type="number" min={1} max={5} required placeholder="Сколько задач разрешено держать одновременно (1–5)" value={form.number_of_slots_for_problems} onChange={handleChange} style={{ width: '100%', margin: '8px 0', padding: '8px' }} />
        <button type="submit" style={{ width: '100%', padding: '8px', background: '#61dafb', color: '#282c34', border: 'none', borderRadius: '4px', fontWeight: '500', marginTop: '12px' }} disabled={loading}>
          {loading ? 'Создание...' : 'Создать'}
        </button>
      </form>
      {error && <ErrorBlock code={error.code} message={error.message} />}
    </div>
  );
}

export default CreateContest;
