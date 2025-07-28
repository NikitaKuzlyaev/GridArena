import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';

function ContestSubmissions() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');
  const [submissions, setSubmissions] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!contestId) return;
    setLoading(true);
    const token = localStorage.getItem('access_token');
    fetch(`${config.backendUrl}api/v1/contest/submissions?contest_id=${contestId}`, {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        setSubmissions(data);
      })
      .finally(() => setLoading(false));
  }, [contestId]);

  return (
    <div style={{ maxWidth: 1000, margin: '32px auto', padding: '0 16px' }}>
      <h1 style={{ textAlign: 'center', marginBottom: 32 }}>Посылки</h1>
      
      {loading && (
        <div style={{ textAlign: 'center', padding: 20 }}>
          <p>Загрузка...</p>
        </div>
      )}

      {submissions && (
        <>
          {/* Информация о соревновании */}
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '20px',
            borderRadius: '12px',
            marginBottom: '24px',
            boxShadow: '0 4px 16px rgba(102, 126, 234, 0.2)',
          }}>
            <h2 style={{ margin: '0 0 12px 0', fontSize: '20px', textAlign: 'center' }}>
              {submissions.name}
            </h2>
            <div style={{ display: 'flex', justifyContent: 'space-around', fontSize: 14 }}>
              <div>
                <strong>Начало:</strong> {new Date(submissions.startedAt).toLocaleString('ru-RU')}
              </div>
              <div>
                <strong>Окончание:</strong> {new Date(submissions.closedAt).toLocaleString('ru-RU')}
              </div>
            </div>
          </div>

          {/* Таблица посылок */}
          {submissions.submissions && submissions.submissions.body && submissions.submissions.body.length > 0 ? (
            <div style={{ overflowX: 'auto' }}>
              <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                background: 'white',
                borderRadius: '8px',
                overflow: 'hidden',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              }}>
                <thead>
                  <tr style={{ background: '#f8f9fa' }}>
                    <th style={{
                      padding: '12px 16px',
                      textAlign: 'left',
                      borderBottom: '2px solid #dee2e6',
                      fontWeight: 600,
                      fontSize: 14,
                    }}>
                      Участник
                    </th>
                    <th style={{
                      padding: '12px 16px',
                      textAlign: 'left',
                      borderBottom: '2px solid #dee2e6',
                      fontWeight: 600,
                      fontSize: 14,
                    }}>
                      Категория
                    </th>
                    <th style={{
                      padding: '12px 16px',
                      textAlign: 'center',
                      borderBottom: '2px solid #dee2e6',
                      fontWeight: 600,
                      fontSize: 14,
                    }}>
                      Цена
                    </th>
                    <th style={{
                      padding: '12px 16px',
                      textAlign: 'center',
                      borderBottom: '2px solid #dee2e6',
                      fontWeight: 600,
                      fontSize: 14,
                    }}>
                      Вердикт
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {submissions.submissions.body.map((submission, index) => (
                    <tr key={index} style={{
                      borderBottom: '1px solid #f1f3f4',
                      '&:hover': { background: '#f8f9fa' },
                    }}>
                      <td style={{
                        padding: '12px 16px',
                        fontSize: 14,
                        fontWeight: 500,
                      }}>
                        {submission.contestantName}
                      </td>
                      <td style={{
                        padding: '12px 16px',
                        fontSize: 14,
                      }}>
                        {submission.problemCard.categoryName}
                      </td>
                      <td style={{
                        padding: '12px 16px',
                        textAlign: 'center',
                        fontSize: 14,
                        fontWeight: 500,
                      }}>
                        {submission.problemCard.categoryPrice}
                      </td>
                      <td style={{
                        padding: '12px 16px',
                        textAlign: 'center',
                        fontSize: 14,
                        fontWeight: 600,
                      }}>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: '4px',
                          fontSize: 12,
                          fontWeight: 600,
                          background: submission.verdict === 'ACCEPTED' ? '#d4edda' : '#f8d7da',
                          color: submission.verdict === 'ACCEPTED' ? '#155724' : '#721c24',
                        }}>
                          {submission.verdict === 'ACCEPTED' ? '✅ Принято' : '❌ Неверно'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: 40, color: '#666' }}>
              <p>Нет данных о посылках</p>
            </div>
          )}
        </>
      )}

      {!loading && !submissions && (
        <div style={{ textAlign: 'center', padding: 40, color: '#666' }}>
          <p>Здесь в будущем появится список ваших посылок.</p>
        </div>
      )}
    </div>
  );
}

export default ContestSubmissions; 