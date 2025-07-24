import React, { useEffect, useState, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import './SolveContest.css';
import FallingFlowers from './FallingFlowers';
import pinkGif from './pink-gif.gif';
import pinkGif2 from './pink-gif-2.gif';

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
  const [holdProgress, setHoldProgress] = useState({}); // для анимации удержания
  const holdTimeouts = useRef({});
  const holdIntervals = useRef({});
  const [contestantInfo, setContestantInfo] = useState(null);

  // Определяем класс для фона в зависимости от темы
  const theme = localStorage.getItem('selected_theme') || 'light';
  const bgClass = `solve-bg solve-bg--${theme}`;

  // Drag and drop для стикера
  const [stickerPos, setStickerPos] = useState(() => {
    const saved = localStorage.getItem('pinkStickerPos');
    return saved ? JSON.parse(saved) : { left: 24, bottom: 24 };
  });
  const [dragging, setDragging] = useState(false);
  const dragOffset = useRef({ x: 0, y: 0 });
  const stickerRef = useRef(null);
  const stickerSize = 180;

  // Drag and drop для второго стикера
  const [sticker2Pos, setSticker2Pos] = useState(() => {
    const saved = localStorage.getItem('pinkSticker2Pos');
    return saved ? JSON.parse(saved) : { right: 24, bottom: 24 };
  });
  const [dragging2, setDragging2] = useState(false);
  const drag2Offset = useRef({ x: 0, y: 0 });
  const sticker2Ref = useRef(null);
  const sticker2Size = 90;

  useEffect(() => {
    if (!dragging) return;
    function onMove(e) {
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      const winW = window.innerWidth, winH = window.innerHeight;
      let left = clientX - dragOffset.current.x;
      let top = clientY - dragOffset.current.y;
      // Ограничения, чтобы стикер не выходил за экран
      left = Math.max(0, Math.min(left, winW - stickerSize));
      top = Math.max(0, Math.min(top, winH - stickerSize));
      setStickerPos({ left, top });
    }
    function onUp() {
      setDragging(false);
      localStorage.setItem('pinkStickerPos', JSON.stringify(stickerPos));
    }
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    window.addEventListener('touchmove', onMove);
    window.addEventListener('touchend', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
      window.removeEventListener('touchmove', onMove);
      window.removeEventListener('touchend', onUp);
    };
  }, [dragging, stickerPos]);

  useEffect(() => {
    if (!dragging2) return;
    function onMove(e) {
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      const winW = window.innerWidth, winH = window.innerHeight;
      let right = winW - clientX - (sticker2Size - drag2Offset.current.x);
      let top = clientY - drag2Offset.current.y;
      right = Math.max(0, Math.min(right, winW - sticker2Size));
      top = Math.max(0, Math.min(top, winH - sticker2Size));
      setSticker2Pos({ right, top });
    }
    function onUp() {
      setDragging2(false);
      localStorage.setItem('pinkSticker2Pos', JSON.stringify(sticker2Pos));
    }
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    window.addEventListener('touchmove', onMove);
    window.addEventListener('touchend', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
      window.removeEventListener('touchmove', onMove);
      window.removeEventListener('touchend', onUp);
    };
  }, [dragging2, sticker2Pos]);

  function startDrag(e) {
    setDragging(true);
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const rect = stickerRef.current.getBoundingClientRect();
    dragOffset.current = {
      x: clientX - rect.left,
      y: clientY - rect.top,
    };
    e.preventDefault();
  }

  function startDrag2(e) {
    setDragging2(true);
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const rect = sticker2Ref.current.getBoundingClientRect();
    drag2Offset.current = {
      x: clientX - rect.left,
      y: clientY - rect.top,
    };
    e.preventDefault();
  }

  useEffect(() => {
    // Имитация загрузки
    // setTimeout(() => {
    //   setLoading(false);
    // }, 1);
    setLoading(false);
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
      .then(async res => {
        if (res.ok) {
          const data = await res.json();
          setContestantInfo(data);
        }
      })
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
      <p>загрузка</p>
      // <div className={bgClass} style={{ minHeight: '100vh', width: '100vw', position: 'relative' }}>
      //   {theme === 'pink' && <FallingFlowers />}
      //   {theme === 'pink' && (
      //     <img
      //       ref={stickerRef}
      //       src={pinkGif}
      //       alt="pink sticker"
      //       style={{
      //         position: 'fixed',
      //         width: stickerSize,
      //         height: stickerSize,
      //         zIndex: 10,
      //         cursor: 'grab',
      //         bottom: stickerPos.bottom,
      //         left: stickerPos.left,
      //         top: stickerPos.top,
      //         ...(stickerPos.left !== undefined && stickerPos.top !== undefined
      //           ? { right: undefined, bottom: undefined }
      //           : {}),
      //         userSelect: 'none',
      //         touchAction: 'none',
      //       }}
      //       onMouseDown={startDrag}
      //       onTouchStart={startDrag}
      //       draggable={false}
      //     />
      //   )}
      //   {theme === 'pink' && (
      //     <img
      //       ref={sticker2Ref}
      //       src={pinkGif2}
      //       alt="pink sticker 2"
      //       style={{
      //         position: 'fixed',
      //         width: sticker2Size,
      //         height: sticker2Size,
      //         zIndex: 10,
      //         cursor: 'grab',
      //         bottom: sticker2Pos.bottom,
      //         right: sticker2Pos.right,
      //         top: sticker2Pos.top,
      //         ...(sticker2Pos.right !== undefined && sticker2Pos.top !== undefined
      //           ? { left: undefined, bottom: undefined }
      //           : {}),
      //         userSelect: 'none',
      //         touchAction: 'none',
      //       }}
      //       onMouseDown={startDrag2}
      //       onTouchStart={startDrag2}
      //       draggable={false}
      //     />
      //   )}
      //   <div style={{
      //     maxWidth: 800,
      //     margin: '40px auto',
      //     padding: '40px',
      //     textAlign: 'center',
      //     background: '#fff',
      //     borderRadius: '12px',
      //     boxShadow: '0 4px 16px rgba(0,0,0,0.1)'
      //   }}>
      //     <div style={{ fontSize: '24px', marginBottom: '16px' }}>⏳</div>
      //     <div style={{ fontSize: '18px' }}>Загрузка соревнования...</div>
      //   </div>
      // </div>
    );
  }

  return (
    <div className={bgClass} style={{ minHeight: '100vh', width: '100vw', position: 'relative' }}>
      {theme === 'pink' && <FallingFlowers />}
      {theme === 'pink' && (
        <img
          ref={stickerRef}
          src={pinkGif}
          alt="pink sticker"
          style={{
            position: 'fixed',
            width: stickerSize,
            height: stickerSize,
            zIndex: 10,
            cursor: 'grab',
            bottom: stickerPos.bottom,
            left: stickerPos.left,
            top: stickerPos.top,
            ...(stickerPos.left !== undefined && stickerPos.top !== undefined
              ? { right: undefined, bottom: undefined }
              : {}),
            userSelect: 'none',
            touchAction: 'none',
          }}
          onMouseDown={startDrag}
          onTouchStart={startDrag}
          draggable={false}
        />
      )}
      {theme === 'pink' && (
        <img
          ref={sticker2Ref}
          src={pinkGif2}
          alt="pink sticker 2"
          style={{
            position: 'fixed',
            width: sticker2Size,
            height: sticker2Size,
            zIndex: 10,
            cursor: 'grab',
            bottom: sticker2Pos.bottom,
            right: sticker2Pos.right,
            top: sticker2Pos.top,
            ...(sticker2Pos.right !== undefined && sticker2Pos.top !== undefined
              ? { left: undefined, bottom: undefined }
              : {}),
            userSelect: 'none',
            touchAction: 'none',
          }}
          onMouseDown={startDrag2}
          onTouchStart={startDrag2}
          draggable={false}
        />
      )}
      <div className="solve-contest-root" style={{
        maxWidth: 1100,
        margin: '0px auto',
        padding: '0px',
        display: 'flex',
        flexDirection: 'row',
        gap: 32,
        alignItems: 'flex-start',
      }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          {/* основной контент */}
          <h1 style={{
            textAlign: 'left',
            marginBottom: '12px',
            fontSize: '28px'
          }}>
            🏆 Соревнование #{contestId}
          </h1>

          {fieldData ? (
            <div style={{ overflowX: 'auto', marginBottom: 16 }}>
              <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                <tbody>
                  {[...Array(fieldData.numberOfRows)].map((_, rowIdx) => (
                    <tr key={rowIdx}>
                      {[...Array(fieldData.numberOfColumns)].map((_, colIdx) => {
                        const card = getCardAt(rowIdx + 1, colIdx + 1);
                        const clickable = card && card.isOpenForBuy;
                        const is_closed_card = card && card.status=='CLOSED';
                        return (
                          <td
                            key={colIdx}
                            className={`problem-card${card ? ` problem-card--${card.status}` : ''}`}
                            style={{
                              border: '3px solid #fff',
                              width: 120,
                              minWidth: 120,
                              maxWidth: 120,
                              height: 80,
                              textAlign: 'center',
                              verticalAlign: 'middle',
                              cursor: clickable ? 'pointer' : 'default',
                              opacity: is_closed_card? 0.5 : 1,
                              position: 'relative',
                              overflow: 'hidden',
                              whiteSpace: 'nowrap',
                              textOverflow: 'ellipsis',
                              fontSize: 14,
                            }}
                            onClick={() => {
                              if (clickable) setModalCard(card);
                            }}
                          >
                            {card ? (
                              <div>
                                {/* <div><b>ID:</b> {card.problem.problemId}</div> */}
                                {/* <div><b>{card.categoryName}</b></div> */}
                                <div>{card.categoryName}</div>
                                <div>{card.categoryPrice}</div>
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
            <div style={{ textAlign: 'center', margin: '32px 0' }}>Нет данных о поле</div>
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
                {buyError && <div style={{ marginBottom: 12 }}>{buyError}</div>}
                <div style={{ display: 'flex', gap: 16 }}>
                  <button
                    style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: buying ? '#90caf9' : '#1677ff', border: 'none', cursor: buying ? 'not-allowed' : 'pointer' }}
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
                    style={{ padding: '8px 24px', fontSize: 16, borderRadius: 6, background: '#eee', border: '1px solid #ccc', cursor: buying ? 'not-allowed' : 'pointer' }}
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
            <div style={{ marginTop: 16 }}>
              <h2 style={{ fontSize: 20, marginBottom: 16, textAlign: 'left', }}>Купленные задачи</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 64, }}>
                {myProblems.map(problem => (
                  <div key={problem.selectedProblemId}
                    className={`bought-problem-card bought-problem-card--${problem.status}`}
                    style={{
                      borderRadius: 10,
                      padding: 24,
                      maxWidth: 800,
                      margin: '0 auto',
                    }}>
                    <div style={{ marginBottom: 36, fontWeight: 500 }}>
                      {/* <span style={{ opacity: 0.7, fontSize: 13 }}>ID: {problem.selectedProblemId}</span> */}
                      <span style={{ float: 'right', opacity: 0.5, fontSize: 13 }}>{new Date(problem.createdAt).toLocaleString()}</span>
                    </div>
                    <div style={{ marginBottom: 16, textAlign: 'left', fontSize: 14, lineHeight: 1.6 }}>
                      <ReactMarkdown
                        remarkPlugins={[remarkMath]}
                        rehypePlugins={[rehypeKatex]}
                      >
                        {problem.problem?.statement || 'Нет условия'}
                      </ReactMarkdown>
                    </div>
                    <div style={{ display: 'flex', gap: 12 }}>
                      <input
                        type="text"
                        placeholder="Ваш ответ"
                        value={answers[problem.selectedProblemId] || ''}
                        onChange={e => setAnswers(a => ({ ...a, [problem.selectedProblemId]: e.target.value }))}
                        style={{ flex: 1, padding: 8, borderRadius: 2, border: '1px solid #bbb', fontSize: 14 }}
                      />
                      <button
                        className="send-answer-btn"
                        style={{
                          width: 36,
                          height: 36,
                          minWidth: 36,
                          minHeight: 36,
                          maxWidth: 36,
                          maxHeight: 36,
                          borderRadius: 6,
                          marginLeft: 6,
                          transition: 'background 0.2s',
                          outline: '1px dashed rgba(80, 94, 124, 0.5)',
                          outlineOffset: '0px',
                        }}
                        onClick={async () => {
                          const token = localStorage.getItem('access_token');
                          await fetch(`${config.backendUrl}api/v1/submission`, {
                            method: 'POST',
                            headers: {
                              'Authorization': token ? `Bearer ${token}` : '',
                              'Content-Type': 'application/json',
                            },
                            credentials: 'include',
                            body: JSON.stringify({
                              selected_problem_id: problem.selectedProblemId,
                              answer: answers[problem.selectedProblemId] || ''
                            }),
                          });
                          window.location.reload();
                        }}
                        title="Отправить ответ"
                      >
                        {/* SVG самолетика из интернета, адаптирован под размер кнопки */}
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 512 512" version="1.1"><path d="M 330.027 181.570 C 231.866 231.882, 151.243 273.374, 150.863 273.773 C 150.483 274.173, 156.197 307.800, 163.560 348.500 C 170.922 389.200, 176.958 422.838, 176.973 423.251 C 177.006 424.156, 281 354.951, 281 354.024 C 281 353.668, 265.725 343.504, 247.055 331.438 C 228.385 319.372, 213.198 309.174, 213.305 308.777 C 213.412 308.379, 278.750 260.084, 358.500 201.456 C 503.398 94.933, 509.937 90.094, 509 90.094 C 508.725 90.094, 428.187 131.258, 330.027 181.570" stroke="none" fill-rule="evenodd"/><path d="M 255.749 140.925 C 115.635 169.934, 0.767 193.900, 0.484 194.182 C 0.202 194.464, 33.732 212.502, 74.996 234.265 L 150.020 273.836 304.260 194.845 C 507.201 90.913, 509.989 89.501, 506.500 92.381 C 504.850 93.743, 438.250 142.827, 358.500 201.456 C 278.750 260.084, 213.413 308.379, 213.307 308.777 C 213.200 309.174, 227.779 318.950, 245.704 330.500 C 263.629 342.050, 279.466 352.455, 280.897 353.621 C 282.329 354.788, 307.125 371.099, 336 389.868 L 388.500 423.994 389.856 420.747 C 392.409 414.632, 512 89.644, 512 88.821 C 512 88.370, 511.663 88.041, 511.250 88.090 C 510.837 88.140, 395.862 111.916, 255.749 140.925" stroke="none" fill-rule="evenodd"/></svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        <div style={{
          width: 260,
          minWidth: 200,
          background: '#f8fafc',
          border: '0px solid #bde0fe',
          borderRadius: 1,
          boxShadow: '1px 1px 4px #a2d2ff',
          padding: 20,
          marginTop: 70,
          position: 'sticky',
          top: 40,
          height: 'fit-content',
          display: 'flex',
          flexDirection: 'column',
          gap: 12,
        }}>
          <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 8 }}>Информация об участнике</div>
          {contestantInfo ? (
            <div style={{ fontSize: 15, lineHeight: 1.7 }}>
              <div><b>ID:</b> {contestantInfo.contestantId}</div>
              <div><b>Имя:</b> {contestantInfo.contestantName}</div>
              <div><b>Баланс:</b> {contestantInfo.points}</div>
              <div><b>Задач сейчас:</b> {contestantInfo.problemsCurrent} / {contestantInfo.problemsMax}</div>
            </div>
          ) : (
            <div style={{ fontSize: 15 }}>Загрузка...</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SolveContest; 