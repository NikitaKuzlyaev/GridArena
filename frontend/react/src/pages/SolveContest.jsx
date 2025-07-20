import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';

function SolveContest() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');
  const [loading, setLoading] = useState(true);
  const [fieldData, setFieldData] = useState(null);
  const [modalCard, setModalCard] = useState(null);

  useEffect(() => {
    // Имитация загрузки
    setTimeout(() => {
      setLoading(false);
    }, 1000);

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
          onClick={() => setModalCard(null)}
        >
          <div style={{ background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, position: 'relative', maxWidth: 500 }} onClick={e => e.stopPropagation()}>
            <h2>Покупка задачи</h2>
            <div style={{ marginBottom: 16 }}>
              <b>ID задачи:</b> {modalCard.problem.problemId}<br />
              <b>Цена:</b> {modalCard.categoryPrice}<br />
              <b>Категория:</b> {modalCard.categoryName}
            </div>
            <div style={{ marginBottom: 24 }}>Вы уверены, что хотите купить эту задачу?</div>
            <div style={{ display: 'flex', gap: 16 }}>
              <button
                style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: '#1677ff', color: '#fff', border: 'none', cursor: 'pointer' }}
                onClick={() => setModalCard(null)}
              >
                Да, купить (заглушка)
              </button>
              <button
                style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: '#eee', color: '#282c34', border: '1px solid #ccc', cursor: 'pointer' }}
                onClick={() => setModalCard(null)}
              >
                Отмена
              </button>
            </div>
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