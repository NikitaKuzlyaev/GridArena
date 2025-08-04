import React, { useState, useRef, useEffect } from 'react';
import './Header.css';
import config from '../config';

function deleteCookie(name) {
  // Удаляем cookie с разными путями и доменами
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + window.location.hostname;
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.' + window.location.hostname;
}

function Header() {
  const [showThemeMenu, setShowThemeMenu] = useState(false);
  const themeBtnRef = useRef(null);
  const themeMenuRef = useRef(null);
  const [selectedTheme, setSelectedTheme] = useState(() => localStorage.getItem('selected_theme') || 'light');
  const [selectedFont, setSelectedFont] = useState(() => localStorage.getItem('selected_font') || 'arial');
  const isAuth = Boolean(localStorage.getItem('access_token'));
  const userType = localStorage.getItem('user_type');
  const isSiteUser = userType === 'SITE';

  useEffect(() => {
    if (!showThemeMenu) return;
    function handleClickOutside(event) {
      if (
        themeMenuRef.current &&
        !themeMenuRef.current.contains(event.target) &&
        themeBtnRef.current &&
        !themeBtnRef.current.contains(event.target)
      ) {
        setShowThemeMenu(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showThemeMenu]);

  // Сохраняем выбранную тему в localStorage при изменении
  useEffect(() => {
    localStorage.setItem('selected_theme', selectedTheme);
  }, [selectedTheme]);
  useEffect(() => {
    localStorage.setItem('selected_font', selectedFont);
  }, [selectedFont]);

  const handleLogout = async () => {
    console.log('Нажата кнопка Выйти');
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) return;
    
    try {
      const response = await fetch(`${config.backendUrl}api/v1/auth/block-my-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ access_token: accessToken }),
        credentials: 'include', // Отправляем cookies автоматически
      });
      console.log('Ответ сервера:', response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (e) {
      console.error('Ошибка при блокировке токена:', e);
      // Можно обработать ошибку, если нужно
    }
    
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_type');
    deleteCookie('refresh_token');
    
    console.log('access_token:', localStorage.getItem('access_token'));
    console.log('refresh_token cookie:', document.cookie);
    window.location.href = '/login';
  };

  return (
    <header className="header">
      <div className="header-left">
        <a href="/" className="header-title">GridArena</a>
        {isAuth && isSiteUser && (
          <a href="/my-contests" className="contests-btn">Мои контесты</a>
        )}
      </div>
      <div className="header-right" style={{ position: 'relative' }}>
        <button
          className="theme-btn"
          ref={themeBtnRef}
          style={{ marginRight: 16, padding: '6px 16px', borderRadius: 6, border: '1px solid #bbb', background: '#f8fafc', cursor: 'pointer' }}
          onClick={() => setShowThemeMenu(m => !m)}
        >
          Тема
        </button>
        {showThemeMenu && (
          <div
            ref={themeMenuRef}
            style={{
              position: 'absolute',
              top: 40,
              right: 90,
              minWidth: 220,
              background: '#fff',
              border: '1px solid #bbb',
              borderRadius: 8,
              boxShadow: '0 4px 16px rgba(0,0,0,0.10)',
              padding: 20,
              zIndex: 100,
            }}
          >
            <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginBottom: 18 }}>
              <button
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: 8,
                  border: selectedTheme === 'light' ? '3px solid #1677ff' : '2px solid #eee',
                  background: '#fff',
                  cursor: 'pointer',
                  boxShadow: selectedTheme === 'light' ? '0 0 0 2px #1677ff33' : 'none',
                }}
                title="Светлая тема"
                onClick={() => { setSelectedTheme('light'); window.location.reload(); }}
              />
              <button
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: 8,
                  border: selectedTheme === 'dark' ? '3px solid #1677ff' : '2px solid #222',
                  background: '#181818',
                  cursor: 'pointer',
                  boxShadow: selectedTheme === 'dark' ? '0 0 0 2px #1677ff33' : 'none',
                }}
                title="Тёмная тема"
                onClick={() => { setSelectedTheme('dark'); window.location.reload(); }}
              />
              <button
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: 8,
                  border: selectedTheme === 'blue' ? '3px solid #1677ff' : '2px solidrgb(0, 0, 255)',
                  background: '#0000ff',
                  cursor: 'pointer',
                  boxShadow: selectedTheme === 'blue' ? '0 0 0 2px #1677ff33' : 'none',
                }}
                title="Синяя тема"
                onClick={() => { setSelectedTheme('blue'); window.location.reload(); }}
              />
              <button
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: 8,
                  border: selectedTheme === 'pink' ? '3px solid #1677ff' : '2px solid #f48fb1',
                  background: '#f8bbd0',
                  cursor: 'pointer',
                  boxShadow: selectedTheme === 'pink' ? '0 0 0 2px #1677ff33' : 'none',
                }}
                title="Розовая тема"
                onClick={() => { setSelectedTheme('pink'); window.location.reload(); }}
              />
            </div>
            <div style={{ fontWeight: 500, marginBottom: 8, textAlign: 'center', fontSize: 15 }}>Шрифт</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              <button
                style={{
                  padding: '6px 0',
                  borderRadius: 6,
                  border: selectedFont === 'arial' ? '2px solid #1677ff' : '1px solid #bbb',
                  background: '#f8fafc',
                  fontFamily: 'Arial, sans-serif',
                  fontWeight: selectedFont === 'arial' ? 700 : 400,
                  color: '#222',
                  cursor: 'pointer',
                }}
                onClick={() => { setSelectedFont('arial'); window.location.reload(); }}
              >Arial</button>
              <button
                style={{
                  padding: '6px 0',
                  borderRadius: 6,
                  border: selectedFont === 'times' ? '2px solid #1677ff' : '1px solid #bbb',
                  background: '#f8fafc',
                  fontFamily: 'Times New Roman, Times, serif',
                  fontWeight: selectedFont === 'times' ? 700 : 400,
                  color: '#222',
                  cursor: 'pointer',
                }}
                onClick={() => { setSelectedFont('times'); window.location.reload(); }}
              >Times New Roman</button>
              <button
                style={{
                  padding: '6px 0',
                  borderRadius: 6,
                  border: selectedFont === 'courier' ? '2px solid #1677ff' : '1px solid #bbb',
                  background: '#f8fafc',
                  fontFamily: 'Courier New, Courier, monospace',
                  fontWeight: selectedFont === 'courier' ? 700 : 400,
                  color: '#222',
                  cursor: 'pointer',
                }}
                onClick={() => { setSelectedFont('courier'); window.location.reload(); }}
              >Courier New</button>
              <button
                style={{
                  padding: '6px 0',
                  borderRadius: 6,
                  border: selectedFont === 'segoe' ? '2px solid #1677ff' : '1px solid #bbb',
                  background: '#f8fafc',
                  fontFamily: 'Segoe UI, Arial, sans-serif',
                  fontWeight: selectedFont === 'segoe' ? 700 : 400,
                  color: '#222',
                  cursor: 'pointer',
                }}
                onClick={() => { setSelectedFont('segoe'); window.location.reload(); }}
              >Segoe UI</button>
              <button
                style={{
                  padding: '6px 0',
                  borderRadius: 6,
                  border: selectedFont === 'varela' ? '2px solid #1677ff' : '1px solid #bbb',
                  background: '#f8fafc',
                  fontFamily: 'Varela Round, Arial, sans-serif',
                  fontWeight: selectedFont === 'varela' ? 700 : 400,
                  color: '#222',
                  cursor: 'pointer',
                }}
                onClick={() => { setSelectedFont('varela'); window.location.reload(); }}
              >Varela Round</button>
              <button
                style={{
                  padding: '6px 0',
                  borderRadius: 6,
                  border: selectedFont === 'jetbrains' ? '2px solid #1677ff' : '1px solid #bbb',
                  background: '#f8fafc',
                  fontFamily: 'JetBrains Mono, Fira Mono, monospace',
                  fontWeight: selectedFont === 'jetbrains' ? 700 : 400,
                  color: '#222',
                  cursor: 'pointer',
                }}
                onClick={() => { setSelectedFont('jetbrains'); window.location.reload(); }}
              >JetBrains Mono</button>
              <button
                style={{
                  padding: '6px 0',
                  borderRadius: 6,
                  border: selectedFont === 'inter' ? '2px solid #1677ff' : '1px solid #bbb',
                  background: '#f8fafc',
                  fontFamily: 'Inter, Segoe UI, Arial, sans-serif',
                  fontWeight: selectedFont === 'inter' ? 700 : 400,
                  color: '#222',
                  cursor: 'pointer',
                }}
                onClick={() => { setSelectedFont('inter'); window.location.reload(); }}
              >Inter</button>
            </div>
          </div>
        )}
        {!isAuth ? (
          <a href="/login" className="login-btn">Войти</a>
        ) : (
          <button className="login-btn" onClick={handleLogout}>Выйти</button>
        )}
      </div>
    </header>
  );
}

export default Header;
