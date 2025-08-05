import React, { useEffect, useState } from 'react';
import { useApi } from '../hooks/useApi';
import config from '../config';

const Logs = () => {
  const [logs, setLogs] = useState(null);
  const { makeRequest, loading } = useApi();

  // Функция для форматирования относительного времени
  const formatTimeAgo = (createdAt, serverTime) => {
    const created = new Date(createdAt);
    const server = new Date(serverTime);
    const diffMs = server - created;
    
    const seconds = Math.floor(diffMs / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (seconds < 60) {
      return `${seconds} ${seconds === 1 ? 'секунду' : seconds < 5 ? 'секунды' : 'секунд'} назад`;
    } else if (minutes < 60) {
      return `${minutes} ${minutes === 1 ? 'минуту' : minutes < 5 ? 'минуты' : 'минут'} назад`;
    } else if (hours < 24) {
      const remainingMinutes = minutes % 60;
      if (remainingMinutes === 0) {
        return `${hours} ${hours === 1 ? 'час' : hours < 5 ? 'часа' : 'часов'} назад`;
      } else {
        return `${hours} ${hours === 1 ? 'час' : hours < 5 ? 'часа' : 'часов'} ${remainingMinutes} ${remainingMinutes === 1 ? 'минуту' : remainingMinutes < 5 ? 'минуты' : 'минут'} назад`;
      }
    } else {
      return `${days} ${days === 1 ? 'день' : days < 5 ? 'дня' : 'дней'} назад`;
    }
  };

  // Функция для форматирования времени в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС.ffffff
  const formatTime = (dateString) => {
    if (!dateString) return '';
    // Обрезаем 'T' и 'Z', заменяем 'T' на пробел
    let formatted = dateString.replace('T', ' ').replace('Z', '');
    return formatted;
  };

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const data = await makeRequest(`${config.backendUrl}api/v1/contestant/my/logs`);
        setLogs(data);
        // Можно добавить console.log для отладки
        // console.log('Логи:', data);
      } catch (error) {
        // Пока просто выводим ошибку в консоль
        console.error('Ошибка при загрузке логов:', error);
      }
    };
    fetchLogs();
  }, [makeRequest]);

  if (loading) {
    return (
      <div style={{ padding: 32, textAlign: 'center' }}>

      </div>
    );
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 32 }}>
      <h2 style={{ textAlign: 'left', marginBottom: 16 }}>Логи участника соревнования</h2>
      
      {logs && logs.body && logs.body.length > 0 ? (
        <div>
          <div style={{ marginBottom: 32, textAlign: 'left', color: '#666' }}>
            Всего записей: {logs.total}. Показываются не более 20 последних записей логов
          </div>
          
          <div style={{ 
            background: '#fff', 
            borderRadius: 8, 
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            overflow: 'hidden'
          }}>
            {logs.body.map((log, index) => (
              <div 
                key={log.contestantLogId}
                style={{
                  padding: '16px 20px',
                  borderBottom: index < logs.body.length - 1 ? '1px solid #f0f0f0' : 'none',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: 12
                }}
              >
                <div style={{
                  padding: '4px 8px',
                  borderRadius: 4,
                  fontSize: 12,
                  fontWeight: 'bold',
                  background: log.logLevel === 'INFO' ? '#e3f2fd' : 
                             log.logLevel === 'ATTENTION' ? '#fff3e0' : 
                             log.logLevel === 'ERROR' ? '#ffebee' : 
                             log.logLevel === 'DEBUG' ? '#ffebee' : '#f5f5f5',
                  color: log.logLevel === 'INFO' ? '#1976d2' : 
                         log.logLevel === 'ATTENTION' ? '#f57c00' : 
                         log.logLevel === 'ERROR' ? '#d32f2f' : 
                         log.logLevel === 'DEBUG' ? '#ffebee' : '#f5f5f5',
                  minWidth: 60,
                  textAlign: 'center',
                  flexShrink: 0
                }}>
                  {log.logLevel}
                </div>
                
                <div style={{ flex: 1 }}>
                <div style={{ fontSize: 10, color: '#666', textAlign: 'left', }}>
                    {formatTime(log.createdAt)} ({formatTimeAgo(log.createdAt, logs.serverTime)})
                  </div>
                  <div style={{ fontSize: 14, marginBottom: 4, textAlign: 'left',  }}>
                    {log.content}
                  </div>
                  
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div style={{ textAlign: 'center', color: '#666' }}>
          <p>Логи не найдены</p>
        </div>
      )}
    </div>
  );
};

export default Logs;