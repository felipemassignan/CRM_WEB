from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models.interaction import Interaction
from src.models.lead import Lead
from src.models.db import db
from datetime import datetime

bp = Blueprint('interactions', __name__, url_prefix='/interactions')

@bp.route('/')
@login_required
def index():
    """Lista todas as interaÃ§Ãµes."""
    interactions = Interaction.query.order_by(Interaction.date.desc()).all()
    return render_template('interactions/index.html', interactions=interactions)

@bp.route('/create/<int:lead_id>', methods=('GET', 'POST'))
@login_required
def create(lead_id):
    """Cria uma nova interaÃ§Ã£o para um lead especÃ­fico."""
    lead = Lead.query.get_or_404(lead_id)
    
    if request.method == 'POST':
        interaction_type = request.form['type']
        content = request.form['content']
        response = 'response' in request.form
        next_step = request.form['next_step']
        result = request.form['result']
        notes = request.form['notes']
        
        # Processar data do prÃ³ximo passo
        next_step_date = None
        if request.form['next_step_date']:
            next_step_date = datetime.strptime(request.form['next_step_date'], '%Y-%m-%d')
        
        error = None
        
        if not interaction_type:
            error = 'Tipo de interaÃ§Ã£o Ã© obrigatÃ³rio.'
        
        if error is not None:
            flash(error)
        else:
            interaction = Interaction(
                lead_id=lead.id,
                type=interaction_type,
                content=content,
                response=response,
                next_step=next_step,
                next_step_date=next_step_date,
                result=result,
                notes=notes,
                date=datetime.utcnow()
            )
            
            # Atualizar a data da Ãºltima interaÃ§Ã£o do lead
            lead.last_interaction_date = datetime.utcnow()
            
            # Se houver prÃ³ximo passo, atualizar no lead tambÃ©m
            if next_step:
                lead.next_action = next_step
                lead.next_action_date = next_step_date
            
            db.session.add(interaction)
            db.session.commit()
            
            flash('InteraÃ§Ã£o registrada com sucesso!')
            return redirect(url_for('leads.view', id=lead.id))
    
    return render_template('interactions/create.html', lead=lead)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Atualiza uma interaÃ§Ã£o existente."""
    interaction = Interaction.query.get_or_404(id)
    lead = Lead.query.get(interaction.lead_id)
    
    if request.method == 'POST':
        interaction.type = request.form['type']
        interaction.content = request.form['content']
        interaction.response = 'response' in request.form
        interaction.next_step = request.form['next_step']
        interaction.result = request.form['result']
        interaction.notes = request.form['notes']
        
        # Processar data do prÃ³ximo passo
        if request.form['next_step_date']:
            interaction.next_step_date = datetime.strptime(request.form['next_step_date'], '%Y-%m-%d')
        
        error = None
        
        if not interaction.type:
            error = 'Tipo de interaÃ§Ã£o Ã© obrigatÃ³rio.'
        
        if error is not None:
            flash(error)
        else:
            # Se houver prÃ³ximo passo, atualizar no lead tambÃ©m
            if interaction.next_step:
                lead.next_action = interaction.next_step
                lead.next_action_date = interaction.next_step_date
                
            db.session.commit()
            flash('InteraÃ§Ã£o atualizada com sucesso!')
            return redirect(url_for('leads.view', id=interaction.lead_id))
    
    return render_template('interactions/update.html', interaction=interaction, lead=lead)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Exclui uma interaÃ§Ã£o."""
    interaction = Interaction.query.get_or_404(id)
    lead_id = interaction.lead_id
    
    db.session.delete(interaction)
    db.session.commit()
    
    flash('InteraÃ§Ã£o excluÃ­da com sucesso!')
    return redirect(url_for('leads.view', id=lead_id))

@bp.route('/lead/<int:lead_id>')
@login_required
def by_lead(lead_id):
    """Lista todas as interaÃ§Ãµes de um lead especÃ­fico."""
    lead = Lead.query.get_or_404(lead_id)
    interactions = Interaction.query.filter_by(lead_id=lead_id).order_by(Interaction.date.desc()).all()
    
    return render_template('interactions/by_lead.html', interactions=interactions, lead=lead)

@bp.route('/pending')
@login_required
def pending():
    """Lista interaÃ§Ãµes pendentes (com prÃ³ximo passo)."""
    interactions = Interaction.query.filter(Interaction.next_step != None, 
                                          Interaction.next_step != '').order_by(Interaction.next_step_date).all()
    
    return render_template('interactions/pending.html', interactions=interactions, now=datetime.utcnow())
