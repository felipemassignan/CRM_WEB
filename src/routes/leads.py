# src/routes/leads.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from src.services.lead_service import LeadService
from src.forms.lead_forms import LeadForm

bp = Blueprint('leads', __name__, url_prefix='/leads')

@bp.route('/')
@login_required
def index():
    leads = LeadService.get_all_leads()
    return render_template('leads/index.html', leads=leads)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = LeadForm()
    if form.validate_on_submit():
        data = form.data
        LeadService.create_lead(data)
        flash('Lead criado com sucesso!')
        return redirect(url_for('leads.index'))
    return render_template('leads/create.html', form=form)

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

    return render_template('leads/edit.html', form=form, lead=lead)

@bp.route('/<int:lead_id>/delete', methods=['POST'])
@login_required
def delete(lead_id):
    lead = LeadService.delete_lead(lead_id)
    if not lead:
        flash('Lead não encontrado.')
    else:
        flash('Lead excluído com sucesso.')
    return redirect(url_for('leads.index'))