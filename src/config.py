# src/config.py
import os
from dotenv import load_dotenv

# Carregar variÃ¡veis de ambiente do arquivo .env
load_dotenv()

class Config:
    """ConfiguraÃ§Ã£o base."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/crm_python')
    
    # ConfiguraÃ§Ãµes de e-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # ConfiguraÃ§Ãµes do LinkedIn
    LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')

class DevelopmentConfig(Config):
    """ConfiguraÃ§Ã£o de desenvolvimento."""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """ConfiguraÃ§Ã£o de teste."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'postgresql://postgres:postgres@db:5432/crm_python_test')

class ProductionConfig(Config):
    """ConfiguraÃ§Ã£o de produÃ§Ã£o."""
    DEBUG = False
    
    # Em produÃ§Ã£o, vocÃª pode querer configuraÃ§Ãµes adicionais de seguranÃ§a
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}