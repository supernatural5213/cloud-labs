FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.1.3
COPY api/index.py app.py
ENV HOST=0.0.0.0 PORT=8080
EXPOSE 8080
CMD ["python", "app.py"]
