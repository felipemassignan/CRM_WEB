from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from src.models.lead import Lead
from src.models.interaction import Interaction
from src.models.template import Template
from src.models.db import db
import csv
import io
import pandas as pd
from datetime import datetime

bp = Blueprint('integrations', __name__, url_prefix='/integrations')

@bp.route('/')
@login_required
def index():
    """PÃ¡gina principal de integraÃ§Ãµes."""
    return render_template('integrations/index.html')

@bp.route('/email', methods=('GET', 'POST'))
@login_required
def email():
    """IntegraÃ§Ã£o com email."""
    if request.method == 'POST':
        # ImplementaÃ§Ã£o bÃ¡sica - serÃ¡ expandida posteriormente
        flash('ConfiguraÃ§Ã£o de email salva com sucesso!')
        return redirect(url_for('integrations.index'))
    
    return render_template('integrations/email.html')

@bp.route('/linkedin', methods=('GET', 'POST'))
@login_required
def linkedin():
    """IntegraÃ§Ã£o com LinkedIn."""
    if request.method == 'POST':
        # ImplementaÃ§Ã£o bÃ¡sica - serÃ¡ expandida posteriormente
        flash('ConfiguraÃ§Ã£o do LinkedIn salva com sucesso!')
        return redirect(url_for('integrations.index'))
    
    return render_template('integrations/linkedin.html')

@bp.route('/import', methods=('GET', 'POST'))
@login_required
def import_data():
    """Importa dados de um arquivo CSV."""
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
                # Ler o arquivo CSV
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_data = csv.reader(stream)
                
                # Obter cabeÃ§alho
                header = next(csv_data)
                
                # Verificar colunas mÃ­nimas necessÃ¡rias
                required_columns = ['name', 'company', 'position']
                missing_columns = [col for col in required_columns if col not in header]
                
                if missing_columns:
                    flash(f'Colunas obrigatÃ³rias ausentes: {", ".join(missing_columns)}')
                    return redirect(request.url)
                
                # Mapear Ã­ndices das colunas
                name_idx = header.index('name')
                company_idx = header.index('company')
                position_idx = header.index('position')
                
                # Ãndices opcionais
                email_idx = header.index('email') if 'email' in header else None
                phone_idx = header.index('phone') if 'phone' in header else None
                industry_idx = header.index('industry') if 'industry' in header else None
                linkedin_idx = header.index('linkedin_url') if 'linkedin_url' in header else None
                region_idx = header.index('region') if 'region' in header else None
                
                # Importar leads
                imported_count = 0
                for row in csv_data:
                    if len(row) >= 3:  # Pelo menos nome, empresa e cargo
                        lead = Lead(
                            name=row[name_idx],
                            company=row[company_idx],
                            position=row[position_idx],
                            email=row[email_idx] if email_idx is not None and email_idx < len(row) else None,
                            phone=row[phone_idx] if phone_idx is not None and phone_idx < len(row) else None,
                            industry=row[industry_idx] if industry_idx is not None and industry_idx < len(row) else None,
                            linkedin_url=row[linkedin_idx] if linkedin_idx is not None and linkedin_idx < len(row) else None,
                            region=row[region_idx] if region_idx is not None and region_idx < len(row) else None,
                            status='Novo',
                            source='ImportaÃ§Ã£o CSV',
                            added_date=datetime.utcnow()
                        )
                        db.session.add(lead)
                        imported_count += 1
                
                db.session.commit()
                flash(f'{imported_count} leads importados com sucesso!')
                return redirect(url_for('leads.index'))
            
            except Exception as e:
                flash(f'Erro ao importar arquivo: {str(e)}')
                return redirect(request.url)
        else:
            flash('Formato de arquivo nÃ£o suportado. Por favor, envie um arquivo CSV.')
            return redirect(request.url)
    
    return render_template('integrations/import.html')

