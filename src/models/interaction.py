from src.models.db import db
from datetime import datetime

class Interaction(db.Model):
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)  # ConexÃ£o LinkedIn, Mensagem, Email, etc.
    content = db.Column(db.Text)
    response = db.Column(db.Boolean, default=False)
    next_step = db.Column(db.String(255))
    next_step_date = db.Column(db.DateTime)
    result = db.Column(db.String(20))  # Positivo, Neutro, Negativo
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Interaction {self.id} - {self.type}>'
