
"""
Flask Application Factory - Production Ready
© 2025 Ervin Remus Radosavlevici
"""

import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Apply production configuration
    try:
        from production_config import ProductionConfig
        ProductionConfig.apply_to_app(app)
    except ImportError:
        # Fallback configuration
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key-change-in-production')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/codecraft_studio.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Register blueprints
    try:
        from routes import main_bp
        app.register_blueprint(main_bp)
    except ImportError as e:
        logging.error(f"Failed to register routes: {e}")
        
        # Create minimal fallback route
        @app.route('/')
        def index():
            return render_template('index.html') if os.path.exists('templates/index.html') else "CodeCraft Studio - Starting..."
    
    # Create database tables
    with app.app_context():
        try:
            # Import models to ensure they are registered
            import models
            
            # Ensure instance directory exists for SQLite
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if db_uri.startswith('sqlite:///'):
                # Ensure instance directory exists
                os.makedirs('instance', exist_ok=True)
                # Test if we can create the database file
                import sqlite3
                test_db_path = 'instance/codecraft_studio.db'
                conn = sqlite3.connect(test_db_path)
                conn.close()
            
            db.create_all()
            logging.info("Database initialized successfully")
        except Exception as e:
            logging.error(f"Database initialization error: {e}")
    
    # Production error handlers
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f"Internal error: {error}")
        return "Internal server error - Check logs", 500
    
    @app.errorhandler(404)
    def not_found(error):
        return "Page not found", 404
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'app': 'CodeCraft Studio'}, 200
    
    return app

import os
import logging
from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
def create_app():
    app = Flask(__name__)

    # Add proxy support for production deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rados-quantum-enforcement-v2.7-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/codecraft_studio.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize database
    db.init_app(app)

    # Initialize error handler
    from error_handler import error_handler
    error_handler.init_app(app)

    # Add request tracking middleware
    @app.before_request
    def before_request():
        g.start_time = time.time()

        # Track page view
        from analytics import analytics
        analytics.track_page_view(
            request.path,
            str(request.user_agent),
            request.remote_addr
        )

    @app.after_request
    def after_request(response):
        # Track response time
        if hasattr(g, 'start_time'):
            response_time = (time.time() - g.start_time) * 1000  # Convert to ms
            from analytics import analytics
            analytics.track_response_time(request.endpoint or request.path, response_time)

        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval'"

        return response

    # Register blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)

    # Create tables and directories
    with app.app_context():
        # Create required directories
        directories = [
            'instance', 'static/audio', 'static/video', 'static/downloads',
            'static/uploads', 'static/voice_training', 'static/voice_models',
            'static/ai_scenes', 'static/collaboration', 'static/mastering',
            'static/mixing', 'logs', 'logs/analytics', 'logs/voice_training',
            'logs/youtube', 'logs/collaboration', 'logs/audio'
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

        # Create database tables
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database initialization failed: {e}")

    return app

# Create the app instance at module level for Gunicorn
app = create_app()