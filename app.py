import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "codecraft-studio-secret-key-2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///codecraft_studio.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_timeout": 20,
    "max_overflow": 0,
}

# Production configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max file size

# Initialize the app with the extension
db.init_app(app)

# Initialize production error handling
from error_handler import error_handler
error_handler.init_app(app)

# Apply production configuration
from production_config import config
config.apply_to_app(app)

# Create directories for static files
os.makedirs('static/audio', exist_ok=True)
os.makedirs('static/video', exist_ok=True)
os.makedirs('static/downloads', exist_ok=True)
os.makedirs('logs', exist_ok=True)

with app.app_context():
    # Import models to create tables
    import models
    db.create_all()
    
    # Import routes
    import routes
