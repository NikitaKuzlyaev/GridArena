import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useApi } from '../hooks/useApi';
import config from '../config';
import { sendNotification } from '../components/NotificationFactory';

function Home() {
  const [markdown, setMarkdown] = useState('');
  const [contestantData, setContestantData] = useState(null);
  const [userType, setUserType] = useState(null);
  const { makeRequest, loading } = useApi();

  useEffect(() => {
    // Загрузка markdown
    fetch('/main.md')
      .then((res) => res.text())
      .then(setMarkdown);

    // Проверка user_type в localStorage
    const userTypeFromStorage = localStorage.getItem('user_type');
    setUserType(userTypeFromStorage);
    
    if (userTypeFromStorage === 'CONTEST') {
      const fetchContestantData = async () => {
        try {
          const data = await makeRequest(`${config.backendUrl}api/v1/contestant/preview`);
          setContestantData(data);
          console.log('Данные участника загружены:', data);
        } catch (error) {
          console.error('Ошибка при загрузке данных участника:', error);
        }
      };

      fetchContestantData();
    }
      }, [makeRequest]);

  return (
    <div style={{ maxWidth: 700, margin: '32px auto' }}>
      {/* Кнопка для теста уведомлений */}
      {/* <button
        onClick={() => sendNotification({
          level: 'INFO',
          content: 'Это тестовое уведомление!',
          color: '#1677ff',
        })}
        style={{
          marginBottom: 24,
          padding: '10px 20px',
          borderRadius: 8,
          border: 'none',
          background: '#1677ff',
          color: '#fff',
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        Показать уведомление
      </button> */}
      {/* Блок с информацией о контесте */}
      {contestantData && (
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          padding: '24px',
          borderRadius: '12px',
          marginBottom: '24px',
          boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)',
          position: 'relative',
          overflow: 'hidden'
        }}>
          {/* Декоративный элемент */}
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
            <h2 style={{
              margin: '0 0 16px 0',
              fontSize: '24px',
              fontWeight: '600',
              textAlign: 'center'
            }}>
              Добро пожаловать, {contestantData.contestantName}!
            </h2>
            
            <div style={{
              background: 'rgba(255, 255, 255, 0.15)',
              padding: '20px',
              borderRadius: '8px',
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{
                margin: '0 0 16px 0',
                fontSize: '20px',
                fontWeight: '500',
                textAlign: 'center'
              }}>
                Контест: {contestantData.contestName}
              </h3>
              
                             <div style={{
                 display: 'grid',
                 gridTemplateColumns: '1fr 1fr',
                 gap: '16px',
                 marginTop: '16px'
               }}>
                 <div style={{ textAlign: 'center' }}>
                   <div style={{
                     fontSize: '14px',
                     opacity: 0.8,
                     marginBottom: '4px'
                   }}>
                     Начало
                   </div>
                   <div style={{
                     fontSize: '16px',
                     fontWeight: '500'
                   }}>
                     {new Date(contestantData.startedAt).toLocaleString('ru-RU')}
                   </div>
                 </div>
                 
                 <div style={{ textAlign: 'center' }}>
                   <div style={{
                     fontSize: '14px',
                     opacity: 0.8,
                     marginBottom: '4px'
                   }}>
                     Окончание
                   </div>
                   <div style={{
                     fontSize: '16px',
                     fontWeight: '500'
                   }}>
                     {new Date(contestantData.closedAt).toLocaleString('ru-RU')}
                   </div>
                 </div>
               </div>
               
               {/* Статус соревнования и кнопка */}
               {contestantData.isContestOpen && (
                 <div style={{
                   marginTop: '20px',
                   textAlign: 'center'
                 }}>
                   <div style={{
                     fontSize: '18px',
                     fontWeight: '600',
                     marginBottom: '16px',
                     color: '#4ade80'
                   }}>
                     🏆 Соревнование идет
                   </div>
                   <a
                     href={`/contest?contest_id=${contestantData.contestId}`}
                     style={{
                       display: 'inline-block',
                       background: '#4ade80',
                       color: 'white',
                       padding: '12px 24px',
                       borderRadius: '8px',
                       textDecoration: 'none',
                       fontWeight: '600',
                       fontSize: '16px',
                       transition: 'all 0.2s ease',
                       boxShadow: '0 4px 12px rgba(74, 222, 128, 0.3)'
                     }}
                     onMouseOver={(e) => {
                       e.target.style.background = '#22c55e';
                       e.target.style.transform = 'translateY(-2px)';
                       e.target.style.boxShadow = '0 6px 16px rgba(74, 222, 128, 0.4)';
                     }}
                     onMouseOut={(e) => {
                       e.target.style.background = '#4ade80';
                       e.target.style.transform = 'translateY(0)';
                       e.target.style.boxShadow = '0 4px 12px rgba(74, 222, 128, 0.3)';
                     }}
                   >
                     Перейти к соревнованию
                   </a>
                 </div>
               )}
            </div>
          </div>
        </div>
      )}
      
      {/* Индикатор загрузки */}
      {loading && (
        <div style={{
          background: '#fff',
          padding: '20px',
          borderRadius: '8px',
          marginBottom: '24px',
          textAlign: 'center',
          color: '#666'
        }}>
          <div style={{ marginBottom: '8px' }}>⏳</div>
          Загрузка данных участника...
        </div>
      )}
      
      {/* Markdown контент - показываем только если НЕ участник */}
      {userType !== 'CONTEST' && (
        <div className="markdown-body" style={{ padding: 24, background: '#fff', borderRadius: 8, textAlign: 'left' }}>
          <ReactMarkdown>{markdown}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default Home; 