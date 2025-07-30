import { useState, useCallback } from 'react';
import config from '../config';

export const useApi = () => {
  const [loading, setLoading] = useState(false);

  const makeRequest = useCallback(async (url, options = {}) => {
    setLoading(true);
    
    try {
      const token = localStorage.getItem('access_token');
      
      const requestOptions = {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
          'Authorization': token ? `Bearer ${token}` : '',
        },
        credentials: 'include',
      };

      let response = await fetch(url, requestOptions);

      // Если получили 401, пробуем обновить токен
      if (response.status === 401) {
        try {
          const refreshResponse = await fetch(`${config.backendUrl}api/v1/auth/refresh`, {
            method: 'POST',
            credentials: 'include',
          });

          if (refreshResponse.ok) {
            const refreshData = await refreshResponse.json();
            localStorage.setItem('access_token', refreshData.accessToken);
            
            // Повторяем исходный запрос с новым токеном
            requestOptions.headers['Authorization'] = `Bearer ${refreshData.accessToken}`;
            response = await fetch(url, requestOptions);
          } else {
            // Если обновление токена не удалось, перенаправляем на логин
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return null;
          }
        } catch (refreshError) {
          console.error('Ошибка при обновлении токена:', refreshError);
          localStorage.removeItem('access_token');
          window.location.href = '/login';
          return null;
        }
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  return { makeRequest, loading };
};