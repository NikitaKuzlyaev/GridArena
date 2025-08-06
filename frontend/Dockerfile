FROM node:20 as builder

WORKDIR /app

COPY frontend /app/frontend
WORKDIR ./frontend

RUN npm install && npm run build



FROM nginx:alpine

COPY --from=builder /app/frontend/dist /usr/share/nginx/html

EXPOSE 80
