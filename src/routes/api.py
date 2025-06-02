# src/routes/api.py (atualizado para usar esquemas Marshmallow)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity
)
from src.models.db import db
from src.models.user import User
from src.models.lead import Lead
from src.models.interaction import Interaction
from src.models.api_token import ApiToken
from src.schemas.api_schemas import UserSchema, LeadSchema, InteractionSchema, AuthSchema
from marshmallow import ValidationError
from datetime import datetime
from functools import wraps
import secrets

bp = Blueprint('api', __name__, url_prefix='/api')

# Inicializar esquemas
user_schema = UserSchema()
lead_schema = LeadSchema()
leads_schema = LeadSchema(many=True)
interaction_schema = InteractionSchema()
interactions_schema = InteractionSchema(many=True)
auth_schema = AuthSchema()

# Função para verificar tokens de API
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verificar se o token está no header Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        # Verificar se o token está nos parâmetros da query
        if not token:
            token = request.args.get('token')
        
        if not token:
            return jsonify({'msg': 'Token ausente!'}), 401
        
        # Verificar se o token existe e está ativo
        api_token = ApiToken.query.filter_by(token=token, is_active=True).first()
        if not api_token:
            return jsonify({'msg': 'Token inválido ou revogado!'}), 401
        
        # Atualizar a data do último uso
        api_token.last_used_at = datetime.utcnow()
        db.session.commit()
        
        # Adicionar o usuário ao contexto da requisição
        request.current_user = api_token.user
        
        return f(*args, **kwargs)
    
    return decorated

# Rota para autenticação e obtenção de token JWT
@bp.route('/auth/token', methods=['POST'])
def get_token():
    try:
        # Validar dados de entrada
        auth_data = auth_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    username = auth_data['username']
    password = auth_data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciais inválidas"}), 401
    
    # Criar tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

# Rota para renovar o token de acesso usando o refresh token
@bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=access_token), 200

# Rota para obter informações do usuário atual
@bp.route('/user/me', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "Usuário não encontrado"}), 404
    
    return jsonify(user_schema.dump(user)), 200

# Rotas para Leads
@bp.route('/leads', methods=['GET'])
@jwt_required()
def get_leads():
    leads = Lead.query.all()
    return jsonify(leads_schema.dump(leads)), 200

@bp.route('/leads', methods=['POST'])
@jwt_required()
def create_lead():
    try:
        # Validar dados de entrada
        lead_data = lead_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    # Criar novo lead
    new_lead = Lead(**lead_data)
    new_lead.created_at = datetime.utcnow()
    
    db.session.add(new_lead)
    db.session.commit()
    
    return jsonify({
        "msg": "Lead criado com sucesso",
        "lead": lead_schema.dump(new_lead)
    }), 201

@bp.route('/leads/<int:lead_id>', methods=['GET'])
@jwt_required()
def get_lead(lead_id):
    lead = Lead.query.get(lead_id)
    
    if not lead:
        return jsonify({"msg": "Lead não encontrado"}), 404
    
    # Incluir interações relacionadas
    result = lead_schema.dump(lead)
    result['interactions'] = interactions_schema.dump(lead.interactions)
    
    return jsonify(result), 200

@bp.route('/leads/<int:lead_id>', methods=['PUT'])
@jwt_required()
def update_lead(lead_id):
    lead = Lead.query.get(lead_id)
    
    if not lead:
        return jsonify({"msg": "Lead não encontrado"}), 404
    
    try:
        # Validar dados de entrada
        lead_data = lead_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    # Atualizar campos do lead
    for key, value in lead_data.items():
        setattr(lead, key, value)
    
    db.session.commit()
    
    return jsonify({
        "msg": "Lead atualizado com sucesso",
        "lead": lead_schema.dump(lead)
    }), 200

@bp.route('/leads/<int:lead_id>', methods=['DELETE'])
@jwt_required()
def delete_lead(lead_id):
    lead = Lead.query.get(lead_id)
    
    if not lead:
        return jsonify({"msg": "Lead não encontrado"}), 404
    
    db.session.delete(lead)
    db.session.commit()
    
    return jsonify({"msg": "Lead excluído com sucesso"}), 200

# Rotas para Interações
@bp.route('/interactions', methods=['POST'])
@jwt_required()
def create_interaction():
    try:
        # Validar dados de entrada
        interaction_data = interaction_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    # Verificar se o lead existe
    lead = Lead.query.get(interaction_data['lead_id'])
    if not lead:
        return jsonify({"msg": "Lead não encontrado"}), 404
    
    # Criar nova interação
    new_interaction = Interaction(**interaction_data)
    new_interaction.created_at = datetime.utcnow()
    
    db.session.add(new_interaction)
    db.session.commit()
    
    return jsonify({
        "msg": "Interação criada com sucesso",
        "interaction": interaction_schema.dump(new_interaction)
    }), 201

# Rotas com autenticação por token simples
@bp.route('/leads/token', methods=['GET'])
@token_required
def get_leads_with_token():
    leads = Lead.query.all()
    return jsonify(leads_schema.dump(leads)), 200

@bp.route('/leads/token', methods=['POST'])
@token_required
def create_lead_with_token():
    try:
        # Validar dados de entrada
        lead_data = lead_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    # Criar novo lead
    new_lead = Lead(**lead_data)
    new_lead.created_at = datetime.utcnow()
    
    db.session.add(new_lead)
    db.session.commit()
    
    return jsonify({
        "msg": "Lead criado com sucesso",
        "lead": lead_schema.dump(new_lead)
    }), 201

# Adicione mais rotas para a API conforme necessário...