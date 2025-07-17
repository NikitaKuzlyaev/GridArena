import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';

function EditContest() {
  const { contestId } = useParams();
  const [form, setForm] = useState({
    name: '',
    start_points: '',
    number_of_slots_for_problems: '',
    started_at: '',
    closed_at: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    fetch(`${config.backendUrl}api/v1/contest/info-editor?contest_id=${contestId}`, {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })
      .then(async res => {
        if (!res.ok) {
          let msg = 'Ошибка загрузки данных';
          try {
            const data = await res.json();
            if (data && data.detail) msg = data.detail;
          } catch {}
          setError({ code: res.status, message: msg });
          setLoading(false);
          return;
        }
        const data = await res.json();
        if (data) {
          setForm({
            name: data.name || '',
            start_points: data.startPoints?.toString() || '',
            number_of_slots_for_problems: data.numberOfSlotsForProblems?.toString() || '',
            started_at: data.startedAt ? data.startedAt.slice(0, 16) : '',
            closed_at: data.closedAt ? data.closedAt.slice(0, 16) : '',
          });
        }
        setLoading(false);
      })
      .catch(() => {
        setError({ code: 'network', message: 'Ошибка сети' });
        setLoading(false);
      });
  }, [contestId]);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${config.backendUrl}api/v1/contest/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        body: JSON.stringify({
          contestId: Number(contestId),
          name: form.name,
          startPoints: Number(form.start_points),
          numberOfSlotsForProblems: Number(form.number_of_slots_for_problems),
          startedAt: form.started_at,
          closedAt: form.closed_at,
        }),
        credentials: 'include',
      });
      const data = await response.json();
      setLoading(false);
      if (!response.ok) {
        let msg = data && data.detail ? data.detail : response.statusText;
        setError({ code: response.status, message: msg });
        return;
      }
      alert('Контест успешно обновлён!');
      window.location.href = '/my-contests';
    } catch (err) {
      setLoading(false);
      setError({ code: 'network', message: 'Ошибка сети' });
    }
  };

  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: '40px' }}>Загрузка...</div>;
  }
  if (error) {
    return <ErrorBlock code={error.code} message={error.message} />;
  }
  return (
    <div>
      <div style={{ maxWidth: 600, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
        <h1 style={{ textAlign: 'center' }}>Редактирование контеста</h1>
        <form style={{ marginTop: 32, display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 400, marginLeft: 'auto', marginRight: 'auto' }} onSubmit={handleSubmit}>
          <label>
            Название:
            <input name="name" type="text" maxLength={256} required value={form.name} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }} />
          </label>
          <label>
            Стартовый баланс:
            <input name="start_points" type="number" min={0} max={10000} required value={form.start_points} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }} />
          </label>
          <label>
            Сколько задач разрешено держать одновременно (1–5):
            <input name="number_of_slots_for_problems" type="number" min={1} max={5} required value={form.number_of_slots_for_problems} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }} />
          </label>
          <label>
            Начало:
            <input name="started_at" type="datetime-local" required value={form.started_at} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }} />
          </label>
          <label>
            Окончание:
            <input name="closed_at" type="datetime-local" required value={form.closed_at} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }} />
          </label>
          <button type="submit" style={{ padding: 10, background: '#61dafb', color: '#282c34', border: 'none', borderRadius: 4, fontWeight: 500, marginTop: 12 }} disabled={loading}>
            {loading ? 'Сохранение...' : 'Сохранить'}
          </button>
        </form>
      </div>
      <div style={{ textAlign: 'center', marginTop: 24 }}>
        <button
          type="button"
          style={{ padding: 10, background: '#eee', color: '#282c34', border: '1px solid #ccc', borderRadius: 4, fontWeight: 500, marginRight: 12 }}
          onClick={() => window.location.href = `/edit-field?contest_id=${contestId}`}
        >
          Редактировать поле
        </button>
        <button
          type="button"
          style={{ padding: 10, background: '#ff4d4f', color: '#fff', border: 'none', borderRadius: 4, fontWeight: 500 }}
          onClick={async () => {
            if (window.confirm('Вы уверены, что хотите удалить этот контест? Это действие необратимо.')) {
              setLoading(true);
              setError(null);
              try {
                const token = localStorage.getItem('access_token');
                const response = await fetch(`${config.backendUrl}api/v1/contest/?contest_id=${contestId}`, {
                  method: 'DELETE',
                  headers: {
                    'Authorization': token ? `Bearer ${token}` : '',
                  },
                  credentials: 'include',
                });
                setLoading(false);
                if (!response.ok) {
                  let msg = 'Ошибка удаления';
                  try {
                    const data = await response.json();
                    if (data && data.detail) msg = data.detail;
                  } catch {}
                  setError({ code: response.status, message: msg });
                  return;
                }
                alert('Контест успешно удалён!');
                window.location.href = '/my-contests';
              } catch (err) {
                setLoading(false);
                setError({ code: 'network', message: 'Ошибка сети' });
              }
            }
          }}
        >
          Удалить контест
        </button>
        <div style={{ marginTop: 24 }}>
          <button
            type="button"
            style={{ padding: 10, background: '#21a1f3', color: '#fff', border: 'none', borderRadius: 4, fontWeight: 500, marginRight: 12 }}
            onClick={() => window.location.href = `/edit-contestants?contest_id=${contestId}`}
          >
            Управление участниками
          </button>
          <button
            type="button"
            style={{ padding: 10, background: '#21a1f3', color: '#fff', border: 'none', borderRadius: 4, fontWeight: 500 }}
            onClick={() => window.location.href = `/edit-submissions?contest_id=${contestId}`}
          >
            Управление посылками
          </button>
        </div>
      </div>
    </div>
  );
}

export default EditContest; 