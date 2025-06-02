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