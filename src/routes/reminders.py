from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models.reminder import Reminder
from src.models.lead import Lead
from src.models.db import db
from datetime import datetime

bp = Blueprint('reminders', __name__, url_prefix='/reminders')

@bp.route('/')
@login_required
def index():
    """Lista todos os lembretes."""
    reminders = Reminder.query.order_by(Reminder.due_date).all()
    return render_template('reminders/index.html', reminders=reminders)

@bp.route('/create/<int:lead_id>', methods=('GET', 'POST'))
@login_required
def create(lead_id):
    """Cria um novo lembrete para um lead especÃ­fico."""
    lead = Lead.query.get_or_404(lead_id)
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date_str = request.form['due_date']
        
        error = None
        
        if not title:
            error = 'TÃ­tulo Ã© obrigatÃ³rio.'
        elif not due_date_str:
            error = 'Data de vencimento Ã© obrigatÃ³ria.'
        
        if error is not None:
            flash(error)
        else:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            
            reminder = Reminder(
                lead_id=lead.id,
                title=title,
                description=description,
                due_date=due_date
            )
            
            # Atualizar prÃ³xima aÃ§Ã£o do lead
            lead.next_action = title
            lead.next_action_date = due_date
            
            db.session.add(reminder)
            db.session.commit()
            
            flash('Lembrete criado com sucesso!')
            return redirect(url_for('leads.view', id=lead.id))
    
    return render_template('reminders/create.html', lead=lead)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Atualiza um lembrete existente."""
    reminder = Reminder.query.get_or_404(id)
    lead = Lead.query.get(reminder.lead_id)
    
    if request.method == 'POST':
        reminder.title = request.form['title']
        reminder.description = request.form['description']
        due_date_str = request.form['due_date']
        reminder.is_completed = 'is_completed' in request.form
        
        error = None
        
        if not reminder.title:
            error = 'TÃ­tulo Ã© obrigatÃ³rio.'
        elif not due_date_str:
            error = 'Data de vencimento Ã© obrigatÃ³ria.'
        
        if error is not None:
            flash(error)
        else:
            reminder.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            
            # Se o lembrete for a prÃ³xima aÃ§Ã£o do lead, atualizar
            if lead.next_action_date == reminder.due_date:
                lead.next_action = reminder.title
                lead.next_action_date = reminder.due_date
            
            db.session.commit()
            flash('Lembrete atualizado com sucesso!')
            return redirect(url_for('reminders.index'))
    
    return render_template('reminders/update.html', reminder=reminder, lead=lead)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Exclui um lembrete."""
    reminder = Reminder.query.get_or_404(id)
    lead_id = reminder.lead_id
    
    db.session.delete(reminder)
    db.session.commit()
    
    flash('Lembrete excluÃ­do com sucesso!')
    return redirect(url_for('leads.view', id=lead_id))

@bp.route('/<int:id>/complete', methods=('POST',))
@login_required
def complete(id):
    """Marca um lembrete como concluÃ­do."""
    reminder = Reminder.query.get_or_404(id)
    reminder.is_completed = True
    db.session.commit()
    
    flash('Lembrete marcado como concluÃ­do!')
    return redirect(url_for('reminders.index'))

@bp.route('/today')
@login_required
def today():
    """Lista lembretes para hoje."""
    today = datetime.utcnow().date()
    reminders = Reminder.query.filter(
        db.func.date(Reminder.due_date) == today,
        Reminder.is_completed == False
    ).order_by(Reminder.due_date).all()
    
    return render_template('reminders/today.html', reminders=reminders)

@bp.route('/lead/<int:lead_id>')
@login_required
def by_lead(lead_id):
    """Lista todos os lembretes de um lead especÃ­fico."""
    lead = Lead.query.get_or_404(lead_id)
    reminders = Reminder.query.filter_by(lead_id=lead_id).order_by(Reminder.due_date).all()
    
    return render_template('reminders/by_lead.html', reminders=reminders, lead=lead)

@bp.route('/overdue')
@login_required
def overdue():
    """Lista lembretes atrasados."""
    today = datetime.utcnow().date()
    reminders = Reminder.query.filter(
        db.func.date(Reminder.due_date) < today,
        Reminder.is_completed == False
    ).order_by(Reminder.due_date).all()
    
    return render_template('reminders/overdue.html', reminders=reminders)
