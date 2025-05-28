FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema para o psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para o banco de dados SQLite (caso seja usado como fallback)
RUN mkdir -p instance

# Dar permissão de execução ao script de entrypoint
RUN chmod +x /app/docker-entrypoint.sh

# Variáveis de ambiente para produção
ENV FLASK_APP=src.main
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expor a porta que o Flask usará
EXPOSE 5000

# Definir o entrypoint para aguardar o PostgreSQL e executar migrações
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Comando para iniciar a aplicação com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.main:app"]
