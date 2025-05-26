FROM python:3.11-slim

WORKDIR /app

# Instalar dependências e ferramentas de depuração
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --no-cache-dir Flask==3.1.0 gunicorn==21.2.0 Flask-SQLAlchemy==3.1.1

# Copiar apenas o arquivo da aplicação
COPY app.py .

# Garantir que o diretório /tmp tenha permissões adequadas
RUN chmod 777 /tmp

# Criar script de inicialização com mais logs
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Verificar ambiente\n\
echo "Verificando ambiente..."\n\
echo "Diretório atual: $(pwd)"\n\
echo "Conteúdo do diretório: $(ls -la)"\n\
echo "Permissões de /tmp: $(ls -la /tmp)"\n\
echo "Variáveis de ambiente: $(env | grep -v PATH)"\n\
\n\
# Iniciar a aplicação com logs detalhados\n\
echo "Iniciando aplicação..."\n\
exec gunicorn --bind 0.0.0.0:${PORT:-8080} --log-level debug --capture-output --enable-stdio-inheritance app:app\n\
' > /app/entrypoint.sh

# Tornar o script executável
RUN chmod +x /app/entrypoint.sh

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Expor a porta
EXPOSE 8080

# Usar o script de inicialização
CMD ["/app/entrypoint.sh"]