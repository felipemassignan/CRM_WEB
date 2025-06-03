# src/routes/user.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from src.services.user_service import UserService
from src.forms.user_forms import LoginForm, RegistrationForm, EditUserForm, ApiTokenForm

bp = Blueprint('user', __name__, url_prefix='/user')

# --- NOVA ROTA DE LOGIN ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm() # Instancia o formulário de login
    if form.validate_on_submit():
        user = UserService.get_user_by_username(form.username.data) # Você precisará de um método para buscar usuário por username
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login bem-sucedido!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Login inválido. Verifique seu nome de usuário e senha.', 'danger')
    
    return render_template('user/login.html', form=form) # Passa o formulário para o template
# --- FIM NOVA ROTA DE LOGIN ---

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('user.login')) # Redireciona para a página de login após o logout

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        UserService.create_user(form.data)
        flash('Conta criada com sucesso! Agora vocÃª pode fazer login.')
        return redirect(url_for('user.login'))
    
    return render_template('user/register.html', form=form)

@bp.route('/manage', methods=['GET'])
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Acesso negado. VocÃª precisa ser um administrador para acessar esta pÃ¡gina.')
        return redirect(url_for('dashboard.index'))
    
    users = UserService.get_all_users()
    return render_template('user/manage.html', users=users)

@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin' and current_user.id != user_id:
        flash('Acesso negado.')
        return redirect(url_for('dashboard.index'))
    
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash('UsuÃ¡rio nÃ£o encontrado.')
        return redirect(url_for('user.manage_users'))
    
    form = EditUserForm(original_username=user.username, original_email=user.email)
    if form.validate_on_submit():
        UserService.update_user(user_id, form.data)
        flash('UsuÃ¡rio atualizado com sucesso.')
        return redirect(url_for('user.manage_users'))
    
    return render_template('user/edit.html', form=form, user=user)

@bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Acesso negado. VocÃª precisa ser um administrador para excluir usuÃ¡rios.')
        return redirect(url_for('dashboard.index'))
    
    user = UserService.delete_user(user_id)
    if not user:
        flash('UsuÃ¡rio nÃ£o encontrado.')
    else:
        flash('UsuÃ¡rio excluÃ­do com sucesso.')
    return redirect(url_for('user.manage_users'))

# --- DEBUG: Confirma que este arquivo foi carregado ---
print("DEBUG: src.routes.user.py loaded and blueprint 'user' defined.")
# --- FIM DEBUG ---