from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from src.models.lead import Lead, INDUSTRY_CHOICES, POSITION_CHOICES, REGION_CHOICES, STATUS_CHOICES, PRIORITY_CHOICES, SOURCE_CHOICES
from src.models.db import db
from datetime import datetime
import csv
import io
import json

bp = Blueprint('leads', __name__, url_prefix='/leads')

@bp.route('/')
@login_required
def index():
    """Lista todos os leads."""
    leads = Lead.query.order_by(Lead.added_date.desc()).all()
    return render_template('leads/index.html', leads=leads, 
                          industry_choices=INDUSTRY_CHOICES,
                          position_choices=POSITION_CHOICES,
                          region_choices=REGION_CHOICES,
                          status_choices=STATUS_CHOICES,
                          priority_choices=PRIORITY_CHOICES)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Cria um novo lead."""
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        company = request.form['company']
        industry = request.form['industry']
        linkedin_url = request.form['linkedin_url']
        email = request.form['email']
        phone = request.form['phone']
        region = request.form['region']
        state = request.form.get('state', '')
        city = request.form.get('city', '')
        status = request.form['status']
        source = request.form['source']
        priority = request.form['priority']
        company_size = request.form.get('company_size', '')
        annual_revenue = request.form.get('annual_revenue', '')
        technologies_used = request.form.get('technologies_used', '')
        pain_points = request.form.get('pain_points', '')
        notes = request.form['notes']
        
        error = None
        
        if not name:
            error = 'Nome é obrigatório.'
        
        if error is not None:
            flash(error)
        else:
            lead = Lead(
                name=name,
                position=position,
                company=company,
                industry=industry,
                linkedin_url=linkedin_url,
                email=email,
                phone=phone,
                region=region,
                state=state,
                city=city,
                status=status,
                source=source,
                priority=priority,
                company_size=company_size,
                annual_revenue=annual_revenue,
                technologies_used=technologies_used,
                pain_points=pain_points,
                notes=notes,
                added_date=datetime.utcnow()
            )
            db.session.add(lead)
            db.session.commit()
            flash('Lead criado com sucesso!')
            return redirect(url_for('leads.index'))
    
    return render_template('leads/create.html',
                          industry_choices=INDUSTRY_CHOICES,
                          position_choices=POSITION_CHOICES,
                          region_choices=REGION_CHOICES,
                          status_choices=STATUS_CHOICES,
                          priority_choices=PRIORITY_CHOICES,
                          source_choices=SOURCE_CHOICES)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Atualiza um lead existente."""
    lead = Lead.query.get_or_404(id)
    
    if request.method == 'POST':
        lead.name = request.form['name']
        lead.position = request.form['position']
        lead.company = request.form['company']
        lead.industry = request.form['industry']
        lead.linkedin_url = request.form['linkedin_url']
        lead.email = request.form['email']
        lead.phone = request.form['phone']
        lead.region = request.form['region']
        lead.state = request.form.get('state', '')
        lead.city = request.form.get('city', '')
        lead.status = request.form['status']
        lead.source = request.form['source']
        lead.priority = request.form['priority']
        lead.company_size = request.form.get('company_size', '')
        lead.annual_revenue = request.form.get('annual_revenue', '')
        lead.technologies_used = request.form.get('technologies_used', '')
        lead.pain_points = request.form.get('pain_points', '')
        lead.notes = request.form['notes']
        
        if 'next_action' in request.form:
            lead.next_action = request.form['next_action']
        
        if 'next_action_date' in request.form and request.form['next_action_date']:
            lead.next_action_date = datetime.strptime(request.form['next_action_date'], '%Y-%m-%d')
        
        error = None
        
        if not lead.name:
            error = 'Nome é obrigatório.'
        
        if error is not None:
            flash(error)
        else:
            db.session.commit()
            flash('Lead atualizado com sucesso!')
            return redirect(url_for('leads.index'))
    
    return render_template('leads/update.html', lead=lead,
                          industry_choices=INDUSTRY_CHOICES,
                          position_choices=POSITION_CHOICES,
                          region_choices=REGION_CHOICES,
                          status_choices=STATUS_CHOICES,
                          priority_choices=PRIORITY_CHOICES,
                          source_choices=SOURCE_CHOICES)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Exclui um lead."""
    lead = Lead.query.get_or_404(id)
    db.session.delete(lead)
    db.session.commit()
    flash('Lead excluído com sucesso!')
    return redirect(url_for('leads.index'))

@bp.route('/<int:id>/view')
@login_required
def view(id):
    """Visualiza detalhes de um lead."""
    lead = Lead.query.get_or_404(id)
    interactions = lead.interactions
    return render_template('leads/view.html', lead=lead, interactions=interactions)

@bp.route('/filter', methods=('GET', 'POST'))
@login_required
def filter():
    """Filtra leads por status, setor, prioridade, etc."""
    status = request.args.get('status')
    industry = request.args.get('industry')
    priority = request.args.get('priority')
    region = request.args.get('region')
    position = request.args.get('position')
    
    query = Lead.query
    
    if status:
        query = query.filter(Lead.status == status)
    
    if industry:
        query = query.filter(Lead.industry == industry)
    
    if priority:
        query = query.filter(Lead.priority == priority)
        
    if region:
        query = query.filter(Lead.region == region)
        
    if position:
        query = query.filter(Lead.position == position)
    
    leads = query.order_by(Lead.added_date.desc()).all()
    
    return render_template('leads/index.html', leads=leads, 
                          status_filter=status, 
                          industry_filter=industry, 
                          priority_filter=priority,
                          region_filter=region,
                          position_filter=position,
                          industry_choices=INDUSTRY_CHOICES,
                          position_choices=POSITION_CHOICES,
                          region_choices=REGION_CHOICES,
                          status_choices=STATUS_CHOICES,
                          priority_choices=PRIORITY_CHOICES)

@bp.route('/import', methods=('GET', 'POST'))
@login_required
def import_leads():
    """Importa leads de um arquivo CSV."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
            
        if file and file.filename.endswith('.csv'):
            try:
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.DictReader(stream)
                
                count = 0
                for row in csv_reader:
                    lead = Lead(
                        name=row.get('name', ''),
                        position=row.get('position', ''),
                        company=row.get('company', ''),
                        industry=row.get('industry', ''),
                        linkedin_url=row.get('linkedin_url', ''),
                        email=row.get('email', ''),
                        phone=row.get('phone', ''),
                        region=row.get('region', ''),
                        state=row.get('state', ''),
                        city=row.get('city', ''),
                        status=row.get('status', 'Novo'),
                        source=row.get('source', 'Importação'),
                        priority=row.get('priority', 'Média'),
                        company_size=row.get('company_size', ''),
                        annual_revenue=row.get('annual_revenue', ''),
                        technologies_used=row.get('technologies_used', ''),
                        pain_points=row.get('pain_points', ''),
                        notes=row.get('notes', ''),
                        added_date=datetime.utcnow()
                    )
                    db.session.add(lead)
                    count += 1
                
                db.session.commit()
                flash(f'{count} leads importados com sucesso!')
                return redirect(url_for('leads.index'))
            except Exception as e:
                flash(f'Erro ao importar: {str(e)}')
                return redirect(request.url)
        else:
            flash('Formato de arquivo inválido. Por favor, envie um arquivo CSV.')
            return redirect(request.url)
    
    return render_template('leads/import.html')

