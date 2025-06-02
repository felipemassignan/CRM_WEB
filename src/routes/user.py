# src/routes/user.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from src.models.db import db
from src.models.user import User
import secrets
from src.models.api_token import ApiToken
from src.forms.user_forms import LoginForm, RegistrationForm, EditUserForm, ApiTokenForm
from datetime import datetime

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já está autenticado, redireciona para o dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        
        flash('Nome de usuário ou senha inválidos.')
    
    return render_template('user/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.')
    return redirect(url_for('user.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Em um ambiente de produção, você pode querer restringir o registro
    # ou permitir apenas que administradores criem novos usuários
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        
        # Se for o primeiro usuário, torná-lo admin
        if User.query.count() == 0:
            new_user.role = 'admin'
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Conta criada com sucesso! Agora você pode fazer login.')
        return redirect(url_for('user.login'))
    
    return render_template('user/register.html', form=form)

# Rota para gerenciar usuários (apenas para administradores)
@bp.route('/manage', methods=['GET'])
@login_required
def manage_users():
    # Verificar se o usuário atual é um administrador
    if current_user.role != 'admin':
        flash('Acesso negado. Você precisa ser um administrador para acessar esta página.')
        return redirect(url_for('dashboard.index'))
    
    users = User.query.all()
    return render_template('user/manage.html', users=users)

# Rota para editar usuários (apenas para administradores)
@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # Verificar se o usuário atual é um administrador
    if current_user.role != 'admin' and current_user.id != user_id:
        flash('Acesso negado.')
        return redirect(url_for('dashboard.index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        
        # Apenas administradores podem alterar o papel do usuário
        if current_user.role == 'admin':
            user.role = request.form.get('role')
            user.is_active = 'is_active' in request.form
        
        # Se uma nova senha foi fornecida, atualize-a
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        flash('Usuário atualizado com sucesso.')
        
        if current_user.role == 'admin':
            return redirect(url_for('user.manage_users'))
        return redirect(url_for('dashboard.index'))
    
    return render_template('user/edit.html', user=user)

# Rota para excluir usuários (apenas para administradores)
@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Acesso negado. Você precisa ser um administrador para excluir usuários.')
        return redirect(url_for('dashboard.index'))
    
    user = User.query.get_or_404(user_id)
    
    # Não permitir que o administrador exclua a si mesmo
    if user.id == current_user.id:
        flash('Você não pode excluir sua própria conta.')
        return redirect(url_for('user.manage_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Usuário excluído com sucesso.')
    return redirect(url_for('user.manage_users'))

@bp.route('/api-tokens', methods=['GET'])
@login_required
def api_tokens():
    tokens = ApiToken.query.filter_by(user_id=current_user.id).all()
    return render_template('user/api_tokens.html', tokens=tokens)

@bp.route('/api-tokens/create', methods=['POST'])
@login_required
def create_api_token():
    token_name = request.form.get('token_name')
    
    if not token_name:
        flash('O nome do token é obrigatório.')
        return redirect(url_for('user.api_tokens'))
    
    # Gerar um token aleatório
    token_value = secrets.token_hex(32)  # 64 caracteres hexadecimais
    
    # Criar o token
    new_token = ApiToken(
        user_id=current_user.id,
        name=token_name,
        token=token_value,
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_token)
    db.session.commit()
    
    flash(f'Token "{token_name}" criado com sucesso. Guarde este valor, pois ele não será mostrado novamente: {token_value}')
    return redirect(url_for('user.api_tokens'))

@bp.route('/api-tokens/revoke/<int:token_id>', methods=['POST'])
@login_required
def revoke_api_token(token_id):
    token = ApiToken.query.get_or_404(token_id)
    
    # Verificar se o token pertence ao usuário atual
    if token.user_id != current_user.id and current_user.role != 'admin':
        flash('Você não tem permissão para revogar este token.')
        return redirect(url_for('user.api_tokens'))
    
    # Desativar o token
    token.is_active = False
    db.session.commit()
    
    flash(f'Token "{token.name}" revogado com sucesso.')
    return redirect(url_for('user.api_tokens'))

@bp.route('/api-tokens/delete/<int:token_id>', methods=['POST'])
@login_required
def delete_api_token(token_id):
    token = ApiToken.query.get_or_404(token_id)
    
    # Verificar se o token pertence ao usuário atual
    if token.user_id != current_user.id and current_user.role != 'admin':
        flash('Você não tem permissão para excluir este token.')
        return redirect(url_for('user.api_tokens'))
    
    # Excluir o token
    db.session.delete(token)
    db.session.commit()
    
    flash(f'Token "{token.name}" excluído com sucesso.')
    return redirect(url_for('user.api_tokens'))