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
except Exception as e:
    print(f"Erro ao conectar ao PostgreSQL: {e}")
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

# Garantir que o Flask-Migrate está instalado
pip install flask-migrate

# Verificar se o comando flask está disponível
which flask || pip install flask

# Executar migrações do banco de dados
echo "Executando migrações do banco de dados..."
export FLASK_APP=src.main
python -m flask db init || true  # Ignora erro se já inicializado
python -m flask db migrate -m "Migração automática" || true  # Ignora erro se não houver alterações
python -m flask db upgrade || true

# Executar script de inicialização do banco
echo "Inicializando banco de dados..."
python -m src.init_db || true

# Iniciar a aplicação
echo "Iniciando a aplicação..."
exec "$@"
