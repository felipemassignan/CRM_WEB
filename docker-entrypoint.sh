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
  until postgres_ready; do
    >&2 echo "PostgreSQL não está disponível - aguardando..."
    sleep 1
  done
  >&2 echo "PostgreSQL está disponível - continuando..."
fi

# Verificar variáveis de ambiente críticas
if [ -z "$SECRET_KEY" ]; then
    echo "ERRO: A variável de ambiente SECRET_KEY não está definida!"
    exit 1
fi

# Aguardar o banco de dados
echo "Aguardando o banco de dados..."
sleep 5

# Instalar dependências Python
pip install -r requirements.txt

# Executar migrações do banco de dados
echo "Executando migrações do banco de dados..."
export FLASK_APP=src.main
python -m flask db upgrade || true

# Executar script de inicialização do banco
echo "Inicializando banco de dados..."
python -m src.init_db || true

# Executar o servidor Gunicorn
exec gunicorn --bind 0.0.0.0:5000 "src.main:app"