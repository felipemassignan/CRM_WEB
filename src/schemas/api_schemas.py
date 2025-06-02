# src/schemas/api_schemas.py
from marshmallow import Schema, fields, validate, ValidationError
from src.models.lead import Lead

class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8), load_only=True)
    role = fields.String(validate=validate.OneOf(['user', 'admin']))
    is_active = fields.Boolean()

class LeadSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    company = fields.String(required=True, validate=validate.Length(min=2, max=100))
    position = fields.String(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(allow_none=True)
    phone = fields.String(validate=validate.Length(max=20), allow_none=True)
    linkedin_url = fields.URL(validate=validate.Length(max=255), allow_none=True)
    status = fields.String(validate=validate.OneOf(Lead.get_status_choices())) # <-- CORREÇÃO AQUI
    source = fields.String(validate=validate.Length(max=100), allow_none=True)
    notes = fields.String(validate=validate.Length(max=1000), allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    

class InteractionSchema(Schema):
    id = fields.Integer(dump_only=True)
    lead_id = fields.Integer(required=True)
    type = fields.String(required=True, validate=validate.OneOf([
        'Email', 'Telefone', 'Reunião', 'LinkedIn', 'Outro'
    ]))
    date = fields.DateTime(required=True)
    notes = fields.String(validate=validate.Length(max=1000), allow_none=True)
    result = fields.String(validate=validate.Length(max=100), allow_none=True)
    created_at = fields.DateTime(dump_only=True)

class AuthSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)