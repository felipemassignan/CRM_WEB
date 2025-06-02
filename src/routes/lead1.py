from src.models.db import db
from datetime import datetime

# Listas de opções para campos específicos
INDUSTRY_CHOICES = [
    'Manufatura Geral',
    'Metalurgia',
    'Usinagem',
    'Autopeças',
    'Linha Branca',
    'Eletrodomésticos',
    'Motores Elétricos',
    'Automação Industrial',
    'Indústria Automotiva',
    'Aeroespacial',
    'Equipamentos Industriais',
    'Plásticos e Borrachas',
    'Eletrônicos',
    'Têxtil',
    'Alimentos e Bebidas',
    'Farmacêutica',
    'Química',
    'Outros'
]

POSITION_CHOICES = [
    'CEO',
    'COO',
    'CTO',
    'CFO',
    'Diretor Industrial',
    'Diretor de Operações',
    'Diretor de Produção',
    'Diretor de Qualidade',
    'Diretor de Manufatura',
    'Gerente Industrial',
    'Gerente de Operações',
    'Gerente de Produção',
    'Gerente de Qualidade',
    'Gerente de Manufatura',
    'Engenheiro de Produção',
    'Engenheiro de Qualidade',
    'Supervisor de Produção',
    'Supervisor de Qualidade',
    'Outros'
]

REGION_CHOICES = [
    'Sul',
    'Sudeste',
    'Centro-Oeste',
    'Nordeste',
    'Norte'
]

STATUS_CHOICES = [
    'Novo',
    'Conectado',
    'Conversando',
    'Reunião Agendada',
    'Proposta Enviada',
    'Negociação',
    'Cliente',
    'Perdido',
    'Em Pausa'
]

PRIORITY_CHOICES = [
    'Alta',
    'Média',
    'Baixa'
]

SOURCE_CHOICES = [
    'LinkedIn',
    'Email',
    'Indicação',
    'Evento',
    'Site',
    'Pesquisa',
    'Outro'
]

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    company = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(255))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    region = db.Column(db.String(100))
    state = db.Column(db.String(50))  # Estado brasileiro específico
    city = db.Column(db.String(100))  # Cidade
    status = db.Column(db.String(50), default='Novo')
    source = db.Column(db.String(50))
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_interaction_date = db.Column(db.DateTime)
    next_action = db.Column(db.String(255))
    next_action_date = db.Column(db.DateTime)
    owner = db.Column(db.String(100))
    priority = db.Column(db.String(20), default='Média')
    company_size = db.Column(db.String(50))  # Tamanho da empresa
    annual_revenue = db.Column(db.String(100))  # Faturamento anual estimado
    technologies_used = db.Column(db.String(255))  # Tecnologias utilizadas
    pain_points = db.Column(db.Text)  # Pontos de dor específicos
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    interactions = db.relationship('Interaction', backref='lead', lazy=True, cascade="all, delete-orphan")
    reminders = db.relationship('Reminder', backref='lead', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Lead {self.name} - {self.company}>'
        
    @staticmethod
    def get_industry_choices():
        return INDUSTRY_CHOICES
        
    @staticmethod
    def get_position_choices():
        return POSITION_CHOICES
        
    @staticmethod
    def get_region_choices():
        return REGION_CHOICES
        
    @staticmethod
    def get_status_choices():
        return STATUS_CHOICES
        
    @staticmethod
    def get_priority_choices():
        return PRIORITY_CHOICES
        
    @staticmethod
    def get_source_choices():
        return SOURCE_CHOICES
