import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.routes.health_routes import health_bp
from backend.routes.risk_routes import risk_bp
from backend.routes.data_routes import data_bp
from backend.routes.alert_routes import alert_bp

from database.init_db import ensure_db_initialized

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Automatically ensure database is initialized & seeded with integrated records
    ensure_db_initialized()

    # Enable production CORS for React frontend origins
    origins = app.config.get('CORS_ALLOWED_ORIGINS', ['*'])
    if '*' in origins or origins == ['*']:
        CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=False)
    else:
        CORS(
            app, 
            resources={r"/api/*": {"origins": origins}},
            supports_credentials=True,
            allow_headers=["Content-Type", "Authorization", "Accept"],
            methods=["GET", "POST", "OPTIONS"]
        )

    # Universal CORS header enforcer to ensure preflights and requests from Vercel never fail
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept, X-Requested-With'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        return response

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(alert_bp)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = app.config.get('DEBUG', False)
    print(f"Starting JalRakshak Flask REST API on port {port} (debug={debug})...")
    app.run(host='0.0.0.0', port=port, debug=debug)
