FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar script de inicialização
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Aplicar migrações existentes\n\
echo "Aplicando migrações..."\n\
flask db upgrade\n\
\n\
# Iniciar a aplicação\n\
exec gunicorn --bind 0.0.0.0:5000 src.main:app\n\
' > /app/entrypoint.sh

# Tornar o script executável
RUN chmod +x /app/entrypoint.sh

# Variáveis de ambiente para produção
ENV FLASK_APP=src.main
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expor a porta que o Flask usará
EXPOSE 5000

# Usar o script de inicialização
CMD ["/app/entrypoint.sh"]