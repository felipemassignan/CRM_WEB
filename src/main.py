# src/main.py
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from datetime import timedelta
from src.config import config
from src.models.db import db
from src.models.user import User

# Importação dos blueprints
from src.routes.dashboard import bp as dashboard_bp
from src.routes.leads import bp as leads_bp
from src.routes.interactions import bp as interactions_bp
from src.routes.templates import bp as templates_bp
from src.routes.reminders import bp as reminders_bp
from src.routes.integrations import bp as integrations_bp
from src.routes.user import bp as user_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Configurações adicionais para JWT
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']  # Usar a mesma chave secreta
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token expira em 1 hora
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Refresh token expira em 30 dias
    
    # Inicializar extensões
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Configurar o LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'  # Rota para redirecionamento quando login é necessário
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Configurar o JWTManager
    jwt = JWTManager(app)
    
    # Registrar blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(leads_bp)
    app.register_blueprint(interactions_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(integrations_bp)
    app.register_blueprint(user_bp)
    from src.routes.api import bp as api_bp
    app.register_blueprint(api_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)