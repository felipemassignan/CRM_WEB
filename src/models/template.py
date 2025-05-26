from src.models.db import db
from datetime import datetime

class Template(db.Model):
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # Conexão LinkedIn, Primeira Mensagem, Follow-up, etc.
    target_position = db.Column(db.String(100))  # Cargo alvo: CEO, CTO, Diretor Industrial, etc.
    subject = db.Column(db.String(255))  # Assunto para emails
    content = db.Column(db.Text, nullable=False)
    variables = db.Column(db.String(255))  # Lista de variáveis utilizadas
    usage_notes = db.Column(db.Text)
    usage_count = db.Column(db.Integer, default=0)
    last_used = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Template {self.id} - {self.category}>'
