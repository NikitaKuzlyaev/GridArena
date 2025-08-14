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

  // Валидация полей
  const validate = (form) => {
    const errors = {};
    if (form.name.length < 1 || form.name.length > 256) {
      errors.name = 'Название должно содержать от 1 до 256 символов';
    }
    const startPoints = Number(form.start_points);
    if (isNaN(startPoints) || startPoints < 0 || startPoints > 10000) {
      errors.start_points = 'Стартовый баланс должен быть от 0 до 10000';
    }
    const slots = Number(form.number_of_slots_for_problems);
    if (isNaN(slots) || slots < 1 || slots > 5) {
      errors.number_of_slots_for_problems = 'Число задач должно быть от 1 до 5';
    }
    return errors;
  };

  const errors = validate(form);
  const isFormValid = Object.keys(errors).length === 0;

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      // Конвертируем локальные даты в UTC для отправки на сервер
      const convertLocalToUtc = (localDateTimeString) => {
        if (!localDateTimeString) return '';
        const localDate = new Date(localDateTimeString);
        return localDate.toISOString();
      };

      const data = await makeRequest(config.backendUrl + 'api/v1/contest', {
        method: 'POST',
        body: JSON.stringify({
          name: form.name,
          started_at: convertLocalToUtc(form.started_at),
          closed_at: convertLocalToUtc(form.closed_at),
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
        <div style={{ marginBottom: 8 }}>
          <input
            name="name"
            type="text"
            placeholder="Название"
            maxLength={256}
            required
            value={form.name}
            onChange={handleChange}
            style={{
              width: '100%', margin: '8px 0', padding: '8px',
              border: errors.name ? '1.5px solid #e53935' : undefined
            }}
          />
          <div style={{ fontSize: 12, color: errors.name ? '#e53935' : '#888', minHeight: 18 }}>
            {'Строка длиной от 1 до 256 символов'}
          </div>
        </div>
        <div style={{ marginBottom: 8 }}>
          <input
            name="started_at"
            type="datetime-local"
            required
            value={form.started_at}
            onChange={handleChange}
            style={{ width: '100%', margin: '8px 0', padding: '8px' }}
          />
        </div>
        <div style={{ marginBottom: 8 }}>
          <input
            name="closed_at"
            type="datetime-local"
            required
            value={form.closed_at}
            onChange={handleChange}
            style={{ width: '100%', margin: '8px 0', padding: '8px' }}
          />
        </div>
        <div style={{ marginBottom: 8 }}>
          <input
            name="start_points"
            type="number"
            min={0}
            max={10000}
            required
            placeholder="Стартовый баланс"
            value={form.start_points}
            onChange={handleChange}
            style={{
              width: '100%', margin: '8px 0', padding: '8px',
              border: errors.start_points ? '1.5px solid #e53935' : undefined
            }}
          />
          <div style={{ fontSize: 12, color: errors.start_points ? '#e53935' : '#888', minHeight: 18 }}>
            {'Целое число от 0 до 10000'}
          </div>
        </div>
        <div style={{ marginBottom: 8 }}>
          <input
            name="number_of_slots_for_problems"
            type="number"
            min={1}
            max={5}
            required
            placeholder="Сколько задач разрешено держать одновременно (1–5)"
            value={form.number_of_slots_for_problems}
            onChange={handleChange}
            style={{
              width: '100%', margin: '8px 0', padding: '8px',
              border: errors.number_of_slots_for_problems ? '1.5px solid #e53935' : undefined
            }}
          />
          <div style={{ fontSize: 12, color: errors.number_of_slots_for_problems ? '#e53935' : '#888', minHeight: 12 }}>
            {'Целое число от 1 до 5'}
          </div>
        </div>
        <button
          type="submit"
          style={{ width: '100%', padding: '8px', background: '#61dafb', color: '#282c34', border: 'none', borderRadius: '4px', fontWeight: '500', marginTop: '12px', opacity: isFormValid && !loading ? 1 : 0.6 }}
          disabled={!isFormValid || loading}
        >
          {loading ? 'Создание...' : 'Создать'}
        </button>
      </form>
      {error && <ErrorBlock code={error.code} message={error.message} />}
    </div>
  );
}

export default CreateContest;
