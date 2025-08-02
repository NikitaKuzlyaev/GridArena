import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useApi } from '../hooks/useApi';
import config from '../config';

function ContestSubmissions() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');
  const [submissions, setSubmissions] = useState(null);
  const [showUserOnly, setShowUserOnly] = useState(false);
  const [initialShowUserOnly, setInitialShowUserOnly] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const { makeRequest, loading } = useApi();

  useEffect(() => {
    if (!contestId) return;
    
    const fetchSubmissions = async () => {
      try {
        const data = await makeRequest(`${config.backendUrl}api/v1/contest/submissions?contest_id=${contestId}&show_user_only=${showUserOnly}`);
        // Сортируем посылки по времени создания (новые сначала)
        if (data.submissions && data.submissions.body) {
          data.submissions.body.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
        }
        setSubmissions(data);
      } catch (error) {
        console.error('Ошибка при загрузке посылок:', error);
      }
    };

    fetchSubmissions();
  }, [contestId, makeRequest]);

  // Отслеживаем изменения состояния чекбокса
  useEffect(() => {
    setHasChanges(showUserOnly !== initialShowUserOnly);
  }, [showUserOnly, initialShowUserOnly]);

  const handleApplyFilter = async () => {
    if (!contestId) return;
    
    try {
      const data = await makeRequest(`${config.backendUrl}api/v1/contest/submissions?contest_id=${contestId}&show_user_only=${showUserOnly}`);
      // Сортируем посылки по времени создания (новые сначала)
      if (data.submissions && data.submissions.body) {
        data.submissions.body.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      }
      setSubmissions(data);
      setInitialShowUserOnly(showUserOnly);
      setHasChanges(false);
    } catch (error) {
      console.error('Ошибка при загрузке посылок:', error);
    }
  };

  return (
    <div style={{ maxWidth: 1000, margin: '32px auto', padding: '0 16px' }}>
      <h1 style={{ textAlign: 'center', marginBottom: 32 }}>Посылки</h1>
      
      {/* Фильтры */}
      <div style={{
        background: 'white',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '24px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        flexWrap: 'wrap'
      }}>
        <label style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          cursor: 'pointer',
          fontSize: '14px',
          fontWeight: 500
        }}>
          <input
            type="checkbox"
            checked={showUserOnly}
            onChange={(e) => setShowUserOnly(e.target.checked)}
            style={{
              width: '16px',
              height: '16px',
              cursor: 'pointer'
            }}
          />
          Показывать только мои попытки
        </label>
        
        <button
          onClick={handleApplyFilter}
          disabled={!hasChanges}
          style={{
            padding: '8px 16px',
            backgroundColor: hasChanges ? '#667eea' : '#ccc',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: hasChanges ? 'pointer' : 'not-allowed',
            fontSize: '14px',
            fontWeight: 500,
            transition: 'background-color 0.2s'
          }}
        >
          Применить
        </button>
      </div>
      
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
                      Время
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
                        fontWeight: 500,
                      }}>
                        {new Date(submission.createdAt).toLocaleString('ru-RU')}
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