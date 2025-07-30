import React, { useState } from 'react';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';
import { useApi } from '../hooks/useApi';

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
  const { makeRequest } = useApi();

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const data = await makeRequest(config.backendUrl + 'api/v1/contest', {
        method: 'POST',
        body: JSON.stringify({
          name: form.name,
          started_at: form.started_at,
          closed_at: form.closed_at,
          start_points: Number(form.start_points),
          number_of_slots_for_problems: Number(form.number_of_slots_for_problems),
        }),
      });
      setLoading(false);
      if (data.contestId) {
        window.location.href = '/my-contests';
      } else {
        setError({ code: 'unknown', message: 'Некорректный ответ сервера' });
      }
    } catch (error) {
      setLoading(false);
      let msg = 'Ошибка сети';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setError({ code: 'network', message: msg });
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
