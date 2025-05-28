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
  
  # Verifica se a tabela alembic_version existe e tem conteúdo
  python << END
import sys
import os
import psycopg2
try:
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Verifica se a tabela alembic_version existe
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version')")
    table_exists = cursor.fetchone()[0]
    
    if table_exists:
        # Verifica se há revisões que não existem nos arquivos
        cursor.execute("SELECT version_num FROM alembic_version")
        version = cursor.fetchone()
        if version:
            version_num = version[0]
            print(f"Versão atual do alembic: {version_num}")
            
            # Verifica se o diretório migrations/versions existe
            import os
            if os.path.exists('/app/migrations/versions'):
                # Verifica se o arquivo de revisão existe
                revision_exists = False
                for filename in os.listdir('/app/migrations/versions'):
                    if version_num in filename:
                        revision_exists = True
                        break
                
                # Se a revisão não existir nos arquivos, remove a tabela
                if not revision_exists:
                    print(f"Revisão {version_num} não encontrada nos arquivos. Removendo tabela alembic_version...")
                    cursor.execute("DROP TABLE alembic_version")
                    conn.commit()
            else:
                # Se o diretório não existir, remove a tabela
                print("Diretório migrations/versions não encontrado. Removendo tabela alembic_version...")
                cursor.execute("DROP TABLE alembic_version")
                conn.commit()
    
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"Erro ao verificar/limpar alembic_version: {e}")
    sys.exit(0)  # Não falha o script se houver erro
END
fi

# Executar migrações do banco de dados
echo "Executando migrações do banco de dados..."
flask db init || true  # Ignora erro se já inicializado
flask db migrate -m "Migração automática" || true  # Ignora erro se não houver alterações
flask db upgrade || true  # Ignora erro se não houver alterações

# Executar script de inicialização do banco
echo "Inicializando banco de dados..."
python -m src.init_db || true  # Ignora erro se houver falha na inicialização

# Iniciar a aplicação
echo "Iniciando a aplicação..."
exec "$@"