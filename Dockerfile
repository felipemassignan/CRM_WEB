FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema para PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc procps net-tools \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --no-cache-dir Flask==3.1.0 gunicorn==21.2.0 \
    Flask-SQLAlchemy==3.1.1 psycopg2-binary==2.9.9

# Copiar código da aplicação
COPY app.py .

# Criar script de inicialização com verificações de conexão
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Verificar ambiente\n\
echo "Verificando ambiente..."\n\
echo "Diretório atual: $(pwd)"\n\
echo "Conteúdo do diretório: $(ls -la)"\n\
\n\
# Verificar variáveis de ambiente\n\
echo "Verificando variáveis de ambiente..."\n\
if [ -z "$DATABASE_URL" ]; then\n\
  echo "AVISO: DATABASE_URL não está definida!"\n\
else\n\
  echo "DATABASE_URL está definida (valor oculto por segurança)"\n\
fi\n\
\n\
# Verificar conectividade com o banco de dados\n\
echo "Verificando conectividade com o banco de dados..."\n\
if [[ "$DATABASE_URL" == *"postgres.railway.internal"* ]]; then\n\
  echo "Tentando conectar ao PostgreSQL do Railway..."\n\
  pg_host=$(echo $DATABASE_URL | sed -n "s/.*@$$[^:]*$$.*/\1/p")\n\
  pg_port=$(echo $DATABASE_URL | sed -n "s/.*:$$[0-9]*$$\/.*/\1/p")\n\
  echo "Host: $pg_host, Porta: $pg_port"\n\
  timeout 5 bash -c "</dev/tcp/$pg_host/$pg_port" && echo "Conexão TCP bem-sucedida!" || echo "Falha na conexão TCP!"\n\
fi\n\
\n\
# Definir a porta\n\
PORT="${PORT:-8080}"\n\
echo "Usando porta: $PORT"\n\
\n\
# Iniciar a aplicação com configurações otimizadas\n\
echo "Iniciando aplicação na porta $PORT..."\n\
exec gunicorn \n\
  --bind "0.0.0.0:$PORT" \n\
  --workers 2 \n\
  --threads 4 \n\
  --timeout 60 \n\
  --log-level debug \n\
  --capture-output \n\
  --access-logfile - \n\
  --error-logfile - \n\
  app:app\n\
' > /app/entrypoint.sh

# Tornar o script executável
RUN chmod +x /app/entrypoint.sh

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Expor a porta
EXPOSE 8080

# Usar o script de inicialização
CMD ["/app/entrypoint.sh"]