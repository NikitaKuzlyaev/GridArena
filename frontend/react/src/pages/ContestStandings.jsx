import React, { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import config from '../config';

function ContestStandings() {
  const [searchParams] = useSearchParams();
  const contestId = searchParams.get('contest_id');

  useEffect(() => {
    if (!contestId) return;
    const token = localStorage.getItem('access_token');
    fetch(`${config.backendUrl}api/v1/contest/standings?contest_id=${contestId}`, {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        // Пока ничего не делаем с данными
      });
  }, [contestId]);


  return (
    <div>
      <h1>Положение</h1>
      {/* Здесь будет таблица или информация о положении */}
    </div>
  );
}

export default ContestStandings; 