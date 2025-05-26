from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Usar um diretório com permissões adequadas
db_path = os.path.join('/tmp', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/')
def hello():
    return "Hello, Railway! App is running with SQLAlchemy."

@app.route('/health')
def health():
    return {"status": "ok"}, 200

@app.route('/setup-db')
def setup_db():
    try:
        db.create_all()
        return {"message": "Database tables created"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/leads')
def get_leads():
    try:
        leads = Lead.query.all()
        return jsonify([lead.to_dict() for lead in leads])
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/add-lead/<name>/<email>')
def add_lead(name, email):
    try:
        lead = Lead(name=name, email=email)
        db.session.add(lead)
        db.session.commit()
        return {"message": f"Lead {name} added successfully", "id": lead.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

@app.route('/debug')
def debug():
    """Endpoint para depuração"""
    info = {
        "sqlite_path": db_path,
        "sqlite_dir_exists": os.path.exists(os.path.dirname(db_path)),
        "sqlite_dir_writable": os.access(os.path.dirname(db_path), os.W_OK),
        "app_dir": os.getcwd(),
        "tmp_dir_exists": os.path.exists('/tmp'),
        "tmp_dir_writable": os.access('/tmp', os.W_OK),
        "env_vars": {k: v for k, v in os.environ.items() if not k.startswith('_')}
    }
    return jsonify(info)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)