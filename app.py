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