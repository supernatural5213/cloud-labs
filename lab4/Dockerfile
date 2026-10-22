FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.1.3
COPY api/index.py app.py
ENV HOST=0.0.0.0 PORT=8080
EXPOSE 8080
# Flask (PID 1) корректно завершается по SIGINT; без этого docker stop ждёт 10 с и шлёт SIGKILL
STOPSIGNAL SIGINT
CMD ["python", "app.py"]
