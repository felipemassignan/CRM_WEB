FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask==3.1.0 gunicorn==21.2.0

COPY app.py .

ENV PORT=5000
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --log-level debug app:app"]