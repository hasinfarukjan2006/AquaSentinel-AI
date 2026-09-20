import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'database', 'jalrakshak.db'))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
REPORTS_DIR = os.path.join(BASE_DIR, 'data', 'reports')
ML_REPORT_DIR = os.path.join(BASE_DIR, 'ml', 'reports')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'jalrakshak-prod-secret-key-2026')
    DATABASE_PATH = DB_PATH
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    ENV = os.environ.get('FLASK_ENV', 'production')
    
    # CORS Configuration
    CORS_ALLOWED_ORIGINS = [
        origin.strip() for origin in os.environ.get(
            'CORS_ALLOWED_ORIGINS', 
            '*'
        ).split(',') if origin.strip()
    ]

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
