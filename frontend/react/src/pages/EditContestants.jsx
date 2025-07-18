import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import config from '../config';

function EditContestants() {
  const location = useLocation();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ username: '', password: '', name: '', points: '' });
  const [modalError, setModalError] = useState(null);
  const [saving, setSaving] = useState(false);

  // Получаем contest_id из query
  const searchParams = new URLSearchParams(location.search);
  const contestId = searchParams.get('contest_id');

  const fetchContestants = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('access_token');
    fetch(`${config.backendUrl}api/v1/contestant?contest_id=${contestId}`, {
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
          setError(msg);
          setLoading(false);
          return;
        }
        const data = await res.json();
        setData(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Ошибка сети');
        setLoading(false);
      });
  };

  useEffect(() => {
    if (!contestId) {
      setError('contest_id не передан в URL');
      setLoading(false);
      return;
    }
    fetchContestants();
    // eslint-disable-next-line
  }, [contestId]);

  const handleOpenModal = () => {
    setForm({ username: '', password: '', name: '', points: '' });
    setModalError(null);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setModalError(null);
  };

  const handleFormChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    setModalError(null);
    setSaving(true);
    const token = localStorage.getItem('access_token');
    try {
      const response = await fetch(`${config.backendUrl}api/v1/contestant`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        credentials: 'include',
        body: JSON.stringify({
          username: form.username,
          password: form.password,
          name: form.name,
          points: Number(form.points),
          contest_id: Number(contestId),
        }),
      });
      const data = await response.json();
      setSaving(false);
      if (!response.ok) {
        let msg = data && data.detail ? data.detail : response.statusText;
        setModalError(msg);
        return;
      }
      handleCloseModal();
      fetchContestants();
    } catch (err) {
      setSaving(false);
      setModalError('Ошибка сети');
    }
  };

  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: '40px' }}>Загрузка...</div>;
  }
  if (error) {
    return <div style={{ color: 'red', textAlign: 'center', marginTop: '40px' }}>{error}</div>;
  }
  return (
    <div style={{ maxWidth: 600, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
      <h1>Управление участниками</h1>
      <button
        style={{ marginBottom: 20, padding: '8px 16px', background: '#21a1f3', color: '#fff', border: 'none', borderRadius: 4, fontWeight: 500 }}
        onClick={handleOpenModal}
      >
        Добавить участника
      </button>
      <pre style={{ background: '#f6f8fa', padding: 12, borderRadius: 4, overflowX: 'auto' }}>{JSON.stringify(data, null, 2)}</pre>
      {showModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, boxShadow: '0 2px 16px rgba(0,0,0,0.15)' }}>
            <h2 style={{ marginTop: 0 }}>Добавить участника</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <input name="username" placeholder="Username" value={form.username} onChange={handleFormChange} style={{ padding: 8 }} />
              <input name="password" type="password" placeholder="Password" value={form.password} onChange={handleFormChange} style={{ padding: 8 }} />
              <input name="name" placeholder="Имя" value={form.name} onChange={handleFormChange} style={{ padding: 8 }} />
              <input name="points" type="number" placeholder="Баллы" value={form.points} onChange={handleFormChange} style={{ padding: 8 }} />
              {modalError && <div style={{ color: 'red', marginTop: 4 }}>{modalError}</div>}
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 8 }}>
                <button onClick={handleCloseModal} style={{ padding: '8px 16px', background: '#eee', border: 'none', borderRadius: 4 }}>Отмена</button>
                <button onClick={handleSave} style={{ padding: '8px 16px', background: '#21a1f3', color: '#fff', border: 'none', borderRadius: 4 }} disabled={saving}>
                  {saving ? 'Сохранение...' : 'Сохранить'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default EditContestants; 