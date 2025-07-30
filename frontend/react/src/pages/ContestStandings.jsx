import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';
import { useApi } from '../hooks/useApi';

function ContestStandings() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');
  const { makeRequest } = useApi();
  const [standingsData, setStandingsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [isFirstLoad, setIsFirstLoad] = useState(true);

  // Функция для загрузки standings
  const fetchStandings = async (showLoader = false) => {
    if (!contestId) return;
    if (showLoader) setLoading(true);
    try {
      const data = await makeRequest(`${config.backendUrl}api/v1/contest/standings?contest_id=${contestId}`);
      setStandingsData(data);
    } catch (error) {
      console.error('Ошибка при загрузке standings:', error);
    } finally {
      if (showLoader) setLoading(false);
      if (isFirstLoad) setIsFirstLoad(false);
    }
  };

  useEffect(() => {
    setIsFirstLoad(true);
    fetchStandings(true);
  }, [contestId]);

  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      fetchStandings(false);
    }, 3000);
    return () => clearInterval(interval);
  }, [autoRefresh, contestId]);

  return (
    <div style={{ maxWidth: 800, margin: '32px auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
        <h1 style={{ margin: 0, fontSize: 28, fontWeight: 700 }}>Положение</h1>
        <label style={{ display: 'flex', alignItems: 'center', fontSize: 16, userSelect: 'none', gap: 8 }}>
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={e => setAutoRefresh(e.target.checked)}
            style={{ width: 18, height: 18 }}
          />
          Автообновление
        </label>
      </div>
      {loading && isFirstLoad && (
        <div style={{
          background: '#fff',
          padding: '20px',
          borderRadius: '8px',
          marginBottom: '24px',
          textAlign: 'center',
          color: '#666'
        }}>
          <div style={{ marginBottom: '8px' }}>⏳</div>
          Загрузка положения...
        </div>
      )}
      {standingsData && (
        <>
          {/* Информация о соревновании */}
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '24px',
            borderRadius: '12px',
            marginBottom: '32px',
            boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <div style={{
              position: 'absolute',
              top: '-20px',
              right: '-20px',
              width: '100px',
              height: '100px',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '50%',
              zIndex: 0
            }}></div>
            <div style={{ position: 'relative', zIndex: 1 }}>
              <h2 style={{ margin: '0 0 16px 0', fontSize: '24px', fontWeight: '600', textAlign: 'center' }}>{standingsData.name}</h2>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '16px' }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '14px', opacity: 0.8, marginBottom: '4px' }}>Начало</div>
                  <div style={{ fontSize: '16px', fontWeight: '500' }}>{new Date(standingsData.startedAt).toLocaleString('ru-RU')}</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '14px', opacity: 0.8, marginBottom: '4px' }}>Окончание</div>
                  <div style={{ fontSize: '16px', fontWeight: '500' }}>{new Date(standingsData.closedAt).toLocaleString('ru-RU')}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Карточки участников */}
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
          }}>
            {standingsData.standings && standingsData.standings.body && standingsData.standings.body.length > 0 ? (
              standingsData.standings.body.map((c) => (
                <div key={c.contestantId} style={{
                  background: '#fff',
                  color: '#222',
                  padding: '12px 20px',
                  borderRadius: '8px',
                  boxShadow: '0 2px 8px rgba(102, 126, 234, 0.07)',
                  display: 'flex',
                  alignItems: 'center',
                  minHeight: 48,
                  fontSize: 16,
                  fontWeight: 500,
                  borderLeft: '6px solid #764ba2',
                }}>
                  <div style={{
                    fontSize: 22,
                    fontWeight: 700,
                    color: '#764ba2',
                    width: 40,
                    textAlign: 'center',
                    marginRight: 18,
                  }}>#{c.rank}</div>
                  <div style={{ flex: 1 }}>{c.name}</div>
                  <div style={{
                    fontWeight: 600,
                    color: '#f7971e',
                    marginLeft: 18,
                    fontSize: 18,
                  }}>Баллы: {c.points}</div>
                </div>
              ))
            ) : (
              <div style={{ textAlign: 'center', color: '#666', fontSize: 18 }}>
                Нет данных о положении участников
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default ContestStandings; 