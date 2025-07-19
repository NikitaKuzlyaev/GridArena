import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

function SolveContest() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Здесь будет логика загрузки данных соревнования
    console.log('Contest ID:', contestId);
    
    // Имитация загрузки
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, [contestId]);

  if (loading) {
    return (
      <div style={{
        maxWidth: 800,
        margin: '40px auto',
        padding: '40px',
        textAlign: 'center',
        background: '#fff',
        borderRadius: '12px',
        boxShadow: '0 4px 16px rgba(0,0,0,0.1)'
      }}>
        <div style={{ fontSize: '24px', marginBottom: '16px' }}>⏳</div>
        <div style={{ fontSize: '18px', color: '#666' }}>Загрузка соревнования...</div>
      </div>
    );
  }

  return (
    <div style={{
      maxWidth: 800,
      margin: '40px auto',
      padding: '40px',
      background: '#fff',
      borderRadius: '12px',
      boxShadow: '0 4px 16px rgba(0,0,0,0.1)'
    }}>
      <h1 style={{
        textAlign: 'center',
        marginBottom: '32px',
        color: '#333',
        fontSize: '28px'
      }}>
        🏆 Соревнование #{contestId}
      </h1>
      
      <div style={{
        textAlign: 'center',
        padding: '40px',
        background: '#f8f9fa',
        borderRadius: '8px',
        border: '2px dashed #dee2e6'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '16px' }}>🚧</div>
        <h2 style={{ color: '#666', marginBottom: '16px' }}>
          Страница в разработке
        </h2>
        <p style={{ color: '#888', fontSize: '16px' }}>
          Здесь будет интерфейс для решения задач соревнования
        </p>
      </div>
      
      <div style={{
        marginTop: '24px',
        padding: '16px',
        background: '#e3f2fd',
        borderRadius: '8px',
        border: '1px solid #bbdefb'
      }}>
        <strong>Отладочная информация:</strong>
        <br />
        Contest ID: {contestId}
      </div>
    </div>
  );
}

export default SolveContest; 