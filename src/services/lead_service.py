# src/services/lead_service.py
from src.models.db import db
from src.models.lead import Lead
from datetime import datetime

class LeadService:
    @staticmethod
    def create_lead(data):
        new_lead = Lead(
            name=data['name'],
            company=data['company'],
            position=data['position'],
            email=data.get('email'),
            phone=data.get('phone'),
            linkedin_url=data.get('linkedin_url'),
            status=data.get('status', 'Novo'),
            source=data.get('source', 'API'),            
            region=data.get('region'),  # Novo campo
            state=data.get('state'),    # Novo campo
            city=data.get('city'),      # Novo campo
            priority=data.get('priority'), # Novo campo
            company_size=data.get('company_size'), # Novo campo
            annual_revenue=data.get('annual_revenue'), # Novo campo
            technologies_used=data.get('technologies_used'), # Novo campo
            pain_points=data.get('pain_points'), # Novo campo
            notes=data.get('notes'), # Novo campo
            created_at=datetime.utcnow()
        )
        db.session.add(new_lead)
        db.session.commit()
        return new_lead

    @staticmethod
    def update_lead(lead_id, data):
        lead = Lead.query.get(lead_id)
        if not lead:
            return None

        for key, value in data.items():
            setattr(lead, key, value)

        db.session.commit()
        return lead

    @staticmethod
    def delete_lead(lead_id):
        lead = Lead.query.get(lead_id)
        if not lead:
            return None

        db.session.delete(lead)
        db.session.commit()
        return lead

    @staticmethod
    def get_lead_by_id(lead_id):
        return Lead.query.get(lead_id)

    @staticmethod
    def get_all_leads():
        return Lead.query.all()