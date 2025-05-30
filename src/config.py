import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'crm_python_secret_key_2025')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração dinâmica do banco de dados
    @staticmethod
    def get_database_url():
        database_url = os.environ.get('DATABASE_URL')
        if database_url and database_url.startswith('postgres://'):
            # Heroku e algumas plataformas usam postgres://, mas SQLAlchemy precisa de postgresql://
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            return database_url
        return os.environ.get('DATABASE_URL', 'sqlite:///crm.db')
    
    SQLALCHEMY_DATABASE_URI = get_database_url.__func__()
    
    # Configurações de email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
# Configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}