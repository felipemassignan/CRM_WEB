import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Inicialização do app
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

app.config['SECRET_KEY'] = 'crm_python_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Importar a instância db centralizada
from src.models.db import db

# Inicializar db com o app
db.init_app(app)
migrate = Migrate(app, db)

# Importar modelos
from src.models.lead import Lead, INDUSTRY_CHOICES, POSITION_CHOICES, REGION_CHOICES, STATUS_CHOICES, PRIORITY_CHOICES, SOURCE_CHOICES
from src.models.interaction import Interaction
from src.models.template import Template
from src.models.reminder import Reminder
from src.models.user import User

# Importar e registrar blueprints
from src.routes.leads import bp as leads_bp
from src.routes.interactions import bp as interactions_bp
from src.routes.templates import bp as templates_bp
from src.routes.reminders import bp as reminders_bp
from src.routes.dashboard import bp as dashboard_bp
from src.routes.integrations import bp as integrations_bp

app.register_blueprint(leads_bp)
app.register_blueprint(interactions_bp)
app.register_blueprint(templates_bp)
app.register_blueprint(reminders_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(integrations_bp)

# Rota principal
@app.route('/')
def index():
    return render_template('base.html')

# Rota para servir arquivos estáticos
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Inicialização do banco de dados
# Nota: before_first_request foi removido em versões recentes do Flask
# Usamos with app.app_context() no bloco principal

# Função para carregar dados de teste
def load_test_data():
    from src.test_data import criar_dados_teste
    criar_dados_teste()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Descomente a linha abaixo para carregar dados de teste
        # load_test_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
