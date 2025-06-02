from src.models.db import db
from src.models.user import User
from src.main import create_app
import os

def init_db():
    """Inicializa o banco de dados com dados iniciais."""
    app = create_app()
    
    with app.app_context():
        # Criar tabelas se não existirem
        db.create_all()
        
        # Verificar se já existe um usuário admin
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            # Criar usuário admin
            admin_password = os.environ.get('ADMIN_INITIAL_PASSWORD', 'admin123')  # Usar variável de ambiente ou senha padrão
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"Usuário admin criado com sucesso. Senha: {admin_password}")
            print("IMPORTANTE: Altere esta senha após o primeiro login!")
        else:
            print("Usuário admin já existe.")

if __name__ == '__main__':
    init_db()