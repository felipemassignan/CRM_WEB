"""
Script para inicialização do banco de dados e criação de tabelas
Este script é executado automaticamente pelo docker-entrypoint.sh
"""

from src.main import app, db
from src.models.user import User

def init_db():
    """Inicializa o banco de dados e cria um usuário admin se não existir"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existe um usuário admin
        admin = User.query.filter_by(username="admin").first()
        if not admin:
            # Criar usuário admin padrão
            admin = User(username="admin", email="admin@exemplo.com")
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe!")

if __name__ == "__main__":
    init_db()
