from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models.template import Template
from src.models.db import db
from datetime import datetime

bp = Blueprint('templates', __name__, url_prefix='/templates')

@bp.route('/')
@login_required
def index():
    """Lista todos os templates de mensagem."""
    templates = Template.query.order_by(Template.category).all()
    return render_template('templates/index.html', templates=templates,
                           category_filter=request.args.get('category'),
                           position_filter=request.args.get('target_position'))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Cria um novo template de mensagem."""
    if request.method == 'POST':
        category = request.form['category']
        target_position = request.form['target_position']
        subject = request.form['subject']
        content = request.form['content']
        variables = request.form['variables']
        usage_notes = request.form['usage_notes']
        
        error = None
        
        if not category:
            error = 'Categoria é obrigatória.'
        elif not content:
            error = 'Conteúdo é obrigatório.'
        
        if error is not None:
            flash(error)
        else:
            template = Template(
                category=category,
                target_position=target_position,
                subject=subject,
                content=content,
                variables=variables,
                usage_notes=usage_notes
            )
            db.session.add(template)
            db.session.commit()
            flash('Template criado com sucesso!')
            return redirect(url_for('templates.index'))
    
    return render_template('templates/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Atualiza um template existente."""
    template = Template.query.get_or_404(id)
    
    if request.method == 'POST':
        template.category = request.form['category']
        template.target_position = request.form['target_position']
        template.subject = request.form['subject']
        template.content = request.form['content']
        template.variables = request.form['variables']
        template.usage_notes = request.form['usage_notes']
        
        error = None
        
        if not template.category:
            error = 'Categoria é obrigatória.'
        elif not template.content:
            error = 'Conteúdo é obrigatório.'
        
        if error is not None:
            flash(error)
        else:
            db.session.commit()
            flash('Template atualizado com sucesso!')
            return redirect(url_for('templates.index'))
    
    return render_template('templates/update.html', template=template)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Exclui um template."""
    template = Template.query.get_or_404(id)
    db.session.delete(template)
    db.session.commit()
    flash('Template excluído com sucesso!')
    return redirect(url_for('templates.index'))

@bp.route('/<int:id>/view')
@login_required
def view(id):
    """Visualiza detalhes de um template."""
    template = Template.query.get_or_404(id)
    return render_template('templates/view.html', template=template)

@bp.route('/filter')
@login_required
def filter():
    """Filtra templates por categoria e cargo alvo."""
    category = request.args.get('category')
    target_position = request.args.get('target_position')
    
    query = Template.query
    
    if category:
        query = query.filter(Template.category == category)
    
    if target_position:
        query = query.filter(Template.target_position == target_position)
    
    templates = query.order_by(Template.category).all()
    
    return render_template('templates/index.html', templates=templates, 
                          category_filter=category, 
                          position_filter=target_position)

@bp.route('/generate/<int:template_id>/<int:lead_id>')
@login_required
def generate(template_id, lead_id):
    """Gera uma mensagem personalizada com base em um template e dados de um lead."""
    from src.models.lead import Lead
    
    template = Template.query.get_or_404(template_id)
    lead = Lead.query.get_or_404(lead_id)
    
    # Substituir variáveis no template
    content = template.content
    
    # Mapeamento de variáveis
    variables = {
        "{nome}": lead.name,
        "{primeiro_nome}": lead.name.split()[0] if lead.name else "",
        "{cargo}": lead.position,
        "{empresa}": lead.company,
        "{setor}": lead.industry,
        "{data}": datetime.now().strftime("%d/%m/%Y")
    }
    
    # Substituir cada variável
    for var, value in variables.items():
        content = content.replace(var, value or "")
    
    # Incrementar contador de uso
    template.usage_count += 1
    template.last_used = datetime.utcnow()
    db.session.commit()
    
    return render_template('templates/generate.html', 
                          template=template, 
                          lead=lead, 
                          generated_content=content)

@bp.route('/categories')
@login_required
def categories():
    """Lista todas as categorias de templates."""
    categories = db.session.query(Template.category).distinct().all()
    return render_template('templates/categories.html', categories=categories)

@bp.route('/positions')
@login_required
def positions():
    """Lista todos os cargos alvo de templates."""
    positions = db.session.query(Template.target_position).distinct().all()
    return render_template('templates/positions.html', positions=positions)
