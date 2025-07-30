import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';
import { useApi } from '../hooks/useApi';

function EditQuizField() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');
  const { makeRequest } = useApi();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rows, setRows] = useState(1);
  const [cols, setCols] = useState(1);
  const [modalCard, setModalCard] = useState(null);
  const [modalCardInfo, setModalCardInfo] = useState(null);
  const [modalLoading, setModalLoading] = useState(false);
  const [editForm, setEditForm] = useState(null);
  const [editErrors, setEditErrors] = useState({});
  const [editSaving, setEditSaving] = useState(false);
  const [createMode, setCreateMode] = useState(false);
  const [createCell, setCreateCell] = useState(null); // {row, col}



  useEffect(() => {
    if (!contestId) {
      setError({ code: 'no_id', message: 'Не передан contest_id' });
      setLoading(false);
      return;
    }
    
    const fetchFieldData = async () => {
      try {
        const data = await makeRequest(`${config.backendUrl}api/v1/quiz-field/info-editor?contest_id=${contestId}`);
        setData(data);
        setRows(data.numberOfRows || 1);
        setCols(data.numberOfColumns || 1);
        setLoading(false);
      } catch (error) {
        let msg = 'Ошибка загрузки данных';
        if (error.message && error.message.includes('detail')) {
          try {
            const errorData = JSON.parse(error.message);
            if (errorData.detail) msg = errorData.detail;
          } catch {}
        }
        setError({ code: 'network', message: msg });
        setLoading(false);
      }
    };

    fetchFieldData();
  }, [contestId, makeRequest]);

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

  // Клик по карточке
  const handleCardClick = async (card, rowIdx, colIdx) => {
    if (!card) {
      // Пустая карточка — открываем форму создания
      setCreateMode(true);
      setCreateCell({ row: rowIdx + 1, col: colIdx + 1 });
      setEditForm({
        categoryName: '-',
        categoryPrice: 0,
        statement: '-',
        answer: '-',
      });
      setEditErrors({});
      setModalCard(null);
      setModalCardInfo(null);
      return;
    }
    setModalLoading(true);
    setModalCard(card); // для совместимости, если нужно оставить старую инфу
    setModalCardInfo(null);
    setEditForm(null);
    setEditErrors({});
    
    try {
      const info = await makeRequest(`${config.backendUrl}api/v1/problem-card/info-editor?problem_card_id=${card.problemCardId}`);
      setModalCardInfo(info);
      setEditForm({
        categoryName: info.categoryName || '',
        categoryPrice: info.categoryPrice || 0,
        statement: (info.problem && info.problem.statement) || '',
        answer: (info.problem && info.problem.answer) || '',
      });
    } catch (error) {
      setModalCardInfo({ error: 'Ошибка сети при загрузке карточки' });
    }
    setModalLoading(false);
  };

  // Валидация формы
  const validateEditForm = (form) => {
    const errors = {};
    if (!form.categoryName || form.categoryName.length < 1 || form.categoryName.length > 32) {
      errors.categoryName = 'Название категории: 1-32 символа';
    }
    if (isNaN(form.categoryPrice) || form.categoryPrice < 0 || form.categoryPrice > 10000) {
      errors.categoryPrice = 'Цена: от 0 до 10000';
    }
    if (form.statement.length > 2048) {
      errors.statement = 'Условие: до 2048 символов';
    }
    if (!form.answer || form.answer.length < 1 || form.answer.length > 32) {
      errors.answer = 'Ответ: 1-32 символа';
    }
    return errors;
  };

  // Сохранение изменений
  const handleEditSave = async () => {
    const errors = validateEditForm(editForm);
    if (Object.keys(errors).length > 0) {
      setEditErrors(errors);
      return;
    }
    setEditErrors({});
    setModalLoading(true);
    try {
      await makeRequest(`${config.backendUrl}api/v1/problem-card/with-problem`, {
        method: 'PATCH',
        body: JSON.stringify({
          problemCardId: modalCard.problemCardId,
          categoryName: editForm.categoryName,
          categoryPrice: Number(editForm.categoryPrice),
          problem: {
            statement: editForm.statement,
            answer: editForm.answer,
          },
        }),
      });
      setModalCard(null);
      setModalCardInfo(null);
      setEditForm(null);
      setEditErrors({});
      // Перезагружаем данные
      window.location.reload();
    } catch (error) {
      let msg = 'Ошибка сохранения';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setEditErrors({ general: msg });
    }
    setModalLoading(false);
  };

  // Создание новой карточки
  const handleCreateSave = async () => {
    const errors = validateEditForm(editForm);
    if (Object.keys(errors).length > 0) {
      setEditErrors(errors);
      return;
    }
    setEditErrors({});
    setModalLoading(true);
    try {
      await makeRequest(`${config.backendUrl}api/v1/problem-card/with-problem`, {
        method: 'POST',
        body: JSON.stringify({
          contestId: Number(contestId),
          row: createCell.row,
          column: createCell.col,
          categoryName: editForm.categoryName,
          categoryPrice: Number(editForm.categoryPrice),
          problem: {
            statement: editForm.statement,
            answer: editForm.answer,
          },
        }),
      });
      setModalCard(null);
      setModalCardInfo(null);
      setEditForm(null);
      setEditErrors({});
      setCreateMode(false);
      setCreateCell(null);
      // Перезагружаем данные
      window.location.reload();
    } catch (error) {
      let msg = 'Ошибка создания';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setEditErrors({ general: msg });
    }
    setModalLoading(false);
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
              try {
                await makeRequest(`${config.backendUrl}api/v1/quiz-field/`, {
                  method: 'PATCH',
                  body: JSON.stringify({
                    quiz_field_id: data.quizFieldId,
                    number_of_rows: rows,
                    number_of_columns: cols,
                  }),
                });
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
                            cursor: 'pointer',
                            position: 'relative',
                          }}
                          onClick={() => handleCardClick(card, rowIdx, colIdx)}
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
          {modalCard !== null && (
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
              onClick={() => { setModalCard(null); setModalCardInfo(null); setEditForm(null); setEditErrors({}); }}
            >
              <div style={{ background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, position: 'relative', maxWidth: 500 }} onClick={e => e.stopPropagation()}>
                <h2>Информация о карточке</h2>
                {modalLoading && <div>Загрузка...</div>}
                {!modalLoading && modalCardInfo && (
                  modalCardInfo.error ? (
                    <div style={{ color: 'red' }}>{modalCardInfo.error}</div>
                  ) : (
                    <form onSubmit={e => { e.preventDefault(); handleEditSave(); }}>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500 }}>Название категории:</label>
                        <input
                          type="text"
                          value={editForm?.categoryName || ''}
                          maxLength={32}
                          onChange={e => setEditForm(f => ({ ...f, categoryName: e.target.value }))}
                          style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc' }}
                        />
                        {editErrors.categoryName && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryName}</div>}
                      </div>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500 }}>Цена:</label>
                        <input
                          type="number"
                          min={0}
                          max={10000}
                          value={editForm?.categoryPrice}
                          onChange={e => setEditForm(f => ({ ...f, categoryPrice: Number(e.target.value) }))}
                          style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc' }}
                        />
                        {editErrors.categoryPrice && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryPrice}</div>}
                      </div>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500 }}>Условие задачи:</label>
                        <textarea
                          value={editForm?.statement || ''}
                          maxLength={2048}
                          onChange={e => setEditForm(f => ({ ...f, statement: e.target.value }))}
                          style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc', minHeight: 60 }}
                        />
                        {editErrors.statement && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.statement}</div>}
                      </div>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500 }}>Ответ:</label>
                        <input
                          type="text"
                          value={editForm?.answer || ''}
                          maxLength={32}
                          onChange={e => setEditForm(f => ({ ...f, answer: e.target.value }))}
                          style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc' }}
                        />
                        {editErrors.answer && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.answer}</div>}
                      </div>
                      {editErrors.global && <div style={{ color: 'red', marginBottom: 8 }}>{editErrors.global}</div>}
                      <button
                        type="submit"
                        disabled={editSaving}
                        style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: '#1677ff', color: '#fff', border: 'none', cursor: 'pointer' }}
                      >
                        {editSaving ? 'Сохранение...' : 'Сохранить'}
                      </button>
                    </form>
                  )
                )}
                {!modalLoading && !modalCardInfo && (
                  <pre style={{ background: '#f7f7f7', padding: 12, borderRadius: 4 }}>{JSON.stringify(modalCard, null, 2)}</pre>
                )}
                <button style={{ marginTop: 16 }} onClick={() => { setModalCard(null); setModalCardInfo(null); setEditForm(null); setEditErrors({}); }}>Закрыть</button>
              </div>
            </div>
          )}
          {/* Модалка создания новой карточки */}
          {createMode && (
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
              onClick={() => { setCreateMode(false); setCreateCell(null); setEditForm(null); setEditErrors({}); }}
            >
              <div style={{ background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, position: 'relative', maxWidth: 500 }} onClick={e => e.stopPropagation()}>
                <h2>Создание карточки</h2>
                <form onSubmit={e => { e.preventDefault(); handleCreateSave(); }}>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500 }}>Название категории:</label>
                    <input
                      type="text"
                      value={editForm?.categoryName || ''}
                      maxLength={32}
                      onChange={e => setEditForm(f => ({ ...f, categoryName: e.target.value }))}
                      style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc' }}
                    />
                    {editErrors.categoryName && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryName}</div>}
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500 }}>Цена:</label>
                    <input
                      type="number"
                      min={0}
                      max={10000}
                      value={editForm?.categoryPrice}
                      onChange={e => setEditForm(f => ({ ...f, categoryPrice: Number(e.target.value) }))}
                      style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc' }}
                    />
                    {editErrors.categoryPrice && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryPrice}</div>}
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500 }}>Условие задачи:</label>
                    <textarea
                      value={editForm?.statement || ''}
                      maxLength={2048}
                      onChange={e => setEditForm(f => ({ ...f, statement: e.target.value }))}
                      style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc', minHeight: 60 }}
                    />
                    {editErrors.statement && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.statement}</div>}
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500 }}>Ответ:</label>
                    <input
                      type="text"
                      value={editForm?.answer || ''}
                      maxLength={32}
                      onChange={e => setEditForm(f => ({ ...f, answer: e.target.value }))}
                      style={{ width: '100%', padding: 6, borderRadius: 4, border: '1px solid #ccc' }}
                    />
                    {editErrors.answer && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.answer}</div>}
                  </div>
                  {editErrors.global && <div style={{ color: 'red', marginBottom: 8 }}>{editErrors.global}</div>}
                  <button
                    type="submit"
                    disabled={editSaving}
                    style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: '#1677ff', color: '#fff', border: 'none', cursor: 'pointer' }}
                  >
                    {editSaving ? 'Создание...' : 'Создать'}
                  </button>
                </form>
                <button style={{ marginTop: 16 }} onClick={() => { setCreateMode(false); setCreateCell(null); setEditForm(null); setEditErrors({}); }}>Закрыть</button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default EditQuizField; 