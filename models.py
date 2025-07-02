from app import db
from datetime import datetime
import json

class Generation(db.Model):
    """Model for tracking music/video generations"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    voice_style = db.Column(db.String(50), nullable=False)
    music_style = db.Column(db.String(50), nullable=False)
    lyrics_data = db.Column(db.Text)
    audio_file = db.Column(db.String(200))
    video_file = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')
    success_rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def get_lyrics_data(self):
        """Parse and return lyrics data as dict"""
        try:
            if self.lyrics_data:
                return json.loads(self.lyrics_data)
            return {}
        except:
            return {}

class LearningData(db.Model):
    """Model for storing AI learning data"""
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String(50), nullable=False)
    data_content = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class SecurityLog(db.Model):
    """Model for security event logging"""
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    event_data = db.Column(db.Text)
    severity = db.Column(db.String(20), default='INFO')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
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
"""
Database Models for CodeCraft Studio
© 2025 Ervin Remus Radosavlevici
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

# Import db from app factory
try:
    from app import db
except ImportError:
    # Fallback for direct imports
    db = SQLAlchemy()

class Generation(db.Model):
    """Generation model for storing AI-generated content"""
    __tablename__ = 'generations'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.String(500), nullable=False)
    music_style = db.Column(db.String(100), default='epic')
    voice_style = db.Column(db.String(100), default='heroic_male')
    
    # Content fields
    lyrics_json = db.Column(db.Text)  # JSON string of lyrics data
    audio_file = db.Column(db.String(255))
    video_file = db.Column(db.String(255))
    
    # Status tracking
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    progress = db.Column(db.Integer, default=0)  # 0-100
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def get_lyrics_data(self):
        """Parse lyrics JSON data"""
        if self.lyrics_json:
            try:
                return json.loads(self.lyrics_json)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_lyrics_data(self, data):
        """Set lyrics data as JSON"""
        self.lyrics_json = json.dumps(data) if data else None
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'theme': self.theme,
            'music_style': self.music_style,
            'voice_style': self.voice_style,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'lyrics_data': self.get_lyrics_data(),
            'audio_file': self.audio_file,
            'video_file': self.video_file
        }

class SecurityLog(db.Model):
    """Security logging model"""
    __tablename__ = 'security_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='INFO')  # INFO, WARNING, ERROR, CRITICAL
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'event_type': self.event_type,
            'message': self.message,
            'severity': self.severity,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

# Create tables function for production
def create_tables(app):
    """Create database tables in application context"""
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
