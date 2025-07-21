import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';
import ReactMarkdown from 'react-markdown';

function SolveContest() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');
  const [loading, setLoading] = useState(true);
  const [fieldData, setFieldData] = useState(null);
  const [modalCard, setModalCard] = useState(null);
  const [buying, setBuying] = useState(false);
  const [buyError, setBuyError] = useState(null);
  const [myProblems, setMyProblems] = useState([]);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    // Имитация загрузки
    setTimeout(() => {
      setLoading(false);
    }, 1);

    // Запрос к API для получения информации о поле для участника
    const token = localStorage.getItem('access_token');
    fetch(`${config.backendUrl}api/v1/quiz-field/info-contestant`, {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })
      .then(async res => {
        if (res.ok) {
          const data = await res.json();
          setFieldData(data);
        }
      })
      .catch(() => {});

    // Новый запрос к API для получения информации об участнике
    fetch(`${config.backendUrl}api/v1/contestant/info`, {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })
      .then(() => {})
      .catch(() => {});

    // Новый запрос к API для получения своих выбранных задач
    fetch(`${config.backendUrl}api/v1/selected-problem/my`, {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })
      .then(async res => {
        if (res.ok) {
          const data = await res.json();
          if (data && Array.isArray(data.body)) {
            setMyProblems(data.body.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)));
          }
        }
      })
      .catch(() => {});
  }, [contestId]);

  const getCardAt = (row, col) => {
    if (!fieldData || !fieldData.problemCards) return null;
    return fieldData.problemCards.find(card => card.row === row && card.column === col);
  };

  if (loading) {
    return (
      <div style={{
        maxWidth: 800,
        margin: '40px auto',
        padding: '40px',
        textAlign: 'center',
        background: '#fff',
        borderRadius: '12px',
        boxShadow: '0 4px 16px rgba(0,0,0,0.1)'
      }}>
        <div style={{ fontSize: '24px', marginBottom: '16px' }}>⏳</div>
        <div style={{ fontSize: '18px', color: '#666' }}>Загрузка соревнования...</div>
      </div>
    );
  }

  return (
    <div style={{
      maxWidth: 800,
      margin: '40px auto',
      padding: '40px',
      background: '#fff',
      borderRadius: '12px',
      boxShadow: '0 4px 16px rgba(0,0,0,0.1)'
    }}>
      <h1 style={{
        textAlign: 'center',
        marginBottom: '32px',
        color: '#333',
        fontSize: '28px'
      }}>
        🏆 Соревнование #{contestId}
      </h1>

      {fieldData ? (
        <div style={{ overflowX: 'auto', marginBottom: 32 }}>
          <table style={{ borderCollapse: 'collapse', width: '100%' }}>
            <tbody>
              {[...Array(fieldData.numberOfRows)].map((_, rowIdx) => (
                <tr key={rowIdx}>
                  {[...Array(fieldData.numberOfColumns)].map((_, colIdx) => {
                    const card = getCardAt(rowIdx + 1, colIdx + 1);
                    const clickable = card && card.isOpenForBuy;
                    return (
                      <td
                        key={colIdx}
                        style={{
                          border: '1px solid #ddd',
                          width: 120,
                          height: 100,
                          textAlign: 'center',
                          verticalAlign: 'middle',
                          background: card ? '#f0f8ff' : '#fafafa',
                          cursor: clickable ? 'pointer' : 'default',
                          opacity: clickable ? 1 : 0.6,
                          position: 'relative',
                        }}
                        onClick={() => {
                          if (clickable) setModalCard(card);
                        }}
                      >
                        {card ? (
                          <div>
                            <div><b>ID:</b> {card.problem.problemId}</div>
                            <div><b>Цена:</b> {card.categoryPrice}</div>
                            <div><b>Категория:</b> {card.categoryName}</div>
                          </div>
                        ) : null}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{ textAlign: 'center', color: '#888', margin: '32px 0' }}>Нет данных о поле</div>
      )}

      {/* Модальное окно подтверждения покупки */}
      {modalCard && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0,0,0,0.3)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}
          onClick={() => { if (!buying) setModalCard(null); }}
        >
          <div style={{ background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, position: 'relative', maxWidth: 500 }} onClick={e => e.stopPropagation()}>
            <h2>Покупка задачи</h2>
            <div style={{ marginBottom: 16 }}>
              <b>ID задачи:</b> {modalCard.problem.problemId}<br />
              <b>Цена:</b> {modalCard.categoryPrice}<br />
              <b>Категория:</b> {modalCard.categoryName}
            </div>
            <div style={{ marginBottom: 24 }}>Вы уверены, что хотите купить эту задачу?</div>
            {buyError && <div style={{ color: 'red', marginBottom: 12 }}>{buyError}</div>}
            <div style={{ display: 'flex', gap: 16 }}>
              <button
                style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: buying ? '#90caf9' : '#1677ff', color: '#fff', border: 'none', cursor: buying ? 'not-allowed' : 'pointer' }}
                disabled={buying}
                onClick={async () => {
                  setBuying(true);
                  setBuyError(null);
                  const token = localStorage.getItem('access_token');
                  try {
                    const res = await fetch(`${config.backendUrl}api/v1/selected-problem/buy`, {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                        'Authorization': token ? `Bearer ${token}` : '',
                      },
                      credentials: 'include',
                      body: JSON.stringify({ problem_card_id: modalCard.problemCardId }),
                    });
                    if (!res.ok) {
                      let msg = 'Ошибка покупки';
                      try {
                        const data = await res.json();
                        if (data && data.detail) msg = data.detail;
                      } catch {}
                      setBuyError(msg);
                      setBuying(false);
                      return;
                    }
                    setModalCard(null);
                    setBuying(false);
                    // Можно добавить обновление поля или уведомление об успехе
                    window.location.reload();
                  } catch {
                    setBuyError('Ошибка сети');
                    setBuying(false);
                  }
                }}
              >
                {buying ? 'Покупка...' : 'Да, купить'}
              </button>
              <button
                style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: '#eee', color: '#282c34', border: '1px solid #ccc', cursor: buying ? 'not-allowed' : 'pointer' }}
                disabled={buying}
                onClick={() => { if (!buying) setModalCard(null); }}
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Купленные задачи */}
      {myProblems.length > 0 && (
        <div style={{ marginTop: 32 }}>
          <h2 style={{ fontSize: 22, marginBottom: 16 }}>Мои купленные задачи</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
            {myProblems.map(problem => (
              <div key={problem.selectedProblemId} style={{
                background: '#f9f9f9',
                border: '1px solid #e0e0e0',
                borderRadius: 8,
                padding: 24,
                boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
                maxWidth: 700,
                margin: '0 auto',
              }}>
                <div style={{ marginBottom: 12, fontWeight: 500, color: '#333' }}>
                  <span style={{ opacity: 0.7, fontSize: 13 }}>ID: {problem.selectedProblemId}</span>
                  <span style={{ float: 'right', opacity: 0.5, fontSize: 13 }}>{new Date(problem.createdAt).toLocaleString()}</span>
                </div>
                <div style={{ marginBottom: 16 }}>
                  <ReactMarkdown>{problem.problem?.statement || 'Нет условия'}</ReactMarkdown>
                </div>
                <div style={{ display: 'flex', gap: 12 }}>
                  <input
                    type="text"
                    placeholder="Ваш ответ"
                    value={answers[problem.selectedProblemId] || ''}
                    onChange={e => setAnswers(a => ({ ...a, [problem.selectedProblemId]: e.target.value }))}
                    style={{ flex: 1, padding: 8, borderRadius: 4, border: '1px solid #bbb', fontSize: 16 }}
                  />
                  <button
                    style={{ padding: '8px 20px', fontSize: 16, borderRadius: 6, background: '#1677ff', color: '#fff', border: 'none', cursor: 'pointer' }}
                    disabled
                  >
                    Отправить ответ
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{
        marginTop: '24px',
        padding: '16px',
        background: '#e3f2fd',
        borderRadius: '8px',
        border: '1px solid #bbdefb'
      }}>
        <strong>Отладочная информация:</strong>
        <br />
        Contest ID: {contestId}
      </div>
    </div>
  );
}

export default SolveContest; 