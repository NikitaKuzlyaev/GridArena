import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import config from '../config';
import ErrorBlock from '../components/ErrorBlock.jsx';
import { useApi } from '../hooks/useApi';

function EditContest() {
  const { contestId } = useParams();
  const { makeRequest } = useApi();
  const [form, setForm] = useState({
    name: '',
    start_points: '',
    number_of_slots_for_problems: '',
    started_at: '',
    closed_at: '',
    rule_type: 'DEFAULT',
    flag_user_can_have_negative_points: false,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Валидация полей
  const validate = (form) => {
    const errors = {};
    if (form.name.length < 1 || form.name.length > 256) {
      errors.name = 'Название должно содержать от 1 до 256 символов';
    }
    const startPoints = Number(form.start_points);
    if (isNaN(startPoints) || startPoints < 0 || startPoints > 10000) {
      errors.start_points = 'Стартовый баланс должен быть от 0 до 10000';
    }
    const slots = Number(form.number_of_slots_for_problems);
    if (isNaN(slots) || slots < 1 || slots > 5) {
      errors.number_of_slots_for_problems = 'Число задач должно быть от 1 до 5';
    }
    return errors;
  };

  const errors = validate(form);
  const isFormValid = Object.keys(errors).length === 0;

  useEffect(() => {
    const fetchContestData = async () => {
      try {
        const data = await makeRequest(`${config.backendUrl}api/v1/contest/info-editor?contest_id=${contestId}`);
        if (data) {
          // Конвертируем UTC даты в локальный часовой пояс для отображения в форме
          const convertUtcToLocal = (utcString) => {
            if (!utcString) return '';
            const date = new Date(utcString);
            // Получаем смещение в минутах и конвертируем в формат YYYY-MM-DDTHH:mm
            const offset = date.getTimezoneOffset();
            const localDate = new Date(date.getTime() - (offset * 60 * 1000));
            return localDate.toISOString().slice(0, 16);
          };

          setForm({
            name: data.name || '',
            start_points: data.startPoints?.toString() || '',
            number_of_slots_for_problems: data.numberOfSlotsForProblems?.toString() || '',
            started_at: convertUtcToLocal(data.startedAt),
            closed_at: convertUtcToLocal(data.closedAt),
            rule_type: data.ruleType || 'DEFAULT',
            flag_user_can_have_negative_points: !!data.flagUserCanHaveNegativePoints,
          });
        }
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

    fetchContestData();
  }, [contestId, makeRequest]);

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(form => ({
      ...form,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      // Конвертируем локальные даты обратно в UTC для отправки на сервер
      const convertLocalToUtc = (localDateTimeString) => {
        if (!localDateTimeString) return '';
        const localDate = new Date(localDateTimeString);
        return localDate.toISOString();
      };

      await makeRequest(`${config.backendUrl}api/v1/contest/`, {
        method: 'PATCH',
        body: JSON.stringify({
          contestId: Number(contestId),
          name: form.name,
          startPoints: Number(form.start_points),
          numberOfSlotsForProblems: Number(form.number_of_slots_for_problems),
          startedAt: convertLocalToUtc(form.started_at),
          closedAt: convertLocalToUtc(form.closed_at),
          ruleType: form.rule_type,
          flagUserCanHaveNegativePoints: form.flag_user_can_have_negative_points,
        }),
      });
      setLoading(false);
      alert('Контест успешно обновлён!');
      window.location.href = '/my-contests';
    } catch (error) {
      setLoading(false);
      let msg = 'Ошибка сети';
      if (error.message && error.message.includes('detail')) {
        try {
          const errorData = JSON.parse(error.message);
          if (errorData.detail) msg = errorData.detail;
        } catch {}
      }
      setError({ code: 'network', message: msg });
    }
  };

  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: '40px' }}>Загрузка...</div>;
  }
  if (error) {
    return <ErrorBlock code={error.code} message={error.message} />;
  }
  return (
    <div>
      <div style={{ maxWidth: 600, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
        <h1 style={{ textAlign: 'center' }}>Редактирование контеста</h1>
        <form style={{ marginTop: 32, display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 400, marginLeft: 'auto', marginRight: 'auto' }} onSubmit={handleSubmit}>
          <label style={{ marginBottom: 0 }}>
            Название:
            <input
              name="name"
              type="text"
              maxLength={256}
              required
              value={form.name}
              onChange={handleChange}
              style={{
                width: '100%', marginTop: 4, padding: 8,
                border: errors.name ? '1.5px solid #e53935' : undefined
              }}
            />
            <div style={{ fontSize: 12, color: errors.name ? '#e53935' : '#888', minHeight: 12 }}>
              {'Строка длиной от 1 до 256 символов'}
            </div>
          </label>
          <label style={{ marginBottom: 0 }}>
            Стартовый баланс:
            <input
              name="start_points"
              type="number"
              min={0}
              max={10000}
              required
              value={form.start_points}
              onChange={handleChange}
              style={{
                width: '100%', marginTop: 4, padding: 8,
                border: errors.start_points ? '1.5px solid #e53935' : undefined
              }}
            />
            <div style={{ fontSize: 12, color: errors.start_points ? '#e53935' : '#888', minHeight: 12 }}>
              {'Целое число от 0 до 10000'}
            </div>
          </label>
          <label style={{ marginBottom: 0 }}>
            Сколько задач разрешено держать одновременно (1–5):
            <input
              name="number_of_slots_for_problems"
              type="number"
              min={1}
              max={5}
              required
              value={form.number_of_slots_for_problems}
              onChange={handleChange}
              style={{
                width: '100%', marginTop: 4, padding: 8,
                border: errors.number_of_slots_for_problems ? '1.5px solid #e53935' : undefined
              }}
            />
            <div style={{ fontSize: 12, color: errors.number_of_slots_for_problems ? '#e53935' : '#888', minHeight: 12 }}>
              {'Целое число от 1 до 5'}
            </div>
          </label>
          <label>
            Начало:
            <input name="started_at" type="datetime-local" required value={form.started_at} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }} />
          </label>
          <label>
            Окончание:
            <input name="closed_at" type="datetime-local" required value={form.closed_at} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }} />
          </label>
          <label>
            Тип правил:
            <select name="rule_type" value={form.rule_type} onChange={handleChange} style={{ width: '100%', marginTop: 4, padding: 8 }}>
              <option value="DEFAULT">DEFAULT</option>
            </select>
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <input
              name="flag_user_can_have_negative_points"
              type="checkbox"
              checked={form.flag_user_can_have_negative_points}
              onChange={handleChange}
            />
            Разрешить отрицательный баланс у участника
          </label>
          <button type="submit" style={{ padding: 10, background: '#61dafb', color: '#282c34', border: 'none', borderRadius: 4, fontWeight: 500, marginTop: 12, opacity: isFormValid && !loading ? 1 : 0.6 }} disabled={!isFormValid || loading}>
            {loading ? 'Сохранение...' : 'Сохранить'}
          </button>
        </form>
      </div>
      <div style={{ textAlign: 'center', marginTop: 24 }}>
        <button
          type="button"
          style={{ padding: 10, background: '#eee', color: '#282c34', border: '1px solid #ccc', borderRadius: 4, fontWeight: 500, marginRight: 12 }}
          onClick={() => window.location.href = `/edit-field?contest_id=${contestId}`}
        >
          Редактировать поле
        </button>
        <button
          type="button"
          style={{ padding: 10, background: '#ff4d4f', color: '#fff', border: 'none', borderRadius: 4, fontWeight: 500 }}
          onClick={async () => {
            if (window.confirm('Вы уверены, что хотите удалить этот контест? Это действие необратимо.')) {
              setLoading(true);
              setError(null);
              try {
                await makeRequest(`${config.backendUrl}api/v1/contest/?contest_id=${contestId}`, {
                  method: 'DELETE',
                });
                setLoading(false);
                alert('Контест успешно удалён!');
                window.location.href = '/my-contests';
              } catch (error) {
                setLoading(false);
                let msg = 'Ошибка сети';
                if (error.message && error.message.includes('detail')) {
                  try {
                    const errorData = JSON.parse(error.message);
                    if (errorData.detail) msg = errorData.detail;
                  } catch {}
                }
                setError({ code: 'network', message: msg });
              }
            }
          }}
        >
          Удалить контест
        </button>
        <div style={{ marginTop: 24 }}>
          <button
            type="button"
            style={{ padding: 10, background: '#21a1f3', color: '#fff', border: 'none', borderRadius: 4, fontWeight: 500, marginRight: 12 }}
            onClick={() => window.location.href = `/edit-contestants?contest_id=${contestId}`}
          >
            Управление участниками
          </button>
          <button
            type="button"
            style={{ padding: 10, background: '#21a1f3', color: '#fff', border: 'none', borderRadius: 4, fontWeight: 500 }}
            onClick={() => window.location.href = `/edit-submissions?contest_id=${contestId}`}
          >
            Управление посылками
          </button>
        </div>
      </div>
    </div>
  );
}

export default EditContest; 