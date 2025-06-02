# src/forms/lead_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, URL
from src.models.lead import Lead # Certifique-se de que esta importaÃ§Ã£o estÃ¡ presente

class LeadForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    company = StringField('Empresa', validators=[DataRequired(), Length(min=2, max=100)])
    position = StringField('Cargo', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    linkedin_url = StringField('URL do LinkedIn', validators=[Optional(), URL(), Length(max=255)])
    status = SelectField('Status', choices=Lead.get_status_choices()) # <-- CORREÃÃO AQUI
    source = StringField('Fonte', validators=[Optional(), Length(max=100)])
    notes = TextAreaField('ObservaÃ§Ãµes', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Salvar')