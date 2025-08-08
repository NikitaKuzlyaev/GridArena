import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import config from '../config';
import { useApi } from '../hooks/useApi';

function EditContestants() {
  const location = useLocation();
  const { makeRequest } = useApi();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ username: '', password: '', contestantName: '', points: '' });
  const [modalError, setModalError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [editForm, setEditForm] = useState({ username: '', password: '', contestantName: '', points: '' });
  const [editModalError, setEditModalError] = useState(null);
  const [editSaving, setEditSaving] = useState(false);
  const [editLoading, setEditLoading] = useState(false);
  const [editId, setEditId] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

  // Получаем contest_id из query
  const searchParams = new URLSearchParams(location.search);
  const contestId = searchParams.get('contest_id');

  // Функция валидации
  const validateForm = (formData, isEdit = false) => {
    const errors = [];
    
    // Валидация username (String(64), nullable=False)
    if (!formData.username || formData.username.trim() === '') {
      errors.push('Username обязателен');
    } else if (formData.username.length > 64) {
      errors.push('Username не может быть длиннее 64 символов');
    }
    
    // Валидация password (только для создания, 3-32 символа)
    if (!isEdit) {
      if (!formData.password || formData.password.trim() === '') {
        errors.push('Password обязателен');
      } else if (formData.password.length < 3 || formData.password.length > 32) {
        errors.push('Password должен быть от 3 до 32 символов');
      }
    } else if (formData.password && (formData.password.length < 3 || formData.password.length > 32)) {
      errors.push('Password должен быть от 3 до 32 символов');
    }
    
    // Валидация contestantName (String(256), nullable=False)
    if (!formData.contestantName || formData.contestantName.trim() === '') {
      errors.push('Имя участника обязательно');
    } else if (formData.contestantName.length > 256) {
      errors.push('Имя участника не может быть длиннее 256 символов');
    }
    
    // Валидация points (Integer, nullable=False, 0-10000)
    if (formData.points === '' || formData.points === null || formData.points === undefined) {
      errors.push('Баллы обязательны');
    } else {
      const pointsNum = Number(formData.points);
      if (isNaN(pointsNum) || !Number.isInteger(pointsNum)) {
        errors.push('Баллы должны быть целым числом');
      } else if (pointsNum < 0 || pointsNum > 10000) {
        errors.push('Баллы должны быть от 0 до 10000');
      }
    }
    
    return errors;
  };

  const fetchContestants = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await makeRequest(`${config.backendUrl}api/v1/contestant?contest_id=${contestId}`);
      setData(data);
      setLoading(false);
    } catch (error) {
      let msg = 'Ошибка загрузки данных';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setError(msg);
      setLoading(false);
    }
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
    setForm({ username: '', password: '', contestantName: '', points: '' });
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
    
    // Валидация
    const validationErrors = validateForm(form, false);
    if (validationErrors.length > 0) {
      setModalError(validationErrors.join(', '));
      return;
    }
    
    setSaving(true);
    try {
      await makeRequest(`${config.backendUrl}api/v1/contestant`, {
        method: 'POST',
                 body: JSON.stringify({
           username: form.username.trim(),
           password: form.password,
           name: form.contestantName.trim(),
           points: Number(form.points),
           contest_id: Number(contestId),
         }),
      });
      setSaving(false);
      handleCloseModal();
      fetchContestants();
    } catch (error) {
      setSaving(false);
      let msg = 'Ошибка сети';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setModalError(msg);
    }
  };

  const handleOpenEditModal = async (contestantId) => {
    setEditModalError(null);
    setEditLoading(true);
    setEditId(contestantId);
    setShowPassword(false); // Сбрасываем состояние показа пароля
    try {
      const data = await makeRequest(`${config.backendUrl}api/v1/contestant/info-editor?contestant_id=${contestantId}`);
      setEditForm({
        username: data.username || '',
        password: data.password || '', // Предзаполняем пароль из API
        contestantName: data.contestantName || '',
        points: data.points?.toString() || '',
      });
      setShowModal('edit-' + contestantId);
    } catch (error) {
      let msg = 'Ошибка загрузки данных';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setEditModalError(msg);
    }
    setEditLoading(false);
  };

  const handleEditFormChange = e => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleEditSave = async () => {
    setEditModalError(null);
    
    // Валидация
    const validationErrors = validateForm(editForm, true);
    if (validationErrors.length > 0) {
      setEditModalError(validationErrors.join(', '));
      return;
    }
    
    setEditSaving(true);
    try {
      const updateData = {
        contestant_id: editId,
        username: editForm.username.trim(),
        contestantName: editForm.contestantName.trim(),
        points: Number(editForm.points),
      };
      
      // Добавляем пароль только если он был изменен
      if (editForm.password && editForm.password.trim() !== '') {
        updateData.password = editForm.password;
      }
      
      await makeRequest(`${config.backendUrl}api/v1/contestant`, {
        method: 'PATCH',
        body: JSON.stringify(updateData),
      });
             setEditSaving(false);
       setShowModal(false);
       setEditId(null);
       setShowPassword(false);
       fetchContestants();
    } catch (error) {
      setEditSaving(false);
      let msg = 'Ошибка сети';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setEditModalError(msg);
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
                      <input 
                        name="username" 
                        placeholder="Username (обязательно, до 64 символов)" 
                        value={editForm.username} 
                        onChange={handleEditFormChange} 
                        style={{ padding: 8 }} 
                      />
                                             <div style={{ position: 'relative' }}>
                         <input 
                           name="password" 
                           type={showPassword ? "text" : "password"}
                           placeholder="Password (необязательно, 3-32 символа)" 
                           value={editForm.password} 
                           onChange={handleEditFormChange} 
                           style={{ padding: 8, paddingRight: 40, width: '100%', boxSizing: 'border-box' }} 
                         />
                         <button
                           type="button"
                           onClick={() => setShowPassword(!showPassword)}
                           style={{
                             position: 'absolute',
                             right: 8,
                             top: '50%',
                             transform: 'translateY(-50%)',
                             background: 'none',
                             border: 'none',
                             cursor: 'pointer',
                             padding: 4,
                             fontSize: 12
                           }}
                           title={showPassword ? "Скрыть пароль" : "Показать пароль"}
                         >
                           {showPassword ? "👁️" : "👁️‍🗨️"}
                         </button>
                       </div>
                      <input 
                        name="contestantName" 
                        placeholder="Имя участника (обязательно, до 256 символов)" 
                        value={editForm.contestantName} 
                        onChange={handleEditFormChange} 
                        style={{ padding: 8 }} 
                      />
                      <input 
                        name="points" 
                        type="number" 
                        min="0"
                        max="10000"
                        placeholder="Баллы (обязательно, 0-10000)" 
                        value={editForm.points} 
                        onChange={handleEditFormChange} 
                        style={{ padding: 8 }} 
                      />
                      {editModalError && <div style={{ color: 'red', marginTop: 4 }}>{editModalError}</div>}
                      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 8 }}>
                                                 <button onClick={() => { setShowModal(false); setEditId(null); setShowPassword(false); }} style={{ padding: '8px 16px', background: '#eee', border: 'none', borderRadius: 4 }}>Отмена</button>
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
              <input 
                name="username" 
                placeholder="Username (обязательно, до 64 символов)" 
                value={form.username} 
                onChange={handleFormChange} 
                style={{ padding: 8 }} 
              />
              <input 
                name="password" 
                type="password" 
                placeholder="Password (обязательно, 3-32 символа)" 
                value={form.password} 
                onChange={handleFormChange} 
                style={{ padding: 8 }} 
              />
              <input 
                name="contestantName" 
                placeholder="Имя участника (обязательно, до 256 символов)" 
                value={form.contestantName} 
                onChange={handleFormChange} 
                style={{ padding: 8 }} 
              />
              <input 
                name="points" 
                type="number" 
                min="0"
                max="10000"
                placeholder="Баллы (обязательно, 0-10000)" 
                value={form.points} 
                onChange={handleFormChange} 
                style={{ padding: 8 }} 
              />
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