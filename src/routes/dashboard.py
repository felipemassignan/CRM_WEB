from flask import Blueprint, render_template, request
from src.models.lead import Lead
from src.models.interaction import Interaction
from src.models.template import Template
from src.models.reminder import Reminder
from src.models.db import db
from sqlalchemy import func
from datetime import datetime, timedelta
import json

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
def index():
    """Página principal do dashboard."""
    # Contagem de leads por status
    leads_by_status = db.session.query(
        Lead.status, func.count(Lead.id)
    ).group_by(Lead.status).all()
    
    # Contagem de leads por setor
    leads_by_industry = db.session.query(
        Lead.industry, func.count(Lead.id)
    ).group_by(Lead.industry).all()
    
    # Contagem de interações por tipo
    interactions_by_type = db.session.query(
        Interaction.type, func.count(Interaction.id)
    ).group_by(Interaction.type).all()
    
    # Interações por semana (últimas 4 semanas)
    today = datetime.utcnow().date()
    four_weeks_ago = today - timedelta(weeks=4)
    
    interactions_by_week = []
    for i in range(4):
        week_start = four_weeks_ago + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        
        count = Interaction.query.filter(
            func.date(Interaction.date) >= week_start,
            func.date(Interaction.date) <= week_end
        ).count()
        
        interactions_by_week.append({
            'week': f'Semana {i+1}',
            'count': count
        })
    
    # Taxa de resposta
    total_interactions = Interaction.query.count()
    interactions_with_response = Interaction.query.filter_by(response=True).count()
    response_rate = interactions_with_response / total_interactions if total_interactions > 0 else 0
    
    # Lembretes para hoje
    today = datetime.utcnow().date()
    reminders_today = Reminder.query.filter(
        func.date(Reminder.due_date) == today,
        Reminder.is_completed == False
    ).order_by(Reminder.due_date).all()
    
    # Lembretes atrasados
    overdue_reminders = Reminder.query.filter(
        func.date(Reminder.due_date) < today,
        Reminder.is_completed == False
    ).order_by(Reminder.due_date).all()
    
    # Leads recentes
    recent_leads = Lead.query.order_by(Lead.added_date.desc()).limit(5).all()
    
    # Interações recentes
    recent_interactions = Interaction.query.order_by(Interaction.date.desc()).limit(5).all()
    
    # Preparar dados para gráficos
    leads_by_status_data = {
        'labels': [status for status, _ in leads_by_status],
        'values': [count for _, count in leads_by_status]
    }
    
    leads_by_industry_data = {
        'labels': [industry if industry else 'Não especificado' for industry, _ in leads_by_industry],
        'values': [count for _, count in leads_by_industry]
    }
    
    interactions_by_type_data = {
        'labels': [type for type, _ in interactions_by_type],
        'values': [count for _, count in interactions_by_type]
    }
    
    interactions_by_week_data = {
        'labels': [item['week'] for item in interactions_by_week],
        'values': [item['count'] for item in interactions_by_week]
    }
    
    return render_template('dashboard/index.html',
                          leads_by_status=json.dumps(leads_by_status_data),
                          leads_by_industry=json.dumps(leads_by_industry_data),
                          interactions_by_type=json.dumps(interactions_by_type_data),
                          interactions_by_week=json.dumps(interactions_by_week_data),
                          response_rate=response_rate,
                          reminders_today=reminders_today,
                          overdue_reminders=overdue_reminders,
                          recent_leads=recent_leads,
                          recent_interactions=recent_interactions)

@bp.route('/metrics')
def metrics():
    """Página de métricas detalhadas."""
    # Total de leads
    total_leads = Lead.query.count()
    
    # Leads por status
    leads_by_status = db.session.query(
        Lead.status, func.count(Lead.id)
    ).group_by(Lead.status).all()
    
    # Leads adicionados nos últimos 30 dias
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_leads_30d = Lead.query.filter(Lead.added_date >= thirty_days_ago).count()
    
    # Taxa de conversão (leads que chegaram a "Cliente")
    client_leads = Lead.query.filter_by(status='Cliente').count()
    conversion_rate = client_leads / total_leads if total_leads > 0 else 0
    
    # Taxa de churn (leads perdidos)
    lost_leads = Lead.query.filter_by(status='Perdido').count()
    churn_rate = lost_leads / total_leads if total_leads > 0 else 0
    
    # Tempo médio de conversão (dias entre adição e status "Cliente")
    client_leads_data = Lead.query.filter_by(status='Cliente').all()
    conversion_times = []
    
    for lead in client_leads_data:
        if lead.added_date:
            # Aqui assumimos que updated_at é quando o lead virou cliente
            # Em uma implementação real, seria melhor ter um campo específico
            days = (lead.updated_at - lead.added_date).days
            conversion_times.append(days)
    
    avg_conversion_time = sum(conversion_times) / len(conversion_times) if conversion_times else 0
    
    return render_template('dashboard/metrics.html',
                          total_leads=total_leads,
                          leads_by_status=leads_by_status,
                          new_leads_30d=new_leads_30d,
                          conversion_rate=conversion_rate,
                          churn_rate=churn_rate,
                          avg_conversion_time=avg_conversion_time)

@bp.route('/activities')
def activities():
    """Página de atividades recentes."""
    # Interações recentes
    recent_interactions = Interaction.query.order_by(Interaction.date.desc()).limit(20).all()
    
    # Leads recentes
    recent_leads = Lead.query.order_by(Lead.added_date.desc()).limit(20).all()
    
    # Templates mais usados
    popular_templates = Template.query.order_by(Template.usage_count.desc()).limit(5).all()
    
    return render_template('dashboard/activities.html',
                          recent_interactions=recent_interactions,
                          recent_leads=recent_leads,
                          popular_templates=popular_templates)

@bp.route('/reports')
def reports():
    """Página de relatórios."""
    # Implementação básica - será expandida posteriormente
    return render_template('dashboard/reports.html')
