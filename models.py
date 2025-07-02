"""
Database Models for CodeCraft Studio
© 2025 Ervin Remus Radosavlevici
"""

from app import db
from datetime import datetime
import json


class Generation(db.Model):
    """Model for content generations"""
    __tablename__ = 'generations'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')
    music_style = db.Column(db.String(100), default='epic')
    voice_style = db.Column(db.String(100), default='heroic_male')
    lyrics_data = db.Column(db.Text)
    audio_file = db.Column(db.String(500))
    video_file = db.Column(db.String(500))
    error_message = db.Column(db.Text)
    
    # Business licensing
    license_key = db.Column(db.String(255))  # Associated license key
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def get_lyrics_data(self):
        """Parse lyrics data from JSON"""
        if self.lyrics_data:
            try:
                return json.loads(self.lyrics_data)
            except:
                return {}
        return {}

    def __repr__(self):
        return f'<Generation {self.id}: {self.title}>'


class LearningData(db.Model):
    """Model for storing AI learning data"""
    __tablename__ = 'learning_data'
    
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String(50), nullable=False)
    data_content = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class SecurityLog(db.Model):
    """Model for security event logging"""
    __tablename__ = 'security_logs'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20), default='INFO')
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SecurityLog {self.id}: {self.event_type}>'


def create_tables(app):
    """Create database tables in application context"""
    with app.app_context():
        db.create_all()