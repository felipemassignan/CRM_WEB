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

# Criar script de inicialização simplificado e corrigido
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Verificar ambiente\n\
echo "Verificando ambiente..."\n\
echo "Diretório atual: $(pwd)"\n\
echo "Conteúdo do diretório: $(ls -la)"\n\
\n\
# Verificar se o arquivo app.py existe\n\
if [ ! -f "app.py" ]; then\n\
  echo "ERRO: app.py não encontrado!"\n\
  exit 1\n\
fi\n\
\n\
# Verificar se o módulo pode ser importado\n\
echo "Verificando se o módulo pode ser importado..."\n\
python -c "import app"\n\
\n\
# Definir a porta\n\
PORT="${PORT:-8080}"\n\
echo "Usando porta: $PORT"\n\
\n\
# Iniciar a aplicação com configurações simplificadas\n\
echo "Iniciando aplicação na porta $PORT..."\n\
exec gunicorn --bind "0.0.0.0:$PORT" app:app\n\
' > /app/entrypoint.sh

# Tornar o script executável
RUN chmod +x /app/entrypoint.sh

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Expor a porta
EXPOSE 8080

# Usar o script de inicialização
CMD ["/app/entrypoint.sh"]