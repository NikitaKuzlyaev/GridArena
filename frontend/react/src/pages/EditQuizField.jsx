import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import config from '../config';

function EditQuizField() {
  const location = useLocation();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rows, setRows] = useState(1);
  const [cols, setCols] = useState(1);
  const [modalCard, setModalCard] = useState(null);

  // Получаем contest_id из query-параметров
  const searchParams = new URLSearchParams(location.search);
  const contestId = searchParams.get('contest_id');

  useEffect(() => {
    if (!contestId) {
      setError({ code: 'no_id', message: 'Не передан contest_id' });
      setLoading(false);
      return;
    }
    const token = localStorage.getItem('access_token');
    fetch(`${config.backendUrl}api/v1/quiz-field/info-editor?contest_id=${contestId}`, {
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
        setData(data);
        setRows(data.numberOfRows || 1);
        setCols(data.numberOfColumns || 1);
        setLoading(false);
      })
      .catch(() => {
        setError({ code: 'network', message: 'Ошибка сети' });
        setLoading(false);
      });
  }, [contestId]);

  const handleRowsChange = (e) => {
    let value = Math.max(1, Math.min(8, Number(e.target.value)));
    setRows(value);
  };
  const handleColsChange = (e) => {
    let value = Math.max(1, Math.min(8, Number(e.target.value)));
    setCols(value);
  };

  // Получить карточку по позиции
  const getCardAt = (row, col) => {
    if (!data || !data.problemCards) return null;
    return data.problemCards.find(card => card.row === row && card.column === col);
  };

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      <h1 style={{ textAlign: 'center' }}>Редактирование поля</h1>
      {loading && <div>Загрузка...</div>}
      {error && <div style={{ color: 'red' }}>{error.message}</div>}
      {data && (
        <>
          <div style={{ display: 'flex', gap: 24, marginBottom: 24 }}>
            <label>
              Число строк:
              <input
                type="number"
                min={1}
                max={8}
                value={rows}
                onChange={handleRowsChange}
                style={{ marginLeft: 8, width: 60 }}
              />
            </label>
            <label>
              Число колонок:
              <input
                type="number"
                min={1}
                max={8}
                value={cols}
                onChange={handleColsChange}
                style={{ marginLeft: 8, width: 60 }}
              />
            </label>
          </div>
          <button
            style={{ marginBottom: 24, padding: '8px 24px', fontSize: 16, borderRadius: 6, background: '#1677ff', color: '#fff', border: 'none', cursor: 'pointer' }}
            onClick={async () => {
              if (!data) return;
              const token = localStorage.getItem('access_token');
              try {
                const res = await fetch(`${config.backendUrl}api/v1/quiz-field/`, {
                  method: 'PATCH',
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : '',
                  },
                  credentials: 'include',
                  body: JSON.stringify({
                    quiz_field_id: data.quizFieldId,
                    number_of_rows: rows,
                    number_of_columns: cols,
                  }),
                });
                if (!res.ok) {
                  let msg = 'Ошибка сохранения';
                  try {
                    const err = await res.json();
                    if (err && err.detail) msg = err.detail;
                  } catch {}
                  alert(msg);
                  return;
                }
                window.location.reload();
              } catch {
                alert('Ошибка сети при сохранении');
              }
            }}
          >
            Сохранить
          </button>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ borderCollapse: 'collapse', width: '100%' }}>
              <tbody>
                {[...Array(rows)].map((_, rowIdx) => (
                  <tr key={rowIdx}>
                    {[...Array(cols)].map((_, colIdx) => {
                      const card = getCardAt(rowIdx + 1, colIdx + 1);
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
                            cursor: card ? 'pointer' : 'default',
                            position: 'relative',
                          }}
                          onClick={() => card && setModalCard(card)}
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
          {/* Модальное окно */}
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
              <div style={{ background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, position: 'relative' }} onClick={e => e.stopPropagation()}>
                <h2>Информация о карточке</h2>
                <pre style={{ background: '#f7f7f7', padding: 12, borderRadius: 4 }}>{JSON.stringify(modalCard, null, 2)}</pre>
                <button style={{ marginTop: 16 }} onClick={() => setModalCard(null)}>Закрыть</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default EditQuizField; 