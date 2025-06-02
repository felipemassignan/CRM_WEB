import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from flask import current_app

class EmailSender:
    def __init__(self, smtp_server=None, smtp_port=None, smtp_user=None, smtp_password=None):
        """
        Inicializa o serviÃ§o de envio de emails.
        Se os parÃ¢metros nÃ£o forem fornecidos, tentarÃ¡ usar variÃ¡veis de ambiente.
        """
        self.smtp_server = smtp_server or os.environ.get('SMTP_SERVER')
        self.smtp_port = smtp_port or os.environ.get('SMTP_PORT', 587)
        self.smtp_user = smtp_user or os.environ.get('SMTP_USER')
        self.smtp_password = smtp_password or os.environ.get('SMTP_PASSWORD')
        
    def send_email(self, to_email, subject, body, is_html=False):
        """
        Envia um email para o destinatÃ¡rio especificado.
        
        Args:
            to_email (str): Email do destinatÃ¡rio
            subject (str): Assunto do email
            body (str): Corpo do email
            is_html (bool): Se o corpo do email Ã© HTML
            
        Returns:
            bool: True se o email foi enviado com sucesso, False caso contrÃ¡rio
        """
        if not all([self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_password]):
            current_app.logger.error("ConfiguraÃ§Ãµes de SMTP incompletas")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
                
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            current_app.logger.info(f"Email enviado com sucesso para {to_email}")
            return True
            
        except Exception as e:
            current_app.logger.error(f"Erro ao enviar email: {str(e)}")
            return False
            
    def send_reminder(self, to_email, lead_name, action, due_date):
        """
        Envia um lembrete sobre uma aÃ§Ã£o pendente com um lead.
        
        Args:
            to_email (str): Email do destinatÃ¡rio
            lead_name (str): Nome do lead
            action (str): AÃ§Ã£o pendente
            due_date (str): Data de vencimento formatada
            
        Returns:
            bool: True se o email foi enviado com sucesso, False caso contrÃ¡rio
        """
        subject = f"Lembrete: AÃ§Ã£o pendente com {lead_name}"
        
        body = f"""
        <html>
        <body>
            <h2>Lembrete de AÃ§Ã£o Pendente</h2>
            <p>VocÃª tem uma aÃ§Ã£o pendente com o lead <strong>{lead_name}</strong>.</p>
            <p><strong>AÃ§Ã£o:</strong> {action}</p>
            <p><strong>Data de vencimento:</strong> {due_date}</p>
            <p>Acesse o CRM para mais detalhes e para registrar a interaÃ§Ã£o.</p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, is_html=True)
        
    def send_bulk_emails(self, template, leads):
        """
        Envia emails em massa usando um template para vÃ¡rios leads.
        
        Args:
            template (dict): Template com assunto e corpo
            leads (list): Lista de leads com emails
            
        Returns:
            dict: DicionÃ¡rio com contagem de sucessos e falhas
        """
        results = {'success': 0, 'failed': 0, 'failed_emails': []}
        
        for lead in leads:
            if not lead.email:
                continue
                
            # Personalizar o template para este lead
            personalized_body = template['body']
            personalized_body = personalized_body.replace('{nome}', lead.name)
            personalized_body = personalized_body.replace('{empresa}', lead.company or '')
            personalized_body = personalized_body.replace('{cargo}', lead.position or '')
            
            success = self.send_email(
                lead.email, 
                template['subject'], 
                personalized_body,
                is_html=template.get('is_html', False)
            )
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
                results['failed_emails'].append(lead.email)
                
        return results
