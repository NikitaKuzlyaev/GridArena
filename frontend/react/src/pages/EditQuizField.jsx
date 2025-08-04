import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';
import { useApi } from '../hooks/useApi';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import Icon from '../components/Icon';

// Error Boundary для ReactMarkdown
class MarkdownErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Markdown parsing error:', error);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.statement !== this.props.statement && this.state.hasError) {
      this.setState({ hasError: false });
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ color: 'red', fontSize: '14px' }}>
          ошибка рендера условия
        </div>
      );
    }

    return this.props.children;
  }
}

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

  // Добавляем CSS стили в head при монтировании компонента
  useEffect(() => {
    const styleElement = document.createElement('style');
    styleElement.textContent = `
      .preview-card {
        background: #ffffff;
        border: 1px solid #bde0fe;
        color: #222;
        border-radius: 10px;
        padding: 18px;
        box-sizing: border-box;
        width: 100%;
        margin: 0 auto;
        position: relative;
        padding-top: 0;
      }
      
      .preview-card .category-info {
        font-size: 15px;
        font-weight: 500;
        color: #7b2ff2;
        margin-bottom: 2px;
      }
      
      .preview-card .date-info {
        font-weight: 400;
        color: #555;
        font-size: 13px;
      }
      
      .preview-card .statement {
        margin-bottom: 16px;
        text-align: left;
        font-size: 14px;
        line-height: 1.6;
      }
      
      .preview-card .answer-input {
        flex: 1;
        padding: 8px;
        border-radius: 2px;
        border: 1px solid #bbb;
        font-size: 14px;
        background: #f5f5f5;
        color: #888;
      }
      
      .preview-card .send-btn {
        width: 36px;
        height: 36px;
        min-width: 36px;
        min-height: 36px;
        max-width: 36px;
        max-height: 36px;
        border-radius: 6px;
        margin-left: 6px;
        transition: background 0.2s;
        outline: 1px dashed rgba(80, 94, 124, 0.5);
        outline-offset: 0px;
        background: #1677ff;
        color: #fff;
        border: none;
        cursor: default;
        opacity: 0.6;
      }
    `;
    document.head.appendChild(styleElement);

    // Удаляем стили при размонтировании
    return () => {
      document.head.removeChild(styleElement);
    };
  }, []);

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
        categoryName: '',
        categoryPrice: 0,
        statement: '',
        answer: '',
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
          problemId: modalCardInfo.problem.problemId, // Добавляем problemId
          categoryName: editForm.categoryName,
          categoryPrice: Number(editForm.categoryPrice),
          statement: editForm.statement, // Выносим на верхний уровень
          answer: editForm.answer, // Выносим на верхний уровень
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
          quizFieldId: data.quizFieldId, // Добавляем quizFieldId
          row: createCell.row,
          column: createCell.col,
          categoryName: editForm.categoryName,
          categoryPrice: Number(editForm.categoryPrice),
          statement: editForm.statement, // Выносим на верхний уровень
          answer: editForm.answer, // Выносим на верхний уровень
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
                             <div style={{ 
                 background: '#fff',
                  padding: 16,
                  boxSizing: 'border-box',
                   borderRadius: 8,
                    minWidth: '50%', 
                    maxHeight: '90vh',
                    position: 'relative', 
                    maxWidth: '50%',
                    overflowY: 'auto',
                 }} onClick={e => e.stopPropagation()}>
                <h2>Информация о карточке</h2>
                {modalLoading && <div>Загрузка...</div>}
                {!modalLoading && modalCardInfo && (
                  modalCardInfo.error ? (
                    <div style={{ color: 'red' }}>{modalCardInfo.error}</div>
                  ) : (
                    <form onSubmit={e => { e.preventDefault(); handleEditSave(); }}>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500, textAlign: 'left', }}>Название категории:</label>
                        <input
                          type="text"
                          value={editForm?.categoryName || ''}
                          maxLength={32}
                          onChange={e => setEditForm(f => ({ ...f, categoryName: e.target.value }))}
                          style={{ width: '25%', padding: 6, borderRadius: 4, border: '1px solid #ccc', display:'block', }}
                        />
                        {editErrors.categoryName && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryName}</div>}
                      </div>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500, textAlign: 'left',}}>Цена:</label>
                        <input
                          type="number"
                          min={0}
                          max={10000}
                          value={editForm?.categoryPrice}
                          onChange={e => setEditForm(f => ({ ...f, categoryPrice: Number(e.target.value) }))}
                          style={{ width: '25%', padding: 6, borderRadius: 4, border: '1px solid #ccc', display:'block', }}
                        />
                        {editErrors.categoryPrice && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryPrice}</div>}
                      </div>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500, textAlign:'left', }}>Условие задачи:</label>
                        <textarea
                          value={editForm?.statement || ''}
                          maxLength={2048}
                          onChange={e => setEditForm(f => ({ ...f, statement: e.target.value }))}
                          style={{ width: '75%', padding: 6, borderRadius: 4, border: '1px solid #ccc', minHeight: 120, display:'block', }}
                        />
                        {editErrors.statement && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.statement}</div>}
                      </div>
                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500, textAlign:'left',  }}>Ответ:</label>
                        <input
                          type="text"
                          value={editForm?.answer || ''}
                          maxLength={32}
                          onChange={e => setEditForm(f => ({ ...f, answer: e.target.value }))}
                          style={{ width: '25%', padding: 6, borderRadius: 4, border: '1px solid #ccc', display:'block', }}
                        />
                        {editErrors.answer && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.answer}</div>}
                      </div>


                      <div style={{ marginBottom: 12 }}>
                        <label style={{ display: 'block', fontWeight: 500, textAlign:'left',  }}>Предпросмотр:</label>

                        <div className="preview-card" style={{width: '75%', display:'block',}}>
                          {/* Верхний flex-блок: категория, дата */}
                          <div style={{
                            display: 'flex', 
                            justifyContent: 'space-between',
                            alignItems: 'flex-start', 
                            marginBottom: 16, 
                            marginTop: 16,
                          }}>
                            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                              <div className="category-info">
                                {editForm?.categoryName && editForm?.categoryPrice ? 
                                  `${editForm.categoryName} за ${editForm.categoryPrice}` : 
                                  'Название категории'
                                }
                              </div>
                              <div className="date-info">
                                {new Date().toLocaleString()}
                              </div>
                            </div>
                          </div>
                          
                          {/* Условие задачи */}
                          <div className="statement">
                            {editForm?.statement ? (
                              <MarkdownErrorBoundary statement={editForm?.statement}>
                                <ReactMarkdown
                                  remarkPlugins={[remarkMath]}
                                  rehypePlugins={[rehypeKatex]}
                                >
                                  {typeof editForm?.statement === 'string' ? editForm.statement : ''}
                                </ReactMarkdown>
                              </MarkdownErrorBoundary>
                            ) : (
                              <div style={{ color: '#888', fontStyle: 'italic' }}>
                                Условие задачи не указано
                              </div>
                            )}
                          </div>
                          
                          {/* Поле для ответа */}
                          <div style={{ display: 'flex', gap: 12 }}>
                            <input
                              type="text"
                              placeholder="Ваш ответ"
                              disabled
                              className="answer-input"
                            />
                            <button
                              className="send-btn"
                              disabled
                              title="Предпросмотр"
                            >
                              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 512 512" version="1.1"><path d="M 330.027 181.570 C 231.866 231.882, 151.243 273.374, 150.863 273.773 C 150.483 274.173, 156.197 307.800, 163.560 348.500 C 170.922 389.200, 176.958 422.838, 176.973 423.251 C 177.006 424.156, 281 354.951, 281 354.024 C 281 353.668, 265.725 343.504, 247.055 331.438 C 228.385 319.372, 213.198 309.174, 213.305 308.777 C 213.412 308.379, 278.750 260.084, 358.500 201.456 C 503.398 94.933, 509.937 90.094, 509 90.094 C 508.725 90.094, 428.187 131.258, 330.027 181.570" stroke="none" fill-rule="evenodd"/><path d="M 255.749 140.925 C 115.635 169.934, 0.767 193.900, 0.484 194.182 C 0.202 194.464, 33.732 212.502, 74.996 234.265 L 150.020 273.836 304.260 194.845 C 507.201 90.913, 509.989 89.501, 506.500 92.381 C 504.850 93.743, 438.250 142.827, 358.500 201.456 C 278.750 260.084, 213.413 308.379, 213.307 308.777 C 213.200 309.174, 227.779 318.950, 245.704 330.500 C 263.629 342.050, 279.466 352.455, 280.897 353.621 C 282.329 354.788, 307.125 371.099, 336 389.868 L 388.500 423.994 389.856 420.747 C 392.409 414.632, 512 89.644, 512 88.821 C 512 88.370, 511.663 88.041, 511.250 88.090 C 510.837 88.140, 395.862 111.916, 255.749 140.925" stroke="none" fill-rule="evenodd"/></svg>
                            </button>
                          </div>
                        </div>
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
              background: 'rgba(0, 0, 0, 0.30)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 999,
            }}
              onClick={() => { setCreateMode(false); setCreateCell(null); setEditForm(null); setEditErrors({}); }}
            >
              <div style={{ 
                 background: '#fff',
                 padding: 16,
                 boxSizing: 'border-box',
                  borderRadius: 8,
                   minWidth: '50%', 
                   maxHeight: '90vh',
                   position: 'relative', 
                   maxWidth: '50%',
                   overflowY: 'auto',
               }} onClick={e => e.stopPropagation()}>
                <h2>Создание карточки</h2>
                <form onSubmit={e => { e.preventDefault(); handleCreateSave(); }}>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500, textAlign: 'left', }}>Название категории:</label>
                    <input
                      type="text"
                      value={editForm?.categoryName || ''}
                      maxLength={32}
                      onChange={e => setEditForm(f => ({ ...f, categoryName: e.target.value }))}
                      style={{ width: '25%', padding: 6, borderRadius: 4, border: '1px solid #ccc', display:'block', }}
                    />
                    {editErrors.categoryName && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryName}</div>}
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500, textAlign:'left', }}>Цена:</label>
                    <input
                      type="number"
                      min={0}
                      max={10000}
                      value={editForm?.categoryPrice}
                      onChange={e => setEditForm(f => ({ ...f, categoryPrice: Number(e.target.value) }))}
                      style={{ width: '25%', padding: 6, borderRadius: 4, border: '1px solid #ccc', display:'block', }}
                    />
                    {editErrors.categoryPrice && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.categoryPrice}</div>}
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500, textAlign:'left', }}>Условие задачи:</label>
                    <textarea
                      value={editForm?.statement || ''}
                      maxLength={2048}
                      onChange={e => setEditForm(f => ({ ...f, statement: e.target.value }))}
                      style={{ width: '75%', padding: 6, borderRadius: 4, border: '1px solid #ccc', minHeight: 60, display: 'block', }}
                    />
                    {editErrors.statement && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.statement}</div>}
                  </div>
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500, textAlign: 'left', }}>Ответ:</label>
                    <input
                      type="text"
                      value={editForm?.answer || ''}
                      maxLength={32}
                      onChange={e => setEditForm(f => ({ ...f, answer: e.target.value }))}
                      style={{ width: '25%', padding: 6, borderRadius: 4, border: '1px solid #ccc', display:'block', }}
                    />
                    {editErrors.answer && <div style={{ color: 'red', fontSize: 13 }}>{editErrors.answer}</div>}
                  </div>
                  
                  <div style={{ marginBottom: 12 }}>
                    <label style={{ display: 'block', fontWeight: 500, textAlign:'left', }}>Предпросмотр:</label>
                    <div className="preview-card" style={{width: '80%', }}>
                      {/* Верхний flex-блок: категория, дата */}
                      <div style={{
                        display: 'flex', 
                        justifyContent: 'space-between',
                        alignItems: 'flex-start', 
                        marginBottom: 16, 
                        marginTop: 16,
                      }}>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                          <div className="category-info">
                            {editForm?.categoryName && editForm?.categoryPrice ? 
                              `${editForm.categoryName} за ${editForm.categoryPrice}` : 
                              'Категория не указана'
                            }
                          </div>
                          <div className="date-info">
                            {new Date().toLocaleString()}
                          </div>
                        </div>
                      </div>
                      
                      {/* Условие задачи */}
                      <div className="statement">
                        {editForm?.statement ? (
                          <MarkdownErrorBoundary statement={editForm?.statement}>
                            <ReactMarkdown
                              remarkPlugins={[remarkMath]}
                              rehypePlugins={[rehypeKatex]}
                            >
                              {typeof editForm?.statement === 'string' ? editForm.statement : ''}
                            </ReactMarkdown>
                          </MarkdownErrorBoundary>
                        ) : (
                          <div style={{ color: '#888', fontStyle: 'italic' }}>
                            Условие задачи не указано
                          </div>
                        )}
                      </div>
                      
                      {/* Поле для ответа */}
                      <div style={{ display: 'flex', gap: 12 }}>
                        <input
                          type="text"
                          placeholder="Ваш ответ"
                          disabled
                          className="answer-input"
                        />
                        <button
                          className="send-btn"
                          disabled
                          title="Предпросмотр"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 512 512" version="1.1"><path d="M 330.027 181.570 C 231.866 231.882, 151.243 273.374, 150.863 273.773 C 150.483 274.173, 156.197 307.800, 163.560 348.500 C 170.922 389.200, 176.958 422.838, 176.973 423.251 C 177.006 424.156, 281 354.951, 281 354.024 C 281 353.668, 265.725 343.504, 247.055 331.438 C 228.385 319.372, 213.198 309.174, 213.305 308.777 C 213.412 308.379, 278.750 260.084, 358.500 201.456 C 503.398 94.933, 509.937 90.094, 509 90.094 C 508.725 90.094, 428.187 131.258, 330.027 181.570" stroke="none" fill-rule="evenodd"/><path d="M 255.749 140.925 C 115.635 169.934, 0.767 193.900, 0.484 194.182 C 0.202 194.464, 33.732 212.502, 74.996 234.265 L 150.020 273.836 304.260 194.845 C 507.201 90.913, 509.989 89.501, 506.500 92.381 C 504.850 93.743, 438.250 142.827, 358.500 201.456 C 278.750 260.084, 213.413 308.379, 213.307 308.777 C 213.200 309.174, 227.779 318.950, 245.704 330.500 C 263.629 342.050, 279.466 352.455, 280.897 353.621 C 282.329 354.788, 307.125 371.099, 336 389.868 L 388.500 423.994 389.856 420.747 C 392.409 414.632, 512 89.644, 512 88.821 C 512 88.370, 511.663 88.041, 511.250 88.090 C 510.837 88.140, 395.862 111.916, 255.749 140.925" stroke="none" fill-rule="evenodd"/></svg>
                        </button>
                      </div>
                    </div>
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