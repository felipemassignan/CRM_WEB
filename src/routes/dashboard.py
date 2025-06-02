from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from src.models.lead import Lead
from src.models.interaction import Interaction
from src.models.reminder import Reminder
from src.models.db import db
from sqlalchemy import func
from datetime import datetime, timedelta
import humanize
import pytz

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    """Enhanced dashboard with better usability and more insights."""
    # Quick stats
    total_leads = Lead.query.count()
    client_leads = Lead.query.filter_by(status='Cliente').count()
    conversion_rate = client_leads / total_leads if total_leads > 0 else 0
    
    today = datetime.now(pytz.UTC).date()
    today_interactions = Interaction.query.filter(
        func.date(Interaction.date) == today
    ).count()
    
    pending_reminders = Reminder.query.filter_by(is_completed=False).count()

    # Leads by status for pipeline
    leads_by_status = {}
    for status in ['Novo', 'Conectado', 'Conversando', 'ReuniÃ£o Agendada', 'Proposta Enviada', 'Cliente']:
        leads_by_status[status] = Lead.query.filter_by(status=status).all()

    # Recent activities
    recent_activities = []
    
    # Get recent interactions
    recent_interactions = Interaction.query.order_by(Interaction.date.desc()).limit(10).all()
    for interaction in recent_interactions:
        activity_type = {
            'Email': {'class': 'info', 'icon': 'envelope'},
            'LigaÃ§Ã£o': {'class': 'success', 'icon': 'telephone'},
            'ReuniÃ£o': {'class': 'primary', 'icon': 'calendar-event'},
            'Mensagem LinkedIn': {'class': 'info', 'icon': 'linkedin'}
        }.get(interaction.type, {'class': 'secondary', 'icon': 'chat'})
        
        recent_activities.append({
            'type_class': activity_type['class'],
            'icon': activity_type['icon'],
            'description': f"InteraÃ§Ã£o com {interaction.lead.name} ({interaction.type})",
            'time_ago': humanize.naturaltime(datetime.now() - interaction.date)
        })

    # Get recent leads
    recent_leads = Lead.query.order_by(Lead.added_date.desc()).limit(5).all()
    for lead in recent_leads:
        recent_activities.append({
            'type_class': 'primary',
            'icon': 'person-plus',
            'description': f"Novo lead adicionado: {lead.name} ({lead.company})",
            'time_ago': humanize.naturaltime(datetime.now() - lead.added_date)
        })

    # Sort activities by time
    recent_activities.sort(key=lambda x: x['time_ago'])

    # Upcoming reminders
    upcoming_reminders = Reminder.query.filter(
        Reminder.due_date >= datetime.now(),
        Reminder.is_completed == False
    ).order_by(Reminder.due_date).limit(5).all()

    # Chart data
    # Industry distribution
    industry_data = db.session.query(
        Lead.industry,
        func.count(Lead.id)
    ).group_by(Lead.industry).all()
    
    industry_labels = [ind[0] for ind in industry_data]
    industry_counts = [ind[1] for ind in industry_data]

    # Weekly interactions
    week_labels = []
    week_data = []
    for i in range(7, 0, -1):
        date = datetime.now().date() - timedelta(days=i)
        week_labels.append(date.strftime('%d/%m'))
        count = Interaction.query.filter(
            func.date(Interaction.date) == date
        ).count()
        week_data.append(count)

    return render_template('dashboard/index.html',
                         total_leads=total_leads,
                         conversion_rate=conversion_rate,
                         today_interactions=today_interactions,
                         pending_reminders=pending_reminders,
                         leads_by_status=leads_by_status,
                         recent_activities=recent_activities,
                         upcoming_reminders=upcoming_reminders,
                         industry_labels=industry_labels,
                         industry_data=industry_counts,
                         week_labels=week_labels,
                         week_data=week_data,
                         now=datetime.now(pytz.UTC)) 