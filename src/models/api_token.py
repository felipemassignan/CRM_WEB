# src/models/api_token.py
from src.models.db import db
from datetime import datetime

class ApiToken(db.Model):
    __tablename__ = 'api_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Nome descritivo do token
    token = db.Column(db.String(64), unique=True, nullable=False)  # Token de acesso
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, nullable=True)
    
    # Relacionamento com o usuário
    user = db.relationship('User', backref=db.backref('api_tokens', lazy=True))