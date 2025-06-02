# src/init_db.py
from src.models.db import db
from src.models.user import User
from src.main import create_app
import os

def init_db():
    """Inicializa o banco de dados com dados iniciais."""
    app = create_app()
    
    with app.app_context():
        # Criar tabelas se nÃ£o existirem
        db.create_all()
        
        # Verificar se jÃ¡ existe um usuÃ¡rio admin
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            # Criar usuÃ¡rio admin
            admin_password = os.environ.get('ADMIN_INITIAL_PASSWORD', 'admin123')  # Usar variÃ¡vel de ambiente ou senha padrÃ£o
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"UsuÃ¡rio admin criado com sucesso. Senha: {admin_password}")
            print("IMPORTANTE: Altere esta senha apÃ³s o primeiro login!")
        else:
            print("UsuÃ¡rio admin jÃ¡ existe.")

if __name__ == '__main__':
    init_db()