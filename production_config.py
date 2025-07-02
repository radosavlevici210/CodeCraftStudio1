
"""
Production Configuration for CodeCraft Studio
Optimized settings for production deployment
© 2025 Ervin Remus Radosavlevici
"""

import os
from datetime import timedelta

class ProductionConfig:
    """Production-ready configuration settings"""
    
    # API Timeouts (seconds)
    OPENAI_TIMEOUT = 15
    API_RATE_LIMIT = 60  # requests per minute
    GENERATION_TIMEOUT = 30  # Total generation timeout
    
    # Worker Configuration
    WORKER_TIMEOUT = 30  # seconds
    MAX_WORKERS = 4
    
    # Feature Flags
    ENABLE_AI_IMAGE_GENERATION = False  # Disabled for performance
    ENABLE_REAL_TIME_COLLABORATION = True
    ENABLE_VOICE_TRAINING = True
    ENABLE_YOUTUBE_UPLOAD = True
    
    # Performance Settings
    MAX_CONCURRENT_GENERATIONS = 3
    CACHE_TIMEOUT = timedelta(hours=1)
    
    # File Limits
    MAX_AUDIO_DURATION = 300  # 5 minutes
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Database Configuration
    DB_POOL_SIZE = 10
    DB_POOL_TIMEOUT = 20
    DB_POOL_RECYCLE = 300
    
    # Security Settings
    SESSION_TIMEOUT = timedelta(hours=8)
    MAX_LOGIN_ATTEMPTS = 5
    
    @staticmethod
    def apply_to_app(app):
        """Apply production configuration to Flask app"""
        # Basic Flask configuration
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rados-quantum-enforcement-v2.7-production')
        
        # Database configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/codecraft_studio.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': ProductionConfig.DB_POOL_SIZE,
            'pool_timeout': ProductionConfig.DB_POOL_TIMEOUT,
            'pool_recycle': ProductionConfig.DB_POOL_RECYCLE
        }
        
        # Apply timeout settings
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(hours=1)
        app.config['PERMANENT_SESSION_LIFETIME'] = ProductionConfig.SESSION_TIMEOUT
        
        # Apply security settings
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        if not app.debug:
            app.config['SESSION_COOKIE_SECURE'] = True
        
        # Apply production-specific settings
        app.config['WTF_CSRF_TIME_LIMIT'] = 3600
        app.config['MAX_CONTENT_LENGTH'] = ProductionConfig.MAX_FILE_SIZE
        
        # Performance settings
        app.config['JSON_SORT_KEYS'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        
        # Template settings for production
        app.jinja_env.auto_reload = False
        app.jinja_env.cache_size = 400
        
        return app

# Global configuration instance
config = ProductionConfig()
