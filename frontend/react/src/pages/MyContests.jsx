
import React, { useEffect, useState } from 'react';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';

function MyContests() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [contests, setContests] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    fetch(config.backendUrl + 'api/v1/contest', {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })
      .then(async res => {
        if (!res.ok) {
          setError({ code: res.status, message: res.statusText });
          setLoading(false);
          return;
        }
        const data = await res.json();
        setContests(data);
        setLoading(false);
      })
      .catch(err => {
        setError({ code: 'network', message: 'Ошибка сети' });
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: '40px' }}>Загрузка...</div>;
  }
  if (error) {
    return <ErrorBlock code={error.code} message={error.message} />;
  }
  return (
    <div style={{ maxWidth: 600, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      <h1 style={{ textAlign: 'center' }}>Мои контесты</h1>
      <a href="/create-contest" style={{
        display: 'inline-block',
        margin: '24px 0',
        padding: '8px 24px',
        background: '#61dafb',
        color: '#282c34',
        borderRadius: '4px',
        textDecoration: 'none',
        fontWeight: '500',
        fontSize: '1rem',
        transition: 'background 0.2s'
      }}>Создать контест</a>
      {contests && Array.isArray(contests.body) && contests.body.length > 0 ? (
        <div style={{ marginTop: 24 }}>
          {contests.body.map(contest => (
            <div key={contest.contestId} style={{
              border: '1px solid #eee',
              borderRadius: 6,
              padding: '16px 20px',
              marginBottom: 16,
              boxShadow: '0 1px 6px rgba(0,0,0,0.04)',
              background: '#fafbfc'
            }}>
              <h3 style={{ margin: '0 0 8px 0', color: '#282c34' }}>{contest.name}</h3>
              <div style={{ fontSize: '0.95rem', color: '#555' }}>
                <b>ID:</b> {contest.contestId}<br />
                <b>Начало:</b> {new Date(contest.startedAt).toLocaleString()}<br />
                <b>Окончание:</b> {new Date(contest.closedAt).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div style={{ marginTop: 24, color: '#888', textAlign: 'center' }}>Нет контестов</div>
      )}
    </div>
  );
}

export default MyContests;
