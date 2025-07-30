
import React, { useEffect, useState } from 'react';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';
import { useApi } from '../hooks/useApi';

function MyContests() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [contests, setContests] = useState(null);
  const { makeRequest } = useApi();

  useEffect(() => {
    const fetchContests = async () => {
      try {
        const data = await makeRequest(config.backendUrl + 'api/v1/contest');
        setContests(data);
        setLoading(false);
      } catch (err) {
        setError({ code: 'network', message: 'Ошибка сети' });
        setLoading(false);
      }
    };

    fetchContests();
  }, [makeRequest]);

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
              position: 'relative',
              border: '1px solid #eee',
              borderRadius: 8,
              padding: '20px 24px 20px 24px',
              marginBottom: 20,
              boxShadow: '0 1px 8px rgba(0,0,0,0.06)',
              background: '#fafbfc',
              minHeight: 90,
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'flex-start',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
                <span style={{ opacity: 0.4, fontSize: 14, fontWeight: 500, marginRight: 12 }}>
                  {contest.contestId}
                </span>
                <span style={{ fontWeight: 'bold', fontSize: 20, color: '#282c34', flex: 1 }}>
                  {contest.name}
                </span>
              </div>
              <div style={{ display: 'flex', alignItems: 'stretch', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <div style={{ fontSize: '0.97rem', color: '#555', marginBottom: 2 }}>
                    <b>Начало:</b> {new Date(contest.startedAt).toLocaleString()}
                  </div>
                  <div style={{ fontSize: '0.97rem', color: '#555' }}>
                    <b>Окончание:</b> {new Date(contest.closedAt).toLocaleString()}
                  </div>
                </div>
                <a
                  href={`/edit-contest/${contest.contestId}`}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: 48,
                    height: 48,
                    marginLeft: 16,
                    background: '#e3e6e8',
                    borderRadius: 8,
                    border: 'none',
                    cursor: 'pointer',
                    textDecoration: 'none',
                    transition: 'background 0.2s',
                  }}
                  title="Редактировать контест"
                >
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#282c34" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4 12.5-12.5z"/></svg>
                </a>
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
