# src/routes/leads.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.services.lead_service import LeadService
from src.forms.lead_forms import LeadForm
from src.models.lead import Lead # Adicione esta importação
from flask import request # Adicione esta importação para filtros
from datetime import datetime

bp = Blueprint('leads', __name__, url_prefix='/leads')

@bp.route('/')
@login_required
def index():
    leads = LeadService.get_all_leads()
    return render_template('leads/index.html',
                              leads=leads,
                              status_choices=Lead.get_status_choices(),
                              industry_choices=Lead.get_industry_choices(),
                              priority_choices=Lead.get_priority_choices(),
                              region_choices=Lead.get_region_choices(),
                              position_choices=Lead.get_position_choices(),
                              status_filter=request.args.get('status'),
                              industry_filter=request.args.get('industry'),
                              priority_filter=request.args.get('priority'),
                              region_filter=request.args.get('region'),
                              position_filter=request.args.get('position'))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = LeadForm()
    if form.validate_on_submit():
        data = form.data
        LeadService.create_lead(data)
        flash('Lead criado com sucesso!')
        return redirect(url_for('leads.index'))
        return render_template('leads/create.html',
                           form=form,
                           position_choices=Lead.get_position_choices(),
                           industry_choices=Lead.get_industry_choices(),
                           region_choices=Lead.get_region_choices(),
                           status_choices=Lead.get_status_choices(),
                           priority_choices=Lead.get_priority_choices(),
                           source_choices=Lead.get_source_choices())

@bp.route('/<int:lead_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(lead_id):
    lead = LeadService.get_lead_by_id(lead_id)
    if not lead:
        flash('Lead não encontrado.')
        return redirect(url_for('leads.index'))

    form = LeadForm(obj=lead)
    if form.validate_on_submit():
        LeadService.update_lead(lead_id, form.data)
        flash('Lead atualizado com sucesso!')
        return redirect(url_for('leads.index'))

    return render_template('leads/edit.html',
                              form=form,
                              lead=lead,
                              position_choices=Lead.get_position_choices(),
                              industry_choices=Lead.get_industry_choices(),
                              region_choices=Lead.get_region_choices(),
                              status_choices=Lead.get_status_choices(),
                              priority_choices=Lead.get_priority_choices(),
                              source_choices=Lead.get_source_choices())

@bp.route('/<int:lead_id>/delete', methods=['POST'])
@login_required
def delete(lead_id):
    lead = LeadService.delete_lead(lead_id)
    if not lead:
        flash('Lead não encontrado.')
    else:
        flash('Lead excluído com sucesso.')
    return redirect(url_for('leads.index'))

@bp.route('/<int:lead_id>')
@login_required
def view(lead_id):
    lead = LeadService.get_lead_by_id(lead_id)
    if not lead:
        flash('Lead não encontrado.')
        return redirect(url_for('leads.index'))
    
    # Carregar interações e lembretes para o lead
    interactions = Interaction.query.filter_by(lead_id=lead_id).order_by(Interaction.date.desc()).all()
    reminders = Reminder.query.filter_by(lead_id=lead_id).order_by(Reminder.due_date).all()

    return render_template('leads/view.html', 
                           lead=lead, 
                           interactions=interactions, 
                           reminders=reminders, 
                           now=datetime.utcnow())