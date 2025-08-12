FROM node:20 as build

WORKDIR /app

# Копируем package.json файлы
COPY frontend/react/package*.json ./frontend/react/

# Устанавливаем зависимости
WORKDIR /app/frontend/react
RUN npm install

# Копируем исходный код React приложения
COPY frontend/react/ ./

# Собираем приложение
RUN npm run build

# Второй этап - nginx
FROM nginx:alpine

# Копируем nginx конфигурацию
COPY docker/nginx/nginx.conf /etc/nginx/nginx.conf

# Копируем собранные файлы из первого этапа
COPY --from=build /app/frontend/react/dist /usr/share/nginx/html

# Открываем порт
EXPOSE 80

# Запускаем nginx
CMD ["nginx", "-g", "daemon off;"]