@bp.route('/export')
@login_required
def export_data():
    """Exporta dados para um arquivo CSV."""
    export_type = request.args.get('type', 'leads')
    
    if export_type == 'leads':
        # Exportar leads
        leads = Lead.query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escrever cabeÃ§alho
        writer.writerow(['id', 'name', 'position', 'company', 'industry', 'linkedin_url', 
                        'email', 'phone', 'region', 'status', 'source', 'added_date', 
                        'last_interaction_date', 'next_action', 'next_action_date', 
                        'priority', 'notes'])
        
        # Escrever dados
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
                lead.status,
                lead.source,
                lead.added_date.strftime('%Y-%m-%d %H:%M:%S') if lead.added_date else '',
                lead.last_interaction_date.strftime('%Y-%m-%d %H:%M:%S') if lead.last_interaction_date else '',
                lead.next_action,
                lead.next_action_date.strftime('%Y-%m-%d %H:%M:%S') if lead.next_action_date else '',
                lead.priority,
                lead.notes
            ])
        
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=leads.csv'
        }
    
    elif export_type == 'interactions':
        # Exportar interaÃ§Ãµes
        interactions = Interaction.query.all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Escrever cabeÃ§alho
        writer.writerow(['id', 'lead_id', 'lead_name', 'date', 'type', 'content', 
                        'response', 'next_step', 'next_step_date', 'result', 'notes'])
        
        # Escrever dados
        for interaction in interactions:
            writer.writerow([
                interaction.id,
                interaction.lead_id,
                interaction.lead.name if interaction.lead else '',
                interaction.date.strftime('%Y-%m-%d %H:%M:%S') if interaction.date else '',
                interaction.type,
                interaction.content,
                'Sim' if interaction.response else 'NÃ£o',
                interaction.next_step,
                interaction.next_step_date.strftime('%Y-%m-%d %H:%M:%S') if interaction.next_step_date else '',
                interaction.result,
                interaction.notes
            ])
        
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=interactions.csv'
        }
    
    else:
        flash('Tipo de exportaÃ§Ã£o nÃ£o suportado.')
        return redirect(url_for('dashboard.index'))

@bp.route('/send_email/<int:lead_id>', methods=('GET', 'POST'))
@login_required
def send_email(lead_id):
    """Envia email para um lead especÃ­fico."""
    lead = Lead.query.get_or_404(lead_id)
    
    if request.method == 'POST':
        subject = request.form['subject']
        content = request.form['content']
        
        if not lead.email:
            flash('Este lead nÃ£o possui email cadastrado.')
            return redirect(url_for('leads.view', id=lead_id))
        
        # ImplementaÃ§Ã£o bÃ¡sica - serÃ¡ expandida posteriormente
        # Em uma implementaÃ§Ã£o real, aqui seria feita a integraÃ§Ã£o com um serviÃ§o de email
        
        # Registrar a interaÃ§Ã£o
        interaction = Interaction(
            lead_id=lead.id,
            type='Email',
            content=content,
            date=datetime.utcnow(),
            notes=f'Assunto: {subject}'
        )
        
        lead.last_interaction_date = datetime.utcnow()
        
        db.session.add(interaction)
        db.session.commit()
        
        flash('Email registrado com sucesso! (Funcionalidade de envio serÃ¡ implementada em breve)')
        return redirect(url_for('leads.view', id=lead_id))
    
    # Obter templates de email
    templates = Template.query.filter_by(category='Email').all()
    
    return render_template('integrations/send_email.html', lead=lead, templates=templates)

@bp.route('/api/leads')
@login_required
def api_leads():
    """API simples para obter leads em formato JSON."""
    leads = Lead.query.all()
    leads_list = []
    
    for lead in leads:
        leads_list.append({
            'id': lead.id,
            'name': lead.name,
            'company': lead.company,
            'position': lead.position,
            'status': lead.status
        })
    
    return jsonify(leads_list)

@bp.route('/api/interactions/<int:lead_id>')
@login_required
def api_interactions(lead_id):
    """API simples para obter interaÃ§Ãµes de um lead em formato JSON."""
    interactions = Interaction.query.filter_by(lead_id=lead_id).all()
    interactions_list = []
    
    for interaction in interactions:
        interactions_list.append({
            'id': interaction.id,
            'date': interaction.date.strftime('%Y-%m-%d %H:%M:%S') if interaction.date else '',
            'type': interaction.type,
            'content': interaction.content,
            'response': interaction.response
        })
    
    return jsonify(interactions_list)