@bp.route('/export')
@login_required
def export_leads():
    """Exporta leads para um arquivo CSV."""
    leads = Lead.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Cabeçalho
    writer.writerow(['id', 'name', 'position', 'company', 'industry', 'linkedin_url', 
                    'email', 'phone', 'region', 'state', 'city', 'status', 'source', 
                    'added_date', 'last_interaction_date', 'next_action', 'next_action_date', 
                    'owner', 'priority', 'company_size', 'annual_revenue', 'technologies_used', 
                    'pain_points', 'notes'])
    
    # Dados
    for lead in leads:
        writer.writerow([
            lead.id,
            lead.name,
            lead.position,
            lead.company,
            lead.industry,
            lead.linkedin_url,
            lead.email,
            lead.phone,
            lead.region,
            lead.state,
            lead.city,
            lead.status,
            lead.source,
            lead.added_date.strftime('%Y-%m-%d %H:%M:%S') if lead.added_date else '',
            lead.last_interaction_date.strftime('%Y-%m-%d %H:%M:%S') if lead.last_interaction_date else '',
            lead.next_action,
            lead.next_action_date.strftime('%Y-%m-%d %H:%M:%S') if lead.next_action_date else '',
            lead.owner,
            lead.priority,
            lead.company_size,
            lead.annual_revenue,
            lead.technologies_used,
            lead.pain_points,
            lead.notes
        ])
    
    output.seek(0)
    return jsonify({'csv_data': output.getvalue()})

@bp.route('/options')
@login_required
def get_options():
    """Retorna as opções para os campos de seleção."""
    return jsonify({
        'industry_choices': INDUSTRY_CHOICES,
        'position_choices': POSITION_CHOICES,
        'region_choices': REGION_CHOICES,
        'status_choices': STATUS_CHOICES,
        'priority_choices': PRIORITY_CHOICES,
        'source_choices': SOURCE_CHOICES
    })
