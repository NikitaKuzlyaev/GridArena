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
  const [editForm, setEditForm] = useState({ username: '', name: '', points: '' });
  const [editModalError, setEditModalError] = useState(null);
  const [editSaving, setEditSaving] = useState(false);
  const [editLoading, setEditLoading] = useState(false);
  const [editId, setEditId] = useState(null);

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

  const handleOpenEditModal = async (contestantId) => {
    setEditModalError(null);
    setEditLoading(true);
    setEditId(contestantId);
    setShowModal('edit-' + contestantId);
    const token = localStorage.getItem('access_token');
    try {
      const res = await fetch(`${config.backendUrl}api/v1/contestant/info-editor?contestant_id=${contestantId}`, {
        method: 'GET',
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
        },
        credentials: 'include',
      });
      const data = await res.json();
      if (!res.ok) {
        setEditModalError(data && data.detail ? data.detail : 'Ошибка загрузки');
        setEditLoading(false);
        return;
      }
      setEditForm({
        username: data.username || '',
        name: data.name || '',
        points: data.points !== undefined ? String(data.points) : '',
      });
      setEditLoading(false);
    } catch {
      setEditModalError('Ошибка сети');
      setEditLoading(false);
    }
  };

  const handleEditFormChange = e => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleEditSave = async () => {
    setEditModalError(null);
    setEditSaving(true);
    const token = localStorage.getItem('access_token');
    try {
      const response = await fetch(`${config.backendUrl}api/v1/contestant`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
        },
        credentials: 'include',
        body: JSON.stringify({
          contestant_id: editId,
          username: editForm.username,
          name: editForm.name,
          points: Number(editForm.points),
        }),
      });
      const data = await response.json();
      setEditSaving(false);
      if (!response.ok) {
        let msg = data && data.detail ? data.detail : response.statusText;
        setEditModalError(msg);
        return;
      }
      setShowModal(false);
      setEditId(null);
      fetchContestants();
    } catch (err) {
      setEditSaving(false);
      setEditModalError('Ошибка сети');
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
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {Array.isArray(data?.body) && data.body.length > 0 ? data.body.map(contestant => (
          <div key={contestant.contestantId} style={{
            background: '#f6f8fa',
            borderRadius: 8,
            padding: 16,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 1px 4px rgba(0,0,0,0.04)',
          }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <div><b>ID:</b> {contestant.contestantId}</div>
              <div><b>Username:</b> {contestant.username}</div>
              <div><b>Имя:</b> {contestant.name}</div>
              <div><b>Баллы:</b> {contestant.points}</div>
            </div>
            <button
              style={{
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: 8,
                marginLeft: 12,
                borderRadius: 4,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'background 0.2s',
              }}
              onClick={() => handleOpenEditModal(contestant.contestantId)}
              title="Редактировать"
            >
              {/* SVG иконка карандаша */}
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M14.846 2.439a2.25 2.25 0 0 1 3.182 3.183l-1.06 1.06-3.183-3.182 1.06-1.06ZM2.5 15.293l9.546-9.546 3.182 3.182-9.545 9.546H2.5v-3.182Z" stroke="#21a1f3" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/></svg>
            </button>
            {/* Модальное окно для редактирования участника */}
            {showModal === 'edit-' + contestant.contestantId && (
              <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
                <div style={{ background: '#fff', padding: 32, borderRadius: 8, minWidth: 320, boxShadow: '0 2px 16px rgba(0,0,0,0.15)' }}>
                  <h2 style={{ marginTop: 0 }}>Редактировать участника</h2>
                  {editLoading ? (
                    <div style={{ minHeight: 60 }}>Загрузка...</div>
                  ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                      <input name="username" placeholder="Username" value={editForm.username} onChange={handleEditFormChange} style={{ padding: 8 }} />
                      <input name="name" placeholder="Имя" value={editForm.name} onChange={handleEditFormChange} style={{ padding: 8 }} />
                      <input name="points" type="number" placeholder="Баллы" value={editForm.points} onChange={handleEditFormChange} style={{ padding: 8 }} />
                      {editModalError && <div style={{ color: 'red', marginTop: 4 }}>{editModalError}</div>}
                      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 8 }}>
                        <button onClick={() => { setShowModal(false); setEditId(null); }} style={{ padding: '8px 16px', background: '#eee', border: 'none', borderRadius: 4 }}>Отмена</button>
                        <button onClick={handleEditSave} style={{ padding: '8px 16px', background: '#21a1f3', color: '#fff', border: 'none', borderRadius: 4 }} disabled={editSaving}>
                          {editSaving ? 'Сохранение...' : 'Сохранить'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )) : <div style={{ color: '#888', textAlign: 'center' }}>Нет участников</div>}
      </div>
      {/* Модальное окно для добавления участника */}
      {showModal === true && (
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