from flask import Flask, jsonify, request
import os
import sys
import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Inicializar aplicação
app = Flask(__name__)

# Obter a URL do banco de dados da variável de ambiente
database_url = os.getenv('DATABASE_URL')

if not database_url:
    logger.warning("DATABASE_URL não está definida. Usando SQLite como fallback.")
    database_url = "sqlite:///tmp/app.db"
else:
    logger.info(f"Conectando ao PostgreSQL: {database_url.split('@')[0].split('://')[0]}://*****@{database_url.split('@')[1]}")

# Ajustar URL para SQLAlchemy se necessário
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Verificar conexão antes de usar
    'pool_recycle': 300,    # Reciclar conexões a cada 5 minutos
    'pool_timeout': 30,     # Timeout de 30 segundos para obter conexão
    'pool_size': 5,         # Tamanho do pool de conexões
    'max_overflow': 10      # Máximo de conexões extras
}

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Defina um modelo simples
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Função para tentar conectar ao banco de dados com retry
def connect_db_with_retry(max_retries=5, retry_delay=2):
    retries = 0
    while retries < max_retries:
        try:
            logger.info(f"Tentativa {retries + 1} de conectar ao banco de dados...")
            with app.app_context():
                # Testar conexão
                db.session.execute('SELECT 1')
                logger.info("Conexão com o banco de dados estabelecida com sucesso!")
                return True
        except Exception as e:
            retries += 1
            logger.warning(f"Falha ao conectar ao banco de dados (tentativa {retries}/{max_retries}): {str(e)}")
            if retries < max_retries:
                logger.info(f"Tentando novamente em {retry_delay} segundos...")
                time.sleep(retry_delay)
    
    logger.error(f"Não foi possível conectar ao banco de dados após {max_retries} tentativas.")
    return False

# Inicializar banco de dados
def init_db():
    if connect_db_with_retry():
        try:
            with app.app_context():
                logger.info("Criando tabelas do banco de dados...")
                db.create_all()
                logger.info("Tabelas criadas com sucesso!")
                return True
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {str(e)}")
    return False

# Inicializar banco de dados na inicialização
db_initialized = init_db()

@app.route('/')
def hello():
    db_type = "PostgreSQL" if "postgresql" in database_url else "SQLite"
    db_status = "initialized" if db_initialized else "not initialized"
    return jsonify({
        "message": f"Hello, Railway! App is running with {db_type}.",
        "database_status": db_status,
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    try:
        # Verificar conexão com o banco de dados
        with app.app_context():
            db.session.execute('SELECT 1')
        db_status = "connected"
    except Exception as e:
        logger.error(f"Erro na verificação de saúde do banco de dados: {str(e)}")
        db_status = f"error: {str(e)}"
    
    return jsonify({
        "status": "ok",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/setup-db')
def setup_db():
    try:
        with app.app_context():
            db.create_all()
        return jsonify({"message": "Database tables created"}), 200
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/leads', methods=['GET'])
def get_leads():
    try:
        with app.app_context():
            leads = Lead.query.all()
            return jsonify([lead.to_dict() for lead in leads])
    except Exception as e:
        logger.error(f"Erro ao obter leads: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/leads', methods=['POST'])
def create_lead():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados JSON não fornecidos"}), 400
        
        required_fields = ['name', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo obrigatório ausente: {field}"}), 400
        
        with app.app_context():
            lead = Lead(name=data['name'], email=data['email'])
            db.session.add(lead)
            db.session.commit()
            return jsonify({
                "message": "Lead criado com sucesso",
                "lead": lead.to_dict()
            }), 201
    except Exception as e:
        logger.error(f"Erro ao criar lead: {str(e)}")
        if 'db' in locals() and db.session:
            db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/add-lead/<name>/<email>')
def add_lead(name, email):
    try:
        with app.app_context():
            lead = Lead(name=name, email=email)
            db.session.add(lead)
            db.session.commit()
            return jsonify({"message": f"Lead {name} added successfully", "id": lead.id}), 201
    except Exception as e:
        logger.error(f"Erro ao adicionar lead: {str(e)}")
        if 'db' in locals() and db.session:
            db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/debug')
def debug():
    """Endpoint para depuração"""
    try:
        # Testar conexão com o banco de dados
        with app.app_context():
            db_connection_test = "success"
            try:
                db.session.execute('SELECT 1')
            except Exception as e:
                db_connection_test = f"error: {str(e)}"
        
        info = {
            "database_url": f"{database_url.split('@')[0].split('://')[0]}://*****@{database_url.split('@')[1]}" if '@' in database_url else database_url,
            "database_connection_test": db_connection_test,
            "database_initialized": db_initialized,
            "app_dir": os.getcwd(),
            "env_vars": {k: v for k, v in os.environ.items() if not k.startswith('_') and "SECRET" not in k and "KEY" not in k and "PASSWORD" not in k and "TOKEN" not in k}
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)