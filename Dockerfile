FROM python:3.11-slim

WORKDIR /app

# Instalar apenas o mínimo necessário
RUN pip install --no-cache-dir Flask==3.1.0 gunicorn==21.2.0

# Copiar apenas o arquivo da aplicação
COPY app.py .

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Expor a porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --log-level debug app:app"]