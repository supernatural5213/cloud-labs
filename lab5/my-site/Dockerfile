# Базовый образ
FROM nginx:alpine

# Копируем свой HTML
COPY index.html /usr/share/nginx/html/

# Порт (документация)
EXPOSE 80

# Запуск nginx
CMD ["nginx", "-g", "daemon off;"]
