#!/bin/bash
set -e

# Função para verificar se o PostgreSQL está disponível
postgres_ready() {
  python << END
import sys
import os
import psycopg2
try:
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Se não houver DATABASE_URL, consideramos que está usando SQLite
        sys.exit(0)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    conn = psycopg2.connect(database_url)
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
END
}

# Verificar se estamos usando PostgreSQL
if [ -n "$DATABASE_URL" ]; then
  # Aguardar até que o PostgreSQL esteja disponível
  until postgres_ready; do
    >&2 echo "PostgreSQL não está disponível - aguardando..."
    sleep 1
  done

  >&2 echo "PostgreSQL está disponível - continuando..."
fi

# Executar migrações do banco de dados
echo "Executando migrações do banco de dados..."
flask db init || true  # Ignora erro se já inicializado
flask db migrate -m "Migração automática" || true  # Ignora erro se não houver alterações
flask db upgrade

# Executar script de inicialização do banco
echo "Inicializando banco de dados..."
python -m src.init_db

# Iniciar a aplicação
echo "Iniciando a aplicação..."
exec "$@"
